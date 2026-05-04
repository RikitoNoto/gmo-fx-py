from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Side, Symbol, SettleType


@dataclass
class ActiveOrder:
    class OrderType(Enum):
        NORMAL = "NORMAL"
        OCO = "OCO"
        IFD = "IFD"
        IFDOCO = "IFDOCO"

    class ExecutionType(Enum):
        LIMIT = "LIMIT"
        STOP = "STOP"

    class Status(Enum):
        WAITING = "WAITING"
        MODIFYING = "MODIFYING"
        ORDERED = "ORDERED"

    Side = Side
    Symbol = Symbol
    SettleType = SettleType

    root_order_id: int
    order_id: int
    symbol: Symbol
    side: Side
    order_type: OrderType
    execution_type: ExecutionType
    settle_type: SettleType
    size: int
    price: float
    status: Status
    expiry: date
    timestamp: datetime
    client_order_id: Optional[str] = None


class ActiveOrdersResponse(ResponseBase):
    active_orders: list[ActiveOrder]

    def __init__(self, response: dict):
        super().__init__(response)

        data = response["data"]["list"]
        self.active_orders = [
            ActiveOrder(
                root_order_id=int(d["rootOrderId"]),
                order_id=int(d["orderId"]),
                symbol=ActiveOrder.Symbol(d["symbol"]),
                side=ActiveOrder.Side(d["side"]),
                order_type=ActiveOrder.OrderType(d["orderType"]),
                execution_type=ActiveOrder.ExecutionType(d["executionType"]),
                settle_type=ActiveOrder.SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d["price"]),
                status=ActiveOrder.Status(d["status"]),
                expiry=datetime.strptime(d["expiry"], "%Y%m%d").date(),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
                client_order_id=d.get("clientOrderId"),
            )
            for d in data
        ]


class ActiveOrdersApi(PrivateApiBase):
    Symbol = Symbol

    @property
    def _path(self) -> str:
        return "activeOrders"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return ActiveOrdersResponse

    def _api_error_message(self, response: Response):
        return (
            "有効注文一覧が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Optional[Symbol] = None,
        prev_id: Optional[int] = None,
        count: Optional[int] = None,
    ) -> ActiveOrdersResponse:
        query_params = []
        if symbol:
            query_params.append(f"symbol={symbol.value}")
        if prev_id:
            query_params.append(f"prevId={prev_id}")
        if count:
            query_params.append(f"count={count}")

        path_query = "&".join(query_params) if query_params else None
        return super().__call__(path_query=path_query)
