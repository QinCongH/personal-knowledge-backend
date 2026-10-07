import os
from dotenv import load_dotenv
load_dotenv()


class ModelConfig:
    """模型配置类"""

    # LLM 配置
    LLM_MODEL_NAME = os.getenv("AUTO_MODEL_NAME", "glm-5.2")
    LLM_API_KEY = os.getenv("AUTO_API_KEY")
    LLM_BASE_URL = os.getenv("AUTO_BASE_URL")
    LLM_TEMPERATURE = 0.7

    # Embedding 配置（知识库必备）
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "qwen3-embedding:0.6b")
    EMBEDDING_API_KEY = os.getenv("AUTO_API_KEY")
    EMBEDDING_BASE_URL = os.getenv("AUTO_BASE_URL")
    EMBEDDING_DIMENSIONS = int(os.getenv("EMBEDDING_DIMENSIONS", 1024))

    # Ollama 独立配置（Embedding 专用）
    OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
