from unittest.mock import MagicMock, patch
from gmo_fx.api.status import StatusApi, StatusResponse, Status

from tests.api_test_base import ApiTestBase


class TestStatusApi(ApiTestBase):

    def call_api(
        self,
    ) -> StatusResponse:
        return StatusApi()()

    @patch("gmo_fx.api.api_base.get")
    def test_status_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: self.call_api())

    @patch("gmo_fx.api.api_base.get")
    def test_status_open(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "OPEN"})
        actual = self.call_api()
        assert actual.status == Status.OPEN

    @patch("gmo_fx.api.api_base.get")
    def test_status_close(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "CLOSE"})
        actual = self.call_api()
        assert actual.status == Status.CLOSE

    @patch("gmo_fx.api.api_base.get")
    def test_status_maintenance(self, get_mock: MagicMock):
        get_mock.return_value = self.create_response(data={"status": "MAINTENANCE"})
        actual = self.call_api()
        assert actual.status == Status.MAINTENANCE
