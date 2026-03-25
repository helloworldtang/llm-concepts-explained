# LLM、Workflow、Function Call、MCP、Skill、Agent、OpenClaw 完全指南

> 从零理解 AI 应用开发的核心概念，配合可运行代码示例

## 📚 文档

- **[完整概念讲解](docs/concepts.md)** - 详细讲解每个概念的区别与联系

## 🚀 快速开始

```bash
# 安装依赖
pip install openai

# 设置 API Key
export OPENAI_API_KEY="sk-xxxxxxxx"

# 运行示例
python examples/01_llm_basics.py      # LLM 基础
python examples/03_function_call.py   # Function Call
python examples/04_agent.py           # Agent 智能体
python examples/06_comparison.py      # 概念对比
```

## 📁 项目结构

```
llm-concepts-explained/
├── README.md
├── docs/
│   └── concepts.md          # 完整概念文档
└── examples/
    ├── 01_llm_basics.py     # LLM 基础调用
    ├── 02_workflow.py       # 工作流示例
    ├── 03_function_call.py  # 函数调用示例
    ├── 04_agent.py          # 智能体示例
    ├── 05_skill.py          # 技能系统示例
    └── 06_comparison.py     # 概念对比演示
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

## 🔗 概念关系

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

## 📊 选择指南

| 场景 | 推荐方案 |
|------|----------|
| 简单问答 | LLM 直接调用 |
| 标准化任务（如数据ETL） | Workflow |
| 需要外部数据 | Function Call |
| 多平台工具复用 | MCP |
| 特定领域能力 | Skill |
| 复杂自主任务 | Agent |
| 生产环境多渠道部署 | OpenClaw |

## 📖 参考资料

- [OpenAI API 文档](https://platform.openai.com/docs)
- [Anthropic MCP](https://modelcontextprotocol.io)
- [LangChain](https://python.langchain.com)
- [OpenClaw](https://openclaw.ai)

## 📄 License

MIT License
