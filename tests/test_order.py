from datetime import datetime, timezone
import re
from typing import Callable, Optional, Union
from unittest.mock import MagicMock, patch
from api.order import (
    Order,
    OrderApi,
    OrderResponse,
)

from tests.api_test_base import ApiTestBase


class TestOrderApi(ApiTestBase):

    def call_api(
        self,
        # symbol: Optional[Symbol] = None,
        # prev_id: Optional[int] = None,
        # count: Optional[int] = None,
    ) -> OrderResponse:
        return OrderApi(
            api_key="",
            secret_key="",
        )()

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
        price: Optional[float] = 130.5,
        status: str = "WAITING",
        cancel_type: Optional[str] = "PRICE_BOUND",
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
            "status": status,
            "expiry": expiry,
            "timestamp": timestamp,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if price is not None:
            data["price"] = str(price)

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
        assert url.startswith("https://forex-api.coin.z.com/private/v1/order")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> OrderResponse:
        post_mock.return_value = self.create_response(
            data=[self.create_order_data(**kwargs)]
        )
        response = self.call_api()
        assert len(response.orders) == 1
        return response

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert response.orders[0].root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id="abbb324dff")
        assert response.orders[0].client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, client_order_id=None)
        assert response.orders[0].client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_id(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, order_id=156789)
        assert response.orders[0].order_id == 156789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in Order.Symbol:
            response = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert response.orders[0].symbol == symbol

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_side(self, post_mock: MagicMock):
        for side in Order.Side:
            response = self.check_parse_a_data(post_mock, side=side.value)
            assert response.orders[0].side == side

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_order_type(self, post_mock: MagicMock):
        for order_type in Order.OrderType:
            response = self.check_parse_a_data(post_mock, order_type=order_type.value)
            assert response.orders[0].order_type == order_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_execution_type(self, post_mock: MagicMock):
        for execution_type in Order.ExecutionType:
            response = self.check_parse_a_data(
                post_mock, execution_type=execution_type.value
            )
            assert response.orders[0].execution_type == execution_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_settle_type(self, post_mock: MagicMock):
        for settle_type in Order.SettleType:
            response = self.check_parse_a_data(post_mock, settle_type=settle_type.value)
            assert response.orders[0].settle_type == settle_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_size(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, size=6100)
        assert response.orders[0].size == 6100

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_price(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, price=155.44)
        assert response.orders[0].price == 155.44

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_price(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, price=None)
        assert response.orders[0].price is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_status(self, post_mock: MagicMock):
        for status in Order.Status:
            response = self.check_parse_a_data(post_mock, status=status.value)
            assert response.orders[0].status == status

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_cancel_type(self, post_mock: MagicMock):
        for cancel_type in Order.CancelType:
            response = self.check_parse_a_data(post_mock, cancel_type=cancel_type.value)
            assert response.orders[0].cancel_type == cancel_type

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_cancel_type(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, cancel_type=None)
        assert response.orders[0].cancel_type is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_expiry(self, post_mock: MagicMock):
        response = self.check_parse_a_data(post_mock, expiry="20190418")
        assert response.orders[0].expiry == datetime(2019, 4, 18).date()

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_timestamp(self, post_mock: MagicMock):
        response = self.check_parse_a_data(
            post_mock, timestamp="2024-09-13T15:21:03.059Z"
        )
        assert response.orders[0].timestamp == datetime(
            2024, 9, 13, 15, 21, 3, 59000, tzinfo=timezone.utc
        )

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_with_symbol(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(symbol=Symbol.GBP_USD)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "symbol=GBP_USD" in url

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_without_symbol(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(symbol=None)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "symbol=" not in url

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_with_prev_id(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(prev_id=12345)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "prevId=12345" in url

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_without_prev_id(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(prev_id=None)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "prevId=" not in url

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_with_count(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(count=12345)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "count=12345" in url

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_call_api_without_count(
    #     self,
    #     get_mock: MagicMock,
    # ) -> None:
    #     get_mock.return_value = self.create_response()
    #     self.call_api(count=None)
    #     url = get_mock.mock_calls[0].args[0]
    #     assert "count=" not in url

    # def check_parse_a_data(
    #     self, get_mock: MagicMock, **kwargs
    # ) -> OpenPositionsResponse:
    #     get_mock.return_value = self.create_response(
    #         data=[self.create_open_position_data(**kwargs)]
    #     )
    #     response = self.call_api()
    #     assert len(response.open_positions) == 1
    #     return response

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_position_id(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, position_id=123123)
    #     assert response.open_positions[0].position_id == 123123

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_symbol(self, get_mock: MagicMock):
    #     for symbol in Symbol:
    #         response = self.check_parse_a_data(get_mock, symbol=symbol.value)
    #         assert response.open_positions[0].symbol == symbol

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_side(self, get_mock: MagicMock):
    #     for side in OpenPosition.Side:
    #         response = self.check_parse_a_data(get_mock, side=side.value)
    #         assert response.open_positions[0].side == side

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_size(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, size=130204)
    #     assert response.open_positions[0].size == 130204

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_ordersize(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, ordered_size=99864)
    #     assert response.open_positions[0].ordered_size == 99864

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_price(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, price=101.123)
    #     assert response.open_positions[0].price == 101.123

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_loss_gain(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, loss_gain=10500.66)
    #     assert response.open_positions[0].loss_gain == 10500.66

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_total_swap(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(get_mock, total_swap=166.13)
    #     assert response.open_positions[0].total_swap == 166.13

    # @patch("gmo_fx.api.api_base.get")
    # def test_should_get_timestamp(self, get_mock: MagicMock):
    #     response = self.check_parse_a_data(
    #         get_mock, timestamp="2019-03-21T05:18:09.011Z"
    #     )
    #     assert response.open_positions[0].timestamp == datetime(
    #         2019, 3, 21, 5, 18, 9, 11000, tzinfo=timezone.utc
    #     )
