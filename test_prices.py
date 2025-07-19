import pandas as pd
from pandas import MultiIndex
from prices import prepare_prices, insert_prices

def test_insert_prices_accesses_ticker():
    columns = MultiIndex.from_product([
        ['Open', 'High', 'Low', 'Close', 'Volume'],
        ['AAPL']
    ])
    data = [
        [1, 2, 3, 4, 5],
        [6, 7, 8, 9, 10]
    ]
    df = pd.DataFrame(data, index=pd.date_range('2025-01-01', periods=2, freq='D'), columns=columns)
    prepared = prepare_prices(df, 'AAPL', '1d')
    assert insert_prices(prepared) is True
