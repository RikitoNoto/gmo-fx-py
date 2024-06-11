import pytest
import time
import time_machine
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

    def test_api_key_header(self):
        header = PrivateApiBaseStub(api_key="api_key").header
        assert header["API-KEY"] == "api_key"

    @time_machine.travel(datetime(2022, 12, 25))
    def test_api_key_timestamp(self):
        header = PrivateApiBaseStub(api_key="api_key").header
        assert header["API-TIMESTAMP"] == "{0}000".format(
            int(time.mktime(datetime.now().timetuple()))
        )
