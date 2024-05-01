from dataclasses import dataclass
from datetime import datetime
from enum import auto, Enum
from typing import Type
from requests import get, Response
from gmo_fx.response import Response as ResponseBase
from gmo_fx.symbols import Symbol


@dataclass
class Kline:
    open_time: datetime
    open: float
    high: float
    low: float
    close: float


class KlinesResponse(ResponseBase):
    klines: list[Kline]

    def __init__(self, response: dict):
        super().__init__(response)
        self.klines = []

        data = response["data"]
        self.klines = [
            Kline(
                open=float(d["open"]),
                high=float(d["high"]),
                low=float(d["low"]),
                close=float(d["close"]),
                open_time=datetime.fromtimestamp(int(d["openTime"]) / 1000),
            )
            for d in data
        ]


def get_klines() -> KlinesResponse:
    response: Response = get("https://forex-api.coin.z.com/public/v1/klines")
    if response.status_code == 200:
        response_json = response.json()
        return KlinesResponse(response_json)

    raise RuntimeError(
        "Klineが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
