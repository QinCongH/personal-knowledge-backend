# agent/rag/factory.py
import os
from dotenv import load_dotenv
load_dotenv()

from .base import BaseRAG
from .vector import VectorRAG


def get_rag_strategy(config: dict) -> BaseRAG:
    """
    根据配置获取 RAG 实例
    """
    rag_type = config.get("RAG_TYPE", "vector")  # 默认用向量检索

    if rag_type == "vector":
        # 从配置或环境变量获取向量库路径
        persist_directory = config.get(
            "VECTOR_DB_PATH",
            os.getenv("CHROMA_PERSIST_DIR", "./db/chroma_langchain_db")
        )
        return VectorRAG(persist_directory=persist_directory)

    elif rag_type == "hybrid":
        # return HybridRAG(...)
        pass

    else:
        raise ValueError(f"未知的 RAG 类型: {rag_type}")
