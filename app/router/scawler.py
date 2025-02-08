from app.api.crawler_controller import ScawlerRequest, scawler
from fastapi import APIRouter

api_router = APIRouter()

@api_router.post("/scawler")
def scawler_api(scawlerRequest: ScawlerRequest):
    return scawler(scawlerRequest)