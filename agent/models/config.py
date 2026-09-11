import os
from dotenv import load_dotenv
load_dotenv()
class ModelConfig:
    """模型配置类"""
    # LLM 配置
    LLM_MODEL_NAME = os.getenv("AUTO_MODEL_NAME", "glm-5.2") # 建议在 .env 里配置，这里给个默认值
    LLM_API_KEY = os.getenv("AUTO_API_KEY")
    LLM_BASE_URL = os.getenv("AUTO_BASE_URL")
    LLM_TEMPERATURE = 0.7

    # Embedding 配置 (知识库必备)
    # 通常 Embedding API Key 和 LLM 的是通用的，但模型名不同
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "embedding-2")
    EMBEDDING_API_KEY = os.getenv("AUTO_API_KEY")
    EMBEDDING_BASE_URL = os.getenv("AUTO_BASE_URL")