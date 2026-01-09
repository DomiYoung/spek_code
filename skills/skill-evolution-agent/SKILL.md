---
name: skill-evolution-agent
description: |
  Skill 自进化代理 - 专注于观察、分析和优化 Skills 系统。
  ① 帮我干什么：从执行历史中提取模式，自动改进 Skills
  ② 什么时候出场：每周/每 N 次会话后/手动触发
  ③ 和项目有无关系：适用于所有项目，是 Skills 系统的元优化器
triggers:
  - "/evolve-skills"
  - "优化 skills"
  - "检查 skills"
  - "skill 进化"
---

# Skill Evolution Agent（Skill 自进化代理）

> **Agent 类型**：Meta-Learning（元学习型）
> **核心理念**：从 AI 的错误中学习，让 Skills 系统自己变得更聪明。这是一个"训练 AI 的 AI"。

---

## 架构定位

```
┌──────────────────────────────────────────────────────────────────┐
│                        双循环架构                                 │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   ┌─────────────┐     执行      ┌─────────────────────────┐     │
│   │  主 Agent   │ ────────────→ │ 任务完成 / 踩坑记录     │     │
│   │(你平时用的) │               │ (pitfalls.md)           │     │
│   └─────────────┘               └───────────┬─────────────┘     │
│          ↑                                   │                   │
│          │                                   ↓                   │
│   ┌──────┴──────┐     观察      ┌─────────────────────────┐     │
│   │ 更新 Skills │ ←──────────── │  Skill-Evolution Agent  │     │
│   │ (更好的)    │               │  (本 Skill)             │     │
│   └─────────────┘               └─────────────────────────┘     │
│                                                                  │
│   快循环：任务执行（秒/分钟级）                                    │
│   慢循环：Skill 进化（日/周级）                                   │
└──────────────────────────────────────────────────────────────────┘
```

---

## 触发条件

| 条件 | 频率 | 说明 |
|------|------|------|
| **定期触发** | 每周一次 | 建议周末运行 |
| **累计触发** | 每 50 次会话 | 自动统计 |
| **手动触发** | `/evolve-skills` | 用户主动调用 |
| **事件触发** | pitfalls 新增 3+ 条 | 足够的学习样本 |

---

## 输入源

| 数据源 | 路径 | 用途 |
|--------|------|------|
| **全局踩坑** | `~/.ai-knowledge/global/pitfalls.md` | 跨项目问题模式 |
| **领域踩坑** | `~/.ai-knowledge/domains/*/pitfalls.md` | 技术栈问题模式 |
| **项目踩坑** | `~/.ai-knowledge/projects/*/pitfalls.md` | 项目特定问题 |
| **Serena Memory** | Serena 工具 | 代码符号记忆 |
| **Skills 定义** | `~/.claude/skills/*/SKILL.md` | 现有 Skill 内容 |

---

## 执行流程

```
Step 1: 收集数据
    │
    ▼
Step 2: 模式识别
    │
    ▼
Step 3: 改进建议
    │
    ▼
Step 4: 人工审核
    │
    ▼
Step 5: 应用更新
```

---

## Step 1: 收集数据

### 收集命令

```bash
# 收集所有 pitfalls
find ~/.ai-knowledge -name "pitfalls.md" -exec cat {} \;

# 收集所有 Skills
find ~/.claude/skills -name "SKILL.md" -exec cat {} \;

# 统计踩坑数量
grep -c "^### \[" ~/.ai-knowledge/*/pitfalls.md
```

### 输出格式

```
╔════════════════════════════════════════════════════════════╗
║  📊 数据收集报告                                            ║
╠════════════════════════════════════════════════════════════╣
║  数据源               │  条目数  │  最近更新               ║
╠───────────────────────┼──────────┼─────────────────────────╣
║  全局踩坑              │  5       │  2026-01-08            ║
║  frontend 领域踩坑     │  8       │  2026-01-09            ║
║  backend 领域踩坑      │  3       │  2026-01-05            ║
║  react_ai 项目踩坑     │  2       │  2026-01-07            ║
║  ─────────────────────┼──────────┼─────────────────────────║
║  Skills 总数          │  45      │  -                      ║
║  本周活跃 Skills       │  12      │  -                      ║
╚════════════════════════════════════════════════════════════╝
```

