import os
from langchain.agents import create_agent
from  langchain.messages import HumanMessage
from tools.base import BaseTools
from tools.default_tools import DefaultTools
from prompts.system import DEFAULT_SYSTEM_PROMPT
from models import get_model
from memory.checkpoint import get_checkpoint
class BaseAgent(object):
    model=None
    agent=None
    checkpointer=None
    base_tool=BaseTools()
    system_prompt=DEFAULT_SYSTEM_PROMPT
    def __init__(self, tools: BaseTools = None):
        self.model = get_model("llm")
        # 创建记忆
            # 初始化checkpointer
        self.checkpointer = get_checkpoint()
        # 如果外部没传工具集，就用默认的；如果传了就用外部传的（方便以后扩展）
        self.tool_manager = tools if tools else DefaultTools()

    # 创建agent
    def create_agent(self):
        agent = create_agent(
            model=self.model,
            system_prompt=self.system_prompt,
            tools=self.tool_manager.get_tools(),
            checkpointer=self.checkpointer
        )
        return agent

    # 测试agent输出
    def test_agent(self,message):
        agent = self.create_agent()
        config = {
            "configurable": {
                "thread_id": "thread-001",
                "checkpoint_ns": "research_subgraph"  # 子图的独立 checkpoint 空间
            }
        }
        res = agent.invoke({
            "messages": [
                HumanMessage(message)
            ],
        },config=config)
        for msg in res['messages']:
            msg.pretty_print()
        return res

if __name__ == '__main__':
    agent_init = BaseAgent()
    agent_init.test_agent("北京明天天气怎么样")