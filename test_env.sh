#!/bin/bash
# 测试脚本 - 验证环境配置

echo "=== 检查 Python 环境 ==="
python3 --version

echo ""
echo "=== 检查 openai 包 ==="
python3 -c "import openai; print(f'✅ openai {openai.__version__}')" || {
    echo "❌ openai 未安装，正在安装..."
    pip3 install openai
}

echo ""
echo "=== 检查 OPENAI_API_KEY ==="
if [ -z "$OPENAI_API_KEY" ]; then
    echo "❌ OPENAI_API_KEY 未设置"
    echo ""
    echo "请先设置 API Key："
    echo "  export OPENAI_API_KEY='sk-xxxxxxxx'"
    echo ""
    echo "或者在 PyCharm 中："
    echo "  Run -> Edit Configurations -> Environment variables"
    echo "  添加: OPENAI_API_KEY=sk-xxxxxxxx"
else
    echo "✅ OPENAI_API_KEY 已设置 (长度: ${#OPENAI_API_KEY})"
fi

echo ""
echo "=== 测试 LLM 调用 ==="
cd ~/workspace/github/llm-concepts-explained/examples
python3 01_llm_simple.py
