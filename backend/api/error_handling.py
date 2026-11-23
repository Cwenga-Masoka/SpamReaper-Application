import logging

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from api.constants import ErrorMessage
from auth.errors import NotLoggedInError

UNEXPECTED_ERROR_LOG_FORMAT = "Unexpected error on %s %s"

logger = logging.getLogger(__name__)


async def convert_unexpected_errors_to_500(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception:
        logger.exception(UNEXPECTED_ERROR_LOG_FORMAT, request.method, request.url.path)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": ErrorMessage.INTERNAL_ERROR},
        )


async def convert_not_logged_in_to_401(request: Request, error: NotLoggedInError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"detail": str(error)},
    )


def bad_request(detail: str) -> HTTPException:
    return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)