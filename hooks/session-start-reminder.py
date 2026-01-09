#!/usr/bin/env python3
"""
SessionStart Hook: 会话启动时输出自检提醒

功能：
1. 提醒 LLM 遵循 RULES.md 规范
2. 输出必须执行的检查项
3. 提醒读取 pitfalls.md 历史经验
"""
import json
import os

def main():
    # 构建提醒消息
    reminder = """
📋 **会话启动自检提醒**

根据 RULES.md，每个任务必须遵循以下流程：

```
┌─ 强制检查项 ──────────────────────────────────┐
│ 1. 输出权重评估表格（每个任务开头）            │
│ 2. 权重≥7 → 强制 Spec-Kit 流程                │
│ 3. 需求模糊 → 先 brainstorm                   │
│ 4. 代码编写前 → spec.md 必须存在（Hook 拦截） │
│ 5. 开发前 → 触发 component-reuse-expert       │
└───────────────────────────────────────────────┘
```

**豁免关键词**: "跳过检查", "skip-check", "hotfix", "调试"
"""

    # 输出成功，附带提醒
    print(reminder)

if __name__ == "__main__":
    main()
