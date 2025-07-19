from typing import List
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import boto3
import psycopg2
import pandas as pd

app = FastAPI()

# allow requests from the demo page
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db_config(env: str) -> dict:
    """Load database configuration from AWS SSM."""
    ssm = boto3.client("ssm")
    keys = ["PGHOST", "PGPORT", "PGUSER", "PGPASSWORD"]
    cfg = {}
    for key in keys:
        name = f"/stockapp/{env}/{key}"
        resp = ssm.get_parameter(Name=name, WithDecryption=True)
        cfg[key] = resp["Parameter"]["Value"]
    return cfg


def get_connection(env: str):
    cfg = get_db_config(env)
    conn = psycopg2.connect(
        host=cfg["PGHOST"],
        port=cfg["PGPORT"],
        user=cfg["PGUSER"],
        password=cfg["PGPASSWORD"],
        dbname="postgres",
    )
    return conn


def fetch_prices(conn, tickers: List[str], interval: str, days: int) -> pd.DataFrame:
    placeholders = ",".join(["%s"] * len(tickers))
    params: List = [interval] + tickers + [f"{days} days"]
    query = (
        f"""
        SELECT ticker, ts, close
        FROM stock_ohlcv
        WHERE interval = %s AND ticker IN ({placeholders})
          AND ts >= NOW() - INTERVAL %s
        ORDER BY ts
        """
    )
    df = pd.read_sql(query, conn, params=params)
    return df


def compute_rrg(df: pd.DataFrame, tickers: List[str], benchmark: str, tail: int):
    pivot = df.pivot(index="ts", columns="ticker", values="close").sort_index()
    benchmark_series = pivot[benchmark]
    rrg = {}
    for t in tickers:
        if t == benchmark:
            continue
        rel = pivot[t] / benchmark_series
        ratio = rel / rel.iloc[0]
        momentum = ratio.diff()
        points = [
            {
                "x": float(ratio.iloc[i]),
                "y": float(momentum.iloc[i]),
                "date": ratio.index[i].isoformat(),
            }
            for i in range(-tail, 0)
            if i < len(ratio)
        ]
        rrg[t] = points
    return rrg


@app.get("/rrg")
def rrg(
    tickers: str = Query(..., description="Comma separated list of tickers"),
    benchmark: str = Query("SPY"),
    interval: str = Query("1d"),
    tail: int = Query(30),
    env: str = Query("devtest"),
):
    symbols = [t.strip().upper() for t in tickers.split(",") if t.strip()]
    all_symbols = symbols + [benchmark]
    conn = get_connection(env)
    try:
        df = fetch_prices(conn, all_symbols, interval, tail * 10)
    finally:
        conn.close()
    data = compute_rrg(df, symbols, benchmark, tail)
    return {"benchmark": benchmark, "points": data}


