from fastapi import Request
from log.logger import logger

async def log_middleware(request: Request, call_next):
    log_dict = {
        'url': request.url.path,
        'method': request.method,
        'query_parameters': request.query_params
    }
    logger.info(log_dict)
    response = await call_next(request)
    return response