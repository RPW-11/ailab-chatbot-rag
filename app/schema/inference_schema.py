from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class InferenceRequestSchema(BaseModel):
    user_id: str
    conversation_id: str
    prompt: str
    model_name: str = 'deepseek-v2'
    optimized_search: Optional[bool]
    is_streaming: bool = True
    

class Message(BaseModel):
    text: str
    time_stamp: Optional[datetime] = None
    is_assistant: bool
    
    
class Conversation(BaseModel):
    pass
    