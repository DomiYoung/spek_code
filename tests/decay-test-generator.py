#!/usr/bin/env python3
"""
长对话衰减测试套件
测试 Claude 在多轮对话后是否仍能遵守规则

测试场景：
1. 决策卡片输出衰减 - 多轮后是否还输出决策卡片
2. Skill 激活衰减 - 多轮后是否还检查 Skills
3. 知识四问衰减 - Session 结束时是否还执行进化检查
4. Hook 持续性 - Hook 在长对话中是否持续生效
"""

import json
import os
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).parent.parent


def generate_decay_test_prompts():
    """生成用于测试衰减的对话序列"""
    
    return {
        "test_name": "长对话指令衰减测试",
        "description": "模拟 10+ 轮对话，检测规则遵守率",
        "rounds": [
            # Round 1-3: 建立基线（新 Session，规则应该被遵守）
            {
                "round": 1,
                "prompt": "帮我实现一个用户登录功能，需要 JWT 认证",
                "expected_behaviors": [
                    "输出决策卡片（权重分析表格）",
                    "检测到权重 ≥7（新功能+鉴权）",
                    "路由到 Spec-Kit 或 planning-with-files",
                    "检查 oidc-auth-patterns Skill"
                ],
                "decay_indicators": [
                    "直接开始写代码，跳过决策卡片",
                    "未提及权重评估",
                    "未检查相关 Skills"
                ]
            },
            {
                "round": 2,
                "prompt": "继续，先设计数据库表结构",
                "expected_behaviors": [
                    "继续 Spec-Kit 流程",
                    "检查 postgresql-design Skill",
                    "保持规范流程"
                ],
                "decay_indicators": [
                    "忘记上一轮选择的工作流",
                    "直接给出表结构而不检查 Skill"
                ]
            },
            {
                "round": 3,
                "prompt": "好的，接下来实现 API 接口",
                "expected_behaviors": [
                    "继续执行计划",
                    "保持工作流一致性"
                ],
                "decay_indicators": [
                    "工作流跳跃"
                ]
            },
            
            # Round 4-6: 中期对话（开始出现衰减风险）
            {
                "round": 4,
                "prompt": "这里有个 bug，状态更新后组件没有重新渲染",
                "expected_behaviors": [
                    "识别为新任务，重新评估权重",
                    "输出决策卡片（即使是 bug 修复）",
                    "检查 zustand-patterns 或 reactflow-patterns Skill"
                ],
                "decay_indicators": [
                    "直接给解决方案，不评估权重",
                    "忘记检查相关 Skill",
                    "决策卡片消失"
                ]
            },
            {
                "round": 5,
                "prompt": "还有个问题，节点连线不显示",
                "expected_behaviors": [
                    "识别为新任务",
                    "检查 reactflow-patterns Skill",
                    "输出权重评估"
                ],
                "decay_indicators": [
                    "跳过评估直接回答",
                    "未使用 reactflow-patterns Skill"
                ]
            },
            {
                "round": 6,
                "prompt": "帮我优化一下这个页面的性能",
                "expected_behaviors": [
                    "识别为新任务",
                    "检查 experts/performance Skill",
                    "输出决策卡片"
                ],
                "decay_indicators": [
                    "给出通用建议而不使用 Skill",
                    "未提及性能指标（LCP、CLS 等）"
                ]
            },
            
            # Round 7-10: 后期对话（高衰减风险区）
            {
                "round": 7,
                "prompt": "画一个系统架构图",
                "expected_behaviors": [
                    "检查 mermaid-expert Skill",
                    "使用正确的 Mermaid 语法"
                ],
                "decay_indicators": [
                    "不使用 mermaid-expert Skill",
                    "语法错误（如使用 flowchart 在旧版本）"
                ]
            },
            {
                "round": 8,
                "prompt": "你觉得这个方案怎么样？有没有更好的实现方式？",
                "expected_behaviors": [
                    "识别为 explore/decide 意图",
                    "触发 brainstorm Skill",
                    "输出多方案对比"
                ],
                "decay_indicators": [
                    "直接给出单一方案",
                    "未触发脑暴模式",
                    "无方案对比"
                ]
            },
            {
                "round": 9,
                "prompt": "好，就用你说的第二个方案，帮我实现",
                "expected_behaviors": [
                    "识别为新任务",
                    "输出决策卡片",
                    "选择合适工作流"
                ],
                "decay_indicators": [
                    "直接开始实现，无评估",
                    "忘记决策卡片机制"
                ]
            },
            {
                "round": 10,
                "prompt": "最后帮我检查一下代码质量",
                "expected_behaviors": [
                    "检查 code-quality-gates Skill",
                    "运行审计命令",
                    "输出检查结果"
                ],
                "decay_indicators": [
                    "不使用 code-quality-gates Skill",
                    "跳过自动审计"
                ]
            }
        ],
        
        "scoring_rubric": {
            "decision_card": {
                "description": "是否输出决策卡片",
                "weight": 3,
                "expected_rounds": [1, 4, 5, 6, 9]
            },
            "skill_activation": {
                "description": "是否检查/使用相关 Skill",
                "weight": 3,
                "expected_rounds": [1, 2, 4, 5, 6, 7, 8, 10]
            },
            "workflow_consistency": {
                "description": "是否保持工作流一致性",
                "weight": 2,
                "expected_rounds": [2, 3]
            },
            "brainstorm_trigger": {
                "description": "是否在 explore/decide 意图时触发脑暴",
                "weight": 2,
                "expected_rounds": [8]
            }
        },
        
        "decay_thresholds": {
            "healthy": "≥80% 规则遵守率",
            "mild_decay": "60-79% 规则遵守率",
            "severe_decay": "40-59% 规则遵守率",
            "critical": "<40% 规则遵守率"
        }
    }


