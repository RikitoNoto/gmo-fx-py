from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase

from gmo_fx.common import (
    OrderType,
    SettleType,
    Side,
    Symbol,
)
from gmo_fx.api.response import Response as ResponseBase


@dataclass
class SpeedOrder:

    class ExecutionType(Enum):
        """注文タイプ"""

        MARKET = "MARKET"

    class Status(Enum):
        EXECUTED = "EXECUTED"
        EXPIRED = "EXPIRED"

    class CancelType(Enum):
        PRICE_BOUND = "PRICE_BOUND"

    OrderType = OrderType
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
    status: Status
    cancel_type: Optional[CancelType]
    timestamp: datetime


class SpeedOrderResponse(ResponseBase):
    speed_orders: list[SpeedOrder]

    def __init__(self, response: dict):
        super().__init__(response)

        data: list[dict] = response["data"]
        self.speed_orders = [
            SpeedOrder(
                root_order_id=d["rootOrderId"],
                client_order_id=d.get("clientOrderId"),
                order_id=d["orderId"],
                symbol=SpeedOrder.Symbol(d["symbol"]),
                side=SpeedOrder.Side(d["side"]),
                order_type=SpeedOrder.OrderType(d["orderType"]),
                execution_type=SpeedOrder.ExecutionType(d["executionType"]),
                settle_type=SpeedOrder.SettleType(d["settleType"]),
                size=int(d["size"]),
                status=SpeedOrder.Status(d["status"]),
                cancel_type=(
                    SpeedOrder.CancelType(d.get("cancelType"))
                    if d.get("cancelType")
                    else None
                ),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
            )
            for d in data
        ]


class SpeedOrderApi(PrivateApiBase):
    Symbol = Symbol
    Side = Side

    @property
    def _path(self) -> str:
        return "speedOrder"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.POST

    @property
    def _response_parser(self):
        return SpeedOrderResponse

    def _api_error_message(self, response: Response):
        return (
            "スピード注文が失敗しました\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Symbol,
        side: Side,
        size: int,
        client_order_id: Optional[str] = None,
        lower_bound: Optional[float] = None,
        upper_bound: Optional[float] = None,
        is_hedgeable: Optional[bool] = None,
    ) -> SpeedOrderResponse:
        data = {
            "symbol": symbol.value,
            "side": side.value,
            "size": str(size),
        }

        if client_order_id is not None:
            data["clientOrderId"] = client_order_id

        if lower_bound is not None:
            data["lowerBound"] = str(lower_bound)

        if upper_bound is not None:
            data["upperBound"] = str(upper_bound)

        if is_hedgeable is not None:
            data["isHedgeable"] = is_hedgeable

        return super().__call__(
            data=data,
        )
