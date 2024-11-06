from fastapi import FastAPI

app = FastAPI()

from .middlewares import response_time_middleware
from app.routers import urlpatterns
