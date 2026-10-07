# agent/rag/vector.py
import sys
import os

# 确保 agent/ 目录在 sys.path（models/tools/memory 等都在 agent 包下）
_agent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _agent_dir not in sys.path:
    sys.path.insert(0, _agent_dir)

from langchain_unstructured import UnstructuredLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_chroma import Chroma
from dotenv import load_dotenv
from models import get_model

load_dotenv()


class VectorRAG:
    """基于 Chroma 的向量检索 RAG"""

    minerU_loader = None
    unstructured_loader = None

    def __init__(self, persist_directory: str = None):
        """
        初始化 VectorRAG

        Args:
            persist_directory: Chroma 向量库持久化目录
        """
        self.persist_directory = persist_directory or os.getenv(
            "CHROMA_PERSIST_DIR", "./db/chroma_langchain_db"
        )
        self.collection_name = os.getenv("CHROMA_COLLECTION_NAME", "default_collection")
        self._vectorstore = None

    @property
    def vectorstore(self) -> Chroma:
        """延迟初始化 Chroma 向量库"""
        if self._vectorstore is None:
            self._vectorstore = Chroma(
                collection_name=self.collection_name,
                embedding_function=get_model("embedding"),
                persist_directory=self.persist_directory,
            )
        return self._vectorstore

    # 文档加载
    @staticmethod
    def load_unstructured_loader(file_path):
        unstructured_loader = UnstructuredLoader(file_path=file_path, strategy="fast")
        docs = unstructured_loader.load()
        print(f"加载了 {len(docs)} 个文档")
        return docs

    # 文档切分
    @staticmethod
    def doc_split(docs, filename):
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=100,
            chunk_overlap=0,
        )
        # 切分文档
        chunks = text_splitter.split_documents(docs)
        print(f"原始文本长度: {len(docs)} 字符")
        print(f"切分为 {len(chunks)} 个块:\n")
        # 给文档生成id
        ids = []
        for i, c in enumerate(chunks):
            c.id = f"doc_{i + 1}"
            c.metadata['id'] = c.id
            c.metadata["filename"] = filename
            ids.append(c.id)
        return chunks, ids

    # ==================== Chroma 向量库操作 ====================

    def add_documents(self, documents: list[Document], ids: list[str] = None):
        """
        向向量库添加文档

        Args:
            documents: Document 对象列表
            ids: 可选的文档 ID 列表
        """
        self.vectorstore.delete(ids)
        self.vectorstore.add_documents(documents, ids=ids)
        print(f"成功添加 {len(documents)} 个文档到向量库")

    def save_to_vectorstore(self, documents: list[Document], ids: list[str] = None):
        """
        将切分后的文档存入向量库（持久化）

        Args:
            documents: Document 对象列表
            ids: 可选的文档 ID 列表
        """
        self.add_documents(documents, ids=ids)
        print(f"向量库已保存至: {self.persist_directory}")

    def similarity_search(self, query: str, top_k: int = 5) -> list[Document]:
        """
        相似度检索

        Args:
            query: 查询文本
            top_k: 返回几条相关内容

        Returns:
            相关文档列表
        """
        return self.vectorstore.similarity_search(query, k=top_k)

    def similarity_search_with_score(self, query: str, top_k: int = 5) -> list:
        """
        带相似度分数的检索

        Returns:
            [(Document, score), ...]
        """
        return self.vectorstore.similarity_search_with_score(query, k=top_k)

    def as_retriever(self, top_k: int = 5):
        """
        获取 LangChain Retriever，可直接挂载到 Agent

        Returns:
            Chroma Retriever
        """
        return self.vectorstore.as_retriever(search_kwargs={"k": top_k})

    def delete_collection(self):
        """删除整个向量库集合"""
        self.vectorstore.delete_collection()
        self._vectorstore = None
        print(f"已删除集合: {self.collection_name}")

    def get_collection_count(self) -> int:
        """获取当前集合中的文档数量"""
        return self.vectorstore._collection.count()


if __name__ == "__main__":
    vector = VectorRAG(persist_directory="./db/chroma_langchain_db")

    def get_knowledge_url():
        current_path = os.path.dirname(__file__)
        BASE_DIR = os.path.dirname(os.path.dirname(current_path))
        DB_DIR = os.path.join(BASE_DIR, "knowledge_base", "md")
        url = os.path.join(DB_DIR, "html常用技巧.txt")
        print(url)
        return url

    docs1 = vector.load_unstructured_loader(get_knowledge_url())
    chunks, ids = vector.doc_split(docs=docs1, filename="html常用技巧.txt")
    vector.save_to_vectorstore(chunks, ids=ids)
    # 检索
    results = vector.similarity_search("元素等比例缩放", top_k=3)
    for i, doc in enumerate(results):
        print(f"结果 {i + 1}: {doc.page_content}")
        print(f"  元数据: {doc.metadata}")
    # 作为 Retriever 挂载到 Agent
    retriever = vector.as_retriever(top_k=5)


"""
VectorRAG使用示例：
from agent.rag import VectorRAG

# 初始化（自动读取 env 或使用默认路径）
rag = VectorRAG(persist_directory="./db/chroma_langchain_db")

# 加载、切分、存入向量库
docs = VectorRAG.load_unstructured_loader("知识库文件路径")
chunks = VectorRAG.doc_split(docs, filename="example.txt")
rag.save_to_vectorstore(chunks, ids=chunks)

# 检索
results = rag.similarity_search("如何实现弹性布局？", top_k=3)
for doc in results:
    print(doc.page_content)

# 作为 Retriever 挂载到 Agent
retriever = rag.as_retriever(top_k=5)
"""