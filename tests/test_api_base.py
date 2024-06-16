import hmac
import hashlib
import json
import time
import time_machine
from datetime import datetime
from gmo_fx.api.api_base import PrivateApiBase
from gmo_fx.api.response import Response
from typing import Any


class PrivateApiBaseStub(PrivateApiBase):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        method: str = "GET",
        body: dict = {},
        path: str = "/v1/test",
    ) -> None:
        self.__method = (
            self._HttpMethod.POST if method == "POST" else self._HttpMethod.GET
        )
        self.__path = path
        self.__body = body
        super().__init__(api_key, secret_key)

    def __call__(self, *args: Any, **kwds: Any) -> Response:
        pass

    @property
    def _path(
        self,
    ) -> str:
        return self.__path

    @property
    def _body(
        self,
    ) -> str:
        return self.__body

    @property
    def _method(self):
        return self.__method

    @property
    def header(
        self,
    ) -> dict:
        return super()._create_header()


class TestPrivateApiBase:

    def test_api_key_header(self):
        header = PrivateApiBaseStub(api_key="api_key", secret_key="secret").header
        assert header["API-KEY"] == "api_key"

    @time_machine.travel(datetime(2022, 12, 25))
    def test_timestamp(self):
        header = PrivateApiBaseStub(api_key="api_key", secret_key="secret").header
        assert header["API-TIMESTAMP"] == "{0}000".format(
            int(time.mktime(datetime.now().timetuple()))
        )

    @time_machine.travel(datetime(2024, 1, 3))
    def test_api_sign_get(self):

        method = "GET"
        path = "/v1/test"
        body = {"a": "a"}
        header = PrivateApiBaseStub(
            api_key="api_key", secret_key="secret", method=method, path=path, body=body
        ).header
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = timestamp + method + path + json.dumps(body)
        assert (
            header["API-SIGN"]
            == hmac.new(
                bytes("secret".encode("ascii")),
                bytes(text.encode("ascii")),
                hashlib.sha256,
            ).hexdigest()
        )
