from pydantic import BaseModel
from enum import Enum


class State(str, Enum):
    OK = 'ok'
    NOT_OK = 'nok'


class ServiceState(BaseModel):
    """
        index - should represent the order from config file (starting from zero)
        last_updated - stringified datetime in ISO format; 
            there is a possibility to have a datetime type here but only after implementing tindyDB DateTimeSerializer
            https://tinydb.readthedocs.io/en/v2.4/extend.html
    """
    index: int
    url: str
    state: State
    last_updated: str
