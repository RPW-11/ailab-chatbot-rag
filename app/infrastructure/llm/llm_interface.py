from abc import ABC, abstractmethod
from typing import AsyncIterator


class LLM(ABC):
    @abstractmethod
    async def astream(self, input: str) -> AsyncIterator[str]:
        pass
    
    @abstractmethod
    async def ainvoke(self, input: str) -> str:
        pass
    
    @abstractmethod
    async def change_model(self, model_name: str) -> None:
        pass