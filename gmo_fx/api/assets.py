from dataclasses import dataclass
from requests import Response
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response as ResponseBase


@dataclass
class Asset:
    equity: int
    available_amount: int
    balance: int
    estimated_trade_fee: float
    margin: int
    margin_ratio: float
    position_loss_gain: float
    total_swap: float
    transferable_amount: int


class AssetsResponse(ResponseBase):
    assets: list[Asset]

    def __init__(self, response: dict):
        super().__init__(response)
        self.assets = []

        data = response["data"]
        self.assets = [
            Asset(
                equity=d["equity"],
                available_amount=0,
                balance=0,
                estimated_trade_fee=0.0,
                margin=0,
                margin_ratio=0.0,
                position_loss_gain=0.0,
                total_swap=0.0,
                transferable_amount=0,
            )
            for d in data
        ]


class AssetsApi(PrivateApiBase):

    @property
    def _path(self) -> str:
        return "account/assets"

    @property
    def _method(self) -> PrivateApiBase._HttpMethod:
        return self._HttpMethod.GET

    @property
    def _response_parser(self):
        return AssetsResponse

    def _api_error_message(self, response: Response):
        return (
            "資産残高が取得できませんでした。\n"
            f"status code: {response.status_code}\n"
            f"response: {response.text}"
        )
