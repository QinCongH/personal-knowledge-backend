# agent/tools/default_tools.py
from tools.base import BaseTools
# 导入你具体的工具
from tools.get_weather import get_weather
# 将来你可以导入更多，比如 search_kb

class DefaultTools(BaseTools):
    def __init__(self):
        super().__init__()
    def get_tools(self):
        return [
            get_weather,
            # future: search_knowledge_tool
        ]
