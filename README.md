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

## Front‑end

`frontend/index.html` is a small React page that fetches RRG data and
displays it using Chart.js. Open the file in a browser while the API is
running.

