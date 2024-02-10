import requests
from requests import Response
from lxml import html
from ..models import State, HealthCheckResult, ServiceConfig
from requests.exceptions import RequestException


class WebHealthChecker:

    def check(self, service: ServiceConfig) -> HealthCheckResult:
        try:
            res = requests.get(service.url)
        except RequestException as e:
            # * will catch ConnectionError, HTTPError, Timeout, TooManyRedirects
            return HealthCheckResult(
                state=State.RED,
                message="There is a problem with connecting to the server. For details see logs."
            )
        if res.status_code != service.expected_status_code:
            return HealthCheckResult(
                state=State.RED,
                response_time_miliseconds=self._get_response_time(res),
                message=f"Status code is wrong. Expected: {service.expected_status_code}, received: {res.status_code}"
            )
        if service.xpath is None or self._is_xpath_passing(res, service.xpath):
            return HealthCheckResult(
                state=State.GREEN,
                response_time_miliseconds=self._get_response_time(res),
                message="All checks are passing!"
            )
        return HealthCheckResult(
                state=State.YELLOW,
                response_time_miliseconds=self._get_response_time(res),
                message=(
                    f"Status code is ok, but given Xpath expression '{service.xpath}' is not "
                    "pointing to any element on the page. Most likely element is missing!"
                )
            )
    
    
    def _get_response_time(self, res: Response) -> float:
        """ returns request response time in miliseconds """
        return res.elapsed.total_seconds()*1000
    
    def _is_xpath_passing(self, res: Response, xpath: str) -> bool:
        """ check if we can find any element using given xpath """
        root = html.fromstring(res.text)
        tree = root.getroottree()
        results = tree.xpath(xpath)
        return bool(results)
