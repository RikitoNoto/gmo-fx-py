from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.symbols import Symbol
from gmo_fx.api.position_summary import PositionSummaryApi, PositionSummaryResponse

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
    def test_should_get_equity(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_position_summary_data(average_position_rate=1.0)]
        )
        response = self.call_api()
        average_position_rates = [
            position.average_position_rate for position in response.positions
        ]
        assert average_position_rates[0] == 1.0
