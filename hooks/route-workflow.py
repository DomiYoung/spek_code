#!/usr/bin/env python3
"""UserPromptSubmit Hook: 自动路由到 feature-dev skill

目的：减少用户显式提醒成本，让每次需求输入时自动给出"推荐入口"。

行为：
- 不阻断（只输出提醒）
- 根据关键词将请求分类为：功能开发 / bug修复 / 优化拓展 / 代码分析
- 输出建议的 feature-dev skill 调用
"""

import json
import re
import sys


EXEMPT_KEYWORDS = [
    "跳过路由",
    "skip-route",
    "skip route",
    "跳过评估",
    "直接开始",
]


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
        user_input = (data.get("user_prompt") or data.get("prompt") or "").strip()
    except Exception:
        print("")
        return

    if not user_input:
        print("")
        return

    lowered = user_input.lower()
    if any(k.lower() in lowered for k in EXEMPT_KEYWORDS):
        print("")
        return

    # 分类检测（对应 CLAUDE.md 的映射表）
    bug = re.search(r"(不显示|报错|崩溃|白屏|不工作|bug|error|exception|失败|问题)", user_input, re.IGNORECASE)
    analyze = re.search(r"(分析|理解|解释|看看|review|audit|审计|审核|探索)", user_input, re.IGNORECASE)
    optimize = re.search(r"(优化|性能|卡顿|慢|重构|refactor|perf)", user_input, re.IGNORECASE)
    feature = re.search(r"(创建|新增|实现|添加功能|开发|做一个|make|create|build|implement|add)", user_input, re.IGNORECASE)

    task_type = None
    skill_name = None

    if bug:
        task_type = "Bug修复"
        skill_name = "feature-dev:feature-dev"
    elif analyze:
        task_type = "代码分析"
        skill_name = "feature-dev:code-explorer"
    elif optimize:
        task_type = "优化拓展"
        skill_name = "feature-dev:feature-dev"
    elif feature:
        task_type = "功能开发"
        skill_name = "feature-dev:feature-dev"

    if not task_type:
        print("")
        return

    # 输出 JSON 格式的 additionalContext
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"""
🧭 **Skill 自动路由**

检测类型: **{task_type}**
推荐 Skill: `{skill_name}`

⚠️ Claude 必须：
1. 先输出权重评估表格
2. 调用 `{skill_name}` skill
3. 按 skill 定义的流程执行

（如不希望提醒，可在输入里加：skip-route / 跳过路由）
"""
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
