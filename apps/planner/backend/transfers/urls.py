from fastapi import APIRouter, status

from .controllers import add

router = APIRouter()

router.add_api_route(
    "/v1/transfers/{id}",
    methods=["POST"],
    endpoint=add,
    tags=["movements"],
    status_code=status.HTTP_201_CREATED,
)
