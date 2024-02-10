from pydantic import BaseModel
from .state import State


class ServiceState(BaseModel):
    """
        index - should represent the order from config file (starting from zero)
        last_updated - stringified datetime in ISO format
    """
    index: int
    state: State
    last_updated: str
    details: str = ''
