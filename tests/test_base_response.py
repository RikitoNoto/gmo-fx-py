import pytest
from gmo_fx.response import Response
from datetime import datetime


class TestBaseResponse:
    testdata = [
        (0, datetime(2001, 12, 12)),
        (1, datetime(2010, 3, 1)),
        (1001, datetime(2020, 5, 20)),
    ]

    @pytest.mark.parametrize("status, time", testdata)
    def test_convert_response(
        self,
        status: int,
        time: datetime,
    ):
        data = {
            "status": status,
            "responsetime": time.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        response = Response(data)
        assert response.response_status == status
        assert response.response_time == time
