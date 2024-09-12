from dataclasses import dataclass
from datetime import datetime, timezone
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
    expiry: datetime
    timestamp: datetime


class OrderResponse(ResponseBase):
    orders: list[Order]

    def __init__(self, response: dict):
        super().__init__(response)
        self.orders = []

        data = response["data"]
        self.orders = [
            Order(
                root_order_id=0,
                client_order_id="",
                order_id=0,
                symbol=Order.Symbol(d["symbol"]),
                side=Order.Side.BUY,
                order_type=Order.OrderType.NORMAL,
                execution_type=Order.ExecutionType.MARKET,
                settle_type=Order.SettleType.OPEN,
                size=0,
                price=None,
                status=Order.Status.WAITING,
                cancel_type=None,
                expiry=datetime.now(),
                timestamp=datetime.now(),
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
