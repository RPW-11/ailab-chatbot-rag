from fastapi import UploadFile
from typing import List

def validate_document_type(document_files: List[UploadFile]) -> bool:
    """
    Validate the document types.
    """
    for document_file in document_files:
        if not any(document_file.filename.endswith(ext) for ext in [".pdf", ".docx", ".txt"]):
            return False
    return True