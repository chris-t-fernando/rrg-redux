# RRG Redux

This project simulates downloading price data with `yfinance` and preparing it
for further analysis. It includes a small example loader and a unit test.

## Installation

Create a virtual environment and install dependencies:

```bash
pip install -r requirements.txt
```

## Running Tests

Execute the unit tests with `pytest`:

```bash
pytest
```

## Usage Example

The loader module can download price data for multiple tickers. Make sure you
run the command from the project root so that Python can locate the `backend`
package.

Below is an example invocation. Replace the tickers with the symbols you want
to download.





```bash
python -m backend.load_yfinance SPY,AAPL,MSFT --interval 1d --env devtest
```

The command downloads daily prices for the specified tickers using the
``yfinance`` loader inside the ``backend`` package. The ``--env`` option selects
which environment configuration to use.

## Contributing

Contributions are welcome. Feel free to open issues or pull requests.

## License

This project is licensed under the MIT License.
