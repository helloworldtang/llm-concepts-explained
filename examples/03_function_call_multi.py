"""
Function Call 示例 - 支持 DeepSeek / 通义千问
运行方式: python 03_function_call_multi.py

注意：DeepSeek 和通义千问都支持 Function Call（与 OpenAI 兼容）

设置环境变量：
  DeepSeek: export DEEPSEEK_API_KEY='sk-xxxxxxxx'
  通义千问: export DASHSCOPE_API_KEY='sk-xxxxxxxx'
"""
from openai import OpenAI
import json
import os

# ==================== 配置区 ====================
PROVIDER = "deepseek"  # "deepseek" | "qwen"

API_KEYS = {
    "deepseek": os.getenv("DEEPSEEK_API_KEY", ""),
    "qwen": os.getenv("DASHSCOPE_API_KEY", ""),
}

MODELS = {
    "deepseek": {
        "base_url": "https://api.deepseek.com",
        "model": "deepseek-chat",
    },
    "qwen": {
        "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "model": "qwen-turbo",
    },
}
# ================================================

def get_client(provider: str) -> OpenAI:
    api_key = API_KEYS.get(provider, "")
    if not api_key:
        print(f"❌ 请设置 {provider.upper()}_API_KEY")
        if provider == "deepseek":
            print("   获取: https://platform.deepseek.com/api_keys")
            print("   设置: export DEEPSEEK_API_KEY='sk-xxx'")
        else:
            print("   获取: https://dashscope.console.aliyun.com/apiKey")
            print("   设置: export DASHSCOPE_API_KEY='sk-xxx'")
        exit(1)
    return OpenAI(api_key=api_key, base_url=MODELS[provider]["base_url"])

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取城市天气信息",
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

def get_weather(city: str) -> dict:
    """模拟天气 API"""
    data = {
        "北京": {"temp": 15, "condition": "晴"},
        "上海": {"temp": 18, "condition": "多云"},
        "广州": {"temp": 25, "condition": "晴"},
    }
    return data.get(city, {"error": "未找到该城市"})

def chat_with_tools(question: str) -> str:
    print(f"\n📥 问题: {question}")
    
    client = get_client(PROVIDER)
    model = MODELS[PROVIDER]["model"]
    print(f"🔧 模型: {PROVIDER}/{model}")
    
    # 第一次调用
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": question}],
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        func_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        print(f"🔧 调用函数: {func_name}({args})")
        
        result = get_weather(args["city"])
        print(f"📊 返回结果: {result}")
        
        # 第二次调用
        response = client.chat.completions.create(
            model=model,
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
