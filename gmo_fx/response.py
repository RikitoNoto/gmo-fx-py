from datetime import datetime


class Response:
    response_status: int
    response_time: datetime

    def __init__(self, response: dict):
        self.response_status = response["status"]
        self.response_time = datetime.strptime(
            response["responsetime"], "%Y-%m-%dT%H:%M:%S.%fZ"
        )