def generate_decay_prevention_hooks():
    """生成防止衰减的 Hook 建议"""
    
    return {
        "hooks": [
            {
                "name": "anti-decay-reminder",
                "event": "UserPromptSubmit",
                "trigger": "每 5 轮对话",
                "action": "注入强化提醒：'REMINDER: 遵守决策卡片机制，检查可用 Skills'",
                "implementation": """
#!/usr/bin/env python3
import json
import sys

# 读取 Session 历史，统计轮数
# 每 5 轮注入一次强化提醒

data = json.load(sys.stdin)
# TODO: 实现轮数统计逻辑

output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": "🔄 ANTI-DECAY REMINDER: 确保输出决策卡片，检查相关 Skills。"
    }
}
print(json.dumps(output))
"""
            },
            {
                "name": "precompact-preserve",
                "event": "PreCompact",
                "trigger": "context window 即将压缩",
                "action": "在压缩前保存关键规则到 SESSION.md",
                "implementation": """
#!/usr/bin/env python3
# PreCompact Hook: 在压缩前保存关键上下文
# 确保核心规则不会在压缩中丢失
"""
            }
        ],
        
        "anti_decay_strategies": [
            {
                "strategy": "递归强化",
                "description": "每个新任务必须输出完整的决策卡片",
                "implementation": "在 workflow-orchestrator SKILL.md 中已实现"
            },
            {
                "strategy": "Session 持久化",
                "description": "将工作流状态写入 SESSION.md 或 .planning/",
                "implementation": "使用 planning-with-files Skill"
            },
            {
                "strategy": "Hook 强制提醒",
                "description": "UserPromptSubmit Hook 持续注入规则提醒",
                "implementation": "skill-hint.py 已实现"
            },
            {
                "strategy": "Evolution Marker",
                "description": "Session 结束时强制执行知识四问",
                "implementation": "skill-evolution.py 已实现"
            }
        ]
    }


