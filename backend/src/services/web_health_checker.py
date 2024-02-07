import requests


class WebHealthChecker:

    def check(self, url: str, expected_status_code: int) -> str:
        res = requests.get(url)
        print(f"Recived status code: {res.status_code}")
        if res.status_code == expected_status_code:
            return "All good"
        return "Not good"
        


