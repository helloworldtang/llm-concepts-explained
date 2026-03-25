"""
Skill 示例：一个可复用的技能模块
运行: python 05_skill.py
"""
from dataclasses import dataclass, field
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
    """
    技能定义
    
    Skill 是封装好的能力模块，包含：
    - 名称和描述
    - 工具列表
    - 提示词模板
    - 使用示例
    """
    name: str
    description: str
    tools: list[Tool]
    prompt_template: str
    examples: list[str] = field(default_factory=list)
    config: dict = field(default_factory=dict)

# ===== 定义天气技能 =====
weather_skill = Skill(
    name="weather-assistant",
    description="天气查询助手，可以查询任意城市的天气和预报",
    
    tools=[
        Tool(
            name="get_weather",
            description="获取城市当前天气",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                }
            },
            handler=lambda city: {
                "北京": {"temp": 15, "condition": "晴"},
                "上海": {"temp": 18, "condition": "多云"},
            }.get(city, {"error": "未找到城市"})
        ),
        Tool(
            name="get_forecast",
            description="获取未来3天天气预报",
            parameters={
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "城市名称"}
                }
            },
            handler=lambda city: [
                {"date": "明天", "temp": 16, "condition": "阴"},
                {"date": "后天", "temp": 14, "condition": "小雨"},
            ]
        )
    ],
    
    prompt_template="""你是一个专业的天气助手。
当用户询问天气时：
1. 确认城市名称
2. 使用 get_weather 获取当前天气
3. 如需预报，使用 get_forecast
4. 友好地回复用户

用户问题：{question}""",
    
    examples=[
        "北京今天天气怎么样？",
        "上海未来三天会下雨吗？",
    ],
    
    config={
        "default_city": "北京",
        "temperature_unit": "摄氏度"
    }
)

# ===== 定义计算技能 =====
calculator_skill = Skill(
    name="calculator",
    description="数学计算助手，可以执行各种数学运算",
    
    tools=[
        Tool(
            name="calculate",
            description="执行数学表达式计算",
            parameters={
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "数学表达式"}
                }
            },
            handler=lambda expr: {"result": eval(expr)} if all(c in "0123456789+-*/.() " for c in expr) else {"error": "无效表达式"}
        )
    ],
    
    prompt_template="你是一个计算助手。计算用户的问题：{question}",
    
    examples=[
        "123 * 456 等于多少？",
        "(100 + 200) / 2 是多少？",
    ]
)

# ===== 技能注册表 =====
class SkillRegistry:
    """技能注册表 - 管理所有可用技能"""
    
    def __init__(self):
        self.skills: dict[str, Skill] = {}
    
    def register(self, skill: Skill):
        """注册技能"""
        self.skills[skill.name] = skill
        print(f"✅ 已注册技能: {skill.name}")
    
    def get(self, name: str) -> Skill | None:
        """获取技能"""
        return self.skills.get(name)
    
    def list_skills(self) -> list[str]:
        """列出所有技能"""
        return list(self.skills.keys())
    
    def get_skill_info(self, name: str) -> dict:
        """获取技能详细信息"""
        skill = self.skills.get(name)
        if not skill:
            return {"error": "技能不存在"}
        
        return {
            "name": skill.name,
            "description": skill.description,
            "tools": [t.name for t in skill.tools],
            "examples": skill.examples
        }

if __name__ == "__main__":
    # 创建注册表
    registry = SkillRegistry()
    
    # 注册技能
    registry.register(weather_skill)
    registry.register(calculator_skill)
    
    print("\n" + "="*50)
    print("📦 已注册的技能:")
    for name in registry.list_skills():
        info = registry.get_skill_info(name)
        print(f"\n  🔹 {name}")
        print(f"     描述: {info['description']}")
        print(f"     工具: {info['tools']}")
    
    # 模拟使用技能
    print("\n" + "="*50)
    print("🎯 使用 weather-assistant 技能:")
    skill = registry.get("weather-assistant")
    
    # 调用工具
    weather_tool = next(t for t in skill.tools if t.name == "get_weather")
    result = weather_tool.handler("北京")
    print(f"   天气查询结果: {result}")