---

## Step 2: 模式识别

### 分析维度

| 维度 | 说明 | 阈值 |
|------|------|------|
| **重复问题** | 同类问题出现 N 次 | N ≥ 3 触发 |
| **Skill 覆盖** | 问题是否有对应 Skill | 无覆盖 = 缺口 |
| **Skill 失效** | 有 Skill 但仍出问题 | 需要改进 |
| **关联模式** | 问题之间的关联 | 可合并 |

### 输出格式

```
╔════════════════════════════════════════════════════════════╗
║  🔍 模式识别结果                                            ║
╠════════════════════════════════════════════════════════════╣
║                                                            ║
║  🔴 重复问题模式（需立即处理）                               ║
║  ┌────────────────────────────────────────────────────────┐║
║  │ 1. "useEffect 依赖数组" - 出现 4 次                     ║│
║  │    → 现有 Skill: react-patterns (未覆盖此场景)          ║│
║  │    → 建议: 添加 exhaustive-deps 检查规则               ║│
║  │                                                        ║│
║  │ 2. "Zustand selector 无限渲染" - 出现 3 次             ║│
║  │    → 现有 Skill: zustand-patterns (规则不足)           ║│
║  │    → 建议: 添加 shallow 比较红线规则                   ║│
║  └────────────────────────────────────────────────────────┘║
║                                                            ║
║  🟡 覆盖缺口（建议处理）                                     ║
║  ┌────────────────────────────────────────────────────────┐║
║  │ 1. "环境变量 fallback" - 无对应 Skill                   ║│
║  │    → 建议: 创建 env-config-patterns Skill              ║│
║  └────────────────────────────────────────────────────────┘║
║                                                            ║
║  🟢 已良好覆盖                                               ║
║  ┌────────────────────────────────────────────────────────┐║
║  │ - ReactFlow 相关问题: reactflow-patterns 覆盖良好      ║│
║  │ - SignalR 相关问题: signalr-patterns 覆盖良好          ║│
║  └────────────────────────────────────────────────────────┘║
╚════════════════════════════════════════════════════════════╝
```

---

## Step 3: 改进建议

### 建议类型

| 类型 | 说明 | 优先级 |
|------|------|--------|
| **新增 Skill** | 覆盖新的问题领域 | 中 |
| **修改 Skill** | 增加规则或修正逻辑 | 高 |
| **合并 Skill** | 相似 Skills 合并 | 低 |
| **废弃 Skill** | 不再适用的 Skill | 低 |

### 输出格式：Patch 建议

```markdown
## 📝 Skill 改进建议 #1

**目标 Skill**: `~/.claude/skills/zustand-patterns/SKILL.md`
**改进类型**: 修改（添加规则）
**触发原因**: "Zustand selector 无限渲染" 问题出现 3 次

### 建议的 Patch

\`\`\`diff
## 红线规则

+ ### [新增] Selector 必须使用 shallow 比较
+ 
+ **问题**: 返回新对象的 selector 会导致无限重渲染
+ 
+ \`\`\`typescript
+ // ❌ 错误 - 每次返回新对象
+ const data = useStore(state => ({ a: state.a, b: state.b }));
+ 
+ // ✅ 正确 - 使用 shallow
+ import { shallow } from 'zustand/shallow';
+ const data = useStore(state => ({ a: state.a, b: state.b }), shallow);
+ \`\`\`
+ 
+ **检测**: grep "useStore.*=>" | 检查是否有 shallow
\`\`\`

### 验证方式
- [ ] 应用 patch 后，zustand-patterns Skill 包含新规则
- [ ] 下次遇到类似问题时，Skill 应提前警告
```

---

## Step 4: 人工审核

### 审核流程

```
建议生成
    │
    ▼
┌─────────────────────────────────────────┐
│ 输出到: ~/.claude/skills/PENDING_CHANGES.md │
└─────────────────────────────────────────┘
    │
    ▼
人工审核（用户）
    │
    ├─→ 批准 → Step 5: 应用更新
    │
    └─→ 拒绝 → 记录拒绝原因，供下次参考
```

### PENDING_CHANGES.md 格式

