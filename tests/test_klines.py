import re
from typing import Callable, Optional
from unittest.mock import MagicMock, patch

import pytest
from gmo_fx.klines import get_klines
from datetime import datetime

from gmo_fx.symbols import Symbol
from tests.api_test_base import ApiTestBase


class TestKlineApi(ApiTestBase):

    def create_kline(
        self,
        open_time: str = "0000000000000",
        open: float = 0.0,
        high: float = 0.0,
        low: float = 0.0,
        close: float = 0.0,
    ) -> dict:
        return {
            "openTime": open_time,
            "open": str(open),
            "high": str(high),
            "low": str(low),
            "close": str(close),
        }

    def create_klines(
        self, size: int, kline_builder: Optional[Callable[[int], dict]] = None
    ) -> list[dict]:
        kline_builder = kline_builder or (lambda i: self.create_kline())
        return [kline_builder(i) for i in range(size)]

    @patch("gmo_fx.klines.get")
    def test_klines_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: get_klines(Symbol.USD_JPY, "BID"))

    @patch("gmo_fx.klines.get")
    def test_should_get_klines_from_response_klines_accesser(self, get_mock: MagicMock):
        expect_klines = [
            {
                "openTime": datetime(i + 1980, 1, 1),
                "open": float(i),
                "high": float(i),
                "low": float(i),
                "close": float(i),
            }
            for i in range(100)
        ]
        get_mock.return_value = self.create_response(
            data=self.create_klines(
                100,
                lambda i: self.create_kline(
                    open_time=str(int(expect_klines[i]["openTime"].timestamp()) * 1000),
                    open=expect_klines[i]["open"],
                    high=expect_klines[i]["high"],
                    low=expect_klines[i]["low"],
                    close=expect_klines[i]["close"],
                ),
            )
        )
        klines_response = get_klines(Symbol.USD_JPY, "BID")
        for i, expect in enumerate(expect_klines):
            assert klines_response.klines[i].open_time == expect["openTime"]
            assert klines_response.klines[i].open == expect["open"]
            assert klines_response.klines[i].high == expect["high"]
            assert klines_response.klines[i].low == expect["low"]
            assert klines_response.klines[i].close == expect["close"]

    def check_url_parameter(
        self,
        get_mock: MagicMock,
        symbol: Symbol = Symbol.USD_JPY,
        symbol_str: str = "USD_JPY",
        price_type: str = "ASK",
        price_type_str: str = "ASK",
    ) -> None:

        get_mock.return_value = self.create_response(data=self.create_klines(1))
        get_klines(symbol, price_type)
        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"symbol={symbol_str}" in param
        assert f"priceType={price_type_str}" in param

    symbol_strs = [
        (Symbol.USD_JPY, "USD_JPY"),
        (Symbol.EUR_JPY, "EUR_JPY"),
        (Symbol.GBP_JPY, "GBP_JPY"),
        (Symbol.AUD_JPY, "AUD_JPY"),
        (Symbol.NZD_JPY, "NZD_JPY"),
        (Symbol.CAD_JPY, "CAD_JPY"),
        (Symbol.CHF_JPY, "CHF_JPY"),
        (Symbol.TRY_JPY, "TRY_JPY"),
        (Symbol.ZAR_JPY, "ZAR_JPY"),
        (Symbol.MXN_JPY, "MXN_JPY"),
        (Symbol.EUR_USD, "EUR_USD"),
        (Symbol.GBP_USD, "GBP_USD"),
        (Symbol.AUD_USD, "AUD_USD"),
        (Symbol.NZD_USD, "NZD_USD"),
    ]

    @pytest.mark.parametrize("symbol, symbol_str", symbol_strs)
    @patch("gmo_fx.klines.get")
    def test_should_call_get_with_symbol(
        self, get_mock: MagicMock, symbol: Symbol, symbol_str: str
    ):
        self.check_url_parameter(
            get_mock,
            symbol=symbol,
            symbol_str=symbol_str,
        )

    price_type_strs = [
        ("BID", "BID"),
        ("ASK", "ASK"),
    ]

    @pytest.mark.parametrize("price_type, price_type_str", price_type_strs)
    @patch("gmo_fx.klines.get")
    def test_should_call_get_with_price_type(
        self, get_mock: MagicMock, price_type: str, price_type_str: str
    ):
        self.check_url_parameter(
            get_mock,
            price_type=price_type,
            price_type_str=price_type_str,
        )
