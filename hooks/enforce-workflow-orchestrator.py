#!/usr/bin/env python3
"""
工作流编排器强制约束 Hook
每次用户输入任务请求时，强制提醒必须先输出决策卡片
"""

import json
import sys
import re

def detect_task_request(user_input: str) -> bool:
    """检测是否为任务请求"""
    if not user_input or len(user_input.strip()) < 3:
        return False
    
    # 跳过简单对话
    skip_patterns = [
        r'^(好的|ok|yes|no|是|否|可以|行|嗯|hmm|lgtm|继续)$',
        r'^(谢谢|thanks|thank you)',
        r'^[!?。，]$',
    ]
    user_lower = user_input.strip().lower()
    for pattern in skip_patterns:
        if re.match(pattern, user_lower):
            return False
    
    # 检测跳过关键词
    skip_keywords = ['跳过评估', '直接开始', 'skip', '跳过']
    for kw in skip_keywords:
        if kw in user_lower:
            return False
    
    # 任务关键词 - 动作词
    task_keywords = [
        '实现', '修改', '添加', '修复', '创建', '删除', '重构',
        '优化', '设计', '部署', '配置', '安装', '更新', '升级',
        '帮我', '帮忙', '能不能', '怎么',
        'implement', 'modify', 'add', 'fix', 'create', 'refactor'
    ]

    # Bug/问题描述关键词 - 即使没有动作词也应触发
    bug_keywords = [
        '不显示', '不工作', '报错', '崩溃', '白屏', '失败', '问题',
        '没有正确', '不正确', '错误', '异常', 'bug', 'error', 'exception',
        '不能', '无法', '卡住', '卡顿', '慢', '丢失', '缺失'
    ]

    # 检测 Bug 描述
    for kw in bug_keywords:
        if kw in user_lower:
            return True
    
    # 发散性思维关键词
    brainstorm_keywords = [
        '你觉得', '建议', '想法', '怎么设计', '如何优化',
        '可能性', '探索', '对比', '权衡', '方案'
    ]
    
    all_keywords = task_keywords + brainstorm_keywords
    for kw in all_keywords:
        if kw in user_lower:
            return True
    
    return False

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
    
    if detect_task_request(user_input):
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": """
🔒 **工作流强制约束**

回应前**必须**输出：
1. 📊 权重分析表格
2. 🧠 发散检测（是否脑暴）
3. 🎯 工作流选择 + Skill 路由

规则见 `~/.claude/skills/workflow-orchestrator/SKILL.md`
"""
            }
        }
        print(json.dumps(output))
    else:
        print(json.dumps({}))

if __name__ == "__main__":
    main()
