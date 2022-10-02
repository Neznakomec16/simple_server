from fastapi import APIRouter

from .health_check import HealthCheckResponse, health_check

services_router = APIRouter(prefix="/services")
services_router.add_api_route("/health_check", health_check, response_model=HealthCheckResponse)
