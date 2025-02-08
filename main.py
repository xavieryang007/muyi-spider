from fastapi import FastAPI

from app.router.scawler import api_router

app = FastAPI()

app.include_router(api_router)