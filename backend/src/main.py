import os
from contextlib import asynccontextmanager

from celery.app import Celery
from celery.result import AsyncResult
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from fastapi_restful.tasks import repeat_every
from fastapi.middleware.cors import CORSMiddleware
from tinydb import Query

from .services import WebHealthChecker
from .utils import YamlReader, CollectionProvider
from .models import ServiceState, Config, ServiceConfig, HealthCheckResult
import datetime as dt
import typing as t


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

config = Config(**YamlReader.read("./config.yaml"))

collection_provider = CollectionProvider()
ServiceQuery = Query()
services_collection = collection_provider.provide("services")


@asynccontextmanager
async def lifespan(app: FastAPI):
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


@app.get("/api/v1/task/{task_id}")
def get_task(task_id: str):
    res = celery_app.AsyncResult(task_id)
    return JSONResponse(
        content={
            "result": res.result,
            "id": task_id,
            "status": res.status
        },
        status_code=status.HTTP_200_OK
    )


@app.get("/api/v1/services")
def get_services():
    services_coll = collection_provider.provide("services")
    return JSONResponse(content=services_coll.all(), status_code=status.HTTP_200_OK)



@app.get("/api/v1/config")
def get_config():
    return JSONResponse(
        content=[{
            "index": idx,
            "url": service.url,
            "expected_status_code": service.expected_status_code
        } for idx, service in enumerate(config.services)],
        status_code=status.HTTP_200_OK
    )


@celery_app.task
def sub_task(service_index: int) -> t.Dict[str, t.Any]:
    """
        ? https://tinydb.readthedocs.io/en/stable/api.html?highlight=upsert#tinydb.table.Table.upsert
    """
    service = config.services[service_index]
    result: HealthCheckResult = WebHealthChecker().check(service)
    state = ServiceState(
        index=service_index,
        state=result.state,
        last_updated=dt.datetime.now().isoformat(),
        details=result.message
    )
    services_collection.upsert(state.model_dump(), ServiceQuery.index == service_index)
    return state.model_dump()

@repeat_every(seconds=config.refresh_period_seconds)
async def main_task() -> None:
    for idx in range(len(config.services)):
        res: AsyncResult = sub_task.delay(idx)
        print(f"Task ID: {res.task_id}")        # TODO remove debugging prints
