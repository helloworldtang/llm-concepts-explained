"""
Agent 示例 - 支持 DeepSeek / 通义千问
运行方式: python 04_agent_multi.py

DeepSeek 和通义千问都支持 Function Call，可以用来构建 Agent

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
        exit(1)
    return OpenClient(api_key=api_key, base_url=MODELS[provider]["base_url"]) if False else OpenAI(api_key=api_key, base_url=MODELS[provider]["base_url"])

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

def search_web(query: str) -> dict:
    """模拟搜索"""
    data = {
        "Python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。",
        "DeepSeek": "DeepSeek 是国产大模型，支持 Function Call，性价比高。",
        "AI": "人工智能是计算机科学的一个分支。",
    }
    for key in data:
        if key.lower() in query.lower():
            return {"result": data[key]}
    return {"result": "未找到相关信息"}

def save_note(title: str, content: str) -> dict:
    print(f"   📝 保存笔记: {title}")
    return {"status": "success", "message": f"笔记 '{title}' 已保存"}

tool_handlers = {"search_web": search_web, "save_note": save_note}

def run_agent(goal: str) -> str:
    print(f"🤖 Agent 开始处理: {goal}\n")
    print(f"🔧 模型: {PROVIDER}/{MODELS[PROVIDER]['model']}\n")
    
    client = get_client(PROVIDER)
    model = MODELS[PROVIDER]["model"]
    
    messages = [
        {"role": "system", "content": "你是一个智能助手。根据用户目标，自主决定使用工具完成任务。"},
        {"role": "user", "content": goal}
    ]
    
    for i in range(3):
        print(f"--- 第 {i+1} 轮 ---")
        
        response = client.chat.completions.create(
            model=model,
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
