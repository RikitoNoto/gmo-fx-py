import hmac
import hashlib
import json
import pytest
import time
import time_machine
from datetime import datetime
from gmo_fx.api.klines import KlinesApi
from gmo_fx.api.order import OrderApi
from api.api_base import PrivateApiBase, PublicApiBase
from api.response import Response
from requests.exceptions import Timeout
from typing import Any, Optional
from unittest.mock import MagicMock, patch


class PublicApiBaseStub(PublicApiBase):
    def __init__(self, method: str = "GET", **kwargs: Any) -> None:
        self.__method = (
            self._HttpMethod.POST if method == "POST" else self._HttpMethod.GET
        )
        super().__init__(**kwargs)

    @property
    def _response_parser(self):
        return MagicMock()

    @property
    def _path(
        self,
    ) -> str:
        return "test"

    @property
    def _method(self):
        return self.__method


class PrivateApiBaseStub(PrivateApiBase):
    def __init__(
        self,
        api_key: str,
        secret_key: str,
        method: str = "GET",
        body: dict = {},
        path: str = "test",
        is_call: bool = False,
        **kwargs: Any,
    ) -> None:
        self.__method = (
            self._HttpMethod.POST if method == "POST" else self._HttpMethod.GET
        )
        self.__path = path
        self.__body = body
        self.__is_call = is_call
        super().__init__(api_key, secret_key, **kwargs)

    def __call__(self, *args: Any, **kwds: Any) -> Response:
        if self.__is_call:
            return super().__call__(*args, **kwds)

    @property
    def _response_parser(self):
        return MagicMock()

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

    bodys = [
        # (body, expect),
        (None, None),
        ({}, "{}"),
        ({"test": "test"}, '{"test":"test"}'),
        ({"test": ""}, '{"test":""}'),
    ]

    @pytest.mark.parametrize(
        "body, expect",
        bodys,
    )
    @patch("api.api_base.post")
    def test_should_post_with_body(
        self,
        post_mock: MagicMock,
        body: Optional[dict],
        expect: Optional[str],
    ):
        respose = MagicMock()
        respose.status_code = 200
        respose.json.return_value = {}
        post_mock.return_value = respose
        api = PrivateApiBaseStub(
            api_key="api_key",
            secret_key="secret",
            body=body,
            method="POST",
            is_call=True,
        )
        api(data=body)
        post_mock.assert_called_once()
        kall = post_mock.call_args
        expect = (
            expect.replace(":", ": ") if expect else None
        )  # FIXME: 定義でスペースを空けるとテストがエラーになる
        assert kall.kwargs["data"] == expect
        assert api._body == body

    @time_machine.travel(datetime(2022, 12, 25))
    def test_timestamp(self):
        header = PrivateApiBaseStub(api_key="api_key", secret_key="secret").header
        assert header["API-TIMESTAMP"] == "{0}000".format(
            int(time.mktime(datetime.now().timetuple()))
        )

    @time_machine.travel(datetime(2024, 1, 3))
    def test_api_sign_get(self):
        method = "GET"
        path = "test"
        body = {"a": "a"}
        header = PrivateApiBaseStub(
            api_key="api_key", secret_key="secret", method=method, path=path, body=body
        ).header
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = timestamp + method + f"/{PrivateApiBaseStub.VERSION}/{path}"
        assert (
            header["API-SIGN"]
            == hmac.new(
                bytes("secret".encode("ascii")),
                bytes(text.encode("ascii")),
                hashlib.sha256,
            ).hexdigest()
        )

    @time_machine.travel(datetime(2024, 1, 3))
    def test_api_sign_post(self):
        method = "POST"
        path = "test"
        body = {"a": "a"}
        header = PrivateApiBaseStub(
            api_key="api_key", secret_key="secret", method=method, path=path, body=body
        ).header
        timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
        text = (
            timestamp
            + method
            + f"/{PrivateApiBaseStub.VERSION}/{path}"
            + json.dumps(body)
        )
        assert (
            header["API-SIGN"]
            == hmac.new(
                bytes("secret".encode("ascii")),
                bytes(text.encode("ascii")),
                hashlib.sha256,
            ).hexdigest()
        )


