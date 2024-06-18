from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.symbols import Symbol
from gmo_fx.api.assets import AssetsApi, AssetsResponse

from tests.api_test_base import ApiTestBase


class TestAssetsApi(ApiTestBase):

    def call_api(
        self,
    ) -> AssetsResponse:
        return AssetsApi(
            api_key="",
            secret_key="",
        )()

    def create_assets_data(
        self,
        equity: int = 0,
        available_amount: int = 0,
        balance: int = 0,
        estimated_trade_fee: float = 0.0,
        margin: int = 0,
        margin_ratio: float = 0.0,
        position_loss_gain: float = 0.0,
        total_swap: float = 0.0,
        transferable_amount: int = 0,
    ) -> dict:
        return [
            {
                "equity": equity,
                "availableAmount": available_amount,
                "balance": balance,
                "estimatedTradeFee": estimated_trade_fee,
                "margin": margin,
                "marginRatio": margin_ratio,
                "positionLossGain": position_loss_gain,
                "totalSwap": total_swap,
                "transferableAmount": transferable_amount,
            }
        ]

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_equity(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=self.create_assets_data(equity=1)
        )
        response = self.call_api()
        equities = [asset.equity for asset in response.assets]
        assert equities[0] == 1
