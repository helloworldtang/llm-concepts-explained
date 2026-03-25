# LLM、Workflow、Function Call、MCP、Skill、Agent、OpenClaw 完全指南

## 开篇：一个类比

想象你在经营一家餐厅：

| 概念 | 类比 |
|------|------|
| **LLM** | 厨师的大脑 - 懂得如何做菜，但没有具体的食材和工具 |
| **Workflow** | 菜谱流程 - 先洗菜、再切菜、再炒菜的固定步骤 |
| **Function Call** | 厨师喊"拿盐" - 调用外部工具获取数据或执行操作 |
| **MCP** | 统一的厨房工具接口 - 所有工具用同样的方式连接 |
| **Skill** | 拿手菜谱 - 做红烧肉的一整套技能包 |
| **Agent** | 整个厨师 - 大脑+双手+工具，能自主完成复杂任务 |
| **OpenClaw** | 智能餐厅系统 - 多个厨师协作，还能接外卖订单 |

---

## 一、LLM（大语言模型）

### 是什么
LLM（Large Language Model）是整个 AI 应用的"大脑"。它通过海量文本训练，学会了理解和生成人类语言。

### 核心能力
- **理解**：解析用户意图
- **推理**：逻辑分析和决策
- **生成**：输出文本回复

### 最简单的例子

```python
# examples/01_llm_basics.py
"""
LLM 基础示例：一个只会"说话"的模型
"""
from openai import OpenAI

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "今天北京天气怎么样？"}
    ]
)

print(response.choices[0].message.content)
# 输出：抱歉，我无法获取实时天气信息。建议您查看天气预报...
```

### 局限性
- ❌ 无法访问实时数据（天气、股价）
- ❌ 无法执行操作（发邮件、查数据库）
- ❌ 知识有截止日期
- ❌ 不会"记住"上一次对话

---

## 二、Workflow（工作流）

### 是什么
Workflow 是**预定义的任务执行流程**。就像一条流水线，每一步都按固定规则执行。

### 特点
- 确定性：同样的输入必定得到同样的输出
- 可预测：每个步骤都明确知道做什么
- 易调试：出问题容易定位

### 代码示例

```python
# examples/02_workflow.py
"""
Workflow 示例：一个固定流程的问答系统
"""
from openai import OpenAI

client = OpenAI()

def qa_workflow(question: str) -> str:
    """
    一个简单的问答工作流：
    1. 分析问题类型
    2. 根据类型选择处理方式
    3. 生成答案
    """
    # 步骤1：分析问题类型
    classify_prompt = f"""
    分析以下问题属于哪个类别，只回答一个词：
    - 天气
    - 计算
    - 常识
    - 其他
    
    问题：{question}
    """
    
    category = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": classify_prompt}]
    ).choices[0].message.content.strip()
    
    print(f"🔍 问题类别: {category}")
    
    # 步骤2：根据类别处理
    if category == "计算":
        # 计算类问题：让 LLM 直接计算
        answer = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"计算并回答：{question}"}]
        ).choices[0].message.content
    elif category == "天气":
        # 天气类问题：提示无法获取实时数据
        answer = "抱歉，我无法获取实时天气数据。请查看天气预报应用。"
    else:
        # 其他问题：正常回答
        answer = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        ).choices[0].message.content
    
    return answer

# 测试
print(qa_workflow("123 * 456 等于多少？"))
print("---")
print(qa_workflow("Python 是什么？"))
```

### Workflow 的优缺点
| 优点 | 缺点 |
|------|------|
| 流程清晰可控 | 灵活性差 |
| 易于调试和优化 | 无法处理意外情况 |
| 性能可预测 | 需要人工设计所有分支 |

---

## 三、Function Call（函数调用）

### 是什么
Function Call 让 LLM 能够**调用外部函数**获取数据或执行操作。这是 LLM 从"只会说话"变成"能干实事"的关键。

