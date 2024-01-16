import os

from fastapi import APIRouter, Response

router = APIRouter()

@router.get('/healthcheck')
async def healthcheck():
    return Response('OK',status_code=200)

# Import all apps/*/urls.py files and add them to the router
for module in os.listdir('apps'):
    if module.startswith('_'):
        continue
    try:
        module = __import__(f'apps.{module}.urls', fromlist=['router'])
    except ImportError:
        continue

    router.include_router(module.router, tags=[module])
