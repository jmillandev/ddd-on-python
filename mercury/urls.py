from fastapi import APIRouter, Response
from apps.users.urls import router as auth_router
router = APIRouter()

@router.get('/healthcheck')
async def healthcheck():
    return Response('OK',status_code=200)

router.include_router(auth_router, tags=['auth'])
