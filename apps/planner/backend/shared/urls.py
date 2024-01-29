import os
from importlib import import_module

from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/healthcheck")
async def healthcheck():
    return Response("OK", status_code=200)


# Import all apps/plannner/backend/*/urls.py files and add them to the router
for module in os.listdir("apps/planner/backend"):
    if module.startswith("_"):
        continue
    if module in ["shared"]:
        continue
    try:
        urls = import_module(f"apps.planner.backend.{module}.urls")
    except ImportError:
        continue

    router.include_router(urls.router, tags=[module])
