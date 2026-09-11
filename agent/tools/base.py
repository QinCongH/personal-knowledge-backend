# agent/tools/base.py
from typing import List
from langchain_core.tools import BaseTool

class BaseTools:
    """
    工具集基类。
    所有的工具集合都应该继承这个类，并重写 get_tools 方法。
    """
    def __init__(self):
        pass

    def get_tools(self) -> List[BaseTool]:
        """
        返回该工具集中的所有工具列表。
        默认返回空列表，子类自行覆盖。
        """
        return []
