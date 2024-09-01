from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.common import Symbol


@dataclass
class OpenPosition:
    class Side(Enum):
        BUY = "BUY"
        SELL = "SELL"

    position_id: int
    symbol: Symbol
    side: Side
    orderd_size: int
    price: float
    loss_gain: float
    total_swap: float
    timestamp: datetime


class OpenPositionsResponse(ResponseBase):
    open_positions: list[OpenPosition]

    def __init__(self, response: dict):
        super().__init__(response)
        self.open_positions = []

        # data = response["data"]
        # self.positions = [
        #     Position(
        #         average_position_rate=d["averagePositionRate"],
        #         position_loss_gain=d["positionLossGain"],
        #         side=Position.Side(d["side"]),
        #         sum_ordered_size=d["sumOrderedSize"],
        #         sum_position_size=d["sumPositionSize"],
        #         sum_total_swap=d["sumTotalSwap"],
        #         symbol=Symbol(d["symbol"]),
        #     )
        #     for d in data
        # ]


class OpenPositionsApi(PrivateApiBase):

    @property
    def _path(self) -> str:
        return "openPositions"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return OpenPositionsResponse

    def _api_error_message(self, response: Response):
        return (
            "建玉一覧が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )

    def __call__(
        self,
        symbol: Optional[Symbol] = None,
        prev_id: Optional[int] = None,
        count: Optional[int] = None,
    ) -> OpenPositionsResponse:
        path_query = ""
        if symbol:
            path_query = f"symbol={symbol.value}"

        if prev_id:
            if path_query:
                path_query += "&"
            path_query = f"prevId={prev_id}"

        if count:
            if path_query:
                path_query += "&"
            path_query = f"count={count}"

        return super().__call__(path_query=path_query)
