from enum import auto

from pydantic import BaseModel
from starlette.requests import Request

from main.application.context import postgres_context, redis_context
from main.application.routes.services.utils import check_postgres, check_redis
from main.application.utils import AutoName


class StatusEnum(AutoName):
    OK = auto()
    Failed = auto()


class HealthCheckResponse(BaseModel):
    server_status: StatusEnum
    postgres_status: StatusEnum
    redis_status: StatusEnum


async def health_check(request: Request) -> HealthCheckResponse:
    postgres = postgres_context.get(request)
    postgres_status = await check_postgres(postgres)
    redis = redis_context.get(request)
    redis_status = await check_redis(redis)
    return HealthCheckResponse(
        server_status=StatusEnum.OK,
        postgres_status=StatusEnum.OK if postgres_status else StatusEnum.Failed,
        redis_status=StatusEnum.OK if redis_status else StatusEnum.Failed,
    )
