import json
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from gmo_fx import ChangeIfdOrderApi as PackageChangeIfdOrderApi
from gmo_fx.api.change_ifd_order import ChangeIfdOrderApi, ChangeIfdOrderResponse, Order
from tests.api_test_base import ApiTestBase


class TestChangeIfdOrderApi(ApiTestBase):

    def call_api(
        self,
        root_order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        first_price: Optional[float] = 136.201,
        second_price: Optional[float] = 139.802,
    ) -> ChangeIfdOrderResponse:
        return ChangeIfdOrderApi(
            api_key="",
            secret_key="",
        )(
            root_order_id=root_order_id,
            client_order_id=client_order_id,
            first_price=first_price,
            second_price=second_price,
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
        order_type: str = "IFD",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 10000,
        price: float = 136.201,
        status: str = "ORDERED",
        expiry: str = "20190418",
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
        self.check_404_error(post_mock, lambda: self.call_api(root_order_id=123456789))

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        self.call_api(root_order_id=123456789)
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/changeIfdOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> Order:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api(root_order_id=123456789)
        assert len(response.orders) == 1
        return response.orders[0]

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert order.root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert order.client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id=None)
        assert order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, order_id=156789)
        assert order.order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in Order.Symbol:
            order = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert order.symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in Order.Side:
            order = self.check_parse_a_data(post_mock, side=side.value)
            assert order.side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        for order_type in Order.OrderType:
            order = self.check_parse_a_data(post_mock, order_type=order_type.value)
            assert order.order_type == order_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        for execution_type in Order.ExecutionType:
            order = self.check_parse_a_data(
                post_mock, execution_type=execution_type.value
            )
            assert order.execution_type == execution_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in Order.SettleType:
            order = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert order.settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, size=6100)
        assert order.size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_price(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, price=155.44)
        assert order.price == 155.44

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in Order.Status:
            order = self.check_parse_a_data(post_mock, status=status.value)
            assert order.status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_expiry(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, expiry="20190418")
        assert order.expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, timestamp="2024-09-13T15:21:03.059Z")
        assert order.timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(), self.create_order_data()]
        )
        response = self.call_api(root_order_id=123456789)
        assert len(response.orders) == 2

    def check_call_with(self, post_mock: MagicMock, **kwargs) -> dict:
        post_mock.return_value = self.create_response()
        if "root_order_id" not in kwargs and "client_order_id" not in kwargs:
            kwargs["root_order_id"] = 123456789
        self.call_api(**kwargs)
        kall = post_mock.call_args
        request_body = kall.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_root_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, root_order_id=987654321)
        assert body["rootOrderId"] == 987654321

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_root_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock, root_order_id=None, client_order_id="test123"
        )
        assert "rootOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_client_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, client_order_id="alfsdj32432enl")
        assert body["clientOrderId"] == "alfsdj32432enl"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_client_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock, client_order_id=None, root_order_id=123456789
        )
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, first_price=136.201)
        assert body["firstPrice"] == "136.201"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_first_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, first_price=None, second_price=139.802)
        assert "firstPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, second_price=139.802)
        assert body["secondPrice"] == "139.802"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_second_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, second_price=None, first_price=136.201)
        assert "secondPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_both_prices(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock, first_price=136.201, second_price=139.802
        )
        assert body["firstPrice"] == "136.201"
        assert body["secondPrice"] == "139.802"

    def test_raise_error_without_order_ids(self) -> None:
        with pytest.raises(ValueError):
            self.call_api(root_order_id=None, client_order_id=None)

    def test_should_import_from_package(self) -> None:
        assert PackageChangeIfdOrderApi is ChangeIfdOrderApi
