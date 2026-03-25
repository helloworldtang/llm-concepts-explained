"""
LLM 基础示例 - 最简单的版本
运行方式: python 01_llm_simple.py
"""
from openai import OpenAI

# 方式一：直接设置 API Key（不推荐用于生产环境）
# client = OpenAI(api_key="sk-xxxxxxxx")

# 方式二：从环境变量读取（推荐）
import os
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌ 错误：请先设置 OPENAI_API_KEY 环境变量")
    print("\n设置方法：")
    print("  macOS/Linux: export OPENAI_API_KEY='sk-xxxxxxxx'")
    print("  Windows: set OPENAI_API_KEY=sk-xxxxxxxx")
    print("\n或者在代码中直接设置：")
    print("  client = OpenAI(api_key='sk-xxxxxxxx')")
    exit(1)

client = OpenAI(api_key=api_key)

print("=== 测试 1: 简单问答 ===")
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "用一句话解释什么是 LLM"}]
)
print(f"回答: {response.choices[0].message.content}")

print("\n=== 测试 2: 多轮对话 ===")
messages = [
    {"role": "user", "content": "我叫张三"},
    {"role": "assistant", "content": "你好张三！"},
    {"role": "user", "content": "我叫什么名字？"}
]
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=messages
)
print(f"回答: {response.choices[0].message.content}")
