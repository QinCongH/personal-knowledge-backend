# agent/models/factory.py
import os
from dotenv import load_dotenv
load_dotenv()

from .llm import get_llm
from .embeddings import get_embeddings


def get_model(model_type: str = None, **kwargs):
    """
    根据模型类型统一获取模型实例的工厂函数

    Args:
        model_type: 模型类型，支持 "llm" / "embedding"
                    不传则从环境变量 MODEL_TYPE 读取，默认 "llm"
        **kwargs: 透传给具体工厂函数的参数（如 temperature 等）

    Returns:
        LLM 实例 或 Embeddings 实例
    """
    model_type = (model_type or os.getenv("MODEL_TYPE", "llm")).lower()

    if model_type in ("llm", "chat"):
        temperature = kwargs.pop("temperature", None)
        return get_llm(temperature=temperature)

    elif model_type in ("embedding", "embeddings", "vector"):
        return get_embeddings()

    else:
        raise ValueError(f"未知的模型类型: {model_type}（支持 llm / embedding）")