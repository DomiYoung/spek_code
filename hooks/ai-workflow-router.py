#!/usr/bin/env python3
"""
AI-Powered Workflow Router Hook (Prompt-Based)

使用 Claude Haiku 智能判断用户请求类型，替代硬编码关键词匹配。
这是一个 prompt-based hook，由 AI 来决定：
1. 是否需要权重评估
2. 任务类型分类
3. 推荐的 Skill 路由

优势：
- 理解语义和上下文，不依赖关键词
- 自动适应新场景
- 更准确的意图识别
"""

import json
import sys
import os

# 豁免关键词 - 这些仍然硬编码，因为是明确的用户指令
EXEMPT_KEYWORDS = [
    "跳过路由", "skip-route", "skip route",
    "跳过评估", "直接开始", "跳过"
]

# 简单对话模式 - 不需要 AI 判断
# 注意：移除了"继续"，因为"继续处理"可能包含任务上下文
SIMPLE_PATTERNS = [
    "好的", "ok", "yes", "no", "是", "否", "可以", "行", "嗯",
    "谢谢", "thanks", "lgtm"
]

# 需要权重评估的延续性指令
CONTINUATION_WITH_TASK = [
    "继续处理", "继续执行", "继续修复", "继续开发",
    "proceed", "continue with"
]


def is_exempt(user_input: str) -> bool:
    """检查是否豁免

    注意：延续性任务指令（如"继续处理"）不豁免，需要触发权重评估
    """
    lower = user_input.lower().strip()

    # 太短的输入（但先检查延续性指令）
    if len(lower) < 5:
        return True

    # 🔴 延续性任务指令 - 不豁免，必须触发权重评估
    for continuation in CONTINUATION_WITH_TASK:
        if continuation in lower:
            return False  # 不豁免，触发工作流提醒

    # 简单对话（纯确认性回复）
    for pattern in SIMPLE_PATTERNS:
        if lower == pattern or lower.startswith(pattern):
            return True

    # 明确的豁免关键词
    for kw in EXEMPT_KEYWORDS:
        if kw in lower:
            return True

    return False


def create_classification_prompt(user_input: str) -> str:
    """
    创建让 AI 分类用户请求的 prompt
    这个 prompt 会被传递给 Claude Haiku 进行智能判断
    """
    return f"""你是一个任务分类助手。分析以下用户请求，判断：

1. task_type: 任务类型
   - "bug_fix": Bug 修复（报错、不显示、崩溃、功能异常等）
   - "feature": 新功能开发（创建、添加、实现新特性）
   - "optimize": 优化/重构（性能、代码质量、架构改进）
   - "analyze": 代码分析/理解（查看、解释、审计、探索）
   - "brainstorm": 发散性讨论（你觉得、建议、方案对比、怎么设计）
   - "simple": 简单操作（配置、文档、格式化等）
   - "question": 纯问答（不涉及代码变更）

2. needs_weight_assessment: 是否需要权重评估（true/false）
   - 涉及代码变更、Bug 修复、功能开发 → true
   - 纯问答、简单配置 → false

3. recommended_skill: 推荐的 Skill
   - bug_fix/feature/optimize → "feature-dev:feature-dev"
   - analyze → "feature-dev:code-explorer"
   - brainstorm → "brainstorm"
   - simple/question → null

4. confidence: 置信度 (0.0-1.0)

用户请求：
---
{user_input}
---

请用 JSON 格式回复，只输出 JSON，不要其他内容：
{{"task_type": "...", "needs_weight_assessment": true/false, "recommended_skill": "...", "confidence": 0.x}}"""


def main():
    """
    Main hook logic

    对于 prompt-based hook:
    - 输入: stdin 接收 JSON (包含 prompt, sessionId, timestamp 等)
    - 输出: stdout 输出 JSON (hookSpecificOutput.additionalContext)

    注意：这个脚本本身不调用 LLM，而是输出一个结构化的提示，
    由 Claude Code 的 prompt-based hook 机制来处理。
    """
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        user_input = (data.get("prompt") or data.get("user_prompt") or "").strip()
    except Exception:
        print(json.dumps({}))
        return

    if not user_input or is_exempt(user_input):
        print(json.dumps({}))
        return

    # 输出智能路由提示
    # 注意：由于当前 Claude Code 的 prompt-based hook 实现可能有限制，
    # 我们先用一个混合方案：基础的启发式规则 + 详细的提示

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"""
🤖 **AI 智能路由激活**

请根据用户请求智能判断（不要依赖关键词匹配）：

**用户请求**: "{user_input[:100]}{'...' if len(user_input) > 100 else ''}"

**你需要判断**：
1. 这是什么类型的任务？（Bug修复/功能开发/优化重构/代码分析/发散讨论/简单操作/纯问答）
2. 是否需要输出权重评估表格？
3. 应该调用哪个 Skill？

**决策后必须输出**：
```
┌─ 权重评估 ──────────────────────────────────────┐
│ 任务类型: [你的判断]                              │
│ 权重得分: [0-10]                                  │
│ Spec-Kit: [是/否]                                │
│ 推荐 Skill: [skill 名称]                         │
└─────────────────────────────────────────────────┘
```

然后调用对应的 Skill 执行标准流程。
"""
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
