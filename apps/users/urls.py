from fastapi import APIRouter, status

from apps.users.controllers import sign_up
from apps.users.schemas import Token, User

router = APIRouter()


router.add_api_route('/v1/sign-up', methods=['POST'],
                     endpoint=sign_up, tags=['users'], status_code=status.HTTP_201_CREATED)
# router.add_api_route('/v1/sign-in', methods=['POST'], response_model=Token,
#                      endpoint=sign_in, tags=['auth'], status_code=status.HTTP_200_OK)
# router.add_api_route('/v1/users/{id}', methods=['POST'], response_model=User,
#                      endpoint=retrieve, tags=['users'], status_code=status.HTTP_200_OK)
