from pydantic import BaseModel
import typing as t


class ServiceConfig(BaseModel):
    url: str
    expected_status_code: int
    xpath: t.Optional[str] = None
