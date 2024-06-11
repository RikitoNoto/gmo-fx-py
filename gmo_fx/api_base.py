import time

from abc import ABC, abstractmethod
from datetime import datetime
from gmo_fx.response import Response
from typing import Any


class ApiBase(ABC):
    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Response:
        pass


class PrivateApiBase(ApiBase):
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key
        super().__init__()

    def _create_header(
        self,
    ) -> dict:
        return {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": "{0}000".format(
                int(time.mktime(datetime.now().timetuple()))
            ),
        }
