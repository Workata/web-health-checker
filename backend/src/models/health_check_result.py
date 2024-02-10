from pydantic import BaseModel
from .state import State
import typing as t


class HealthCheckResult(BaseModel):
    state: State
    response_time_miliseconds: t.Optional[float] = None
    message: str
