from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional

from requests import Response

from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import SettleType, Side, Symbol


@dataclass
class Order:

    class OrderType(Enum):
        IFDOCO = "IFDOCO"

    class Status(Enum):
        WAITING = "WAITING"
        ORDERED = "ORDERED"
        MODIFYING = "MODIFYING"
        EXECUTED = "EXECUTED"
        EXPIRED = "EXPIRED"

    class CancelType(Enum):
        """取り消し区分"""

        OCO = "OCO"

    class ExecutionType(Enum):
        """注文タイプ"""

        LIMIT = "LIMIT"
        STOP = "STOP"

    SettleType = SettleType
    Side = Side
    Symbol = Symbol

    root_order_id: int
    client_order_id: Optional[str]
    order_id: int
    symbol: Symbol
    side: Side
    order_type: OrderType
    execution_type: ExecutionType
    settle_type: SettleType
    size: int
    price: float
    status: Status
    cancel_type: Optional[CancelType]
    expiry: date
    timestamp: datetime


class ChangeIfoOrderResponse(ResponseBase):
    orders: list[Order]

    def __init__(self, response: dict):
        super().__init__(response)

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
                price=float(d["price"]),
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


class ChangeIfoOrderApi(PrivateApiBase):
    @property
    def _path(self) -> str:
        return "changeIfoOrder"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return ChangeIfoOrderResponse

    def _api_error_message(self, response: Response):
        return (
            "IFDOCO注文変更が失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        root_order_id: Optional[int] = None,
        client_order_id: Optional[str] = None,
        first_price: Optional[float] = None,
        second_limit_price: Optional[float] = None,
        second_stop_price: Optional[float] = None,
    ) -> ChangeIfoOrderResponse:
        if root_order_id is None and client_order_id is None:
            raise ValueError("root_order_id or client_order_id must be provided")

        if (
            first_price is None
            and second_limit_price is None
            and second_stop_price is None
        ):
            raise ValueError(
                "first_price, second_limit_price, or second_stop_price must be provided"
            )

        data: dict = {}

        if root_order_id is not None:
            data["rootOrderId"] = root_order_id

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if first_price is not None:
            data["firstPrice"] = str(first_price)

        if second_limit_price is not None:
            data["secondLimitPrice"] = str(second_limit_price)

        if second_stop_price is not None:
            data["secondStopPrice"] = str(second_stop_price)

        return super().__call__(
            data=data,
        )
