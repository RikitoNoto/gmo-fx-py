from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Literal
from requests import get, Response
from gmo_fx.response import Response as ResponseBase
from gmo_fx.symbols import Symbol
from gmo_fx.urls import BASE_URL_PUBLIC


class KlineInterval(Enum):
    Min1 = "1min"
    Min5 = "5min"
    Min10 = "10min"
    Min15 = "15min"
    Min30 = "30min"
    H1 = "1hour"
    H4 = "4hour"
    H8 = "8hour"
    H12 = "12hour"
    D1 = "1day"
    W1 = "1week"
    M1 = "1month"


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


def get_klines(
    symbol: Symbol,
    price_type: Literal["BID", "ASK"],
    interval: KlineInterval,
    date: datetime,
) -> KlinesResponse:
    date_str = f"{date.year:04}"
    if interval in (
        KlineInterval.Min1,
        KlineInterval.Min5,
        KlineInterval.Min10,
        KlineInterval.Min15,
        KlineInterval.Min30,
        KlineInterval.H1,
    ):
        date_str += f"{date.month:02}{date.day:02}"
    base_url = f"{BASE_URL_PUBLIC}/klines"
    response: Response = get(
        f"{base_url}?"
        f"symbol={symbol.value}"
        f"&priceType={price_type}"
        f"&interval={interval.value}"
        f"&date={date_str}"
    )
    if response.status_code == 200:
        response_json = response.json()
        return KlinesResponse(response_json)

    raise RuntimeError(
        "Klineが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
