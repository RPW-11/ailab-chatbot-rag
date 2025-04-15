from typing import List
from app.schema.inference_schema import Message
from app.schema.indexing_schema import PointSchema


def format_conversation_history(messages: List[Message]) -> str:
    """
    Format the conversation history to accepted string format
    """
    conversation_str = ""
    for message in messages:
        conversation_str += f"{'Assistant' if message.is_assistant else 'User'}: {message.text}\n"
    return conversation_str


def format_retrieved_documents(document_points: List[PointSchema]) -> str:
    """
    Format the document points to accepted string format
    """
    documents_str = ""
    for point in document_points:
        documents_str += f"\n- Document name: {point.payload.document_id}\nPage number: {point.payload.page_number}\nContent: {point.payload.text}"
    return documents_str


def build_prompt(system_prompt: str, conversation_history: str, retrieved_docs: str, user_query: str):
    if not conversation_history:
        conversation_history = f"<empty>"
    if not retrieved_docs:
        retrieved_docs=f"<empty>"
    
    return system_prompt.format(
        history=conversation_history,
        context=retrieved_docs,
        user_input=user_query
    )
        