### 工作原理
```
用户问题 → LLM 判断需要调用函数 → 返回函数名和参数 → 执行函数 → 结果返回 LLM → 生成最终回答
```

### 代码示例

```python
# examples/03_function_call.py
"""
Function Call 示例：让 LLM 能查天气、算汇率
"""
from openai import OpenAI
import json

client = OpenAI()

# 定义可用函数
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
    }
]

# 实际函数实现
def get_weather(city: str) -> dict:
    """模拟天气 API"""
    # 实际项目中这里会调用真实 API
    weather_data = {
        "北京": {"temp": 15, "condition": "晴", "humidity": 30},
        "上海": {"temp": 18, "condition": "多云", "humidity": 60},
    }
    return weather_data.get(city, {"error": "未找到该城市"})

def get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """模拟汇率 API"""
    rates = {"USD_CNY": 7.2, "EUR_CNY": 7.8, "JPY_CNY": 0.048}
    return rates.get(f"{from_currency}_{to_currency}", 0)

def run_with_function_call(user_message: str) -> str:
    """带 Function Call 的对话"""
    messages = [{"role": "user", "content": user_message}]
    
    # 第一次调用：LLM 决定是否需要调用函数
    response = client.chat.completions.create(
        model="gpt-4",
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
        
        print(f"🔧 LLM 决定调用函数: {function_name}({arguments})")
        
        # 执行函数
        if function_name == "get_weather":
            result = get_weather(arguments["city"])
        elif function_name == "get_exchange_rate":
            result = get_exchange_rate(
                arguments["from_currency"],
                arguments["to_currency"]
            )
        else:
            result = {"error": "未知函数"}
        
        print(f"📊 函数返回结果: {result}")
        
        # 将结果发回 LLM
        messages.append(message)
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result, ensure_ascii=False)
        })
        
        # 第二次调用：LLM 基于函数结果生成最终回答
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    # 如果不需要调用函数，直接返回回答
    return message.content

# 测试
print(run_with_function_call("北京今天天气怎么样？"))
print("\n" + "="*50 + "\n")
print(run_with_function_call("100美元能换多少人民币？"))
```

### Function Call 的本质
```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   用户问题   │ ──→ │     LLM     │ ──→ │  决定调函数  │
└─────────────┘     └─────────────┘     └─────────────┘
                                               │
                                               ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   最终回答   │ ←── │     LLM     │ ←── │  函数结果   │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## 四、MCP（Model Context Protocol）

### 是什么
MCP 是 **Anthropic 提出的统一协议**，让 AI 模型能够以标准方式连接各种外部工具和数据源。

### 为什么需要 MCP
Function Call 的问题：
- 每个 AI 平台定义函数的方式不同
- 工具无法跨平台复用
- 开发者要为每个平台写适配代码

MCP 的解决方案：
- **统一协议**：所有工具用同样的方式描述和调用
- **一次开发，到处运行**：同一个 MCP Server 可以被 Claude、ChatGPT 等复用

### MCP 架构

```
┌────────────────────────────────────────────────────┐
│                    AI 应用                          │
│  (Claude Desktop / ChatGPT / OpenClaw)             │
└─────────────────────┬──────────────────────────────┘
                      │ MCP 协议
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
   ┌─────────┐   ┌─────────┐   ┌─────────┐
   │ 文件系统 │   │ 数据库  │   │ 搜索引擎 │
   │ Server  │   │ Server  │   │ Server  │
   └─────────┘   └─────────┘   └─────────┘
```

### MCP Server 示例

```python
# examples/04_mcp_server.py
"""
MCP Server 示例：一个简单的文件读取服务
运行方式：mcp run server.py
"""
from mcp.server import Server
from mcp.types import Tool, TextContent
import os

app = Server("file-reader")

