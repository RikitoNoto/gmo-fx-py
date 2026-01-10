from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Side, Symbol, SettleType


@dataclass
class Execution:
    Side = Side
    Symbol = Symbol
    SettleType = SettleType

    execution_id: int
    order_id: int
    position_id: int
    symbol: Symbol
    side: Side
    settle_type: SettleType
    size: int
    price: float
    loss_gain: float
    fee: float
    settled_swap: float
    amount: float
    timestamp: datetime
    client_order_id: Optional[str] = None


class ExecutionsResponse(ResponseBase):
    executions: list[Execution]

    def __init__(self, response: dict):
        super().__init__(response)

        data = response["data"]["list"]
        self.executions = [
            Execution(
                execution_id=int(d["executionId"]),
                order_id=int(d["orderId"]),
                position_id=int(d["positionId"]),
                symbol=Execution.Symbol(d["symbol"]),
                side=Execution.Side(d["side"]),
                settle_type=Execution.SettleType(d["settleType"]),
                size=int(d["size"]),
                price=float(d["price"]),
                loss_gain=float(d["lossGain"]),
                fee=float(d["fee"]),
                settled_swap=float(d["settledSwap"]),
                amount=float(d["amount"]),
                timestamp=datetime.strptime(
                    d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"
                ).replace(tzinfo=timezone.utc),
                client_order_id=d.get("clientOrderId"),
            )
            for d in data
        ]


class ExecutionsApi(PrivateApiBase):
    @property
    def _path(self) -> str:
        return "executions"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return ExecutionsResponse

    def _api_error_message(self, response: Response):
        return (
            "約定情報が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        order_id: list[int] = None,
        execution_id: list[int] = None,
    ) -> ExecutionsResponse:
        query_params = []
        if execution_id:
            query_params.append(
                f"executionId={','.join([str(id) for id in execution_id])}"
            )
        if order_id:
            query_params.append(f"orderId={','.join([str(id) for id in order_id])}")

        path_query = "&".join(query_params) if query_params else None
        return super().__call__(path_query=path_query)
