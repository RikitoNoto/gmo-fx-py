from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.klines import get_klines
from datetime import datetime

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
        self.check_404_error(get_mock, lambda: get_klines())

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
        klines_response = get_klines()
        for i, expect in enumerate(expect_klines):
            assert klines_response.klines[i].open_time == expect["openTime"]
            assert klines_response.klines[i].open == expect["open"]
            assert klines_response.klines[i].high == expect["high"]
            assert klines_response.klines[i].low == expect["low"]
            assert klines_response.klines[i].close == expect["close"]
