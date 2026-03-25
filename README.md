# LLM、Workflow、Function Call、MCP、Skill、Agent、OpenClaw 完全指南

> 从零理解 AI 应用开发的核心概念，配合可运行代码示例

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install openai
```

### 2. 获取 API Key（选择一个）

| 提供商 | 获取地址 | 特点 |
|--------|----------|------|
| **DeepSeek** | https://platform.deepseek.com/ | 推荐，国内可用，便宜 |
| **通义千问** | https://dashscope.console.aliyun.com/ | 阿里云，国内可用 |
| OpenAI | https://platform.openai.com/ | 需要科学上网 |

### 3. 设置环境变量

```bash
# DeepSeek（推荐）
export DEEPSEEK_API_KEY='sk-xxxxxxxx'

# 或 通义千问
export DASHSCOPE_API_KEY='sk-xxxxxxxx'
```

### 4. 运行示例

```bash
cd examples

# LLM 基础
python 01_llm_multi_provider.py

# Function Call 函数调用
python 03_function_call_multi.py

# Agent 智能体
python 04_agent_multi.py
```

## 📁 项目结构

```
llm-concepts-explained/
├── README.md
├── docs/
│   └── concepts.md              # 完整概念文档
└── examples/
    ├── API_KEY_GUIDE.md         # API Key 获取指南
    ├── 01_llm_multi_provider.py # ✅ LLM 基础（支持 DeepSeek/通义千问）
    ├── 03_function_call_multi.py# ✅ Function Call（支持多模型）
    ├── 04_agent_multi.py        # ✅ Agent 智能体（支持多模型）
    └── ...
```

## 🧠 概念速查

| 概念 | 是什么 | 一句话总结 |
|------|--------|-----------|
| **LLM** | 大语言模型 | AI 的"大脑" |
| **Workflow** | 工作流 | 固定的任务执行流程 |
| **Function Call** | 函数调用 | 让 LLM 能调用外部工具 |
| **MCP** | 模型上下文协议 | 标准化的工具连接协议 |
| **Skill** | 技能 | 封装好的能力模块 |
| **Agent** | 智能体 | 能自主规划执行的 AI 系统 |
| **OpenClaw** | Agent 框架 | 开源的多渠道 Agent 平台 |

## ⚠️ 常见问题

### Q: 没有国外信用卡，无法使用 OpenAI？
**A**: 使用 DeepSeek 或通义千问，国内可直接访问，价格更便宜。

### Q: 运行报错 "API Key not found"？
**A**: 确保设置了正确的环境变量：
```bash
export DEEPSEEK_API_KEY='sk-xxxxxxxx'
```

### Q: 如何切换模型？
**A**: 修改代码开头的 `PROVIDER` 变量：
```python
PROVIDER = "deepseek"  # 或 "qwen"
```

## 📖 参考资料

- [DeepSeek 文档](https://platform.deepseek.com/docs)
- [通义千问文档](https://help.aliyun.com/zh/dashscope/)
- [OpenClaw](https://openclaw.ai)

## 📄 License

MIT License
