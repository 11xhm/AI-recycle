from dataclasses import dataclass
from typing import Any

from fastapi.responses import JSONResponse


@dataclass
class AppError(Exception):
    status_code: int
    code: str
    message: str
    details: Any | None = None

    @staticmethod
    def invalid_request(message: str, details: Any | None = None) -> "AppError":
        return AppError(status_code=400, code="INVALID_REQUEST", message=message, details=details)

    @staticmethod
    def unsupported_file(message: str, details: Any | None = None) -> "AppError":
        return AppError(status_code=415, code="UNSUPPORTED_FILE", message=message, details=details)

    @staticmethod
    def unauthorized(message: str = "未登录", details: Any | None = None) -> "AppError":
        return AppError(status_code=401, code="UNAUTHORIZED", message=message, details=details)

    @staticmethod
    def forbidden(message: str = "无权限", details: Any | None = None) -> "AppError":
        return AppError(status_code=403, code="FORBIDDEN", message=message, details=details)

    @staticmethod
    def not_found(message: str = "资源不存在", details: Any | None = None) -> "AppError":
        return AppError(status_code=404, code="NOT_FOUND", message=message, details=details)

    @staticmethod
    def conflict(message: str = "资源冲突", details: Any | None = None) -> "AppError":
        return AppError(status_code=409, code="CONFLICT", message=message, details=details)

    @staticmethod
    def ai_provider_error(message: str, details: Any | None = None) -> "AppError":
        return AppError(status_code=502, code="AI_PROVIDER_ERROR", message=message, details=details)

    @staticmethod
    def internal_error(message: str = "服务内部错误", details: Any | None = None) -> "AppError":
        return AppError(status_code=500, code="INTERNAL_ERROR", message=message, details=details)


def app_error_to_response(err: AppError) -> JSONResponse:
    payload: dict[str, Any] = {"error": {"code": err.code, "message": err.message}}
    if err.details is not None:
        payload["error"]["details"] = err.details
    return JSONResponse(status_code=err.status_code, content=payload)
