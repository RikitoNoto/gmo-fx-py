import json
from datetime import datetime, timezone
from tests.api_test_base import ApiTestBase
from typing import Optional
from unittest.mock import MagicMock, patch
from api.speed_order import (
    SpeedOrder,
    SpeedOrderApi,
    SpeedOrderResponse,
)


class TestSpeedOrderApi(ApiTestBase):

    def call_api(
        self,
        symbol: SpeedOrderApi.Symbol = SpeedOrderApi.Symbol.USD_JPY,
        side: SpeedOrderApi.Side = SpeedOrderApi.Side.BUY,
        size: int = 10000,
        client_order_id: Optional[str] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
        is_hedgeable: Optional[bool] = None,
    ) -> SpeedOrderResponse:
        return SpeedOrderApi(
            api_key="",
            secret_key="",
        )(
            symbol=symbol,
            side=side,
            size=size,
            client_order_id=client_order_id,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            is_hedgeable=is_hedgeable,
        )

    def create_response(
        self,
        data: Optional[list[dict]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = [self.create_speed_order_data()]

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_speed_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "NORMAL",
        execution_type: str = "MARKET",
        settle_type: str = "OPEN",
        size: int = 10000,
        status: str = "EXECUTED",
        cancel_type: Optional[str] = None,
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
            "status": status,
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if cancel_type is not None:
            data["cancelType"] = cancel_type

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
        assert url.startswith("https://forex-api.coin.z.com/private/v1/speedOrder")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> SpeedOrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_speed_order_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.speed_orders) == 1
        return response

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert response.speed_orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert response.speed_orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id=None)
        assert response.speed_orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_id=156789)
        assert response.speed_orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in SpeedOrder.Symbol:
            response = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert response.speed_orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in SpeedOrder.Side:
            response = self.check_parse_a_data(post_mock, side=side.value)
            assert response.speed_orders[0].side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_type="NORMAL")
        assert response.speed_orders[0].order_type == SpeedOrder.OrderType.NORMAL

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, execution_type="MARKET")
        assert response.speed_orders[0].execution_type == (
            SpeedOrder.ExecutionType.MARKET
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in SpeedOrder.SettleType:
            response = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert response.speed_orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, size=6100)
        assert response.speed_orders[0].size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in SpeedOrder.Status:
            response = self.check_parse_a_data(post_mock, status=status.value)
            assert response.speed_orders[0].status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_cancel_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, cancel_type="PRICE_BOUND")
        assert response.speed_orders[0].cancel_type == SpeedOrder.CancelType.PRICE_BOUND

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_cancel_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, cancel_type=None)
        assert response.speed_orders[0].cancel_type is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        response = self.check_parse_a_data(
            post_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.speed_orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock) -> SpeedOrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_speed_order_data(), self.create_speed_order_data()]
        )
        response = self.call_api()
        assert len(response.speed_orders) == 2

    def check_call_with(self, post_mock, **kwargs):
        post_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        kall = post_mock.call_args
        request_body = kall.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_symbol(
        self,
        post_mock: MagicMock,
    ) -> None:
        for symbol in SpeedOrderApi.Symbol:
            body = self.check_call_with(post_mock, symbol=symbol)
            assert body["symbol"] == symbol.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_side(
        self,
        post_mock: MagicMock,
    ) -> None:
        for side in SpeedOrderApi.Side:
            body = self.check_call_with(post_mock, side=side)
            assert body["side"] == side.value

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_size(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, size=6530)
        assert body["size"] == "6530"

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
        body = self.check_call_with(post_mock, client_order_id=None)
        assert "clientOrderId" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_lower_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, lower_bound=101.93)
        assert body["lowerBound"] == "101.93"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_lower_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, lower_bound=None)
        assert "lowerBound" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_upper_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, upper_bound=99.85)
        assert body["upperBound"] == "99.85"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_upper_bound(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, upper_bound=None)
        assert "upperBound" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_is_hedgeable(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, is_hedgeable=True)
        assert body["isHedgeable"] is True

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_is_hedgeable(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, is_hedgeable=None)
        assert "isHedgeable" not in body.keys()
