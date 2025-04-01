from fastapi import Form
from pydantic import BaseModel
from typing import List, Optional

class IndexDocumentRequestSchema(BaseModel):
    document_ids: List[str]

    @classmethod
    def as_form(
        cls,
        document_ids: List[str] = Form(...),
    ):
        return cls(document_ids=document_ids)
    

class PointPayloadSchema(BaseModel):
    document_id: str
    text: str
    type: str
    page_number: Optional[int] = None
    img_url: Optional[str] = None
    document_url: Optional[str] = None


class PointSchema(BaseModel):
    id: str
    vector: List[float]
    payload: PointPayloadSchema
