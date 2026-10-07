# agent/rag/base.py
from abc import ABC, abstractmethod
from typing import List


class BaseRAG(ABC):
    """RAG 策略的基类"""

    @abstractmethod
    def retrieve(self, query: str, top_k: int = 5) -> List[str]:
        """
        根据问题检索相关文档片段

        Args:
            query: 用户的问题
            top_k: 返回几条相关内容

        Returns:
            包含文档内容的字符串列表
        """
        pass

    @abstractmethod
    def to_tool(self):
        """
        将 RAG 策略转换为 LangChain Tool 对象
        这样就可以直接挂载到 Agent 上
        """
        pass
