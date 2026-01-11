#!/usr/bin/env python3
"""
40 轮长对话衰减压力测试
包含干扰轮次（无关对话）后的回归测试
"""

import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def generate_40_round_stress_test():
    """生成 40 轮压力测试配置"""
    
    rounds = []
    
    # ========== Phase 1: 基线建立 (Round 1-5) ==========
    rounds.extend([
        {
            "round": 1,
            "phase": "baseline",
            "type": "task",
            "prompt": "帮我实现一个用户登录功能，需要 JWT 认证",
            "expected": ["决策卡片", "权重≥7", "oidc-auth-patterns", "Spec-Kit"],
            "critical": True
        },
        {
            "round": 2,
            "phase": "baseline",
            "type": "continue",
            "prompt": "继续，先设计数据库表结构",
            "expected": ["保持Spec-Kit", "postgresql-design"],
            "critical": False
        },
        {
            "round": 3,
            "phase": "baseline",
            "type": "continue",
            "prompt": "好的，接下来实现 API 接口",
            "expected": ["工作流一致性"],
            "critical": False
        },
        {
            "round": 4,
            "phase": "baseline",
            "type": "task",
            "prompt": "这里有个 bug，状态更新后组件没有重新渲染",
            "expected": ["识别新任务", "决策卡片", "zustand-patterns"],
            "critical": True
        },
        {
            "round": 5,
            "phase": "baseline",
            "type": "task",
            "prompt": "帮我优化一下这个页面的性能",
            "expected": ["决策卡片", "experts/performance", "LCP/CLS指标"],
            "critical": True
        },
    ])
    
    # ========== Phase 2: 第一次干扰 (Round 6-10) ==========
    rounds.extend([
        {
            "round": 6,
            "phase": "distraction_1",
            "type": "offtopic",
            "prompt": "今天天气怎么样？",
            "expected": ["识别为非任务"],
            "critical": False
        },
        {
            "round": 7,
            "phase": "distraction_1",
            "type": "offtopic",
            "prompt": "给我讲个笑话",
            "expected": ["识别为非任务"],
            "critical": False
        },
        {
            "round": 8,
            "phase": "distraction_1",
            "type": "offtopic",
            "prompt": "你觉得 AI 会取代程序员吗？",
            "expected": ["识别为讨论"],
            "critical": False
        },
        {
            "round": 9,
            "phase": "distraction_1",
            "type": "offtopic",
            "prompt": "推荐一本编程书籍",
            "expected": ["识别为非任务"],
            "critical": False
        },
        {
            "round": 10,
            "phase": "distraction_1",
            "type": "offtopic",
            "prompt": "解释一下什么是闭包",
            "expected": ["识别为知识问答"],
            "critical": False
        },
    ])
    
    # ========== Phase 3: 第一次回归测试 (Round 11-15) ==========
    rounds.extend([
        {
            "round": 11,
            "phase": "regression_1",
            "type": "task",
            "prompt": "帮我实现一个文件上传功能",
            "expected": ["决策卡片", "权重评估", "工作流选择"],
            "critical": True,
            "regression_check": "干扰后是否恢复决策卡片机制"
        },
        {
            "round": 12,
            "phase": "regression_1",
            "type": "task",
            "prompt": "节点之间的连线不显示，帮我看看",
            "expected": ["决策卡片", "reactflow-patterns"],
            "critical": True,
            "regression_check": "是否检查 Skill"
        },
        {
            "round": 13,
            "phase": "regression_1",
            "type": "explore",
            "prompt": "这个功能有几种实现方式？你觉得哪种更好？",
            "expected": ["识别explore意图", "brainstorm", "多方案对比"],
            "critical": True,
            "regression_check": "是否触发脑暴"
        },
        {
            "round": 14,
            "phase": "regression_1",
            "type": "task",
            "prompt": "画一个系统架构图",
            "expected": ["mermaid-expert", "正确语法"],
            "critical": True,
            "regression_check": "是否使用 Skill"
        },
        {
            "round": 15,
            "phase": "regression_1",
            "type": "task",
            "prompt": "帮我检查一下代码质量",
            "expected": ["code-quality-gates", "审计命令"],
            "critical": True,
            "regression_check": "是否运行审计"
        },
    ])
    
    # ========== Phase 4: 持续工作 (Round 16-20) ==========
    rounds.extend([
        {
            "round": 16,
            "phase": "sustained",
            "type": "task",
            "prompt": "创建一个 Zustand store 来管理用户状态",
            "expected": ["zustand-patterns", "store设计规范"],
            "critical": True
        },
        {
            "round": 17,
            "phase": "sustained",
            "type": "continue",
            "prompt": "添加一个 selector 来获取当前用户信息",
            "expected": ["保持 zustand 上下文"],
            "critical": False
        },
        {
            "round": 18,
            "phase": "sustained",
            "type": "task",
            "prompt": "实现 SignalR 实时消息推送",
            "expected": ["决策卡片", "signalr-patterns"],
            "critical": True
        },
        {
            "round": 19,
            "phase": "sustained",
            "type": "continue",
            "prompt": "添加断线重连机制",
            "expected": ["保持 signalr 上下文"],
            "critical": False
        },
        {
            "round": 20,
            "phase": "sustained",
            "type": "task",
            "prompt": "用 React Query 封装 API 请求",
            "expected": ["react-query-patterns"],
            "critical": True
        },
    ])
    
    # ========== Phase 5: 第二次干扰 (Round 21-25) ==========
    rounds.extend([
        {
            "round": 21,
            "phase": "distraction_2",
            "type": "offtopic",
            "prompt": "你会下象棋吗？",
            "expected": ["识别为非任务"],
            "critical": False
        },
        {
            "round": 22,
            "phase": "distraction_2",
            "type": "offtopic",
            "prompt": "帮我写一首关于编程的诗",
            "expected": ["识别为创意任务"],
            "critical": False
        },
        {
            "round": 23,
            "phase": "distraction_2",
            "type": "offtopic",
            "prompt": "什么是量子计算？",
            "expected": ["识别为知识问答"],
            "critical": False
        },
        {
            "round": 24,
            "phase": "distraction_2",
            "type": "offtopic",
            "prompt": "推荐一个好用的 VSCode 插件",
            "expected": ["识别为非任务"],
            "critical": False
        },
        {
            "round": 25,
            "phase": "distraction_2",
            "type": "offtopic",
            "prompt": "你最喜欢什么编程语言？",
            "expected": ["识别为讨论"],
            "critical": False
        },
    ])
    
    # ========== Phase 6: 第二次回归测试 (Round 26-30) ==========
    rounds.extend([
        {
            "round": 26,
            "phase": "regression_2",
            "type": "task",
            "prompt": "实现一个复杂的表单验证，包含多步骤和条件逻辑",
            "expected": ["决策卡片", "权重≥7", "react-hook-form-patterns"],
            "critical": True,
            "regression_check": "长时间干扰后是否恢复"
        },
        {
            "round": 27,
            "phase": "regression_2",
            "type": "task",
            "prompt": "这个表格数据量很大，需要虚拟滚动",
            "expected": ["决策卡片", "virtual-list-patterns或ag-grid"],
            "critical": True,
            "regression_check": "是否检查相关 Skill"
        },
        {
            "round": 28,
            "phase": "regression_2",
            "type": "explore",
            "prompt": "数据缓存应该放在前端还是后端？有什么权衡？",
            "expected": ["识别explore", "brainstorm", "多方案分析"],
            "critical": True,
            "regression_check": "是否触发脑暴"
        },
        {
            "round": 29,
            "phase": "regression_2",
            "type": "task",
            "prompt": "重构这个模块，拆分成更小的组件",
            "expected": ["决策卡片", "权重评估"],
            "critical": True,
            "regression_check": "重构任务是否正确评估"
        },
        {
            "round": 30,
            "phase": "regression_2",
            "type": "task",
            "prompt": "添加 IndexedDB 离线缓存支持",
            "expected": ["决策卡片", "indexeddb-patterns"],
            "critical": True,
            "regression_check": "是否使用专门 Skill"
        },
    ])
    
    # ========== Phase 7: 高压测试 (Round 31-35) ==========
    rounds.extend([
        {
            "round": 31,
            "phase": "stress",
            "type": "rapid",
            "prompt": "快速修复：按钮点击没反应",
            "expected": ["快速评估", "识别简单bug"],
            "critical": False
        },
        {
            "round": 32,
            "phase": "stress",
            "type": "rapid",
            "prompt": "样式问题：边距不对",
            "expected": ["识别为简单样式问题", "权重低"],
            "critical": False
        },
        {
            "round": 33,
            "phase": "stress",
            "type": "task",
            "prompt": "实现 OAuth2 第三方登录，支持 Google 和 GitHub",
            "expected": ["决策卡片", "权重≥7", "oidc-auth-patterns"],
            "critical": True
        },
        {
            "round": 34,
            "phase": "stress",
            "type": "rapid",
            "prompt": "console 有个警告，帮我看看",
            "expected": ["快速诊断"],
            "critical": False
        },
        {
            "round": 35,
            "phase": "stress",
            "type": "task",
            "prompt": "设计一个插件系统架构",
            "expected": ["决策卡片", "权重≥7", "experts/architect"],
            "critical": True
        },
    ])
    
    # ========== Phase 8: 最终回归测试 (Round 36-40) ==========
    rounds.extend([
        {
            "round": 36,
            "phase": "final_regression",
            "type": "task",
            "prompt": "帮我实现一个工作流编辑器，支持节点拖拽和连线",
            "expected": ["决策卡片", "权重≥7", "reactflow-patterns", "Spec-Kit"],
            "critical": True,
            "regression_check": "40轮后复杂任务处理"
        },
        {
            "round": 37,
            "phase": "final_regression",
            "type": "explore",
            "prompt": "这个编辑器的状态管理方案，你有什么建议？",
            "expected": ["brainstorm", "多方案对比", "zustand/redux对比"],
            "critical": True,
            "regression_check": "是否仍能触发脑暴"
        },
        {
            "round": 38,
            "phase": "final_regression",
            "type": "task",
            "prompt": "性能分析一下这个页面，找出瓶颈",
            "expected": ["experts/performance", "具体指标", "工具推荐"],
            "critical": True,
            "regression_check": "是否使用性能专家 Skill"
        },
        {
            "round": 39,
            "phase": "final_regression",
            "type": "task",
            "prompt": "画一个完整的系统架构图，包含前后端和数据流",
            "expected": ["mermaid-expert", "正确语法", "完整图表"],
            "critical": True,
            "regression_check": "是否使用 mermaid Skill"
        },
        {
            "round": 40,
            "phase": "final_regression",
            "type": "task",
            "prompt": "最后，帮我做一个完整的代码审查，检查所有文件",
            "expected": ["code-quality-gates", "review-quality-gates", "完整审计"],
            "critical": True,
            "regression_check": "最终回归：是否完整遵守规则"
        },
    ])
    
    return {
        "test_name": "40轮长对话衰减压力测试",
        "total_rounds": 40,
        "phases": {
            "baseline": {"rounds": "1-5", "description": "建立基线"},
            "distraction_1": {"rounds": "6-10", "description": "第一次干扰（无关对话）"},
            "regression_1": {"rounds": "11-15", "description": "第一次回归测试"},
            "sustained": {"rounds": "16-20", "description": "持续工作"},
            "distraction_2": {"rounds": "21-25", "description": "第二次干扰"},
            "regression_2": {"rounds": "26-30", "description": "第二次回归测试"},
            "stress": {"rounds": "31-35", "description": "高压混合测试"},
            "final_regression": {"rounds": "36-40", "description": "最终回归测试"}
        },
        "rounds": rounds,
        "critical_checkpoints": [r["round"] for r in rounds if r.get("critical")],
        "regression_checkpoints": [r["round"] for r in rounds if r.get("regression_check")],
        "scoring": {
            "total_critical": len([r for r in rounds if r.get("critical")]),
            "total_regression": len([r for r in rounds if r.get("regression_check")])
        }
    }


