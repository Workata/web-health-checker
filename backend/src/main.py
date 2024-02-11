import datetime as dt
import logging
import logging.config
import os
import typing as t
from contextlib import asynccontextmanager

from celery.app import Celery
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi_restful.tasks import repeat_every
from tinydb import Query

from .models import Config, HealthCheckResult, ServiceState
from .services import WebHealthChecker
from .settings import get_settings
from .utils import CollectionProvider, YamlReader


settings = get_settings()
logging.config.dictConfig(settings.logging)
logger = logging.getLogger("general")

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

config = Config(**YamlReader.read("./config.yaml"))

collection_provider = CollectionProvider()
ServiceQuery = Query()
services_collection = collection_provider.provide("services")


@asynccontextmanager
async def lifespan(app: FastAPI) -> t.Any:
    """
    ? https://fastapi.tiangolo.com/advanced/events/
    """
    await main_task()
    yield


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/services")
def get_services() -> JSONResponse:
    services_coll = collection_provider.provide("services")
    return JSONResponse(content=services_coll.all(), status_code=status.HTTP_200_OK)


@app.get("/api/v1/config")
def get_config() -> JSONResponse:
    return JSONResponse(
        content=[
            {
                "index": idx,
                "url": service.url,
                "expected_status_code": service.expected_status_code,
            }
            for idx, service in enumerate(config.services)
        ],
        status_code=status.HTTP_200_OK,
    )


@celery_app.task
def sub_task(service_index: int) -> t.Dict[str, t.Any]:
    """
    ? https://tinydb.readthedocs.io/en/stable/api.html?highlight=upsert#tinydb.table.Table.upsert
    """
    service = config.services[service_index]
    result: HealthCheckResult = WebHealthChecker().check(service)
    logger.info(
        f"URL: {service.url}, status: {result.state}, response time: "
        f"{result.response_time_miliseconds if result.response_time_miliseconds is not None else '---'} "
        f"message: {result.message} "
        f"traceback: {result.error_message if result.error_message is not None else '---'}"
    )
    state = ServiceState(
        index=service_index,
        state=result.state,
        response_time_miliseconds=(
            round(result.response_time_miliseconds, 2)
            if result.response_time_miliseconds
            else None
        ),
        last_updated=dt.datetime.now(dt.timezone.utc).isoformat(),
        details=result.message,
    )
    services_collection.upsert(state.model_dump(), ServiceQuery.index == service_index)
    return state.model_dump()  # type: ignore[no-any-return]


@repeat_every(seconds=config.refresh_period_seconds)
async def main_task() -> None:
    for idx in range(len(config.services)):
        sub_task.delay(idx)
