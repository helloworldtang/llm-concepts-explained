"""
Agent 示例 - 简化版
运行方式: python 04_agent_simple.py

使用前请设置环境变量: export OPENAI_API_KEY='sk-xxxxxxxx'
"""
from openai import OpenAI
import json
import os

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ 请先设置 OPENAI_API_KEY 环境变量")
    exit(1)

client = OpenAI(api_key=api_key)

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索网络获取信息",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string", "description": "搜索关键词"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "保存笔记",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "标题"},
                    "content": {"type": "string", "description": "内容"}
                },
                "required": ["title", "content"]
            }
        }
    }
]

# 工具实现
def search_web(query: str) -> dict:
    """模拟搜索"""
    data = {
        "Python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
        "AI": "人工智能是计算机科学的一个分支。",
    }
    for key in data:
        if key.lower() in query.lower():
            return {"result": data[key]}
    return {"result": "未找到相关信息"}

def save_note(title: str, content: str) -> dict:
    """模拟保存笔记"""
    print(f"   📝 保存笔记: {title}")
    return {"status": "success"}

tool_handlers = {"search_web": search_web, "save_note": save_note}

def run_agent(goal: str) -> str:
    """Agent 主循环"""
    print(f"🤖 Agent 开始处理: {goal}\n")
    
    messages = [
        {"role": "system", "content": "你是一个智能助手。根据用户目标，自主决定使用工具。"},
        {"role": "user", "content": goal}
    ]
    
    for i in range(3):  # 最多3轮
        print(f"--- 第 {i+1} 轮 ---")
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        if not message.tool_calls:
            print("✅ 任务完成！\n")
            return message.content
        
        for tool_call in message.tool_calls:
            func_name = tool_call.function.name
            args = json.loads(tool_call.function.arguments)
            print(f"   🔧 调用: {func_name}({args})")
            
            result = tool_handlers.get(func_name, lambda **kw: {"error": "未知函数"})(**args)
            print(f"   📊 结果: {result}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result, ensure_ascii=False)
            })
    
    return "⚠️ 达到最大迭代次数"

if __name__ == "__main__":
    result = run_agent("帮我查一下 Python 是什么，然后保存成笔记")
    print(f"最终结果:\n{result}")