def create_ok_response() -> MagicMock:
    response = MagicMock()
    response.status_code = 200
    response.json.return_value = {}
    return response


class TestTimeout:

    timeouts = [
        # (kwargs, expect),
        ({}, None),
        ({"timeout": None}, None),
        ({"timeout": 3}, 3),
        ({"timeout": 2.5}, 2.5),
        ({"timeout": (3.05, 27)}, (3.05, 27)),
    ]

    @pytest.mark.parametrize("method", ["GET", "POST"])
    @pytest.mark.parametrize("kwargs, expect", timeouts)
    @patch("api.api_base.post")
    @patch("api.api_base.get")
    def test_public_api_should_pass_timeout(
        self,
        get_mock: MagicMock,
        post_mock: MagicMock,
        kwargs: dict,
        expect: Any,
        method: str,
    ):
        get_mock.return_value = create_ok_response()
        post_mock.return_value = create_ok_response()
        PublicApiBaseStub(method=method, **kwargs)()
        request_mock = get_mock if method == "GET" else post_mock
        request_mock.assert_called_once()
        assert request_mock.call_args.kwargs["timeout"] == expect

    @pytest.mark.parametrize("method", ["GET", "POST"])
    @pytest.mark.parametrize("kwargs, expect", timeouts)
    @patch("api.api_base.post")
    @patch("api.api_base.get")
    def test_private_api_should_pass_timeout(
        self,
        get_mock: MagicMock,
        post_mock: MagicMock,
        kwargs: dict,
        expect: Any,
        method: str,
    ):
        get_mock.return_value = create_ok_response()
        post_mock.return_value = create_ok_response()
        PrivateApiBaseStub(
            api_key="api_key",
            secret_key="secret",
            method=method,
            is_call=True,
            **kwargs,
        )()
        request_mock = get_mock if method == "GET" else post_mock
        request_mock.assert_called_once()
        assert request_mock.call_args.kwargs["timeout"] == expect

    @patch("gmo_fx.api.api_base.get")
    def test_klines_api_should_pass_timeout(self, get_mock: MagicMock):
        response = create_ok_response()
        response.json.return_value = {
            "status": 0,
            "data": [],
            "responsetime": "2024-01-01T00:00:00.000Z",
        }
        get_mock.return_value = response
        KlinesApi(timeout=5)(
            KlinesApi.Symbol.USD_JPY,
            "BID",
            KlinesApi.KlineInterval.D1,
            datetime(2024, 1, 1),
        )
        assert get_mock.call_args.kwargs["timeout"] == 5

    @patch("gmo_fx.api.api_base.post")
    def test_order_api_should_pass_timeout(self, post_mock: MagicMock):
        response = create_ok_response()
        response.json.return_value = {
            "status": 0,
            "data": [],
            "responsetime": "2024-01-01T00:00:00.000Z",
        }
        post_mock.return_value = response
        OrderApi(api_key="api_key", secret_key="secret", timeout=(3, 10))(
            symbol=OrderApi.Symbol.USD_JPY,
            side=OrderApi.Side.BUY,
            size=10000,
            execution_type=OrderApi.ExecutionType.MARKET,
        )
        assert post_mock.call_args.kwargs["timeout"] == (3, 10)

    @pytest.mark.parametrize("method", ["GET", "POST"])
    @patch("api.api_base.post")
    @patch("api.api_base.get")
    def test_should_raise_timeout(
        self, get_mock: MagicMock, post_mock: MagicMock, method: str
    ):
        get_mock.side_effect = Timeout
        post_mock.side_effect = Timeout
        with pytest.raises(Timeout):
            PublicApiBaseStub(method=method, timeout=1)()
        with pytest.raises(Timeout):
            PrivateApiBaseStub(
                api_key="api_key",
                secret_key="secret",
                method=method,
                is_call=True,
                timeout=1,
            )()
