"""
LLM 基础示例 - 支持 OpenAI / DeepSeek / 通义千问
运行方式: python 01_llm_multi_provider.py
"""
from openai import OpenAI
import os

# ==================== 配置区 ====================
# 选择提供商: "openai" | "deepseek" | "qwen"
PROVIDER = "deepseek"

# API Key 配置（三选一，根据你有的 key 填写）
API_KEYS = {
    "openai": os.getenv("OPENAI_API_KEY", ""),           # sk-xxx
    "deepseek": os.getenv("DEEPSEEK_API_KEY", ""),       # sk-xxx
    "qwen": os.getenv("DASHSCOPE_API_KEY", ""),          # sk-xxx
}

# 模型配置
MODELS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
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
    """获取客户端"""
    api_key = API_KEYS.get(provider, "")
    
    if not api_key:
        print(f"❌ 错误：{provider.upper()}_API_KEY 未设置")
        print(f"\n获取 API Key：")
        if provider == "deepseek":
            print("  DeepSeek: https://platform.deepseek.com/api_keys")
        elif provider == "qwen":
            print("  通义千问: https://dashscope.console.aliyun.com/apiKey")
        else:
            print("  OpenAI: https://platform.openai.com/api-keys")
        print(f"\n设置方法：")
        print(f"  export {provider.upper()}_API_KEY='sk-xxxxxxxx'")
        exit(1)
    
    return OpenAI(
        api_key=api_key,
        base_url=MODELS[provider]["base_url"]
    )

def chat(message: str, provider: str = PROVIDER) -> str:
    """简单的对话"""
    client = get_client(provider)
    model = MODELS[provider]["model"]
    
    print(f"🔧 使用模型: {provider}/{model}")
    
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": message}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("=" * 50)
    print(f"当前提供商: {PROVIDER}")
    print("=" * 50)
    
    # 测试
    answer = chat("用一句话解释什么是 LLM")
    print(f"\n回答: {answer}")
    
    print("\n" + "=" * 50)
    print("💡 如需切换模型，修改代码开头的 PROVIDER 变量")
    print("   PROVIDER = 'deepseek'  # DeepSeek")
    print("   PROVIDER = 'qwen'      # 通义千问")
    print("   PROVIDER = 'openai'    # OpenAI")
