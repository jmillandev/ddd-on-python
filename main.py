from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from mercury.config import settings
from mercury.urls import router
from utils.errors import BaseError

app = FastAPI(
    title=settings.PROJECT_NAME, openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin)
                       for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router, prefix=settings.API_PREFIX)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    data = ({'source': err['loc'][1], 'msg': err['msg']}
            for err in exc.errors())
    return JSONResponse({'detail': tuple(data)}, status_code=422)


@app.exception_handler(BaseError)
async def base_error_handler(request, exception):
    return JSONResponse({'detail': [dict(exception)]}, status_code=exception.status_code)
