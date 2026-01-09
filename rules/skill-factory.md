# Skill Factory Protocol

> Skill 创建的生产标准，由 RULES.md 引用

## 强制行为

所有知识库文件 (**Knowledge Items**) 必须遵循 "Skill Factory" 生产标准。拒绝任何"手工作坊"式的通用建议。

## 1. 模版强制 (The Mold)

创建新 Skill 前，必须读取并遵循：
`~/.claude/templates/skill-definition-template.md`

## 2. 核心三要素 (The Trinity)

任何 Skill 必须包含以下三部分，否则视为无效：

| 要素 | 说明 |
|------|------|
| **Hard Constraints (红线)** | 明确什么代码会被拒绝 (Must reject) |
| **Audit Logic (审计)** | 提供 Regex 或 Script 自动检测违规 (Must detect) |
| **Self-Correction (自愈)** | 用户该怎么改 (Must fix) |

## 3. 质量阈值 (The Bar)

- **Score < 7**: 禁止入库
- **Specificity**: 必须包含 2+ 个具体命令/配置/代码块
- **Falsifiability**: 建议必须是可验证真伪的（例如 "P99 < 100ms" vs "高性能"）

## 4. 目录规范

```
~/.claude/
├── knowledge/          # 存放 Skill 详情 (必须通过 audit_skills.py)
├── skills/             # Skill 定义文件
│   └── {skill-name}.md
├── AGENTS.md           # 仅做路由索引 (引用 skills/knowledge)
```

## 5. 质量示例

✅ **Right**:
- Database Expert: "CREATE TABLE must have PRIMARY KEY. Audit: `grep 'PRIMARY KEY'`" (Score: 10)

❌ **Wrong**:
- Database Expert: "Remember to use primary keys for better performance." (Score: 3 -> **REJECT**)

## 6. 强制路径

```
创建新 Skill
    ↓
┌─ 强制路径 ─────────────────────────────────────┐
│ 1. 创建文件: ~/.claude/skills/{skill-name}.md  │
│ 2. 如有知识库: ~/.claude/knowledge/{name}.md   │
│ 3. AGENTS.md 仅添加引用（<10行）               │
│ 4. 禁止在 AGENTS.md 直接添加完整定义           │
└─────────────────────────────────────────────────┘
```

## 7. AGENTS.md 引用格式

```xml
<skill>
<name>skill-name</name>
<description>"简短描述"</description>
<trigger>触发关键词</trigger>
<location>global</location>
<source>~/.claude/skills/skill-name.md</source>
</skill>
```

## 8. 违规检测

| 行为 | 判定 | 处理 |
|------|------|------|
| AGENTS.md 新增 >20 行 | ❌ 违规 | 拆分到 skills/ |
| 直接添加完整 `<knowledge-base>` | ❌ 违规 | 移到 knowledge/ |
| 单个 skill 定义 >10 行 | ⚠️ 警告 | 考虑拆分 |

**Detection**: 每次修改 AGENTS.md 前检查行数变化
