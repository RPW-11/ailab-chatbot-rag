from fastapi import APIRouter, Depends
from app.service.inference_service import InferenceService
from app.schema.inference_schema import InferenceRequestSchema

router = APIRouter(
    prefix="/inference",
    tags=["inference"],
)

@router.get("")
async def get_index():
    return {"message": "Inference endpoint"}


@router.post("/infer", status_code=200)
async def infer(
    inferece_body: InferenceRequestSchema,
    inference_service: InferenceService = Depends()
):
    return await inference_service.infer(inferece_body)