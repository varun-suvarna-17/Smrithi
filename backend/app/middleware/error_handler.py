import logging
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("smrithi.error_handler")

async def global_exception_handler(request: Request, exc: Exception):
    """Catches unexpected exceptions and returns structured JSON."""
    logger.error(f"Unhandled server error on {request.method} {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "error_type": "InternalServerError",
            "message": "An unexpected server error occurred while processing the request.",
            "path": str(request.url.path),
            "detail": str(exc) if request.app.debug else "Internal error"
        }
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Formats Starlette / FastAPI HTTPExceptions consistently."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error_type": "HTTPException",
            "status_code": exc.status_code,
            "message": exc.detail,
            "path": str(request.url.path)
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Formats Pydantic request validation errors nicely."""
    errors = []
    for err in exc.errors():
        field = ".".join(str(loc) for loc in err.get("loc", []))
        errors.append({
            "field": field,
            "message": err.get("msg", "Invalid field input"),
            "type": err.get("type", "value_error")
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "success": False,
            "error_type": "ValidationError",
            "message": "Input validation failed. Please check the requested fields.",
            "errors": errors,
            "path": str(request.url.path)
        }
    )
