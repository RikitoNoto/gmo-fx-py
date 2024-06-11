import pytest
from datetime import datetime
from gmo_fx.api_base import PrivateApiBase
from gmo_fx.response import Response
from typing import Any


class PrivateApiBaseStub(PrivateApiBase):
    def __call__(self, *args: Any, **kwds: Any) -> Response:
        pass

    @property
    def header(
        self,
    ) -> dict:
        return super()._create_header()


class TestPrivateApiBase:

    def test_get_api_key(self):
        header = PrivateApiBaseStub(api_key="api_key").header
        assert header["API-KEY"] == "api_key"
