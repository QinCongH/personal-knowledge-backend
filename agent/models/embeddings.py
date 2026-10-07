# agent/models/embeddings.py
from langchain_ollama import OllamaEmbeddings
from .config import ModelConfig


def get_embeddings():
    """
    获取 Ollama Embedding 实例的工厂函数
    用于将文本转换为向量，存入向量数据库
    """
    return OllamaEmbeddings(
        model=ModelConfig.EMBEDDING_MODEL_NAME,
        base_url=ModelConfig.OLLAMA_BASE_URL,
        dimensions=ModelConfig.EMBEDDING_DIMENSIONS
    )
