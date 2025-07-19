import pandas as pd
import yfinance as yf


def download_prices(ticker: str, interval: str = '1m', period: str = '1d') -> pd.DataFrame:
    """Download price data using yfinance."""
    return yf.download(ticker, interval=interval, period=period)


def prepare_prices(df: pd.DataFrame, ticker: str, interval: str) -> pd.DataFrame:
    """Flatten columns and prepare DataFrame for insertion."""
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df = df.rename(columns={
        'Open': 'open',
        'High': 'high',
        'Low': 'low',
        'Close': 'close',
        'Volume': 'volume',
    })
    df['ticker'] = ticker
    df['interval'] = interval
    df.reset_index(inplace=True)
    return df


def insert_prices(df: pd.DataFrame) -> bool:
    """Simulate inserting prices by reading row.ticker."""
    for row in df.itertuples(index=False):
        _ = row.ticker  # access ticker attribute
    return True
