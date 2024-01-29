from fastapi import APIRouter, status

from apps.planner.backend.users.controllers import find, sign_up
from src.planner.users.application.find.responses import UserResponse

router = APIRouter()


router.add_api_route(
    "/v1/sign-up",
    methods=["POST"],
    endpoint=sign_up,
    tags=["auth"],
    status_code=status.HTTP_201_CREATED,
)
router.add_api_route(
    "/v1/users/{id}",
    methods=["GET"],
    response_model=UserResponse,
    endpoint=find,
    status_code=status.HTTP_200_OK,
)
