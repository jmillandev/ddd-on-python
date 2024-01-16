from fastapi import APIRouter, status

from apps.planner.backend.users.controllers import sign_up, find
from src.planner.users.application.responses import UserResponse

router = APIRouter()


router.add_api_route('/v1/sign-up', methods=['POST'],
                     endpoint=sign_up, tags=['users'], status_code=status.HTTP_201_CREATED)
router.add_api_route('/v1/users/{id}', methods=['GET'], response_model=UserResponse,
                     endpoint=find, tags=['users'], status_code=status.HTTP_200_OK)
