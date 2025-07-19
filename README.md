# Relative Rotation Graph Service

This project provides a small FastAPI service and a simple React-based
front‑end to display Relative Rotation Graphs (RRG) for NYSE tickers.

## Backend

The service reads PostgreSQL connection information from AWS SSM
parameters under `/stockapp/<environment>/PGHOST` etc. The AWS profile
is taken from the invoking shell session.

To run the API locally:

```bash
pip install -r backend/requirements.txt
uvicorn backend.app:app --reload
```

### Endpoint

`GET /rrg`

| Parameter | Description | Default |
|-----------|-------------|---------|
| `tickers` | Comma separated tickers to plot | required |
| `benchmark` | Benchmark ticker | `SPY` |
| `interval` | Price interval (e.g. `1d`) | `1d` |
| `tail` | Number of points in each tail | `30` |
| `env` | SSM environment prefix | `devtest` |

The endpoint returns JSON suitable for the front‑end.

### Populating data from yfinance

If your database does not yet contain prices, you can fetch them from
[yfinance](https://pypi.org/project/yfinance/). The ticker symbol for the
S&P 500 ETF is `SPY`. A helper script is provided to load daily (`1d`)
prices into the table:

```bash
python backend/load_yfinance.py SPY,AAPL,MSFT --interval 1d --env devtest
```

This downloads roughly two years of daily data and upserts it into the
`stock_ohlcv` table so that the RRG endpoint can operate.

## Front‑end

`frontend/index.html` is a small React page that fetches RRG data and
displays it using Chart.js. Because it expects the API at `http://localhost:8000`,
run a simple HTTP server from the `frontend` directory and open the page
through that server:

```bash
cd frontend
python3 -m http.server 8080
```

Then browse to <http://localhost:8080/index.html> while the FastAPI
service is running.

