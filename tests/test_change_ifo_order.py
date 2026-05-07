import json
from datetime import datetime, timezone
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from gmo_fx import ChangeIfoOrderApi as PackageChangeIfoOrderApi
from gmo_fx.api.change_ifo_order import (
    ChangeIfoOrderApi,
    ChangeIfoOrderResponse,
    Order,
)
from tests.api_test_base import ApiTestBase


class TestChangeIfoOrderApi(ApiTestBase):

    def call_api(
        self,
        root_order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        first_price: Optional[float] = None,
        second_limit_price: Optional[float] = None,
        second_stop_price: Optional[float] = None,
    ) -> ChangeIfoOrderResponse:
        return ChangeIfoOrderApi(
            api_key="",
            secret_key="",
        )(
            root_order_id=root_order_id,
            client_order_id=client_order_id,
            first_price=first_price,
            second_limit_price=second_limit_price,
            second_stop_price=second_stop_price,
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
        side: str = "SELL",
        order_type: str = "IFDOCO",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 10000,
        price: float = 142.3,
        status: str = "ORDERED",
        cancel_type: Optional[str] = None,
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

        if cancel_type is not None:
            data["cancelType"] = cancel_type

        return data

    @patch("gmo_fx.api.api_base.post")
    def test_404_error(self, post_mock: MagicMock):
        self.check_404_error(
            post_mock,
            lambda: self.call_api(root_order_id=123456789, first_price=142.3),
        )

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(self, post_mock: MagicMock) -> None:
        post_mock.return_value = self.create_response()
        self.call_api(root_order_id=123456789, first_price=142.3)
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/changeIfoOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> Order:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api(root_order_id=123456789, first_price=142.3)
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
            side="BUY",
            execution_type="STOP",
            settle_type="CLOSE",
            size=6100,
            price=155.44,
            status="WAITING",
            cancel_type="OCO",
            expiry="20240913",
            timestamp="2024-09-13T15:21:03.059Z",
        )

        assert order.root_order_id == 2536464541
        assert order.client_order_id == "abbb324dff"
        assert order.order_id == 156789
        assert order.symbol == Order.Symbol.EUR_USD
        assert order.side == Order.Side.BUY
        assert order.order_type == Order.OrderType.IFDOCO
        assert order.execution_type == Order.ExecutionType.STOP
        assert order.settle_type == Order.SettleType.CLOSE
        assert order.size == 6100
        assert order.price == 155.44
        assert order.status == Order.Status.WAITING
        assert order.cancel_type == Order.CancelType.OCO
        assert order.expiry == datetime(2024, 9, 13).date()
        assert order.timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, client_order_id=None)
        assert order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_cancel_type(self, post_mock: MagicMock):
        order = self.check_parse_a_data(post_mock, cancel_type=None)
        assert order.cancel_type is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data=[
                self.create_order_data(),
                self.create_order_data(order_id=123456790, settle_type="CLOSE"),
                self.create_order_data(
                    order_id=123456791,
                    execution_type="STOP",
                    settle_type="CLOSE",
                    status="WAITING",
                ),
            ]
        )
        response = self.call_api(root_order_id=123456789, first_price=142.3)
        assert len(response.orders) == 3

    def check_call_with(self, post_mock: MagicMock, **kwargs):
        post_mock.return_value = self.create_response()
        if "root_order_id" not in kwargs and "client_order_id" not in kwargs:
            kwargs["root_order_id"] = 123456789
        if (
            "first_price" not in kwargs
            and "second_limit_price" not in kwargs
            and "second_stop_price" not in kwargs
        ):
            kwargs["first_price"] = 142.3
        self.call_api(**kwargs)
        request_body = post_mock.call_args.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_root_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, root_order_id=987654321)
        assert body["rootOrderId"] == 987654321

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_root_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            root_order_id=None,
            client_order_id="test123",
        )
        assert "rootOrderId" not in body.keys()

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
            root_order_id=123456789,
        )
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, first_price=142.3)
        assert body["firstPrice"] == "142.3"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_first_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            first_price=None,
            second_limit_price=136,
        )
        assert "firstPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_limit_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, second_limit_price=136)
        assert body["secondLimitPrice"] == "136"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_second_limit_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(
            post_mock,
            first_price=142.3,
            second_limit_price=None,
        )
        assert "secondLimitPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_stop_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, second_stop_price=143.1)
        assert body["secondStopPrice"] == "143.1"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_second_stop_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(
            post_mock,
            first_price=142.3,
            second_stop_price=None,
        )
        assert "secondStopPrice" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_raise_error_without_order_identifier(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        with pytest.raises(ValueError):
            self.call_api(
                root_order_id=None,
                client_order_id=None,
                first_price=142.3,
            )

    @patch("gmo_fx.api.api_base.post")
    def test_should_raise_error_without_change_price(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        with pytest.raises(ValueError):
            self.call_api(
                root_order_id=123456789,
                first_price=None,
                second_limit_price=None,
                second_stop_price=None,
            )

    def test_should_import_from_package(self) -> None:
        assert PackageChangeIfoOrderApi is ChangeIfoOrderApi
