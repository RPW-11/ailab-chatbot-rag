from pydantic import BaseModel
from typing import List, Optional


class InferenceRequestSchema(BaseModel):
    user_id: str
    conversation_id: str
    prompt: str
    model_name: str = 'deepseek-v2'
    optimized_search: Optional[bool]
    is_streaming: bool = True