import logging

from fastapi import FastAPI

app = FastAPI()
logging.basicConfig(level=logging.INFO)

from .middlewares import response_time_middleware
from app.routers import urlpatterns
