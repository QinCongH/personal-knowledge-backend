# agent/model/llm.py
from langchain.chat_models import init_chat_model
from .config import ModelConfig

def get_llm(temperature: float = None):
    """
    获取 LLM 实例的工厂函数
    """
    return init_chat_model(
        model=ModelConfig.LLM_MODEL_NAME,
        model_provider="openai",
        base_url=ModelConfig.LLM_BASE_URL,
        api_key=ModelConfig.LLM_API_KEY,
        temperature=temperature or ModelConfig.LLM_TEMPERATURE
    )
