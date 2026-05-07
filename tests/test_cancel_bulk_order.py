import json
from typing import Optional
from unittest.mock import MagicMock, patch

from gmo_fx import CancelBulkOrderApi as PackageCancelBulkOrderApi
from gmo_fx.api.cancel_bulk_order import (
    CancelBulkOrder,
    CancelBulkOrderApi,
    CancelBulkOrderResponse,
)
from tests.api_test_base import ApiTestBase


class TestCancelBulkOrderApi(ApiTestBase):

    def call_api(
        self,
        symbols: Optional[list[CancelBulkOrderApi.Symbol]] = None,
        side: Optional[CancelBulkOrderApi.Side] = None,
        settle_type: Optional[CancelBulkOrderApi.SettleType] = None,
    ) -> CancelBulkOrderResponse:
        if symbols is None:
            symbols = [
                CancelBulkOrderApi.Symbol.USD_JPY,
                CancelBulkOrderApi.Symbol.CAD_JPY,
            ]

        return CancelBulkOrderApi(
            api_key="",
            secret_key="",
        )(
            symbols=symbols,
            side=side,
            settle_type=settle_type,
        )

    def create_response(
        self,
        data: Optional[dict] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = {"success": [self.create_cancel_bulk_order_data()]}

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_cancel_bulk_order_data(
        self,
        root_order_id: int = 123456789,
        client_order_id: Optional[str] = "abc123",
    ) -> dict:
        data = {
            "rootOrderId": root_order_id,
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        return data

    @patch("gmo_fx.api.api_base.post")
    def test_404_error(self, post_mock: MagicMock):
        self.check_404_error(post_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(self, post_mock: MagicMock) -> None:
        post_mock.return_value = self.create_response()
        self.call_api()
        url: str = post_mock.mock_calls[0].args[0]
        assert url == "https://forex-api.coin.z.com/private/v1/cancelBulkOrder"

    def check_parse_a_data(
        self,
        post_mock: MagicMock,
        **kwargs,
    ) -> CancelBulkOrder:
        post_mock.return_value = self.create_response(
            data={"success": [self.create_cancel_bulk_order_data(**kwargs)]}
        )
        response = self.call_api()
        assert len(response.cancel_bulk_orders) == 1
        return response.cancel_bulk_orders[0]

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        cancel_bulk_order = self.check_parse_a_data(
            post_mock,
            root_order_id=223456789,
        )
        assert cancel_bulk_order.root_order_id == 223456789

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        cancel_bulk_order = self.check_parse_a_data(
            post_mock,
            client_order_id="abbb324dff",
        )
        assert cancel_bulk_order.client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        cancel_bulk_order = self.check_parse_a_data(
            post_mock,
            client_order_id=None,
        )
        assert cancel_bulk_order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data={
                "success": [
                    self.create_cancel_bulk_order_data(root_order_id=123456789),
                    self.create_cancel_bulk_order_data(root_order_id=223456789),
                ]
            }
        )
        response = self.call_api()
        assert len(response.cancel_bulk_orders) == 2

    def check_call_with(self, post_mock: MagicMock, **kwargs) -> dict:
        post_mock.return_value = self.create_response()
        self.call_api(**kwargs)
        request_body = post_mock.call_args.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_symbols(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            symbols=[
                CancelBulkOrderApi.Symbol.USD_JPY,
                CancelBulkOrderApi.Symbol.CAD_JPY,
            ],
        )
        assert body["symbols"] == ["USD_JPY", "CAD_JPY"]

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_side(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, side=CancelBulkOrderApi.Side.BUY)
        assert body["side"] == "BUY"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_side(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, side=None)
        assert "side" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_settle_type(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            settle_type=CancelBulkOrderApi.SettleType.OPEN,
        )
        assert body["settleType"] == "OPEN"

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_settle_type(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, settle_type=None)
        assert "settleType" not in body.keys()

    def test_should_import_from_package(self) -> None:
        assert PackageCancelBulkOrderApi is CancelBulkOrderApi