@app.list_tools()
async def list_tools():
    """声明可用工具"""
    return [
        Tool(
            name="read_file",
            description="读取文件内容",
            inputSchema={
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "文件路径"}
                },
                "required": ["path"]
            }
        ),
        Tool(
            name="list_files",
            description="列出目录下的文件",
            inputSchema={
                "type": "object",
                "properties": {
                    "directory": {"type": "string", "description": "目录路径"}
                },
                "required": ["directory"]
            }
        )
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """执行工具调用"""
    if name == "read_file":
        path = arguments["path"]
        try:
            with open(path, 'r') as f:
                content = f.read()
            return [TextContent(type="text", text=content)]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]
    
    elif name == "list_files":
        directory = arguments["directory"]
        try:
            files = os.listdir(directory)
            return [TextContent(type="text", text="\n".join(files))]
        except Exception as e:
            return [TextContent(type="text", text=f"错误: {str(e)}")]

if __name__ == "__main__":
    app.run()
```

### MCP vs Function Call

| 对比项 | Function Call | MCP |
|--------|---------------|-----|
| 标准化 | 各平台自定义 | 统一协议 |
| 复用性 | 仅限同一平台 | 跨平台复用 |
| 开发成本 | 每个平台写一份 | 一次开发多平台用 |
| 生态 | 各自发展 | 共享生态 |

---

## 五、Skill（技能）

### 是什么
Skill 是 **封装好的能力模块**，包含完成特定任务所需的所有资源：
- 提示词模板
- 工具定义
- 处理逻辑
- 配置参数

### 为什么需要 Skill
- **复用**：常见能力不用重复开发
- **标准化**：统一的能力描述方式
- **可组合**：多个 Skill 组合完成复杂任务

### Skill 示例

```python
# examples/05_skill.py
"""
Skill 示例：一个"天气助手"技能
"""
from dataclasses import dataclass
from typing import Callable, Any
import json

@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    parameters: dict
    handler: Callable

@dataclass
class Skill:
    """技能定义"""
    name: str
    description: str
    tools: list[Tool]
    prompt_template: str
    examples: list[str]

# 定义天气技能
weather_skill = Skill(
    name="weather-assistant",
    description="天气查询助手，可以查询任意城市的天气信息",
    
    tools=[
        Tool(
            name="get_weather",
            description="获取城市天气",
            parameters={
                "city": {"type": "string", "description": "城市名称"}
            },
            handler=lambda city: {
                "北京": {"temp": 15, "condition": "晴"},
                "上海": {"temp": 18, "condition": "多云"}
            }.get(city, {"error": "未找到城市"})
        ),
        Tool(
            name="get_forecast",
            description="获取未来3天天气预报",
            parameters={
                "city": {"type": "string", "description": "城市名称"}
            },
            handler=lambda city: [
                {"date": "明天", "temp": 16, "condition": "阴"},
                {"date": "后天", "temp": 14, "condition": "小雨"},
                {"date": "大后天", "temp": 17, "condition": "晴"}
            ]
        )
    ],
    
    prompt_template="""
你是一个专业的天气助手。当用户询问天气时：
1. 确认用户要查询的城市
2. 使用 get_weather 获取当前天气
3. 如果需要预报，使用 get_forecast
4. 用友好的语言回复用户

用户问题：{question}
""",
    
    examples=[
        "北京今天天气怎么样？",
        "上海未来三天会下雨吗？",
        "广州现在的温度是多少？"
    ]
)

# Skill 注册表
class SkillRegistry:
    """技能注册表"""
    def __init__(self):
        self.skills: dict[str, Skill] = {}
    
    def register(self, skill: Skill):
        self.skills[skill.name] = skill
    
    def get(self, name: str) -> Skill | None:
        return self.skills.get(name)
    
    def list_skills(self) -> list[str]:
        return list(self.skills.keys())

# 使用示例
registry = SkillRegistry()
registry.register(weather_skill)

