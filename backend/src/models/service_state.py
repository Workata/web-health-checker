from pydantic import BaseModel
from enum import Enum


class State(str, Enum):
    """
        GREEN   - all checks are passing
        YELLOW  - status code is ok (equal to expected) but some other checks are not passing
                additional information should be passed via details in ServiceState model
        RED     - status code is not ok (not equal to expected); other checks are omitted
    """
    GREEN = 'ok'
    YELLOW = 'yellow'
    RED = 'red'

    # UNKNOWN = 'unknown'


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
    details: str = ''
