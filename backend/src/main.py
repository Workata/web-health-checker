from fastapi import FastAPI
from fastapi import status
from fastapi_restful.tasks import repeat_every
from contextlib import asynccontextmanager
from celery.app import Celery
# from celery.result import AsyncResult
import os
from .utils import YamlReader
from .services import WebHealthChecker
from fastapi.responses import JSONResponse
# from src.services import WebHealthChecker

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
celery_app = Celery(__name__, broker=redis_url, backend=redis_url)

config = YamlReader.read("./config.yaml")       # TODO validate with pydantic models

@celery_app.task
def sub_task(url: str, expected_status_code: str):
    print(f"{url} -- {expected_status_code}")
    msg = WebHealthChecker().check(url, expected_status_code)
    return msg

@asynccontextmanager
async def lifespan(app: FastAPI):
    await main_task()
    yield


app = FastAPI(lifespan=lifespan)


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


@repeat_every(seconds=5)
async def main_task() -> None:
    for service in config['services']:
        # print(f"{service['url']} -- {service['expected_status_code']}")
        # res -> task_id, status, result
        res = sub_task.delay(service['url'], service['expected_status_code'])       # return async result probably
        print(f"Task ID: {res.task_id}")


# from backend folder
# celery --app=src.main.celery_app worker --concurrency=4 --loglevel=DEBUG
