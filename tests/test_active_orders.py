from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Optional
from unittest.mock import MagicMock, patch
from gmo_fx.api.active_orders import (
    ActiveOrder,
    ActiveOrdersApi,
    ActiveOrdersResponse,
)


class TestActiveOrdersApi(ApiTestBase):

    def call_api(
        self,
        symbol: Optional[ActiveOrdersApi.Symbol] = None,
        prev_id: Optional[int] = None,
        count: Optional[int] = None,
    ) -> ActiveOrdersResponse:
        return ActiveOrdersApi(
            api_key="",
            secret_key="",
        )(symbol=symbol, prev_id=prev_id, count=count)

    def create_response(
        self,
        data: Optional[dict] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = {"list": [self.create_active_order_data()]}

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_active_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "NORMAL",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 10000,
        price: float = 135.5,
        status: str = "ORDERED",
        expiry: str = "20190418",
        timestamp: str = "2019-03-19T01:07:24.217Z",
    ) -> dict:
        data = {
            "rootOrderId": root_order_id,
            "orderId": order_id,
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "executionType": execution_type,
            "settleType": settle_type,
            "size": str(size),
            "price": str(price),
            "status": status,
            "expiry": expiry,
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        return data

    @patch("gmo_fx.api.api_base.get")
    def test_404_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_check_url(
        self,
        get_mock: MagicMock,
    ) -> None:
        get_mock.return_value = self.create_response()
        self.call_api()
        url: str = get_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/activeOrders")

    def check_parse_a_data(
        self, get_mock: MagicMock, **kwargs
    ) -> ActiveOrdersResponse:
        get_mock.return_value = self.create_response(
            data={"list": [self.create_active_order_data(**kwargs)]}
        )
        response = self.call_api()
        assert len(response.active_orders) == 1
        return response

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_root_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, root_order_id=2536464541)
        assert response.active_orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id="abbb324dff")
        assert response.active_orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_none_without_client_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, client_order_id=None)
        assert response.active_orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_id(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, order_id=156789)
        assert response.active_orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_symbol(self, get_mock: MagicMock):
        for symbol in ActiveOrder.Symbol:
            response = self.check_parse_a_data(get_mock, symbol=symbol.value)
            assert response.active_orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_side(self, get_mock: MagicMock):
        for side in ActiveOrder.Side:
            response = self.check_parse_a_data(get_mock, side=side.value)
            assert response.active_orders[0].side == side

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_order_type(self, get_mock: MagicMock):
        for order_type in ActiveOrder.OrderType:
            response = self.check_parse_a_data(get_mock, order_type=order_type.value)
            assert response.active_orders[0].order_type == order_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_execution_type(self, get_mock: MagicMock):
        for execution_type in ActiveOrder.ExecutionType:
            response = self.check_parse_a_data(
                get_mock, execution_type=execution_type.value
            )
            assert response.active_orders[0].execution_type == execution_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_settle_type(self, get_mock: MagicMock):
        for settle_type in ActiveOrder.SettleType:
            response = self.check_parse_a_data(get_mock, settle_type=settle_type.value)
            assert response.active_orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_size(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, size=6100)
        assert response.active_orders[0].size == 6100

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_price(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, price=155.44)
        assert response.active_orders[0].price == 155.44

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_status(self, get_mock: MagicMock):
        for status in ActiveOrder.Status:
            response = self.check_parse_a_data(get_mock, status=status.value)
            assert response.active_orders[0].status == status

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_expiry(self, get_mock: MagicMock):
        response = self.check_parse_a_data(get_mock, expiry="20190418")
        assert response.active_orders[0].expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.get")
    def test_should_get_timestamp(self, get_mock: MagicMock):
        response = self.check_parse_a_data(
            get_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.active_orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_multiple_data(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(
            data={
                "list": [
                    self.create_active_order_data(),
                    self.create_active_order_data(),
                ]
            }
        )
        response = self.call_api()
        assert len(response.active_orders) == 2

    @patch("gmo_fx.api.api_base.get")
    def test_should_parse_empty_list(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"list": []})
        response = self.call_api()
        assert len(response.active_orders) == 0

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
    def test_should_call_api_with_symbol(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, symbol=ActiveOrdersApi.Symbol.USD_JPY)
        assert params["symbol"] == "USD_JPY"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_symbol(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, symbol=None)
        assert "symbol" not in params

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_prev_id(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, prev_id=123456790)
        assert params["prevId"] == "123456790"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_prev_id(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, prev_id=None)
        assert "prevId" not in params

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_count(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, count=10)
        assert params["count"] == "10"

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_without_count(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(get_mock, count=None)
        assert "count" not in params

    @patch("gmo_fx.api.api_base.get")
    def test_should_call_api_with_all_parameters(self, get_mock: MagicMock) -> None:
        params = self.check_call_with(
            get_mock,
            symbol=ActiveOrdersApi.Symbol.USD_JPY,
            prev_id=123456790,
            count=10,
        )
        assert params["symbol"] == "USD_JPY"
        assert params["prevId"] == "123456790"
        assert params["count"] == "10"
