#!/usr/bin/env python3
"""
Anti-Decay Hook - 防止长对话指令衰减
每 N 轮对话注入一次规则强化提醒
"""

import json
import sys
import os
from pathlib import Path

# 配置
REMINDER_INTERVAL = 5  # 每 5 轮提醒一次


def count_conversation_rounds(transcript_path: str) -> int:
    """统计对话轮数"""
    if not transcript_path or not Path(transcript_path).exists():
        return 0
    
    try:
        rounds = 0
        with open(transcript_path, 'r') as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    if entry.get('role') == 'user':
                        rounds += 1
                except:
                    continue
        return rounds
    except:
        return 0


def main():
    session_data = {}
    try:
        if not sys.stdin.isatty():
            data = sys.stdin.read()
            if data:
                try:
                    session_data = json.loads(data)
                except json.JSONDecodeError:
                    pass
    except Exception:
        pass
    
    transcript_path = session_data.get('transcript_path', '')
    rounds = count_conversation_rounds(transcript_path)
    
    # 每 N 轮注入强化提醒
    if rounds > 0 and rounds % REMINDER_INTERVAL == 0:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"""
🔄 **ANTI-DECAY CHECKPOINT** (Round {rounds})

长对话规则强化：
1. **新任务必须输出决策卡片** - 权重分析表格
2. **检查相关 Skills** - 1% 原则：可能适用就要用
3. **识别任务边界** - 新问题 = 新评估

继续遵守 CLAUDE.md 中的协议。
"""
            }
        }
        print(json.dumps(output))
    else:
        # 正常提醒
        print(json.dumps({}))


if __name__ == "__main__":
    main()
