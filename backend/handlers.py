from fastapi import Request, status
from fastapi.responses import JSONResponse

from backend.libs.exceptions import NotFound, AlreadyExists, PaginationError
from backend.room.exceptions import RoomLimitExceeded, FileLimitExceeded, FileSizeExceeded

async def not_found_exception_handler(request: Request, exc: NotFound):
    """
    Handles NotFound exceptions, returning a 404 response.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc) or "Resource not found."},
    )

async def already_exists_exception_handler(request: Request, exc: AlreadyExists):
    """
    Handles AlreadyExists exceptions, returning a 409 response.
    """
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": str(exc) or "Resource already exists."},
    )

async def room_limit_exception_handler(request: Request, exc: RoomLimitExceeded):
    """
    Handles RoomLimitExceeded exceptions, returning a 403 response.
    """
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": str(exc)},
    )

async def file_limit_exception_handler(request: Request, exc: FileLimitExceeded | FileSizeExceeded):
    """
    Handles file-related limit exceptions, returning a 413 response.
    """
    return JSONResponse(
        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
        content={"detail": str(exc)},
    )

async def pagination_exception_handler(request: Request, exc: PaginationError):
    """
    Handles PaginationError exceptions, returning a 400 response.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)},
    )

# Словарь для удобной регистрации обработчиков в приложении
exception_handlers = {
    NotFound: not_found_exception_handler,
    AlreadyExists: already_exists_exception_handler,
    RoomLimitExceeded: room_limit_exception_handler,
    FileLimitExceeded: file_limit_exception_handler,
    FileSizeExceeded: file_limit_exception_handler,
    PaginationError: pagination_exception_handler,
}