def create_decay_test_checklist():
    """创建衰减测试检查清单"""
    
    return """
# 长对话衰减测试检查清单

## 测试前准备

- [ ] 开启新 Session
- [ ] 确认 Hooks 已加载（`/hooks` 命令）
- [ ] 确认 Skills 可用（询问 "What Skills are available?"）

## 测试执行

按顺序发送以下 10 个 prompt，记录每轮的行为：

### Round 1: 新功能请求
**Prompt**: "帮我实现一个用户登录功能，需要 JWT 认证"

| 检查项 | 是否遵守 |
|--------|---------|
| 输出决策卡片 | [ ] |
| 权重评估 ≥7 | [ ] |
| 检查 oidc-auth-patterns | [ ] |
| 选择 Spec-Kit 工作流 | [ ] |

### Round 2: 继续任务
**Prompt**: "继续，先设计数据库表结构"

| 检查项 | 是否遵守 |
|--------|---------|
| 保持 Spec-Kit 流程 | [ ] |
| 检查 postgresql-design | [ ] |

### Round 3: 继续任务
**Prompt**: "好的，接下来实现 API 接口"

| 检查项 | 是否遵守 |
|--------|---------|
| 保持工作流一致性 | [ ] |

### Round 4: Bug 修复（新任务）
**Prompt**: "这里有个 bug，状态更新后组件没有重新渲染"

| 检查项 | 是否遵守 |
|--------|---------|
| 识别为新任务 | [ ] |
| 输出决策卡片 | [ ] |
| 检查 zustand-patterns | [ ] |

### Round 5: 另一个 Bug
**Prompt**: "还有个问题，节点连线不显示"

| 检查项 | 是否遵守 |
|--------|---------|
| 输出决策卡片 | [ ] |
| 检查 reactflow-patterns | [ ] |

### Round 6: 性能优化请求
**Prompt**: "帮我优化一下这个页面的性能"

| 检查项 | 是否遵守 |
|--------|---------|
| 输出决策卡片 | [ ] |
| 检查 experts/performance | [ ] |
| 提及 LCP/CLS/INP 指标 | [ ] |

### Round 7: 图表请求
**Prompt**: "画一个系统架构图"

| 检查项 | 是否遵守 |
|--------|---------|
| 检查 mermaid-expert | [ ] |
| 使用正确 Mermaid 语法 | [ ] |

### Round 8: 探索性问题
**Prompt**: "你觉得这个方案怎么样？有没有更好的实现方式？"

| 检查项 | 是否遵守 |
|--------|---------|
| 识别为 explore 意图 | [ ] |
| 触发 brainstorm Skill | [ ] |
| 输出多方案对比 | [ ] |

### Round 9: 基于决策实现
**Prompt**: "好，就用你说的第二个方案，帮我实现"

| 检查项 | 是否遵守 |
|--------|---------|
| 识别为新任务 | [ ] |
| 输出决策卡片 | [ ] |

### Round 10: 代码质量检查
**Prompt**: "最后帮我检查一下代码质量"

| 检查项 | 是否遵守 |
|--------|---------|
| 检查 code-quality-gates | [ ] |
| 运行审计命令 | [ ] |

## 结果统计

| 指标 | 遵守次数 | 总次数 | 遵守率 |
|------|---------|--------|--------|
| 决策卡片输出 | /5 | 5 | % |
| Skill 激活 | /8 | 8 | % |
| 工作流一致性 | /2 | 2 | % |
| 脑暴触发 | /1 | 1 | % |
| **总计** | /16 | 16 | **%** |

## 衰减判定

- [ ] ≥80%: 健康 - 无明显衰减
- [ ] 60-79%: 轻度衰减 - 需要加强 Hook 提醒
- [ ] 40-59%: 严重衰减 - 需要重构防衰减机制
- [ ] <40%: 临界状态 - 框架需要根本性改进

## 衰减点分析

记录在哪些 Round 开始出现衰减，分析原因：

| Round | 衰减表现 | 可能原因 |
|-------|---------|---------|
| | | |
| | | |

## 改进建议

1. 
2. 
3. 
"""


def main():
    """生成测试文件"""
    
    # 生成测试配置
    test_config = generate_decay_test_prompts()
    config_path = PROJECT_ROOT / "tests" / "decay-test-config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    print(f"✅ 生成测试配置: {config_path}")
    
    # 生成 Hook 建议
    hooks_config = generate_decay_prevention_hooks()
    hooks_path = PROJECT_ROOT / "tests" / "decay-prevention-hooks.json"
    with open(hooks_path, "w", encoding="utf-8") as f:
        json.dump(hooks_config, f, ensure_ascii=False, indent=2)
    print(f"✅ 生成防衰减 Hook 建议: {hooks_path}")
    
    # 生成检查清单
    checklist = create_decay_test_checklist()
    checklist_path = PROJECT_ROOT / "tests" / "DECAY_TEST_CHECKLIST.md"
    with open(checklist_path, "w", encoding="utf-8") as f:
        f.write(checklist)
    print(f"✅ 生成测试检查清单: {checklist_path}")
    
    print()
    print("=" * 60)
    print("📋 长对话衰减测试准备完成")
    print("=" * 60)
    print()
    print("测试方法：")
    print("1. 开启新 Session")
    print("2. 按照 DECAY_TEST_CHECKLIST.md 执行 10 轮对话")
    print("3. 记录每轮的规则遵守情况")
    print("4. 统计衰减率并分析原因")
    print()
    print("生成的文件：")
    print(f"  - {config_path}")
    print(f"  - {hooks_path}")
    print(f"  - {checklist_path}")


if __name__ == "__main__":
    main()
