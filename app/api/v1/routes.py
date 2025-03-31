from fastapi import APIRouter

from app.api.v1.endpoints.indexing import router as indexing_router
from app.api.v1.endpoints.inference import router as inference_router

routers = APIRouter()
router_list = [indexing_router, inference_router]

for router in router_list:
    routers.include_router(router)

