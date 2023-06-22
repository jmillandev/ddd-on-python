from fastapi import APIRouter, Response

router = APIRouter()

@router.get('/healthcheck')
async def healthcheck():
    return Response(status_code=200)
