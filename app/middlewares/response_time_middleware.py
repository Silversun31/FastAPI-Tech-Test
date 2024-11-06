import logging
import time

from app.main import app
from fastapi import Request


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    logger = logging.getLogger('     Request Process Time')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f' {process_time} secs\n')
    return response
