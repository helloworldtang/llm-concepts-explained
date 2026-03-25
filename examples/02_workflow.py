"""
Workflow 示例：一个固定流程的问答系统
运行: python 02_workflow.py
"""
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def classify_question(question: str) -> str:
    """步骤1：分类问题"""
    prompt = f"""分析问题属于哪个类别，只回答一个词（天气/计算/常识/其他）：
问题：{question}"""
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

def handle_calculation(question: str) -> str:
    """处理计算类问题"""
    prompt = f"计算并回答：{question}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def qa_workflow(question: str) -> str:
    """
    问答工作流:
    1. 分析问题类型
    2. 根据类型选择处理方式
    3. 生成答案
    """
    print(f"📥 收到问题: {question}")
    
    # 步骤1：分类
    category = classify_question(question)
    print(f"🔍 问题类别: {category}")
    
    # 步骤2：路由处理
    if category == "计算":
        answer = handle_calculation(question)
    elif category == "天气":
        answer = "❌ 抱歉，我无法获取实时天气数据。"
    else:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content
    
    return answer

if __name__ == "__main__":
    # 测试不同的 workflow 路径
    questions = [
        "123 * 456 等于多少？",
        "今天北京天气怎么样？",
        "Python 是什么？"
    ]
    
    for q in questions:
        print(f"\n{'='*50}")
        result = qa_workflow(q)
        print(f"📤 回答: {result}")
