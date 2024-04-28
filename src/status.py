from dataclasses import dataclass
from enum import auto, Enum
from typing import Type
from requests import get, Response


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


@dataclass
class StatusResponse:
    status: Status


def get_status() -> StatusResponse:
    response: Response = get("https://forex-api.coin.z.com/public/v1/status")
    if response.status_code == 200:
        response_json = response.json()
        status = response_json["data"]["status"]
        return StatusResponse(Status.from_str(status))

    raise RuntimeError(
        "ステータスが取得できませんでした。\n"
        f"status code: {response.status_code}\n"
        f"response: {response.text}"
    )