print("可用技能:", registry.list_skills())
skill = registry.get("weather-assistant")
print(f"技能描述: {skill.description}")
print(f"包含工具: {[t.name for t in skill.tools]}")
```

### Skill 的层级关系

```
┌─────────────────────────────────────────┐
│              Agent (智能体)               │
│  ┌─────────────────────────────────┐    │
│  │         Skill (技能)             │    │
│  │  ┌───────────┐  ┌───────────┐   │    │
│  │  │ Tool 1    │  │ Tool 2    │   │    │
│  │  │(Function) │  │(MCP Tool) │   │    │
│  │  └───────────┘  └───────────┘   │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## 六、Agent（智能体）

### 是什么
Agent 是**能够自主规划、决策、执行任务的 AI 系统**。它不只是回答问题，而是：
- 理解目标
- 拆解任务
- 选择工具
- 执行操作
- 验证结果
- 迭代优化

### Agent vs Workflow vs Function Call

| 特性 | Workflow | Function Call | Agent |
|------|----------|---------------|-------|
| 执行方式 | 固定流程 | 按需调用 | 自主决策 |
| 灵活性 | ❌ 低 | ⚠️ 中 | ✅ 高 |
| 自主性 | ❌ 无 | ❌ 无 | ✅ 有 |
| 错误处理 | 人工定义 | 需要编码 | 自适应 |
| 适用场景 | 标准化任务 | 数据获取 | 复杂任务 |

### Agent 代码示例

```python
# examples/06_agent.py
"""
Agent 示例：一个能自主规划和执行任务的智能体
"""
from openai import OpenAI
import json
import re

client = OpenAI()

class Agent:
    def __init__(self, name: str, tools: list[dict], tool_handlers: dict):
        self.name = name
        self.tools = tools
        self.tool_handlers = tool_handlers
        self.max_iterations = 5
    
    def run(self, user_goal: str) -> str:
        """
        Agent 主循环：
        1. 理解目标
        2. 规划步骤
        3. 执行工具
        4. 检查结果
        5. 必要时迭代
        """
        messages = [
            {"role": "system", "content": f"""
你是一个智能助手，名字是 {self.name}。
你可以使用以下工具来完成任务：
{json.dumps([t['function']['name'] + ': ' + t['function']['description'] for t in self.tools], ensure_ascii=False)}

请根据用户目标，自主决定使用哪些工具，直到完成任务。
"""},
            {"role": "user", "content": user_goal}
        ]
        
        for iteration in range(self.max_iterations):
            print(f"\n--- 第 {iteration + 1} 轮 ---")
            
            # LLM 决策
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=self.tools,
                tool_choice="auto"
            )
            
            message = response.choices[0].message
            messages.append(message)
            
            # 如果不需要调用工具，任务完成
            if not message.tool_calls:
                return message.content
            
            # 执行工具调用
            for tool_call in message.tool_calls:
                func_name = tool_call.function.name
                args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 调用工具: {func_name}({args})")
                
                # 执行函数
                if func_name in self.tool_handlers:
                    result = self.tool_handlers[func_name](**args)
                else:
                    result = {"error": f"未知工具: {func_name}"}
                
                print(f"📊 结果: {result}")
                
                # 将结果加入对话
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(result, ensure_ascii=False)
                })
        
        return "达到最大迭代次数，任务未完成"

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
    }
]

# 工具实现
def search_web(query: str) -> dict:
    """模拟搜索"""
    mock_results = {
        "Python": "Python 是一种高级编程语言，由 Guido van Rossum 于 1991 年创建",
        "AI": "人工智能（Artificial Intelligence）是计算机科学的一个分支",
        "OpenClaw": "OpenClaw 是一个开源的 AI Agent 框架"
    }
    for key in mock_results:
        if key.lower() in query.lower():
            return {"result": mock_results[key]}
    return {"result": "未找到相关信息"}

def calculate(expression: str) -> dict:
    """执行计算"""
    try:
        # 安全起见，只允许数字和基本运算符
        if re.match(r'^[\d\s\+\-\*\/\.\(\)]+$', expression):
            return {"result": eval(expression)}
        return {"error": "无效表达式"}
    except Exception as e:
        return {"error": str(e)}

def save_note(title: str, content: str) -> dict:
    """保存笔记"""
    print(f"📝 保存笔记: {title}")
    return {"status": "success", "message": f"笔记 '{title}' 已保存"}

# 创建 Agent
agent = Agent(
    name="助手",
    tools=tools,
    tool_handlers={
        "search_web": search_web,
        "calculate": calculate,
        "save_note": save_note
    }
)

# 运行 Agent
result = agent.run("帮我查一下 Python 是什么，然后把结果保存成笔记")
print(f"\n✅ 最终结果:\n{result}")
```

