#!/usr/bin/env python3
"""
需求冻结保护 Hook - 全局版本

功能：
- 阻止对 spec.md 等规范文件的修改
- 在需求未完成前保护规范完整性
- 支持 /skip-protect 关键词临时豁免

使用方式：
1. 在 ~/.claude/settings.local.json 中配置 PreToolUse hook
2. 当尝试编辑 spec.md 时会阻止并提示

退出码：
- 0: 允许操作
- 2: 阻止操作（保护文件）
"""

import json
import sys
import os
import re

# 保护文件模式（正则表达式）
PROTECTED_PATTERNS = [
    r"\.specify/specs/.*/spec\.md$",       # Spec-Kit 规范文件
    r"\.specify/specs/.*/plan\.md$",       # 实施计划
    r"\.specify/specs/.*/tasks\.md$",      # 任务清单
    r"\.specify/memory/constitution\.md$", # 项目治理原则
    r".*[/\\]PRD\.md$",                    # PRD 文档
    r".*[/\\]requirements\.md$",           # 需求文档
    r".*[/\\]specs[/\\].*api-spec\.json$", # API 契约 (任意 specs 目录)
    r".*[/\\]specs[/\\].*data-model\.md$", # 数据模型
]

# 豁免关键词（在 session 或 tool input 中检测）
SKIP_KEYWORDS = [
    "/skip-protect",
    "skip-protect",
    "跳过保护",
    "临时修改",
]

def is_protected_file(file_path: str) -> bool:
    """检查文件是否受保护"""
    if not file_path:
        return False

    normalized_path = file_path.replace("\\", "/")

    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, normalized_path, re.IGNORECASE):
            return True

    return False

def has_skip_keyword(data: dict) -> bool:
    """检查是否有豁免关键词"""
    try:
        # 检查 tool_input
        tool_input = data.get("tool_input", {})
        if isinstance(tool_input, dict):
            for key, value in tool_input.items():
                if isinstance(value, str):
                    for keyword in SKIP_KEYWORDS:
                        if keyword in value.lower():
                            return True

        # 检查 session_id（可能包含上下文信息）
        session_id = data.get("session_id", "")
        for keyword in SKIP_KEYWORDS:
            if keyword in session_id.lower():
                return True

    except Exception:
        pass

    return False

def main():
    try:
        # 从 stdin 读取 JSON 输入
        input_data = sys.stdin.read()
        if not input_data.strip():
            sys.exit(0)

        data = json.loads(input_data)

        # 获取工具名称
        tool_name = data.get("tool_name", "")

        # 只检查文件编辑相关的工具
        edit_tools = ["Edit", "Write", "MultiEdit", "mcp__serena__replace_content",
                      "mcp__serena__replace_symbol_body", "mcp__serena__create_text_file"]

        if tool_name not in edit_tools:
            sys.exit(0)

        # 检查豁免关键词
        if has_skip_keyword(data):
            sys.exit(0)

        # 获取文件路径
        tool_input = data.get("tool_input", {})

        # MultiEdit 多文件遍历检查（策略：任意一个受保护 → 整体拒绝）
        file_path = ""
        if tool_name == "MultiEdit":
            edits = tool_input.get("edits", [])
            for edit in edits:
                edit_path = edit.get("file_path") or edit.get("relative_path") or ""
                if is_protected_file(edit_path):
                    file_path = edit_path
                    break
        else:
            file_path = tool_input.get("file_path") or tool_input.get("relative_path") or ""

        # 检查是否为保护文件
        if is_protected_file(file_path):
            error_msg = {
                "error": f"🛡️ 需求冻结保护：禁止修改规范文件 {os.path.basename(file_path)}",
                "reason": "规范文件在需求完成前受保护，防止意外修改",
                "resolution": [
                    "1. 如需修改规范，先通过验收流程",
                    "2. 紧急情况可使用 /skip-protect 临时豁免",
                    "3. 完成后运行 /speckit.analyze 验证一致性"
                ]
            }
            print(json.dumps(error_msg, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)

        # 允许操作
        sys.exit(0)

    except json.JSONDecodeError:
        # JSON 解析失败，允许操作继续
        sys.exit(0)
    except Exception as e:
        # 其他错误，打印警告但允许操作
        print(f"Hook warning: {e}", file=sys.stderr)
        sys.exit(0)

if __name__ == "__main__":
    main()
