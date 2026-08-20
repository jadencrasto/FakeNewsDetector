from abc import ABC, abstractmethod
from typing import Type, TypeVar


T = TypeVar("T")


class LLMClient(ABC):

    @abstractmethod
    def generate_structured(
        self,
        prompt: str,
        response_model: Type[T]
    ) -> T:
        """
        Generate a structured response using an LLM.

        Args:
            prompt: Prompt sent to the model.
            response_model: Pydantic model expected from the LLM.

        Returns:
            Validated instance of response_model.
        """
        pass