from pydantic import BaseModel
from .service_config import ServiceConfig
import typing as t


class Config(BaseModel):
    services: t.List[ServiceConfig]
    refresh_period_seconds: int
