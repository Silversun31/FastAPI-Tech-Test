import time

from app.main import app
from fastapi import Request


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    print(f'\nINFO:     Request Process Time: {process_time} secs')
    return response
