"""
Agent 示例：一个能自主规划和执行任务的智能体
运行: python 04_agent.py
"""
from openai import OpenAI
import json
import os
import re

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class SimpleAgent:
    """简单的智能体实现"""
    
    def __init__(self, name: str, system_prompt: str, tools: list, tool_handlers: dict):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools
        self.tool_handlers = tool_handlers
        self.max_iterations = 5
        self.conversation_history = []
    
    def run(self, user_goal: str) -> str:
        """
        Agent 主循环:
        1. 理解目标
        2. 决定使用哪些工具
        3. 执行并检查结果
        4. 必要时迭代
        """
        print(f"\n🤖 {self.name} 开始处理任务: {user_goal}\n")
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": user_goal}
        ]
        
        for iteration in range(self.max_iterations):
            print(f"--- 第 {iteration + 1} 轮思考 ---")
            
            # LLM 决策
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            # 如果不需要工具，任务完成
            if not message.tool_calls:
                print("✅ 任务完成！\n")
                return message.content
            
            # 执行工具调用
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"   🔧 调用: {func_name}({args})")
                
                if func_name in self.tool_handlers:
                    result = self.tool_handlers[func_name](**args)
                else:
                    result = {"error": f"未知工具: {func_name}"}
                
                print(f"   📊 结果: {result}")
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
        
        return "⚠️ 达到最大迭代次数，任务可能未完成"

# 定义工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "搜索网络获取信息",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "搜索关键词"}
                },
                "required": ["query"]
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
    },
    {
        "type": "function",
        "function": {
            "name": "save_note",
            "description": "保存笔记到文件",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string", "description": "笔记标题"},
                    "content": {"type": "string", "description": "笔记内容"}
                },
                "required": ["title", "content"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "send_email",
            "description": "发送邮件",
            "parameters": {
                "type": "object",
                "properties": {
                    "to": {"type": "string", "description": "收件人邮箱"},
                    "subject": {"type": "string", "description": "邮件主题"},
                    "body": {"type": "string", "description": "邮件内容"}
                },
                "required": ["to", "subject", "body"]
            }
        }
    }
]

# 工具实现
def search_web(query: str) -> dict:
    """模拟搜索"""
    mock_data = {
        "Python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建。特点是语法简洁、易学易用。",
        "AI": "人工智能（Artificial Intelligence）是计算机科学的一个分支，致力于创造能模拟人类智能的系统。",
        "OpenClaw": "OpenClaw 是一个开源的 AI Agent 框架，支持多渠道接入、技能系统、MCP 协议。",
        "天气": "无法获取实时天气数据，请使用天气预报应用。"
    }
    for key in mock_data:
        if key.lower() in query.lower():
            return {"result": mock_data[key]}
    return {"result": "未找到相关信息，建议使用搜索引擎。"}

def calculate(expression: str) -> dict:
    """执行计算"""
    try:
        if re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
            return {"result": str(eval(expression))}
        return {"error": "无效表达式"}
    except Exception as e:
        return {"error": str(e)}

def save_note(title: str, content: str) -> dict:
    """模拟保存笔记"""
    print(f"   📝 正在保存笔记 '{title}'...")
    return {"status": "success", "message": f"笔记 '{title}' 已保存"}

def send_email(to: str, subject: str, body: str) -> dict:
    """模拟发送邮件"""
    print(f"   📧 正在发送邮件到 {to}...")
    return {"status": "success", "message": f"邮件已发送到 {to}"}

# 创建 Agent
agent = SimpleAgent(
    name="智能助手",
    system_prompt="""你是一个智能助手，可以自主决定使用工具来完成任务。
你可以使用以下工具：
- search_web: 搜索信息
- calculate: 数学计算
- save_note: 保存笔记
- send_email: 发送邮件

请根据用户目标，自主规划并执行任务。完成后给出清晰的总结。""",
    tools=tools,
    tool_handlers={
        "search_web": search_web,
        "calculate": calculate,
        "save_note": save_note,
        "send_email": send_email
    }
)

if __name__ == "__main__":
    # 测试 Agent
    tasks = [
        "帮我查一下 Python 是什么，然后把结果保存成笔记",
        "计算 (100 + 200) * 3，然后把结果发邮件给 test@example.com"
    ]
    
    for task in tasks:
        print("=" * 60)
        result = agent.run(task)
        print(f"最终结果:\n{result}\n")