```markdown
# Skill 待审核变更

> 生成时间: 2026-01-09 20:30
> 触发原因: pitfalls 新增 5 条

## 待审核列表

### [PENDING-001] zustand-patterns 添加 shallow 规则
- **状态**: ⏳ 待审核
- **优先级**: 高
- **Patch**: 见下方
- **批准**: `/approve PENDING-001`
- **拒绝**: `/reject PENDING-001 <原因>`

---

### [PENDING-002] 创建 env-config-patterns Skill
- **状态**: ⏳ 待审核
- **优先级**: 中
...
```

---

## Step 5: 应用更新

### 应用命令

```bash
# 批准单个变更
/approve PENDING-001

# 批准所有变更
/approve-all

# 拒绝变更
/reject PENDING-001 "规则过于严格"
```

### 应用后自动操作

1. 修改目标 Skill 文件
2. 更新 Skills 索引
3. 记录变更历史到 `~/.claude/skills/CHANGELOG.md`
4. 清理 PENDING_CHANGES.md 中已处理的条目

---

## 自动触发配置

### settings.json 配置示例

```json
{
  "hooks": {
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/check-skill-evolution.py"
          }
        ]
      }
    ]
  }
}
```

### check-skill-evolution.py

```python
#!/usr/bin/env python3
"""
检查是否需要触发 Skill 进化
条件：pitfalls 新增 >= 3 条 且 距离上次进化 >= 7 天
"""
import os
import subprocess
from datetime import datetime, timedelta

LAST_EVOLUTION_FILE = os.path.expanduser("~/.claude/skills/.last_evolution")
PITFALL_THRESHOLD = 3

def count_recent_pitfalls():
    # 统计最近 7 天的 pitfalls
    # ... 实现略
    return 5

def days_since_last_evolution():
    if not os.path.exists(LAST_EVOLUTION_FILE):
        return 999
    with open(LAST_EVOLUTION_FILE) as f:
        last = datetime.fromisoformat(f.read().strip())
    return (datetime.now() - last).days

def main():
    recent = count_recent_pitfalls()
    days = days_since_last_evolution()
    
    if recent >= PITFALL_THRESHOLD and days >= 7:
        print("🧬 检测到 Skill 进化条件满足，建议运行 /evolve-skills")

if __name__ == "__main__":
    main()
```

---

## 使用示例

### 手动触发

```
用户: /evolve-skills

AI: 🧬 启动 Skill Evolution Agent...

📊 数据收集中...
[收集报告]

🔍 模式识别中...
[模式识别结果]

📝 生成改进建议...
[Patch 建议列表]

已生成 3 个待审核变更，请查看:
~/.claude/skills/PENDING_CHANGES.md

使用 /approve <ID> 或 /reject <ID> <原因> 处理
```

---

## 红线规则

| 规则 | 状态 |
|------|------|
| 不自动应用变更，必须人工审核 | ❌ **Forbidden** 自动应用 |
| 不删除现有 Skill 内容，只添加 | ❌ **Forbidden** 直接删除 |
| 变更必须记录到 CHANGELOG | ❌ **Forbidden** 跳过记录 |
| 每次最多建议 5 个变更 | 避免信息过载 |

---

## 与其他组件的关系

```
ki-manager                    skill-evolution-agent
    │                                │
    │ 写入 pitfalls.md               │ 读取 pitfalls.md
    ▼                                ▼
┌─────────────────────────────────────────────┐
│              ~/.ai-knowledge/                │
│              pitfalls.md                     │
└─────────────────────────────────────────────┘
                     │
                     │ 分析后生成 patch
                     ▼
┌─────────────────────────────────────────────┐
│              ~/.claude/skills/              │
│              各个 SKILL.md                  │
└─────────────────────────────────────────────┘
```

---

## 核心价值

| 对比维度 | VibeCoding 278 Skills | 你的自进化 Skills |
|---------|----------------------|------------------|
| **来源** | 人工策划 | 从实际错误中学习 |
| **更新** | 等社区更新 | 自动持续进化 |
| **针对性** | 通用 | 针对你的项目和习惯 |
| **覆盖** | 固定领域 | 动态扩展 |

> **这是 SPEK 的终极形态**：E (Evolution) 不只是被动记录，而是主动进化整个系统。
