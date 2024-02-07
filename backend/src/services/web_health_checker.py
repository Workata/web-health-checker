import requests
from ..models import State


class WebHealthChecker:

    def check(self, url: str, expected_status_code: int) -> State:
        res = requests.get(url)
        print(f"Received status code: {res.status_code}")
        if res.status_code == expected_status_code:
            return State.OK
        return State.NOT_OK
