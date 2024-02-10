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
from .models import ServiceState, State
import datetime as dt


redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

config = YamlReader.read("./config.yaml")       # TODO validate data with pydantic models

collection_provider = CollectionProvider()
ServiceQuery = Query()
services_collection = collection_provider.provide("services")

@celery_app.task
def sub_task(service_index: int, url: str, expected_status_code: str) -> State:
    print(f"{url} -- {expected_status_code}")
    state = WebHealthChecker().check(url, expected_status_code)
    service_state = ServiceState(
        index=service_index,
        url=url,
        state=state,
        last_updated=dt.datetime.now().isoformat()
    )
    # ? https://tinydb.readthedocs.io/en/stable/api.html?highlight=upsert#tinydb.table.Table.upsert
    services_collection.upsert(service_state.model_dump(), ServiceQuery.index == service_index)
    return state


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ? https://fastapi.tiangolo.com/advanced/events/
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
            "url": service['url'],
            "expected_status_code": service['expected_status_code']
        } for idx, service in enumerate(config['services'])],
        status_code=status.HTTP_200_OK
    )



@repeat_every(seconds=config['refresh_period_seconds'])
async def main_task() -> None:
    for idx, service in enumerate(config['services']):
        res: AsyncResult = sub_task.delay(idx, service['url'], service['expected_status_code'])
        print(f"Task ID: {res.task_id}")
