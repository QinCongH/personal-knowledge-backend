from langchain.tools import tool

@tool
def get_weather(city):
    """根据城市获取天气"""
    return f"明天{city}，天气是雨天"