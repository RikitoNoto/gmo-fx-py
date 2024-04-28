from typing import Optional, Union
import pytest
import json
from unittest.mock import MagicMock, patch
from gmo_fx.status import get_status, Status
from datetime import datetime


class TestStatusApi:

    def create_response(
        self,
        data: Optional[Union[dict, list]] = None,
        status_code: int = 200,
        text: Optional[str] = None,
    ) -> MagicMock:
        response = MagicMock()
        response.status_code = status_code
        json_data = {
            "status": 0,
            "data": data,
            "responsetime": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        response.json.return_value = json_data
        response.text = text or json.dumps(json_data)
        return response

    @patch("gmo_fx.status.get")
    def test_status_open(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "OPEN"})
        actual = get_status()
        assert actual.status == Status.OPEN

    @patch("gmo_fx.status.get")
    def test_status_close(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "CLOSE"})
        actual = get_status()
        assert actual.status == Status.CLOSE

    @patch("gmo_fx.status.get")
    def test_status_maintenance(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "MAINTENANCE"})
        actual = get_status()
        assert actual.status == Status.MAINTENANCE

    @patch("gmo_fx.status.get")
    def test_status_error(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(status_code=404, text="Not Found")
        with pytest.raises(RuntimeError):
            get_status()
