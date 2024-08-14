from datetime import datetime, timedelta, timezone
import re
from typing import Callable, Optional
from unittest.mock import MagicMock, patch
from gmo_fx.common import SettleType, Side, Symbol
from gmo_fx.api.latest_executions import (
    Execution,
    LatestExecutionsApi,
    LatestExecutionsResponse,
)

from tests.api_test_base import ApiTestBase


class TestLatestExecutionsApi(ApiTestBase):

    def call_api(
        self,
        symbol: Symbol = Symbol.USD_JPY,
        count: int = 100,
    ) -> LatestExecutionsResponse:
        return LatestExecutionsApi(
            api_key="",
            secret_key="",
        )(symbol, count)

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
            "timestamp": timestamp.astimezone(timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%S.%fZ"
            ),
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
    def test_should_get_side_buy(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(side="BUY")]
        )
        response = self.call_api()
        sides = [execution.side for execution in response.executions]
        assert sides[0] == Side.BUY

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side_sell(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(side="SELL")]
        )
        response = self.call_api()
        sides = [execution.side for execution in response.executions]
        assert sides[0] == Side.SELL

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type_open(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(settle_type="OPEN")]
        )
        response = self.call_api()
        settle_types = [execution.settle_type for execution in response.executions]
        assert settle_types[0] == SettleType.OPEN

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type_close(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(settle_type="CLOSE")]
        )
        response = self.call_api()
        settle_types = [execution.settle_type for execution in response.executions]
        assert settle_types[0] == SettleType.CLOSE

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(size=100)]
        )
        response = self.call_api()
        sizes = [execution.size for execution in response.executions]
        assert sizes[0] == 100

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(price=100.5)]
        )
        response = self.call_api()
        prices = [execution.price for execution in response.executions]
        assert prices[0] == 100.5

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_loss_gain(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(loss_gain=30)]
        )
        response = self.call_api()
        loss_gains = [execution.loss_gain for execution in response.executions]
        assert loss_gains[0] == 30

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_fee(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(fee=40)]
        )
        response = self.call_api()
        fees = [execution.fee for execution in response.executions]
        assert fees[0] == 40

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settled_swap(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[self.create_execution_data(settled_swap=40.4)]
        )
        response = self.call_api()
        settled_swaps = [execution.settled_swap for execution in response.executions]
        assert settled_swaps[0] == 40.4

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data=[
                self.create_execution_data(
                    timestamp=datetime(2024, 1, 2, 20, 11, tzinfo=timezone.utc)
                )
            ]
        )
        response = self.call_api()
        timestamps = [execution.timestamp for execution in response.executions]
        delta = datetime(2024, 1, 2, 20, 11, tzinfo=timezone.utc) - timestamps[0]
        assert delta.seconds == 0

    @patch("gmo_fx.api.api_base.get")
    def test_should_set_url_symbol(self, get_mock: MagicMock):

        get_mock.return_value = self.create_response(
            data=[self.create_execution_data()]
        )
        response = self.call_api(symbol=Symbol.EUR_USD)

        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"symbol=EUR_USD" in param

    @patch("gmo_fx.api.api_base.get")
    def test_should_set_url_count(self, get_mock: MagicMock):

        get_mock.return_value = self.create_response(
            data=[self.create_execution_data()]
        )
        response = self.call_api(count=20)

        param_match = re.search("\?(.*)", get_mock.mock_calls[0].args[0])
        param = param_match.group(1)
        assert f"count=20" in param
