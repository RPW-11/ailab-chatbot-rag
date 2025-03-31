from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/inference",
    tags=["inference"],
)

@router.get("")
async def get_index():
    return {"message": "Inference endpoint"}