### Agent 的核心能力

```
┌─────────────────────────────────────────────────────┐
│                    Agent 核心能力                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│  │  感知    │ ─→ │  规划   │ ─→ │  执行   │        │
│  │Perceive │    │  Plan   │    │  Act    │        │
│  └─────────┘    └─────────┘    └─────────┘        │
│       ↑              │              │              │
│       │              ↓              ↓              │
│       │         ┌─────────┐    ┌─────────┐        │
│       └─────────│  反思   │ ←──│  验证   │        │
│                 │ Reflect │    │ Verify │        │
│                 └─────────┘    └─────────┘        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

## 七、OpenClaw

### 是什么
OpenClaw 是**开源的 AI Agent 框架**，提供了完整的：
- 多渠道接入（微信、Telegram、Discord 等）
- 技能系统（Skills）
- MCP 协议支持
- 记忆管理
- 多 Agent 协作

### OpenClaw 架构

```
┌────────────────────────────────────────────────────────┐
│                     OpenClaw 架构                       │
├────────────────────────────────────────────────────────┤
│                                                        │
│  ┌──────────────────────────────────────────────────┐ │
│  │              渠道层 (Channels)                     │ │
│  │  微信 │ Telegram │ Discord │ WhatsApp │ WebChat  │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Gateway (网关)                       │ │
│  │  消息路由 │ 会话管理 │ 权限控制                    │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │              Agent 核心                           │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │ │
│  │  │ 记忆    │ │ 技能    │ │ 工具    │            │ │
│  │  │ Memory  │ │ Skills  │ │ Tools   │            │ │
│  │  └─────────┘ └─────────┘ └─────────┘            │ │
│  └──────────────────────────────────────────────────┘ │
│                         ↓                              │
│  ┌──────────────────────────────────────────────────┐ │
│  │              工具层 (Tools)                       │ │
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐            │ │
│  │  │ MCP     │ │ Function│ │ Sandbox │            │ │
│  │  │ Servers │ │ Calls   │ │ 安全沙箱│            │ │
│  │  └─────────┘ └─────────┘ └─────────┘            │ │
│  └──────────────────────────────────────────────────┘ │
│                                                        │
└────────────────────────────────────────────────────────┘
```

### OpenClaw 配置示例

```yaml
# examples/07_openclaw_config.yaml
# OpenClaw 配置文件示例

# 模型配置
models:
  providers:
    openai:
      baseUrl: https://api.openai.com/v1
      apiKey: ${OPENAI_API_KEY}
      api: openai-completions
      models:
        - id: gpt-4
          name: GPT-4

# Agent 配置
agents:
  defaults:
    model:
      primary: openai/gpt-4
    workspace: ~/.openclaw/workspace

# 渠道配置
channels:
  telegram:
    enabled: true
    token: ${TELEGRAM_BOT_TOKEN}
  
  discord:
    enabled: true
    token: ${DISCORD_BOT_TOKEN}

# 技能配置
skills:
  load:
    extraDirs:
      - ~/.openclaw/skills
  entries:
    weather-assistant:
      enabled: true
    code-helper:
      enabled: true

