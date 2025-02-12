from typing import Callable

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

class TileError(Exception):
    """Base class for tile errors."""

class TileNotFoundError(TileError):
    """Tile not found error."""
    
class BadRequestError(TileError):
    """Bad request error."""

DEFAULT_STATUS_CODES = {
    BadRequestError: status.HTTP_400_BAD_REQUEST,
    Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
}

def exception_handler_factory(status_code: int) -> Callable:
    """Create an exception handler for a given status code."""
    def handler(request: Request, exc: Exception):
        if status_code == status.HTTP_204_NO_CONTENT:
            return Response(content=None, status_code=status_code)
        
        return JSONResponse(
            status_code=status_code,
            content={"message": str(exc)},
        )
    return handler

def add_exception_handlers(app: FastAPI):
    """Add exception handlers to the application."""
    for exc, status_code in DEFAULT_STATUS_CODES.items():
        app.add_exception_handler(exc, exception_handler_factory(status_code))