def generate_40_round_checklist():
    """生成 40 轮测试检查清单"""
    
    test_config = generate_40_round_stress_test()
    
    checklist = f"""
# 40 轮长对话衰减压力测试检查清单

> 测试目标：验证在长对话 + 干扰轮次后，框架规则是否仍被遵守

## 测试概览

| 阶段 | 轮次 | 类型 | 目的 |
|------|------|------|------|
| baseline | 1-5 | 正常任务 | 建立基线 |
| distraction_1 | 6-10 | 无关对话 | 第一次干扰 |
| regression_1 | 11-15 | 正常任务 | 第一次回归 |
| sustained | 16-20 | 持续工作 | 连续任务 |
| distraction_2 | 21-25 | 无关对话 | 第二次干扰 |
| regression_2 | 26-30 | 正常任务 | 第二次回归 |
| stress | 31-35 | 混合快速 | 高压测试 |
| final_regression | 36-40 | 正常任务 | 最终回归 |

## 关键检查点

共 {test_config['scoring']['total_critical']} 个关键检查点，{test_config['scoring']['total_regression']} 个回归检查点

---

## 测试执行

"""
    
    for round_data in test_config["rounds"]:
        round_num = round_data["round"]
        phase = round_data["phase"]
        prompt = round_data["prompt"]
        expected = round_data["expected"]
        is_critical = round_data.get("critical", False)
        regression_check = round_data.get("regression_check", "")
        
        critical_marker = "🔴" if is_critical else "⚪"
        regression_marker = f"\n**回归检查**: {regression_check}" if regression_check else ""
        
        checklist += f"""
### Round {round_num} [{phase}] {critical_marker}

**Prompt**: "{prompt}"

| 期望行为 | 是否遵守 |
|----------|---------|
"""
        for exp in expected:
            checklist += f"| {exp} | [ ] |\n"
        
        if regression_marker:
            checklist += regression_marker + "\n"
        
        checklist += "\n"
    
    checklist += """
---

## 结果统计

### 按阶段统计

| 阶段 | 遵守/总计 | 遵守率 |
|------|----------|--------|
| baseline (1-5) | /13 | % |
| regression_1 (11-15) | /14 | % |
| sustained (16-20) | /8 | % |
| regression_2 (26-30) | /12 | % |
| stress (31-35) | /7 | % |
| final_regression (36-40) | /14 | % |

### 回归测试对比

| 对比项 | regression_1 | regression_2 | final_regression |
|--------|-------------|--------------|-----------------|
| 决策卡片输出 | % | % | % |
| Skill 激活 | % | % | % |
| 脑暴触发 | % | % | % |

### 衰减趋势

```
基线(1-5)    第一次回归(11-15)    第二次回归(26-30)    最终回归(36-40)
   |              |                    |                    |
  [%]    →      [%]         →        [%]        →         [%]
```

## 衰减判定

- [ ] 无衰减：所有回归测试 ≥80%
- [ ] 轻度衰减：部分回归 60-79%
- [ ] 严重衰减：回归测试 <60%
- [ ] 干扰敏感：干扰后回归明显下降

## 分析与建议

### 衰减点识别

| 开始衰减轮次 | 衰减表现 | 可能原因 |
|-------------|---------|---------|
| | | |

### 干扰影响分析

| 干扰阶段 | 回归恢复情况 | 分析 |
|---------|-------------|------|
| distraction_1 (6-10) | | |
| distraction_2 (21-25) | | |

### 改进建议

1. 
2. 
3. 
"""
    
    return checklist


def main():
    # 生成测试配置
    test_config = generate_40_round_stress_test()
    config_path = PROJECT_ROOT / "tests" / "stress-40-config.json"
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(test_config, f, ensure_ascii=False, indent=2)
    print(f"✅ 生成 40 轮测试配置: {config_path}")
    
    # 生成检查清单
    checklist = generate_40_round_checklist()
    checklist_path = PROJECT_ROOT / "tests" / "STRESS_40_CHECKLIST.md"
    with open(checklist_path, "w", encoding="utf-8") as f:
        f.write(checklist)
    print(f"✅ 生成 40 轮测试清单: {checklist_path}")
    
    # 打印测试摘要
    print()
    print("=" * 60)
    print("📋 40 轮压力测试准备完成")
    print("=" * 60)
    print()
    print(f"总轮数: {test_config['total_rounds']}")
    print(f"关键检查点: {test_config['scoring']['total_critical']} 个")
    print(f"回归检查点: {test_config['scoring']['total_regression']} 个")
    print()
    print("阶段分布:")
    for phase, info in test_config["phases"].items():
        print(f"  - {phase}: {info['rounds']} ({info['description']})")


if __name__ == "__main__":
    main()
