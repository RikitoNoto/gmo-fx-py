from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.common import Symbol
from gmo_fx.api.position_summary import (
    Position,
    PositionSummaryApi,
    PositionSummaryResponse,
)

from tests.api_test_base import ApiTestBase


class TestPositionSummaryApi(ApiTestBase):

    def call_api(
        self,
    ) -> PositionSummaryResponse:
        return PositionSummaryApi(
            api_key="",
            secret_key="",
        )()

    def create_position_summary_data(
        self,
        average_position_rate: float = 0.0,
        position_loss_gain: float = 0.0,
        side: str = "BUY",
        sum_ordered_size: int = 0,
        sum_position_size: int = 0,
        sum_total_swap: float = 0.0,
        symbol: str = "USD_JPY",
    ) -> dict:
        return {
            "averagePositionRate": average_position_rate,
            "positionLossGain": position_loss_gain,
            "side": side,
            "sumOrderedSize": sum_ordered_size,
            "sumPositionSize": sum_position_size,
            "sumTotalSwap": sum_total_swap,
            "symbol": symbol,
        }

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_average_position_rate(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(average_position_rate=1.0)]
        )
        response = self.call_api()
        average_position_rates = [
            position.average_position_rate for position in response.positions
        ]
        assert average_position_rates[0] == 1.0

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_loss_gain(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(position_loss_gain=1.0)]
        )
        response = self.call_api()
        position_loss_gains = [
            position.position_loss_gain for position in response.positions
        ]
        assert position_loss_gains[0] == 1.0

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_side_buy(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(side="BUY")]
        )
        response = self.call_api()
        sides = [position.side for position in response.positions]
        assert sides[0] == Position.Side.BUY

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_side_sell(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(side="SELL")]
        )
        response = self.call_api()
        sides = [position.side for position in response.positions]
        assert sides[0] == Position.Side.SELL

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_ordered_size(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(sum_ordered_size=984)]
        )
        response = self.call_api()
        sum_ordered_sizes = [
            position.sum_ordered_size for position in response.positions
        ]
        assert sum_ordered_sizes[0] == 984

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_position_size(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(sum_position_size=984)]
        )
        response = self.call_api()
        sum_position_sizes = [
            position.sum_position_size for position in response.positions
        ]
        assert sum_position_sizes[0] == 984

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_sum_total_swap(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(sum_total_swap=654.6)]
        )
        response = self.call_api()
        sum_total_swaps = [position.sum_total_swap for position in response.positions]
        assert sum_total_swaps[0] == 654.6

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_symbol_usd_jpy(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(symbol="USD_JPY")]
        )
        response = self.call_api()
        symbols = [position.symbol for position in response.positions]
        assert symbols[0] == Symbol.USD_JPY

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_symbol_gbp_usd(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(symbol="GBP_USD")]
        )
        response = self.call_api()
        symbols = [position.symbol for position in response.positions]
        assert symbols[0] == Symbol.GBP_USD

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_some_positions(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[
                self.create_position_summary_data(symbol="USD_JPY"),
                self.create_position_summary_data(symbol="GBP_USD"),
            ]
        )
        response = self.call_api()
        symbols = [position.symbol for position in response.positions]
        assert symbols[0] == Symbol.USD_JPY
        assert symbols[1] == Symbol.GBP_USD
