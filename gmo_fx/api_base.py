import hmac
import hashlib
import json
import time

from abc import ABC, abstractmethod
from datetime import datetime
from enum import auto, Enum
from gmo_fx.response import Response
from typing import Any


class ApiBase(ABC):

    class _HttpMethod(Enum):
        GET = "GET"
        POST = "POST"

    @property
    @abstractmethod
    def _path(self) -> str:
        pass

    @property
    @abstractmethod
    def _method(self) -> _HttpMethod:
        pass

    @property
    def _body(self) -> dict:
        return {}

    @abstractmethod
    def __call__(self, *args: Any, **kwds: Any) -> Response:
        pass

    def _create_header(
        self,
    ) -> dict:
        return {}


class PrivateApiBase(ApiBase, ABC):
    def __init__(self, api_key: str, secret_key: str) -> None:
        self._api_key = api_key
        self.__secret_key = secret_key
        super().__init__()

    def _create_header(
        self,
    ) -> dict:
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = timestamp + self._method.value + self._path + json.dumps(self._body)
        sign = hmac.new(
            bytes(self.__secret_key.encode("ascii")),
            bytes(text.encode("ascii")),
            hashlib.sha256,
        ).hexdigest()
        return {
            "API-KEY": self._api_key,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign,
        }
