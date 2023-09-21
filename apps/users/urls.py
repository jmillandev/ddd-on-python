from fastapi import APIRouter

from apps.users.controllers import sign_in, sign_up
from apps.users.schemas import Token, User

router = APIRouter()


router.add_api_route('/v1/sign-up', methods=['POST'], response_model=User,
                     endpoint=sign_up, tags=['sign-up', 'auth'], status_code=201)
router.add_api_route('/v1/sign-in', methods=['POST'], response_model=Token,
                     endpoint=sign_in, tags=['sign-in', 'auth'], status_code=200)
