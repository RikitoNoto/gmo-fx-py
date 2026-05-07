from dataclasses import dataclass
from typing import Optional

from requests import Response

from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase


@dataclass
class CancelOrder:
    root_order_id: int
    client_order_id: Optional[str] = None


class CancelOrdersResponse(ResponseBase):
    cancel_orders: list[CancelOrder]

    def __init__(self, response: dict):
        super().__init__(response)

        data: list[dict] = response["data"]["success"]
        self.cancel_orders = [
            CancelOrder(
                root_order_id=int(d["rootOrderId"]),
                client_order_id=d.get("clientOrderId"),
            )
            for d in data
        ]


class CancelOrdersApi(PrivateApiBase):
    @property
    def _path(self) -> str:
        return "cancelOrders"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return CancelOrdersResponse

    def _api_error_message(self, response: Response):
        return (
            "注文の複数キャンセルが失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        root_order_ids: Optional[list[int]] = None,
        client_order_ids: Optional[list[str]] = None,
    ) -> CancelOrdersResponse:
        targets = [
            root_order_ids is not None,
            client_order_ids is not None,
        ]
        if not any(targets):
            raise ValueError("root_order_ids or client_order_ids must be provided")
        if sum(targets) > 1:
            raise ValueError(
                "root_order_ids and client_order_ids cannot both be provided"
            )

        data: dict = {}

        if root_order_ids is not None:
            data["rootOrderIds"] = root_order_ids

        if client_order_ids is not None:
            data["clientOrderIds"] = client_order_ids

        return super().__call__(
            data=data,
        )
