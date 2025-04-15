from typing import AsyncIterator
from langchain_ollama import OllamaLLM
from .llm_interface import LLM


class Ollama(LLM):
    def __init__(self):
        self._model = OllamaLLM(model='mistral')
        
    async def change_model(self, model_name):
        self._model = OllamaLLM(model=model_name)
    
    async def astream(self, input: str) -> AsyncIterator[str]:
        async for chunk in self._model.astream(input):
            yield chunk
            
    async def ainvoke(self, input: str) -> str:
        return await self._model.ainvoke(input)