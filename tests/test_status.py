from unittest.mock import MagicMock, patch
from gmo_fx.status import get_status, Status

from tests.api_test_base import ApiTestBase


class TestStatusApi(ApiTestBase):

    @patch("gmo_fx.status.get")
    def test_status_error(self, get_mock: MagicMock):
        self.check_404_error(get_mock, lambda: get_status())

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
