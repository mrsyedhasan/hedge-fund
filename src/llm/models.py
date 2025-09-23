import os
from typing import Union, Optional
from langchain_ollama import ChatOllama
from enum import Enum
from pydantic import BaseModel
from typing import Tuple, List


class ModelProvider(str, Enum):
    """Enum for supported LLM providers"""
    OLLAMA = "Ollama"


class LLMModel(BaseModel):
    """Represents an LLM model configuration"""
    display_name: str
    model_name: str
    provider: ModelProvider

    def to_choice_tuple(self) -> Tuple[str, str, str]:
        """Convert to format needed for questionary choices"""
        return (self.display_name, self.model_name, self.provider.value)
    
    def has_json_mode(self) -> bool:
        """Check if the model supports JSON mode"""
        return False  # Ollama models don't support JSON mode
    
    def is_deepseek(self) -> bool:
        """Check if the model is a DeepSeek model"""
        return False
    
    def is_gemini(self) -> bool:
        """Check if the model is a Gemini model"""
        return False


# Define available Ollama models
AVAILABLE_MODELS = [
    LLMModel(
        display_name="[ollama] mistral:7b-instruct",
        model_name="mistral:7b-instruct",
        provider=ModelProvider.OLLAMA
    ),
    LLMModel(
        display_name="[ollama] llama3.1:8b-instruct",
        model_name="llama3.1:8b-instruct",
        provider=ModelProvider.OLLAMA
    ),
    LLMModel(
        display_name="[ollama] codellama:7b-instruct",
        model_name="codellama:7b-instruct",
        provider=ModelProvider.OLLAMA
    ),
    LLMModel(
        display_name="[ollama] qwen2.5:7b-instruct",
        model_name="qwen2.5:7b-instruct",
        provider=ModelProvider.OLLAMA
    ),
]

# Create LLM_ORDER in the format expected by the UI
LLM_ORDER = [model.to_choice_tuple() for model in AVAILABLE_MODELS]

# For compatibility with existing code
OLLAMA_LLM_ORDER = LLM_ORDER

def get_model_info(model_name: str, model_provider: str) -> Optional[LLMModel]:
    """Get model information by model_name"""
    return next((model for model in AVAILABLE_MODELS if model.model_name == model_name and model.provider == model_provider), None)

def get_model(model_name: str, model_provider: ModelProvider, api_keys: dict = None) -> ChatOllama:
    """Get an Ollama model instance"""
    if model_provider == ModelProvider.OLLAMA:
        # For Ollama, we use a base URL instead of an API key
        # Check if OLLAMA_HOST is set (for Docker on macOS)
        ollama_host = os.getenv("OLLAMA_HOST", "localhost")
        base_url = os.getenv("OLLAMA_BASE_URL", f"http://{ollama_host}:11434")
        return ChatOllama(
            model=model_name,
            base_url=base_url,
        )
    else:
        raise ValueError(f"Only Ollama is supported. Unsupported model provider: {model_provider}")
