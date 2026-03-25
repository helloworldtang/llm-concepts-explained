"""
Function Call 示例 - 简化版
运行方式: python 03_function_call_simple.py

使用前请设置环境变量: export OPENAI_API_KEY='sk-xxxxxxxx'
"""
from openai import OpenAI
import json
import os

# 检查 API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ 请先设置 OPENAI_API_KEY 环境变量")
    print("   export OPENAI_API_KEY='sk-xxxxxxxx'")
    exit(1)

client = OpenAI(api_key=api_key)

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                },
                "required": ["city"]
            }
        }
    }
]

# 模拟天气函数
def get_weather(city: str) -> dict:
    """模拟天气 API（实际项目中会调用真实 API）"""
    mock_data = {
        "北京": {"temp": 15, "condition": "晴"},
        "上海": {"temp": 18, "condition": "多云"},
        "广州": {"temp": 25, "condition": "晴"},
    }
    return mock_data.get(city, {"error": "未找到该城市"})

def chat_with_tools(question: str) -> str:
    """带工具调用的对话"""
    print(f"\n📥 问题: {question}")
    
    # 第一次调用
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # 如果需要调用工具
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        print(f"🔧 LLM 决定调用: {func_name}({args})")
        
        # 执行函数
        if func_name == "get_weather":
            result = get_weather(args["city"])
        else:
            result = {"error": "未知函数"}
        
        print(f"📊 函数返回: {result}")
        
        # 将结果发回 LLM
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": question},
                message,
                {"role": "tool", "tool_call_id": tool_call.id, "content": json.dumps(result, ensure_ascii=False)}
            ]
        )
        return response.choices[0].message.content
    
    return message.content

if __name__ == "__main__":
    print("=" * 50)
    answer = chat_with_tools("北京今天天气怎么样？")
    print(f"\n📤 回答: {answer}")
