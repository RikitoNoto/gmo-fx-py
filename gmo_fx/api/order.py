from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase


@dataclass
class Order:
    class Status(Enum):
        WAITING = "WAITING"
        EXECUTED = "EXECUTED"
        EXPIRED = "EXPIRED"

    class CancelType(Enum):
        PRICE_BOUND = "PRICE_BOUND"
        OCO = "OCO"

    from gmo_fx.common import (
        ExecutionType,
        OrderType,
        SettleType,
        Side,
        Symbol,
    )

    root_order_id: int
    client_order_id: Optional[str]
    order_id: int
    symbol: Symbol
    side: Side
    order_type: OrderType
    execution_type: ExecutionType
    settle_type: SettleType
    size: int
    price: Optional[float]
    status: Status
    cancel_type: Optional[CancelType]
    expiry: date
    timestamp: datetime


class OrderResponse(ResponseBase):
    orders: list[Order]

    def __init__(self, response: dict):
        super().__init__(response)
        self.orders = []

        data: list[dict] = response["data"]
        self.orders = [
            Order(
                root_order_id=d["rootOrderId"],
                client_order_id=d.get("clientOrderId"),
                order_id=d["orderId"],
                symbol=Order.Symbol(d["symbol"]),
                side=Order.Side(d["side"]),
                order_type=Order.OrderType(d["orderType"]),
                execution_type=Order.ExecutionType(d["executionType"]),
                settle_type=Order.SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d.get("price")) if d.get("price") else None,
                status=Order.Status(d["status"]),
                cancel_type=(
                    Order.CancelType(d.get("cancelType"))
                    if d.get("cancelType")
                    else None
                ),
                expiry=datetime.strptime(d["expiry"], "%Y%m%d").date(),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
            )
            for d in data
        ]


class OrderApi(PrivateApiBase):

    @property
    def _path(self) -> str:
        return "order"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return OrderResponse

    def _api_error_message(self, response: Response):
        return (
            "注文が失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    # def __call__(
    #     self,
    #     symbol: Optional[Symbol] = None,
    #     prev_id: Optional[int] = None,
    #     count: Optional[int] = None,
    # ) -> OpenPositionsResponse:
    #     path_query = ""
    #     if symbol:
    #         path_query = f"symbol={symbol.value}"

    #     if prev_id:
    #         if path_query:
    #             path_query += "&"
    #         path_query = f"prevId={prev_id}"

    #     if count:
    #         if path_query:
    #             path_query += "&"
    #         path_query = f"count={count}"

    #     return super().__call__(path_query=path_query)
