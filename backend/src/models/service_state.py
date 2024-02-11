from pydantic import BaseModel
from .state import State
import typing as t


class ServiceState(BaseModel):
    """
    index - should represent the order from config file (starting from zero)
    last_updated - stringified datetime in ISO format
    """

    index: int
    state: State
    last_updated: str
    response_time_miliseconds: t.Optional[float] = None
    details: str = ""
