from typing import Callable, Optional, Union
import pytest
import json
from unittest.mock import MagicMock, patch
from gmo_fx.symbols import Symbol
from gmo_fx.ticker import get_ticker
from datetime import datetime


class TestTickerApi:
    SYMBOLS = [
        "USD_JPY",
        "EUR_JPY",
        "GBP_JPY",
        "AUD_JPY",
        "NZD_JPY",
        "CAD_JPY",
        "CHF_JPY",
        "TRY_JPY",
        "ZAR_JPY",
        "MXN_JPY",
        "EUR_USD",
        "GBP_USD",
        "AUD_USD",
        "NZD_USD",
    ]

    SYMBOLS_TABLE = {
        Symbol.USD_JPY: "USD_JPY",
        Symbol.EUR_JPY: "EUR_JPY",
        Symbol.GBP_JPY: "GBP_JPY",
        Symbol.AUD_JPY: "AUD_JPY",
        Symbol.NZD_JPY: "NZD_JPY",
        Symbol.CAD_JPY: "CAD_JPY",
        Symbol.CHF_JPY: "CHF_JPY",
        Symbol.TRY_JPY: "TRY_JPY",
        Symbol.ZAR_JPY: "ZAR_JPY",
        Symbol.MXN_JPY: "MXN_JPY",
        Symbol.EUR_USD: "EUR_USD",
        Symbol.GBP_USD: "GBP_USD",
        Symbol.AUD_USD: "AUD_USD",
        Symbol.NZD_USD: "NZD_USD",
    }

    def create_ticker_data(
        self,
        symbol: str,
        status: str = "OPEN",
        ask: float = 0.0,
        bid: float = 0.0,
        timestamp: Optional[datetime] = None,
    ) -> dict:
        return {
            "symbol": symbol,
            "ask": ask,
            "bid": bid,
            "timestamp": (timestamp or datetime.now()).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
            "status": status,
        }

    def create_tickers_data(
        self, exchange_data_builder: Optional[Callable[[str], dict]] = None
    ) -> list[dict]:
        exchange_data_builder = exchange_data_builder or self.create_ticker_data
        return [exchange_data_builder(symbol) for symbol in self.SYMBOLS]

    def create_response(
        self,
        data: Optional[Union[dict, list]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        json_data = {
            "status": 0,
            "data": data,
            "responsetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        response.json.return_value = json_data
        response.text = text or json.dumps(json_data)
        return response

    @patch("gmo_fx.ticker.get")
    def test_ticker_error(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            status_code=404,
            text="Not Found",
        )
        with pytest.raises(RuntimeError):
            get_ticker()

    @patch("gmo_fx.ticker.get")
    def test_should_get_symbols_from_ticker(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data=self.create_tickers_data())
        ticker_response = get_ticker()
        symbols = [ticker.symbol for ticker in ticker_response.tickers]
        for symbol in Symbol:
            assert symbol in symbols
            symbols.remove(symbol)
        else:
            assert len(symbols) == 0

    @patch("gmo_fx.ticker.get")
    def test_should_get_bid_ask_from_ticker(self, get_mock: MagicMock):
        def fixture_ask_bid(symbol: str):
            return self.SYMBOLS.index(symbol), self.SYMBOLS.index(symbol) * 100

        def fixture_ticker_data(symbol: str) -> dict:
            ask, bid = fixture_ask_bid(symbol)
            return self.create_ticker_data(symbol, ask=ask, bid=bid)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = get_ticker().tickers
        for rate in rates:
            assert rate.ask == fixture_ask_bid(self.SYMBOLS_TABLE[rate.symbol])[0]
            assert rate.bid == fixture_ask_bid(self.SYMBOLS_TABLE[rate.symbol])[1]

    @patch("gmo_fx.ticker.get")
    def test_should_get_timestamp_from_ticker(self, get_mock: MagicMock):
        def fixture_timestamp(symbol: str):
            return datetime(2000, 12, self.SYMBOLS.index(symbol) + 1)  # 0日はないので

        def fixture_ticker_data(symbol: str) -> dict:
            timestamp = fixture_timestamp(symbol)
            return self.create_ticker_data(symbol, timestamp=timestamp)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = get_ticker().tickers
        for rate in rates:
            assert rate.timestamp == fixture_timestamp(self.SYMBOLS_TABLE[rate.symbol])

    @patch("gmo_fx.ticker.get")
    def test_should_get_status_from_ticker(self, get_mock: MagicMock):
        def fixture_status(symbol: str):
            statuses = ["OPEN", "CLOSE"]
            return statuses[self.SYMBOLS.index(symbol) % len(statuses)]

        def fixture_ticker_data(symbol: str) -> dict:
            status = fixture_status(symbol)
            return self.create_ticker_data(symbol, status=status)

        get_mock.return_value = self.create_response(
            data=self.create_tickers_data(exchange_data_builder=fixture_ticker_data)
        )
        rates = get_ticker().tickers
        for rate in rates:
            status_str = fixture_status(self.SYMBOLS_TABLE[rate.symbol])
            for status in ["OPEN", "CLOSE"]:
                if status == status_str:
                    assert rate.status == status
                    break
            else:
                assert False