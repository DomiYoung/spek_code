#!/usr/bin/env python3
"""
Skill 激活提醒 Hook（简化版）
不做硬编码匹配，只提醒 Claude 检查可用 Skills
"""

import json
import sys
import re

def is_task_request(user_input: str) -> bool:
    """检测是否为任务请求（非简单对话）"""
    if not user_input or len(user_input.strip()) < 10:
        return False
    
    # 跳过简单确认
    skip_patterns = [
        r'^(好的|ok|yes|no|是|否|可以|行|嗯|继续|lgtm)$',
        r'^(谢谢|thanks)',
    ]
    user_lower = user_input.strip().lower()
    for pattern in skip_patterns:
        if re.match(pattern, user_lower):
            return False
    
    return True

def main():
    user_input = ""
    try:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            if data:
                try:
                    context = json.loads(data)
                    user_input = context.get('prompt', '') or context.get('input', '')
                except json.JSONDecodeError:
                    user_input = data
    except Exception:
        pass
    
    if is_task_request(user_input):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": "INSTRUCTION: Check available Skills and use any that match this request. Read the SKILL.md for matched skills."
            }
        }
        print(json.dumps(output))
    else:
        print(json.dumps({}))

if __name__ == "__main__":
    main()
