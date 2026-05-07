from dataclasses import dataclass
from typing import Optional

from requests import Response

from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import SettleType, Side, Symbol


@dataclass
class CancelBulkOrder:
    root_order_id: int
    client_order_id: Optional[str]


class CancelBulkOrderResponse(ResponseBase):
    cancel_bulk_orders: list[CancelBulkOrder]

    def __init__(self, response: dict):
        super().__init__(response)

        data: dict = response["data"]
        self.cancel_bulk_orders = [
            CancelBulkOrder(
                root_order_id=d["rootOrderId"],
                client_order_id=d.get("clientOrderId"),
            )
            for d in data["success"]
        ]


class CancelBulkOrderApi(PrivateApiBase):
    Symbol = Symbol
    Side = Side
    SettleType = SettleType

    @property
    def _path(self) -> str:
        return "cancelBulkOrder"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return CancelBulkOrderResponse

    def _api_error_message(self, response: Response):
        return (
            "注文の一括キャンセルが失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbols: list[Symbol],
        side: Optional[Side] = None,
        settle_type: Optional[SettleType] = None,
    ) -> CancelBulkOrderResponse:
        data = {
            "symbols": [symbol.value for symbol in symbols],
        }

        if side is not None:
            data["side"] = side.value

        if settle_type is not None:
            data["settleType"] = settle_type.value

        return super().__call__(
            data=data,
        )
