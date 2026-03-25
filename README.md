# LLM、Workflow、Function Call、MCP、Skill、Agent、OpenClaw 完全指南

> 从零理解 AI 应用开发的核心概念，配合可运行代码示例

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai
```

### 2. 设置 API Key

```bash
# macOS/Linux
export OPENAI_API_KEY='sk-xxxxxxxx'

# Windows
set OPENAI_API_KEY=sk-xxxxxxxx
```

### 3. 运行示例

```bash
cd examples

# LLM 基础（最简单）
python 01_llm_simple.py

# Function Call 函数调用
python 03_function_call_simple.py

# Agent 智能体
python 04_agent_simple.py

# 概念对比演示
python 06_comparison.py
```

## 📁 项目结构

```
llm-concepts-explained/
├── README.md
├── docs/
│   └── concepts.md              # 完整概念文档
└── examples/
    ├── 01_llm_simple.py         # ✅ LLM 基础（推荐先跑这个）
    ├── 01_llm_basics.py         # LLM 基础（完整版）
    ├── 02_workflow.py           # Workflow 工作流
    ├── 03_function_call_simple.py  # ✅ Function Call（推荐）
    ├── 03_function_call.py      # Function Call（完整版）
    ├── 04_agent_simple.py       # ✅ Agent 智能体（推荐）
    ├── 04_agent.py              # Agent 智能体（完整版）
    ├── 05_skill.py              # Skill 技能系统
    └── 06_comparison.py         # 概念对比演示
```

## 🧠 概念速查

| 概念 | 是什么 | 一句话总结 |
|------|--------|-----------|
| **LLM** | 大语言模型 | AI 的"大脑"，能理解和生成文本 |
| **Workflow** | 工作流 | 固定的任务执行流程 |
| **Function Call** | 函数调用 | 让 LLM 能调用外部工具 |
| **MCP** | 模型上下文协议 | 标准化的工具连接协议 |
| **Skill** | 技能 | 封装好的能力模块 |
| **Agent** | 智能体 | 能自主规划执行的 AI 系统 |
| **OpenClaw** | Agent 框架 | 开源的多渠道 Agent 平台 |

## ⚠️ 常见问题

### Q: 运行报错 "No module named 'openai'"

```bash
pip install openai
```

### Q: 报错 "OPENAI_API_KEY not found"

设置环境变量：
```bash
export OPENAI_API_KEY='sk-xxxxxxxx'
```

或者在代码中直接设置：
```python
client = OpenAI(api_key="sk-xxxxxxxx")
```

### Q: 报错 "Incorrect API key provided"

检查 API Key 是否正确，确保以 `sk-` 开头。

## 📊 概念关系

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

## 📖 参考资料

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic MCP](https://modelcontextprotocol.io)
- [OpenClaw](https://openclaw.ai)

## 📄 License

MIT License
