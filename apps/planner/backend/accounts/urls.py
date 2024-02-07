from fastapi import APIRouter, status

from src.planner.shared.application.accounts.response import AccountResponse

from .controllers import create, find

router = APIRouter()


router.add_api_route(
    "/v1/accounts/{id}",
    methods=["POST"],
    endpoint=create,
    status_code=status.HTTP_201_CREATED,
)

router.add_api_route(
    "/v1/accounts/{id}",
    methods=["GET"],
    endpoint=find,
    status_code=status.HTTP_200_OK,
    response_model=AccountResponse,
)
