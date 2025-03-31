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