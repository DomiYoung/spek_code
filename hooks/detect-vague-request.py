#!/usr/bin/env python3
"""
UserPromptSubmit Hook: 检测模糊需求，强制触发脑暴

功能：
1. 检测用户输入是否为模糊需求
2. 模糊需求时提醒先进入脑暴模式
3. 不阻断，但给出强提醒

触发时机：UserPromptSubmit（每次用户输入）
"""
import sys
import json
import re

# ==================== 配置 ====================

# 模糊需求关键词模式
VAGUE_PATTERNS = [
    # 中文模糊表达
    r"我想(做|实现|加|添加|创建|开发)",
    r"帮我(做|实现|写|加|添加|创建|开发)",
    r"能不能",
    r"可不可以",
    r"怎么(做|实现|写)",
    r"想要一个",
    r"需要一个",
    r"大概|可能|也许|或许",
    r"不太确定",
    r"随便|差不多",
    r"类似于",
    r"参考.*做",

    # 英文模糊表达
    r"(?i)i want to",
    r"(?i)can you (help|make|create|build)",
    r"(?i)maybe",
    r"(?i)not sure",
    r"(?i)thinking about",
    r"(?i)something like",
    r"(?i)kind of",
    r"(?i)sort of",
]

# 明确需求的排除模式（检测到这些说明需求已明确）
CLEAR_PATTERNS = [
    r"spec\.md",
    r"\.specify/",
    r"/sc:brainstorm",
    r"/sc:implement",
    r"--bs",
    r"跳过脑暴",
    r"skip.*brainstorm",
    r"直接(开始|实现|做)",
    r"按照.*spec",
    r"根据.*规范",
    r"修复.*bug",
    r"fix.*bug",
    r"错误|报错|error|exception",  # Bug修复通常不需要脑暴
]

# 豁免关键词
EXEMPT_KEYWORDS = [
    "跳过脑暴",
    "skip-brainstorm",
    "直接开始",
    "hotfix",
    "紧急",
    "urgent",
]

# ==================== 核心逻辑 ====================

def is_vague_request(user_input: str) -> tuple[bool, list[str]]:
    """检测是否为模糊需求"""
    # 检查豁免
    for keyword in EXEMPT_KEYWORDS:
        if keyword.lower() in user_input.lower():
            return False, []

    # 检查是否已经明确
    for pattern in CLEAR_PATTERNS:
        if re.search(pattern, user_input, re.IGNORECASE):
            return False, []

    # 检测模糊模式
    matched_patterns = []
    for pattern in VAGUE_PATTERNS:
        if re.search(pattern, user_input):
            matched_patterns.append(pattern)

    return len(matched_patterns) > 0, matched_patterns

def is_implementation_request(user_input: str) -> bool:
    """检测是否为实现类请求（非纯问答）"""
    impl_keywords = [
        r"做|实现|写|加|添加|创建|开发|构建|搭建",
        r"(?i)(make|create|build|implement|add|develop)",
        r"功能|feature|组件|component|页面|page|模块|module",
    ]

    for pattern in impl_keywords:
        if re.search(pattern, user_input):
            return True
    return False

def main():
    # 读取 stdin（用户输入内容）
    try:
        input_data = sys.stdin.read()
        data = json.loads(input_data)
        user_input = data.get("user_prompt", "")
    except:
        # 无法解析时直接放行
        print("")
        return

    # 检测是否为模糊的实现请求
    is_vague, patterns = is_vague_request(user_input)
    is_impl = is_implementation_request(user_input)

    if is_vague and is_impl:
        # 输出脑暴提醒（不阻断，只是提醒）
        reminder = """
🧠 **检测到模糊需求 - 建议先脑暴**

检测到您的请求可能需要进一步明确：
```
┌─ 脑暴建议 ────────────────────────────────────┐
│ ⚠️  需求表述较模糊，建议先进入脑暴模式        │
│                                               │
│ 选项 1: 输入 /sc:brainstorm 进入脑暴          │
│ 选项 2: 补充具体需求后继续                    │
│ 选项 3: 输入 "跳过脑暴" 直接开始              │
└───────────────────────────────────────────────┘
```

**脑暴模式会帮助你**：
- 🎯 明确功能边界和验收标准
- 📋 识别可复用的现有组件
- 🔍 发现潜在的技术难点
- 📝 生成 spec.md 需求文档

💡 输入 `/sc:brainstorm` 开始脑暴，或补充具体需求继续。
"""
        print(reminder)
    else:
        # 不是模糊需求，正常放行
        print("")

if __name__ == "__main__":
    main()
