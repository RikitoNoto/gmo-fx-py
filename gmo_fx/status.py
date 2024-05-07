from enum import auto, Enum
from typing import Type
from requests import get, Response
from gmo_fx.response import Response as ResponseBase
from gmo_fx.urls import BASE_URL_PUBLIC


class Status(Enum):
    """
    外国為替FXの稼動状態
    """

    OPEN = auto()  # オープン
    CLOSE = auto()  # クローズ
    MAINTENANCE = auto()  # メンテナンス

    @classmethod
    def from_str(cls, text: str) -> Type["Status"]:
        match text:
            case "OPEN":
                return cls.OPEN
            case "CLOSE":
                return cls.CLOSE
            case "MAINTENANCE":
                return cls.MAINTENANCE
        raise ValueError(f"不明なステータスです。: {text}")


class StatusResponse(ResponseBase):
    status: Status

    def __init__(self, response: dict):
        super().__init__(response)
        self.status = Status.from_str(response["data"]["status"])


def get_status() -> StatusResponse:
    response: Response = get(f"{BASE_URL_PUBLIC}/status")
    if response.status_code == 200:
        response_json = response.json()
        return StatusResponse(response_json)

    raise RuntimeError(
        "ステータスが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
