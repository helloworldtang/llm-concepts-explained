"""
LLM 基础示例：一个只会"说话"的模型
运行: python 01_llm_basics.py
"""
from openai import OpenAI
import os

# 初始化客户端
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def basic_chat(message: str) -> str:
    """最基础的 LLM 调用"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # 使用更便宜的模型
        messages=[
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

def chat_with_context(messages: list[dict]) -> str:
    """带上下文的对话"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    # 测试 1: 简单问答
    print("=== 测试 1: 简单问答 ===")
    answer = basic_chat("用一句话解释什么是 LLM")
    print(f"回答: {answer}\n")
    
    # 测试 2: 多轮对话
    print("=== 测试 2: 多轮对话 ===")
    messages = [
        {"role": "user", "content": "我叫张三"},
        {"role": "assistant", "content": "你好张三，很高兴认识你！"},
        {"role": "user", "content": "我叫什么名字？"}
    ]
    answer = chat_with_context(messages)
    print(f"回答: {answer}\n")
    
    # 测试 3: LLM 的局限性
    print("=== 测试 3: LLM 的局限性 ===")
    answer = basic_chat("今天北京天气怎么样？")
    print(f"回答: {answer}")
    print("注意: LLM 无法获取实时数据\n")
