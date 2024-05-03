from dataclasses import dataclass
from datetime import datetime
from requests import get, Response
from gmo_fx.response import Response as ResponseBase
from gmo_fx.symbols import Symbol
from gmo_fx.urls import BASE_URL_PUBLIC


@dataclass
class Ticker:
    symbol: Symbol
    ask: float
    bid: float
    timestamp: datetime
    status: str


class TickerResponse(ResponseBase):
    tickers: list[Ticker]

    def __init__(self, response: dict):
        super().__init__(response)
        self.tickers = []

        data = response["data"]
        self.tickers = [
            Ticker(
                symbol=Symbol(d["symbol"]),
                ask=d["ask"],
                bid=d["bid"],
                status=d["status"],
                timestamp=datetime.strptime(d["timestamp"], "%Y-%m-%dT%H:%M:%S.%fZ"),
            )
            for d in data
        ]


def get_ticker() -> TickerResponse:
    response: Response = get(f"{BASE_URL_PUBLIC}/ticker")
    if response.status_code == 200:
        response_json = response.json()
        return TickerResponse(response_json)

    raise RuntimeError(
        "最新レートが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
