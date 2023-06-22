from fastapi import APIRouter, Response

router = APIRouter()

@router.get('/healthcheck')
async def healthcheck():
    return Response('OK',status_code=200)
