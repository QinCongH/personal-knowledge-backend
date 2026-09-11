# # agent/model/embeddings.py
# from langchain.embeddings import OpenAIEmbeddings
# from .config import ModelConfig
#
# def get_embeddings():
#     """
#     获取 Embedding 实例的工厂函数
#     用于将文本转换为向量，存入向量数据库
#     """
#     return OpenAIEmbeddings(
#         model=ModelConfig.EMBEDDING_MODEL_NAME,
#         openai_api_key=ModelConfig.EMBEDDING_API_KEY,
#         openai_api_base=ModelConfig.EMBEDDING_BASE_URL
#     )
