#!/usr/bin/env python3
"""
自动踩坑记录 Hook

在特定条件下自动提示记录踩坑经验：
1. 检测到 Bug 修复类任务完成
2. 对话中出现"踩坑"、"记录"等关键词
3. 同一错误模式出现多次

工作方式：
- 作为 PostToolCall Hook，在工具调用后检查
- 输出提示信息到 stderr，不阻止操作

退出码：
- 0: 正常（不阻止）
"""
import json
import sys
import os
import re
from datetime import datetime

# 触发关键词
TRIGGER_KEYWORDS = [
    "踩坑", "踩了坑", "坑了", "记录一下", "记下来",
    "pitfall", "gotcha", "终于修好", "折腾了",
    "调试了很久", "卡了", "搞定了"
]

# 排除关键词（避免误触发）
EXCLUDE_KEYWORDS = [
    "不用记录", "跳过", "skip", "不需要"
]

def check_trigger(text: str) -> tuple[bool, str]:
    """检查是否触发记录提示"""
    text_lower = text.lower()
    
    # 排除检查
    for kw in EXCLUDE_KEYWORDS:
        if kw in text_lower:
            return False, ""
    
    # 触发检查
    for kw in TRIGGER_KEYWORDS:
        if kw in text_lower:
            return True, kw
    
    return False, ""

def main():
    try:
        input_data = json.load(sys.stdin)
        
        # 获取用户消息或工具输出
        user_message = input_data.get('user_message', '')
        tool_output = input_data.get('tool_output', '')
        session_id = input_data.get('session_id', 'unknown')
        
        # 合并检查文本
        check_text = f"{user_message} {tool_output}"
        
        triggered, keyword = check_trigger(check_text)
        
        if triggered:
            # 输出提示（不阻止操作）
            print("", file=sys.stderr)
            print("═" * 50, file=sys.stderr)
            print("🧠 KI Manager 提示", file=sys.stderr)
            print("═" * 50, file=sys.stderr)
            print(f"检测到关键词: \"{keyword}\"", file=sys.stderr)
            print("", file=sys.stderr)
            print("如果这是一个值得记录的经验，请使用：", file=sys.stderr)
            print("  1. 说「记录到 pitfalls」触发 ki-manager", file=sys.stderr)
            print("  2. 或手动添加到对应的 pitfalls.md", file=sys.stderr)
            print("", file=sys.stderr)
            print("知识库位置：", file=sys.stderr)
            print("  📁 全局: ~/.ai-knowledge/global/pitfalls.md", file=sys.stderr)
            print("  📁 领域: ~/.ai-knowledge/domains/{domain}/pitfalls.md", file=sys.stderr)
            print("  📁 项目: ~/.ai-knowledge/projects/{project}/pitfalls.md", file=sys.stderr)
            print("═" * 50, file=sys.stderr)
        
        # 始终允许操作继续
        sys.exit(0)
        
    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        # 出错时静默失败，不影响主流程
        sys.exit(0)

if __name__ == "__main__":
    main()
