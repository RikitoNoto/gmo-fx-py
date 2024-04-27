from dataclasses import dataclass
from requests import get, Response


@dataclass
class StatusResponse:
    status: str


def status() -> StatusResponse:
    response: Response = get(f"https://forex-api.coin.z.com/public/status")
    if response.status_code == 200:
        response_json = response.json()
        status = response_json["data"]["status"]
        return StatusResponse(status)

    raise RuntimeError(
        f"ステータスが取得できませんでした。\nstatus code: {response.status_code}\nresponse: {response.text}"
    )