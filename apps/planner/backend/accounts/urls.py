from fastapi import APIRouter, status

from .controllers import create

router = APIRouter()


router.add_api_route(
    "/v1/accounts/{id}",
    methods=["POST"],
    endpoint=create,
    tags=["auth"],
    status_code=status.HTTP_201_CREATED,
)
