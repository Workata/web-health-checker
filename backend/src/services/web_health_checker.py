import requests
from ..models import State
import typing as t


class WebHealthChecker:

    def check(self, url: str, expected_status_code: int) -> t.Tuple[State, str]:
        res = requests.get(url)
        print(f"Received status code: {res.status_code}")
        if res.status_code == expected_status_code:
            return State.GREEN, "All checks are passing"
        return State.RED, "Status code is wrong"
