"""
概念关系对比演示
运行: python 06_comparison.py

展示 LLM → Workflow → Function Call → Agent 的能力差异
"""
from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== 1. 纯 LLM =====
def pure_llm(question: str) -> str:
    """纯 LLM：只能基于训练数据回答"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message.content

# ===== 2. Workflow =====
def workflow_approach(question: str) -> str:
    """Workflow：固定流程处理"""
    # 固定步骤1：分类
    classify_prompt = f"这个问题属于什么类型？（天气/计算/其他）：{question}"
    category = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": classify_prompt}]
    ).choices[0].message.content
    
    # 固定步骤2：路由
    if "计算" in category:
        return "走计算流程..."
    elif "天气" in category:
        return "❌ Workflow 无法获取实时天气"
    else:
        return pure_llm(question)

# ===== 3. Function Call =====
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "获取天气",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}]

def function_call_approach(question: str) -> str:
    """Function Call：可以调用外部函数"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}],
        tools=tools,
        tool_choice="auto"
    )
    
    message = response.choices[0].message
    
    if message.tool_calls:
        # 执行函数
        tool_call = message.tool_calls[0]
        args = json.loads(tool_call.function.arguments)
        
        # 模拟天气 API
        weather_data = {"北京": "晴，15°C", "上海": "多云，18°C"}
        result = weather_data.get(args.get("city"), "未找到城市")
        
        # 返回结果给 LLM
        messages = [
            {"role": "user", "content": question},
            message,
            {"role": "tool", "tool_call_id": tool_call.id, "content": result}
        ]
        
        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return final.choices[0].message.content
    
    return message.content

# ===== 4. Agent =====
def agent_approach(question: str) -> str:
    """Agent：自主规划执行"""
    system_prompt = """你是一个智能助手。你可以：
1. 判断是否需要工具
2. 自主决定使用什么工具
3. 验证结果并迭代

如果用户问天气，请调用 get_weather 函数。"""
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question}
    ]
    
    # Agent 循环
    for _ in range(3):
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        messages.append(message)
        
        if not message.tool_calls:
            return message.content
        
        for tool_call in message.tool_calls:
            args = json.loads(tool_call.function.arguments)
            weather_data = {"北京": "晴，15°C", "上海": "多云，18°C"}
            result = weather_data.get(args.get("city"), "未找到")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })

# ===== 对比演示 =====
if __name__ == "__main__":
    question = "北京今天天气怎么样？"
    
    print("=" * 60)
    print(f"问题: {question}\n")
    
    print("1️⃣ 纯 LLM (无外部能力):")
    print(f"   {pure_llm(question)[:100]}...\n")
    
    print("2️⃣ Workflow (固定流程):")
    print(f"   {workflow_approach(question)[:100]}...\n")
    
    print("3️⃣ Function Call (可调用函数):")
    print(f"   {function_call_approach(question)[:100]}...\n")
    
    print("4️⃣ Agent (自主规划):")
    print(f"   {agent_approach(question)[:100]}...\n")
    
    print("=" * 60)
    print("""
能力对比:
┌─────────────────┬────────┬────────┬────────┐
│                 │ 纯 LLM │ Func   │ Agent  │
├─────────────────┼────────┼────────┼────────┤
│ 获取实时数据     │   ❌   │   ✅   │   ✅   │
│ 自主决策         │   ❌   │   ❌   │   ✅   │
│ 多步任务         │   ❌   │   ⚠️   │   ✅   │
│ 错误自愈         │   ❌   │   ❌   │   ✅   │
└─────────────────┴────────┴────────┴────────┘
""")
