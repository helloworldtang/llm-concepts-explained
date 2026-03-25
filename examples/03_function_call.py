"""
Function Call 示例：让 LLM 能查天气、算汇率
运行: python 03_function_call.py
"""
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 定义可用工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "获取指定城市的天气信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如：北京、上海"
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_exchange_rate",
            "description": "获取货币汇率",
            "parameters": {
                "type": "object",
                "properties": {
                    "from_currency": {"type": "string", "description": "源货币代码，如 USD"},
                    "to_currency": {"type": "string", "description": "目标货币代码，如 CNY"}
                },
                "required": ["from_currency", "to_currency"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "执行数学计算",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                },
                "required": ["expression"]
            }
        }
    }
]

# 实际函数实现
def get_weather(city: str) -> dict:
    """模拟天气 API"""
    weather_data = {
        "北京": {"temp": 15, "condition": "晴", "humidity": 30},
        "上海": {"temp": 18, "condition": "多云", "humidity": 60},
        "广州": {"temp": 25, "condition": "晴", "humidity": 70},
    }
    return weather_data.get(city, {"error": "未找到该城市"})

def get_exchange_rate(from_currency: str, to_currency: str) -> dict:
    """模拟汇率 API"""
    rates = {
        "USD_CNY": 7.2,
        "EUR_CNY": 7.8,
        "JPY_CNY": 0.048,
        "GBP_CNY": 9.1
    }
    key = f"{from_currency}_{to_currency}"
    if key in rates:
        return {"rate": rates[key]}
    return {"error": f"不支持 {from_currency} 到 {to_currency} 的汇率"}

def calculate(expression: str) -> dict:
    """执行计算"""
    try:
        import re
        if re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
            return {"result": eval(expression)}
        return {"error": "无效表达式"}
    except Exception as e:
        return {"error": str(e)}

# 函数映射
tool_handlers = {
    "get_weather": get_weather,
    "get_exchange_rate": get_exchange_rate,
    "calculate": calculate
}

def run_with_function_call(user_message: str) -> str:
    """带 Function Call 的对话"""
    messages = [{"role": "user", "content": user_message}]
    
    # 第一次调用：LLM 决定是否需要调用函数
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    # 如果 LLM 决定调用函数
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)
        
        print(f"🔧 LLM 决定调用: {function_name}({arguments})")
        
        # 执行函数
        handler = tool_handlers.get(function_name)
        if handler:
            result = handler(**arguments)
        else:
            result = {"error": "未知函数"}
        
        print(f"📊 函数返回: {result}")
        
        # 将结果发回 LLM
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
        })
        
        # 第二次调用：LLM 基于结果生成最终回答
        final_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    # 如果不需要调用函数
    return message.content

if __name__ == "__main__":
    # 测试不同场景
    questions = [
        "北京今天天气怎么样？",
        "100美元能换多少人民币？",
        "计算 123 * 456",
        "你好，介绍一下 Python"
    ]
    
    for q in questions:
        print(f"\n{'='*50}")
        print(f"📥 问题: {q}")
        answer = run_with_function_call(q)
        print(f"📤 回答: {answer}")
