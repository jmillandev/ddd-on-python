from fastapi import APIRouter, status

from apps.planner.backend.auth.controllers import sign_in
from src.planner.auth_token.application.shared.response import AuthTokenResponse

router = APIRouter()


router.add_api_route(
    "/v1/sign-in",
    methods=["POST"],
    response_model=AuthTokenResponse,
    endpoint=sign_in,
    status_code=status.HTTP_200_OK,
)
