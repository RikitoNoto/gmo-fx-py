import json
from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Optional
from unittest.mock import MagicMock, patch
from api.ifo_order import (
    IfoOrder,
    IfoOrderApi,
    IfoOrderResponse,
)


class TestIfoOrderApi(ApiTestBase):

    def call_api(
        self,
        symbol: IfoOrderApi.Symbol = IfoOrderApi.Symbol.USD_JPY,
        first_side: IfoOrderApi.Side = IfoOrderApi.Side.BUY,
        first_execution_type: IfoOrderApi.ExecutionType = (
            IfoOrderApi.ExecutionType.LIMIT
        ),
        first_size: int = 10000,
        first_price: float = 135,
        second_size: int = 10000,
        second_limit_price: float = 140,
        second_stop_price: float = 132,
        client_order_id: Optional[str] = None,
    ) -> IfoOrderResponse:
        return IfoOrderApi(
            api_key="",
            secret_key="",
        )(
            symbol=symbol,
            first_side=first_side,
            first_execution_type=first_execution_type,
            first_size=first_size,
            first_price=first_price,
            second_size=second_size,
            second_limit_price=second_limit_price,
            second_stop_price=second_stop_price,
            client_order_id=client_order_id,
        )

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = [self.create_ifo_order_data()]

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_ifo_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "IFDOCO",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 10000,
        price: float = 135,
        status: str = "WAITING",
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
        self.check_404_error(post_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(
        self,
        post_mock: MagicMock,
    ) -> None:
        post_mock.return_value = self.create_response()
        self.call_api()
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/ifoOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> IfoOrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_ifo_order_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.ifo_orders) == 1
        return response

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert response.ifo_orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert response.ifo_orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id=None)
        assert response.ifo_orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_id=156789)
        assert response.ifo_orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in IfoOrder.Symbol:
            response = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert response.ifo_orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in IfoOrder.Side:
            response = self.check_parse_a_data(post_mock, side=side.value)
            assert response.ifo_orders[0].side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_type="IFDOCO")
        assert response.ifo_orders[0].order_type == IfoOrder.OrderType.IFDOCO

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        for execution_type in IfoOrder.ExecutionType:
            response = self.check_parse_a_data(
                post_mock, execution_type=execution_type.value
            )
            assert response.ifo_orders[0].execution_type == execution_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in IfoOrder.SettleType:
            response = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert response.ifo_orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, size=6100)
        assert response.ifo_orders[0].size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_price(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, price=155.44)
        assert response.ifo_orders[0].price == 155.44

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in IfoOrder.Status:
            response = self.check_parse_a_data(post_mock, status=status.value)
            assert response.ifo_orders[0].status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_expiry(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, expiry="20190418")
        assert response.ifo_orders[0].expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        response = self.check_parse_a_data(
            post_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.ifo_orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock) -> IfoOrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_ifo_order_data(), self.create_ifo_order_data()]
        )
        response = self.call_api()
        assert len(response.ifo_orders) == 2

    def check_call_with(self, post_mock, **kwargs):
        post_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        kall = post_mock.call_args
        request_body = kall.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_symbol(self, post_mock: MagicMock) -> None:
        for symbol in IfoOrderApi.Symbol:
            body = self.check_call_with(post_mock, symbol=symbol)
            assert body["symbol"] == symbol.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_client_order_id(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, client_order_id="alfsdj32432enl")
        assert body["clientOrderId"] == "alfsdj32432enl"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_client_order_id(
        self, post_mock: MagicMock
    ) -> None:
        body = self.check_call_with(post_mock, client_order_id=None)
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_side(self, post_mock: MagicMock) -> None:
        for side in IfoOrderApi.Side:
            body = self.check_call_with(post_mock, first_side=side)
            assert body["firstSide"] == side.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_execution_type(
        self,
        post_mock: MagicMock,
    ) -> None:
        for execution_type in IfoOrderApi.ExecutionType:
            body = self.check_call_with(post_mock, first_execution_type=execution_type)
            assert body["firstExecutionType"] == execution_type.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_size(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, first_size=6530)
        assert body["firstSize"] == "6530"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_first_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, first_price=155.66)
        assert body["firstPrice"] == "155.66"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_size(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, second_size=13000)
        assert body["secondSize"] == "13000"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_limit_price(
        self, post_mock: MagicMock
    ) -> None:
        body = self.check_call_with(post_mock, second_limit_price=145.5)
        assert body["secondLimitPrice"] == "145.5"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_second_stop_price(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, second_stop_price=132.5)
        assert body["secondStopPrice"] == "132.5"
