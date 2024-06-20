from dataclasses import dataclass
from enum import Enum
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.symbols import Symbol


@dataclass
class Position:
    class Side(Enum):
        BUY = "BUY"
        SELL = "SELL"

    average_position_rate: float
    position_loss_gain: float
    side: Side
    sum_ordered_size: int
    sum_position_size: int
    sum_total_swap: float
    symbol: Symbol


class PositionSummaryResponse(ResponseBase):
    positions: list[Position]

    def __init__(self, response: dict):
        super().__init__(response)
        self.assets = []

        data = response["data"]
        self.positions = [
            Position(
                average_position_rate=d["averagePositionRate"],
                position_loss_gain=0.0,
                side=Position.Side.BUY,
                sum_ordered_size=0,
                sum_position_size=0,
                sum_total_swap=0.0,
                symbol=Symbol.USD_JPY,
            )
            for d in data
        ]


class PositionSummaryApi(PrivateApiBase):

    @property
    def _path(self) -> str:
        return "positionSummary"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return PositionSummaryResponse

    def _api_error_message(self, response: Response):
        return (
            "建玉サマリーが取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
