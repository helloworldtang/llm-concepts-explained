# API Key 获取指南

## DeepSeek（推荐，国内可用，性价比高）

### 获取 API Key
1. 访问：https://platform.deepseek.com/
2. 注册/登录账号
3. 进入「API Keys」页面
4. 点击「创建 API Key」

### 设置环境变量
```bash
# macOS/Linux
export DEEPSEEK_API_KEY='sk-xxxxxxxx'

# Windows
set DEEPSEEK_API_KEY=sk-xxxxxxxx
```

### 价格（2024年参考）
- deepseek-chat: ¥1/百万 tokens（输入），¥2/百万 tokens（输出）
- 比 OpenAI 便宜约 95%

---

## 通义千问（阿里云）

### 获取 API Key
1. 访问：https://dashscope.console.aliyun.com/
2. 开通「灵积模型服务」
3. 创建 API Key

### 设置环境变量
```bash
# macOS/Linux
export DASHSCOPE_API_KEY='sk-xxxxxxxx'

# Windows
set DASHSCOPE_API_KEY=sk-xxxxxxxx
```

### 价格（2024年参考）
- qwen-turbo: ¥2/百万 tokens
- qwen-plus: ¥4/百万 tokens
- qwen-max: ¥40/百万 tokens

---

## OpenAI（需要科学上网）

### 获取 API Key
1. 访问：https://platform.openai.com/api-keys
2. 注册/登录
3. 创建 API Key

### 设置环境变量
```bash
export OPENAI_API_KEY='sk-xxxxxxxx'
```

---

## 快速测试

```bash
# 进入项目目录
cd llm-concepts-explained/examples

# 设置 API Key（选择你有的）
export DEEPSEEK_API_KEY='sk-xxx'
# 或
export DASHSCOPE_API_KEY='sk-xxx'

# 运行测试
python 01_llm_multi_provider.py
python 03_function_call_multi.py
python 04_agent_multi.py
```

## 切换模型

修改代码开头的 `PROVIDER` 变量：

```python
PROVIDER = "deepseek"  # DeepSeek
PROVIDER = "qwen"      # 通义千问
```
