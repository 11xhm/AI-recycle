from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.routes import router as api_router
from app.core.config import settings
from app.core.db import create_tables
from app.core.errors import AppError, app_error_to_response


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(_: FastAPI):
        settings.upload_dir.mkdir(parents=True, exist_ok=True)
        create_tables()
        yield

    app = FastAPI(title="recycle-ai", version="0.1.0", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PATCH", "OPTIONS"],
        allow_headers=["*"],
    )

    app.include_router(api_router)
    app.mount("/uploads", StaticFiles(directory=str(settings.upload_dir), check_dir=False), name="uploads")

    @app.exception_handler(AppError)
    async def _app_error_handler(_, exc: AppError):
        return app_error_to_response(exc)

    @app.exception_handler(Exception)
    async def _unhandled_error_handler(_, exc: Exception):
        return app_error_to_response(AppError.internal_error())

    return app


app = create_app()
