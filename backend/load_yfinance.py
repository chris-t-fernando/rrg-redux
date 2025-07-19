import argparse
from typing import List
import pandas as pd
import yfinance as yf
import psycopg2
from .app import get_db_config


def get_connection(env: str):
    cfg = get_db_config(env)
    return psycopg2.connect(
        host=cfg["PGHOST"],
        port=cfg["PGPORT"],
        user=cfg["PGUSER"],
        password=cfg["PGPASSWORD"],
        dbname="postgres",
    )


def fetch_yf(ticker: str, interval: str) -> pd.DataFrame:
    df = yf.download(ticker, interval=interval, period="2y")
    df = df.reset_index()
    df.rename(
        columns={
            "Date": "ts",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        },
        inplace=True,
    )
    df["ticker"] = ticker
    df["interval"] = interval
    return df


def insert_prices(conn, df: pd.DataFrame):
    with conn.cursor() as cur:
        for row in df.itertuples(index=False):
            cur.execute(
                """
                INSERT INTO stock_ohlcv
                    (ticker, interval, ts, open, high, low, close, volume)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (ticker, interval, ts) DO UPDATE SET
                    open = EXCLUDED.open,
                    high = EXCLUDED.high,
                    low = EXCLUDED.low,
                    close = EXCLUDED.close,
                    volume = EXCLUDED.volume
                """,
                (
                    row.ticker,
                    row.interval,
                    row.ts,
                    row.open,
                    row.high,
                    row.low,
                    row.close,
                    row.volume,
                ),
            )
    conn.commit()


def main(tickers: List[str], interval: str, env: str):
    conn = get_connection(env)
    try:
        for t in tickers:
            df = fetch_yf(t, interval)
            insert_prices(conn, df)
    finally:
        conn.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Load OHLCV data from yfinance into the database"
    )
    parser.add_argument("tickers", help="Comma separated list of tickers")
    parser.add_argument("--interval", default="1d", help="yfinance interval")
    parser.add_argument("--env", default="devtest", help="SSM environment")
    args = parser.parse_args()
    tickers = [t.strip().upper() for t in args.tickers.split(",") if t.strip()]
    main(tickers, args.interval, args.env)
