import json
from typing import Optional
from unittest.mock import MagicMock, patch

import pytest

from gmo_fx import CancelOrdersApi as PackageCancelOrdersApi
from gmo_fx.api.cancel_orders import CancelOrder, CancelOrdersApi, CancelOrdersResponse
from gmo_fx.errors import ApiError
from tests.api_test_base import ApiTestBase


class TestCancelOrdersApi(ApiTestBase):

    def call_api(
        self,
        root_order_ids: Optional[list[int]] = None,
        client_order_ids: Optional[list[str]] = None,
    ) -> CancelOrdersResponse:
        return CancelOrdersApi(
            api_key="",
            secret_key="",
        )(
            root_order_ids=root_order_ids,
            client_order_ids=client_order_ids,
        )

    def create_response(
        self,
        data: Optional[dict] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        if data is None:
            data = {"success": [self.create_cancel_order_data()]}

        return super().create_response(
            data=data,
            status_code=status_code,
            text=text,
        )

    def create_cancel_order_data(
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
        self.check_404_error(
            post_mock,
            lambda: self.call_api(root_order_ids=[123456789]),
        )

    @patch("gmo_fx.api.api_base.post")
    def test_api_error(self, post_mock: MagicMock):
        response = self.create_response()
        response.json.return_value["status"] = 1
        response.json.return_value["messages"] = [
            {
                "message_code": "ERR-5001",
                "message_string": "Invalid parameter",
            }
        ]
        post_mock.return_value = response

        with pytest.raises(ApiError):
            self.call_api(root_order_ids=[123456789])

    @patch("gmo_fx.api.api_base.post")
    def test_check_url(self, post_mock: MagicMock) -> None:
        post_mock.return_value = self.create_response()
        self.call_api(root_order_ids=[123456789])
        url: str = post_mock.mock_calls[0].args[0]
        assert url.startswith("https://forex-api.coin.z.com/private/v1/cancelOrders")

    def check_parse_a_data(self, post_mock: MagicMock, **kwargs) -> CancelOrder:
        post_mock.return_value = self.create_response(
            data={"success": [self.create_cancel_order_data(**kwargs)]}
        )
        response = self.call_api(root_order_ids=[123456789])
        assert len(response.cancel_orders) == 1
        return response.cancel_orders[0]

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_cancel_order(self, post_mock: MagicMock):
        cancel_order = self.check_parse_a_data(
            post_mock,
            root_order_id=2536464541,
            client_order_id="abbb324dff",
        )

        assert cancel_order.root_order_id == 2536464541
        assert cancel_order.client_order_id == "abbb324dff"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_root_order_id(self, post_mock: MagicMock):
        cancel_order = self.check_parse_a_data(post_mock, root_order_id=2536464541)
        assert cancel_order.root_order_id == 2536464541

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_client_order_id(self, post_mock: MagicMock):
        cancel_order = self.check_parse_a_data(post_mock, client_order_id="abc123")
        assert cancel_order.client_order_id == "abc123"

    @patch("gmo_fx.api.api_base.post")
    def test_should_get_none_without_client_order_id(self, post_mock: MagicMock):
        cancel_order = self.check_parse_a_data(post_mock, client_order_id=None)
        assert cancel_order.client_order_id is None

    @patch("gmo_fx.api.api_base.post")
    def test_should_parse_some_data(self, post_mock: MagicMock):
        post_mock.return_value = self.create_response(
            data={
                "success": [
                    self.create_cancel_order_data(),
                    self.create_cancel_order_data(root_order_id=223456789),
                ]
            }
        )
        response = self.call_api(root_order_ids=[123456789, 223456789])
        assert len(response.cancel_orders) == 2

    def check_call_with(self, post_mock: MagicMock, **kwargs) -> dict:
        post_mock.return_value = self.create_response()
        if "root_order_ids" not in kwargs and "client_order_ids" not in kwargs:
            kwargs["root_order_ids"] = [123456789]
        self.call_api(**kwargs)
        request_body = post_mock.call_args.kwargs["data"]
        return json.loads(request_body)

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_root_order_ids(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, root_order_ids=[987654321, 123456789])
        assert body["rootOrderIds"] == [987654321, 123456789]

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_root_order_ids(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(post_mock, client_order_ids=["test123"])
        assert "rootOrderIds" not in body.keys()

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_with_client_order_ids(self, post_mock: MagicMock) -> None:
        body = self.check_call_with(
            post_mock,
            client_order_ids=["alfsdj32432enl", "test123"],
        )
        assert body["clientOrderIds"] == ["alfsdj32432enl", "test123"]

    @patch("gmo_fx.api.api_base.post")
    def test_should_call_api_without_client_order_ids(
        self,
        post_mock: MagicMock,
    ) -> None:
        body = self.check_call_with(post_mock, root_order_ids=[123456789])
        assert "clientOrderIds" not in body.keys()

    def test_should_raise_error_without_order_ids(self) -> None:
        with pytest.raises(ValueError):
            self.call_api()

    def test_should_raise_error_with_root_and_client_order_ids(self) -> None:
        with pytest.raises(ValueError):
            self.call_api(
                root_order_ids=[123456789],
                client_order_ids=["abc123"],
            )

    def test_can_import_from_package(self) -> None:
        assert PackageCancelOrdersApi is CancelOrdersApi
