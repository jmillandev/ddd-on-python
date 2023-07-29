from fastapi import APIRouter

from apps.users.controllers import sign_up
from apps.users.schemas import User

router = APIRouter()


router.add_api_route('/v1/sign-up', methods=['POST'], response_model=User, endpoint=sign_up, tags=['sign-up'], status_code=201)
