from dataclasses import dataclass
from enum import Enum
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase
from gmo_fx.symbols import Symbol


@dataclass
class Execution:
    pass


class LatestExecutionsResponse(ResponseBase):
    executions: list[Execution]

    def __init__(self, response: dict):
        super().__init__(response)
        self.assets = []

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


class LatestExecutionsApi(PrivateApiBase):

    @property
    def _path(self) -> str:
        return "positionSummary"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return LatestExecutionsResponse

    def _api_error_message(self, response: Response):
        return (
            "最新約定一覧が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
