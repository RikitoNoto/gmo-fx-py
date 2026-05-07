from dataclasses import dataclass
from datetime import date, datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase

from gmo_fx.common import (
    SettleType,
    Side,
    Symbol,
)
from gmo_fx.api.response import Response as ResponseBase


@dataclass
class IfoOrder:

    class OrderType(Enum):
        IFDOCO = "IFDOCO"

    class ExecutionType(Enum):
        """注文タイプ"""

        LIMIT = "LIMIT"
        STOP = "STOP"

    class Status(Enum):
        WAITING = "WAITING"
        ORDERED = "ORDERED"
        EXECUTED = "EXECUTED"

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
    expiry: date
    timestamp: datetime


class IfoOrderResponse(ResponseBase):
    ifo_orders: list[IfoOrder]

    def __init__(self, response: dict):
        super().__init__(response)

        data: list[dict] = response["data"]
        self.ifo_orders = [
            IfoOrder(
                root_order_id=d["rootOrderId"],
                client_order_id=d.get("clientOrderId"),
                order_id=d["orderId"],
                symbol=IfoOrder.Symbol(d["symbol"]),
                side=IfoOrder.Side(d["side"]),
                order_type=IfoOrder.OrderType(d["orderType"]),
                execution_type=IfoOrder.ExecutionType(d["executionType"]),
                settle_type=IfoOrder.SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d["price"]),
                status=IfoOrder.Status(d["status"]),
                expiry=datetime.strptime(d["expiry"], "%Y%m%d").date(),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
            )
            for d in data
        ]


class IfoOrderApi(PrivateApiBase):
    Symbol = Symbol
    Side = Side

    class ExecutionType(Enum):
        """注文タイプ"""

        LIMIT = "LIMIT"
        STOP = "STOP"

    @property
    def _path(self) -> str:
        return "ifoOrder"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return IfoOrderResponse

    def _api_error_message(self, response: Response):
        return (
            "IFDOCO注文が失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Symbol,
        first_side: Side,
        first_execution_type: ExecutionType,
        first_size: int,
        first_price: float,
        second_size: int,
        second_limit_price: float,
        second_stop_price: float,
        client_order_id: Optional[str] = None,
    ) -> IfoOrderResponse:
        data = {
            "symbol": symbol.value,
            "firstSide": first_side.value,
            "firstExecutionType": first_execution_type.value,
            "firstSize": str(first_size),
            "firstPrice": str(first_price),
            "secondSize": str(second_size),
            "secondLimitPrice": str(second_limit_price),
            "secondStopPrice": str(second_stop_price),
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        return super().__call__(
            data=data,
        )


IFDOCOOrder = IfoOrder
IFDOCOOrderResponse = IfoOrderResponse
IFDOCOOrderApi = IfoOrderApi
