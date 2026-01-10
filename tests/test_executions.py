from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.executions import (
    Execution,
    ExecutionsApi,
    ExecutionsResponse,
)


class TestExecutionsApi(ApiTestBase):

    def call_api(
        self,
        order_id: Optional[list[int]] = None,
        execution_id: Optional[list[int]] = None,
    ) -> ExecutionsResponse:
        return ExecutionsApi(
            api_key="",
            secret_key="",
        )(
            order_id=order_id,
            execution_id=execution_id,
        )

    def create_response(
        self,
        data: Optional[dict] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = {"list": [self.create_execution_data()]}

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_execution_data(
        self,
        execution_id: int = 92123912,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 223456789,
        position_id: int = 2234567,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        settle_type: str = "OPEN",
        size: int = 10000,
        price: float = 141.269,
        loss_gain: float = 0,
        fee: float = 0,
        settled_swap: float = 0,
        amount: float = 0,
        timestamp: str = "2020-11-24T19:47:51.234Z",
    ) -> dict:
        data = {
            "executionId": execution_id,
            "orderId": order_id,
            "positionId": position_id,
            "symbol": symbol,
            "side": side,
            "settleType": settle_type,
            "size": str(size),
            "price": str(price),
            "lossGain": str(loss_gain),
            "fee": str(fee),
            "settledSwap": str(settled_swap),
            "amount": str(amount),
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        return data

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api(execution_id=[123]))

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api(execution_id=[123])
        url: str = get_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/executions")

    def check_parse_a_data(self, get_mock: MagicMock, **kwargs) -> ExecutionsResponse:
        get_mock.return_value = self.create_response(
            data={"list": [self.create_execution_data(**kwargs)]}
        )
        response = self.call_api(execution_id=[123])
        assert len(response.executions) == 1
        return response

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_execution_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, execution_id=2536464541)
        assert response.executions[0].execution_id == 2536464541

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id="abbb324dff")
        assert response.executions[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_none_without_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id=None)
        assert response.executions[0].client_order_id is None

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, order_id=156789)
        assert response.executions[0].order_id == 156789

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_position_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, position_id=9876543)
        assert response.executions[0].position_id == 9876543

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        for symbol in Execution.Symbol:
            response = self.check_parse_a_data(get_mock, symbol=symbol.value)
            assert response.executions[0].symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        for side in Execution.Side:
            response = self.check_parse_a_data(get_mock, side=side.value)
            assert response.executions[0].side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type(self, get_mock: MagicMock):
        for settle_type in Execution.SettleType:
            response = self.check_parse_a_data(get_mock, settle_type=settle_type.value)
            assert response.executions[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, size=6100)
        assert response.executions[0].size == 6100

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, price=155.44)
        assert response.executions[0].price == 155.44

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_loss_gain(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, loss_gain=15730)
        assert response.executions[0].loss_gain == 15730

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_fee(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, fee=-30)
        assert response.executions[0].fee == -30

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settled_swap(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, settled_swap=515.999)
        assert response.executions[0].settled_swap == 515.999

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_amount(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, amount=16215.999)
        assert response.executions[0].amount == 16215.999

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        response = self.check_parse_a_data(
            get_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.executions[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_multiple_data(
        self, get_mock: MagicMock
    ) -> ExecutionsResponse:
        get_mock.return_value = self.create_response(
            data={"list": [self.create_execution_data(), self.create_execution_data()]}
        )
        response = self.call_api(execution_id=[123])
        assert len(response.executions) == 2

    def check_call_with(self, get_mock, **kwargs):
        get_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        kall = get_mock.call_args
        url = kall.args[0] if kall.args else ""
        if "?" in url:
            query_string = url.split("?", 1)[1]
            params = {}
            for param in query_string.split("&"):
                if "=" in param:
                    key, value = param.split("=", 1)
                    params[key] = value
            return params
        return {}

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_single_execution_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, execution_id=[72123911])
        assert params["executionId"] == "72123911"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_multiple_execution_ids(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, execution_id=[72123911, 92123912])
        assert params["executionId"] == "72123911,92123912"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_single_order_id(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, order_id=[123456789])
        assert params["orderId"] == "123456789"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_multiple_order_ids(
        self,
        get_mock: MagicMock,
    ) -> None:
        params = self.check_call_with(get_mock, order_id=[123456789, 987654321])
        assert params["orderId"] == "123456789,987654321"

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_empty_list(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"list": []})
        response = self.call_api(execution_id=[123])
        assert len(response.executions) == 0
