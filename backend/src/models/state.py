from enum import Enum


class State(str, Enum):
    """
    GREEN   - all checks are passing
    YELLOW  - status code is ok (equal to expected) but some other checks are not passing
            additional information should be passed via details in ServiceState model
    RED     - status code is not ok (not equal to expected); other checks are omitted
    """

    GREEN = "green"
    YELLOW = "yellow"
    RED = "red"
