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
        client_order_id: str = "abc123",
        order_id: int = 123456789,
        symbol: str = "USD_JPY",
        side: str = "BUY",
        order_type: str = "NORMAL",
        execution_type: str = "LIMIT",
        settle_type: str = "OPEN",
        size: int = 100,
        price: float = 130.5,
        status: str = "WAITING",
        expiry: datetime = datetime.now(),
        timestamp: datetime = datetime.now(),
    ) -> dict:
        return {
            "rootOrderId": root_order_id,
            "clientOrderId": client_order_id,
            "orderId": order_id,
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "executionType": execution_type,
            "settleType": settle_type,
            "size": str(size),
            "price": str(price),
            "status": status,
            "expiry": expiry.strftime("%Y%m%d"),
            "timestamp": timestamp.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }

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
    def test_should_get_symbol(self, post_mock: MagicMock):
        for symbol in Order.Symbol:
            response = self.check_parse_a_data(post_mock, symbol=symbol.value)
            assert response.orders[0].symbol == symbol

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
