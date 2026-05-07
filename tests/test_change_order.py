import json
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from gmo_fx import ChangeOrderApi as PackageChangeOrderApi
from gmo_fx.api.change_order import ChangeOrderApi, ChangeOrderResponse, Order
from tests.api_test_base import ApiTestBase


class TestChangeOrderApi(ApiTestBase):

    def call_api(
        self,
        price: Optional[float] = 139.0,
        order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
    ) -> ChangeOrderResponse:
        return ChangeOrderApi(
            api_key="",
            secret_key="",
        )(
            price=price,
            order_id=order_id,
            client_order_id=client_order_id,
        )

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = [self.create_order_data()]

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "NORMAL",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 100,
        price: float = 139.0,
        status: str = "ORDERED",
        expiry: str = "20220113",
        timestamp: str = "2019-03-19T02:15:06.059Z",
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

    @patch("gmo_fx.api.api_base.post")
    def test_404_error(self, post_mock: MagicMock):
        self.check_404_error(
            post_mock,
            lambda: self.call_api(order_id=123456789),
        )

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(self, post_mock: MagicMock) -> None:
        post_mock.return_value = self.create_response()
        self.call_api(order_id=123456789)
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/changeOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> Order:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api(order_id=123456789)
        assert len(response.orders) == 1
        return response.orders[0]

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_order(self, post_mock: MagicMock):
        order = self.check_parse_a_data(
            post_mock,
            root_order_id=2536464541,
            client_order_id="abbb324dff",
            order_id=156789,
            symbol="EUR_USD",
            side="SELL",
            execution_type="STOP",
            settle_type="CLOSE",
            size=6100,
            price=155.44,
            status="MODIFYING",
            expiry="20190418",
            timestamp="2024-09-13T15:21:03.059Z",
        )

        assert order.root_order_id == 2536464541
        assert order.client_order_id == "abbb324dff"
        assert order.order_id == 156789
        assert order.symbol == Order.Symbol.EUR_USD
        assert order.side == Order.Side.SELL
        assert order.order_type == Order.OrderType.NORMAL
        assert order.execution_type == Order.ExecutionType.STOP
        assert order.settle_type == Order.SettleType.CLOSE
        assert order.size == 6100
        assert order.price == 155.44
        assert order.status == Order.Status.MODIFYING
        assert order.expiry == datetime(2019, 4, 18).date()
        assert order.timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_normal_order_type(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, order_type="NORMAL")
        assert order.order_type == Order.OrderType.NORMAL

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id=None)
        assert order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(), self.create_order_data()]
        )
        response = self.call_api(order_id=123456789)
        assert len(response.orders) == 2

    def check_call_with(self, post_mock: MagicMock, **kwargs):
        post_mock.return_value = self.create_response()
        if "order_id" not in kwargs and "client_order_id" not in kwargs:
            kwargs["order_id"] = 123456789
        self.call_api(**kwargs)
        request_body = post_mock.call_args.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, order_id=987654321)
        assert body["orderId"] == 987654321

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            order_id=None,
            client_order_id="test123",
        )
        assert "orderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_client_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, client_order_id="alfsdj32432enl")
        assert body["clientOrderId"] == "alfsdj32432enl"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_client_order_id(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(
            post_mock,
            client_order_id=None,
            order_id=123456789,
        )
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, order_id=123456789, price=155.66)
        assert body["price"] == "155.66"

    @patch("gmo_fx.api.api_base.post")
    def test_should_raise_error_without_order_identifier(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        with pytest.raises(ValueError):
            self.call_api(order_id=None, client_order_id=None)

    def test_should_import_from_package(self) -> None:
        assert PackageChangeOrderApi is ChangeOrderApi
