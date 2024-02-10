import requests
from requests import Response
from lxml import html
from ..models import State
import typing as t
from requests.exceptions import RequestException


class WebHealthChecker:

    def check(self, service: t.Any) -> t.Tuple[State, str]:
        try:
            res = requests.get(service['url'])
        except RequestException as e:
            # * will catch ConnectionError, HTTPError, Timeout, TooManyRedirects
            return State.RED, "There is a problem with connecting to the server. For details see logs."
        if res.status_code == service['expected_status_code']:
            if "xpath" not in service or self._is_xpath_passing(res, service['xpath']):
                return State.GREEN, "All checks are passing!"
            return State.YELLOW, f"Status code is ok, but given Xpath expression \"{service['xpath']}\" is not pointing to any element on the page. Most likely element is missing!"
        return State.RED, "Status code is wrong"
    
    def _is_xpath_passing(self, res: Response, xpath: str) -> bool:
        """ check if we can find any element using given xpath """
        root = html.fromstring(res.text)
        tree = root.getroottree()
        results = tree.xpath(xpath)
        return bool(results)
