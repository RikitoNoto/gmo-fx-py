from datetime import datetime
from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.common import Side, Symbol
from gmo_fx.api.latest_executions import (
    Execution,
    LatestExecutionsApi,
    LatestExecutionsResponse,
)

from tests.api_test_base import ApiTestBase


class TestLatestExecutionsApi(ApiTestBase):

    def call_api(
        self,
    ) -> LatestExecutionsResponse:
        return LatestExecutionsApi(
            api_key="",
            secret_key="",
        )()

    def create_execution_data(
        self,
        amount: float = 0.0,
        execution_id: int = 0,
        client_order_id: str = "id",
        order_id: int = 0,
        position_id: int = 0,
        symbol: str = "USD_JPY",
        side: str = "SELL",
        settle_type: str = "CLOSE",
        size: int = 1,
        price: float = 0.0,
        loss_gain: int = 0,
        fee: int = 0,
        settled_swap: float = 0.0,
        timestamp: datetime = datetime.now(),
    ) -> dict:
        return {
            "amount": amount,
            "executionId": execution_id,
            "clientOrderId": client_order_id,
            "orderId": order_id,
            "positionId": position_id,
            "symbol": symbol,
            "side": side,
            "settleType": settle_type,
            "size": f"{size}",
            "price": f"{price}",
            "lossGain": f"{loss_gain}",
            "fee": f"{fee}",
            "settledSwap": f"{settled_swap}",
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%f%Z"),
        }

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_amount(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(amount=1.2)]
        )
        response = self.call_api()
        amounts = [execution.amount for execution in response.executions]
        assert amounts[0] == 1.2

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_execution_id(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(execution_id=12)]
        )
        response = self.call_api()
        execution_ids = [execution.execution_id for execution in response.executions]
        assert execution_ids[0] == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_client_order_id(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(client_order_id="fdsa")]
        )
        response = self.call_api()
        client_order_ids = [
            execution.client_order_id for execution in response.executions
        ]
        assert client_order_ids[0] == "fdsa"

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_id(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(order_id=12)]
        )
        response = self.call_api()
        order_ids = [execution.order_id for execution in response.executions]
        assert order_ids[0] == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_id(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(position_id=12)]
        )
        response = self.call_api()
        position_ids = [execution.position_id for execution in response.executions]
        assert position_ids[0] == 12

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(symbol="NZD_USD")]
        )
        response = self.call_api()
        symbols = [execution.symbol for execution in response.executions]
        assert symbols[0] == Symbol.NZD_USD

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(side="BUY")]
        )
        response = self.call_api()
        sides = [execution.side for execution in response.executions]
        assert sides[0] == Side.BUY
