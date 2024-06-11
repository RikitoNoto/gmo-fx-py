from abc import ABC, abstractmethod
from typing import Any
from gmo_fx.response import Response


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
        }
