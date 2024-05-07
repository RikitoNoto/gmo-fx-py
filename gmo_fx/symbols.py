from dataclasses import dataclass
from enum import Enum
from gmo_fx.response import Response as ResponseBase
from requests import get, Response
from gmo_fx.urls import BASE_URL_PUBLIC


class Symbol(Enum):
    USD_JPY = "USD_JPY"
    EUR_JPY = "EUR_JPY"
    GBP_JPY = "GBP_JPY"
    AUD_JPY = "AUD_JPY"
    NZD_JPY = "NZD_JPY"
    CAD_JPY = "CAD_JPY"
    CHF_JPY = "CHF_JPY"
    TRY_JPY = "TRY_JPY"
    ZAR_JPY = "ZAR_JPY"
    MXN_JPY = "MXN_JPY"
    EUR_USD = "EUR_USD"
    GBP_USD = "GBP_USD"
    AUD_USD = "AUD_USD"
    NZD_USD = "NZD_USD"


@dataclass
class Rule:
    symbol: Symbol
    min_open_order_size: int
    max_order_size: int
    size_step: int
    tick_size: float


class SymbolsResponse(ResponseBase):
    rules: list[Rule]

    def __init__(self, response: dict):
        super().__init__(response)
        self.rules = []

        data = response["data"]
        self.rules = [
            Rule(
                symbol=Symbol(d["symbol"]),
                min_open_order_size=int(d["minOpenOrderSize"]),
                max_order_size=int(d["maxOrderSize"]),
                size_step=int(d["sizeStep"]),
                tick_size=float(d["tickSize"]),
            )
            for d in data
        ]


def get_symbols() -> SymbolsResponse:
    response: Response = get(f"{BASE_URL_PUBLIC}/symbols")
    if response.status_code == 200:
        response_json = response.json()
        return SymbolsResponse(response_json)

    raise RuntimeError(
        "取引ルールが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