# MCP 服务器
mcp:
  servers:
    filesystem:
      command: mcp-server-filesystem
      args:
        - /home/user/documents
    database:
      command: mcp-server-postgres
      env:
        DATABASE_URL: postgres://localhost/mydb
```

### OpenClaw Skill 示例

```markdown
<!-- examples/08_openclaw_skill/SKILL.md -->
---
name: code-reviewer
description: 代码审查助手，可以分析代码质量、提出改进建议
---

# Code Reviewer Skill

## 功能
- 分析代码质量
- 检测潜在问题
- 提出改进建议
- 生成审查报告

## 使用方式
```
请帮我审查这段代码：
[粘贴代码]
```

## 工具依赖
- `read_file`: 读取代码文件
- `analyze_code`: 代码分析（MCP 工具）

## 提示词模板
```
你是一个专业的代码审查专家。请对以下代码进行全面审查：

1. 代码风格
2. 潜在 Bug
3. 性能问题
4. 安全隐患
5. 改进建议

代码：
{code}

请给出详细的审查报告。
```
```

---

## 八、概念关系总结

### 演进路线

```
LLM (基础能力)
  │
  ├──→ Workflow (固定流程)
  │
  ├──→ Function Call (调用外部工具)
  │      │
  │      └──→ MCP (标准化工具协议)
  │
  ├──→ Skill (封装的能力包)
  │
  └──→ Agent (自主智能体)
         │
         └──→ OpenClaw (Agent 框架 + 多渠道 + 生态)
```

### 层级关系

```
┌─────────────────────────────────────────────────────┐
│                    OpenClaw                          │
│  (框架：整合所有能力，提供多渠道、记忆、协作)          │
├─────────────────────────────────────────────────────┤
│                      Agent                          │
│  (智能体：自主规划、决策、执行)                       │
├─────────────────────────────────────────────────────┤
│                      Skill                          │
│  (技能：封装的领域能力)                              │
├───────────────────┬─────────────────────────────────┤
│    Function Call  │              MCP                │
│    (函数调用)      │        (标准化协议)             │
├───────────────────┴─────────────────────────────────┤
│                    Workflow                         │
│  (工作流：固定流程编排)                              │
├─────────────────────────────────────────────────────┤
│                      LLM                            │
│  (大语言模型：基础能力)                              │
└─────────────────────────────────────────────────────┘
```

### 选择指南

| 场景 | 推荐方案 |
|------|----------|
| 简单问答 | LLM 直接调用 |
| 标准化任务（如数据ETL） | Workflow |
| 需要外部数据 | Function Call |
| 多平台工具复用 | MCP |
| 特定领域能力 | Skill |
| 复杂自主任务 | Agent |
| 生产环境多渠道部署 | OpenClaw |

---

## 九、代码运行说明

### 环境准备

```bash
# 安装依赖
pip install openai

# 设置 API Key
export OPENAI_API_KEY="sk-xxxxxxxx"

# 运行示例
python examples/01_llm_basics.py
python examples/03_function_call.py
python examples/06_agent.py
```

### 项目结构

```
llm-concepts-explained/
├── README.md
├── docs/
│   └── concepts.md (本文档)
└── examples/
    ├── 01_llm_basics.py      # LLM 基础
    ├── 02_workflow.py         # 工作流
    ├── 03_function_call.py    # 函数调用
    ├── 04_mcp_server.py       # MCP 服务
    ├── 05_skill.py            # 技能系统
    ├── 06_agent.py            # 智能体
    ├── 07_openclaw_config.yaml
    └── 08_openclaw_skill/
        └── SKILL.md
```

---

## 参考资料

- OpenAI API 文档: https://platform.openai.com/docs
- Anthropic MCP: https://modelcontextprotocol.io
- LangChain: https://python.langchain.com
- OpenClaw: https://openclaw.ai

---

*本文档由 AI 辅助生成，代码均经过简化，适合学习理解概念。*
