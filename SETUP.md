# Claude Code 配置同步指南

> 基于官方文档 (https://code.claude.com/docs) 的最佳实践

## 📦 仓库信息

- **GitHub**: https://github.com/DomiYoung/spek_code.git
- **本地路径**: `~/.claude/` (实际: `~/Library/Mobile Documents/com~apple~CloudDocs/.claude/`)

---

## 🏗️ 目录结构 (符合官方指南)

```
~/.claude/
├── settings.json           # 共享配置 (已脱敏) ✅
├── settings.local.json     # 本地敏感配置 (不同步) ⚠️
├── CLAUDE.md               # 用户 Memory (支持 @import)
├── skills/                 # 用户 Skills (48个)
│   └── [skill-name]/
│       ├── SKILL.md        # 技能定义 (YAML + Markdown)
│       ├── reference.md    # 详细文档 (按需加载)
│       └── scripts/        # 工具脚本
├── agents/                 # 用户 Sub-agents (空)
├── rules/                  # 模块化规则 (空)
├── commands/               # 自定义命令
└── [配置文件].md           # SuperClaude 框架文件
```

---

## 🔧 配置优先级 (官方规范)

1. **Managed settings** (企业策略)
2. **Command line arguments**
3. **Local project settings** (`.claude/settings.local.json`)
4. **Shared project settings** (`.claude/settings.json`)
5. **User settings** (`~/.claude/settings.json`) ← 本仓库

---

## 🚀 第二台电脑设置

### 方法 1: Git Clone

```bash
# 1. 备份现有配置
[ -d ~/.claude ] && mv ~/.claude ~/.claude.backup.$(date +%Y%m%d)

# 2. 克隆配置仓库
git clone https://github.com/DomiYoung/spek_code.git ~/.claude

# 3. 创建本地敏感配置
cat > ~/.claude/settings.local.json << 'EOF'
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "_comment": "本地敏感配置 - 请填入你的 API Key",
  "env": {
    "ANTHROPIC_API_KEY": "你的-API-KEY",
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:8046"
  }
}
EOF

echo "✅ 配置同步完成！请编辑 ~/.claude/settings.local.json 填入 API Key"
```

### 方法 2: 符号链接 (如果本地文件夹已存在)

```bash
# 假设 spek_code 已在 /Users/jinjia/Desktop/air_files/spek_code
ln -sf /Users/jinjia/Desktop/air_files/spek_code ~/.claude
```

---

## 📚 官方 Skills 指南

### SKILL.md 格式

```yaml
---
name: skill-name
description: "技能描述。触发条件：当用户..."
allowed-tools: tool1, tool2  # 可选：限制工具
context: fork                 # 可选：隔离上下文
user-invocable: true         # 可选：显示在 /commands 菜单
---

# 技能名称

## 指令
提供清晰的步骤指导...

## 示例
展示具体使用示例...
```

### Skills 最佳实践

- **SKILL.md 保持 500 行以内**
- **使用渐进式披露**: 详细内容放在单独文件，按需加载
- **描述要具体**: 包含 "what" 和 "when"
- **使用 allowed-tools**: 增强安全性

---

## 🤖 官方 Sub-agents 指南

### Agent 文件格式

```yaml
---
name: agent-name
description: 何时调用此 agent
tools: tool1, tool2           # 可选
model: sonnet                 # 可选
skills: skill1, skill2        # 可选
---

Agent 的系统提示...
```

### 存储位置

- **用户 agents**: `~/.claude/agents/`
- **项目 agents**: `.claude/agents/`

---

## 🧠 Memory 系统

### CLAUDE.md 导入语法

```markdown
# Project Overview
See @README for project overview and @package.json for available npm commands.

# Additional Instructions
- git workflow @docs/git-instructions.md
```

### Memory 层级

1. **Enterprise Policy** → 组织策略
2. **Project Memory** → `./CLAUDE.md`
3. **Project Rules** → `.claude/rules/`
4. **User Memory** → `~/.claude/CLAUDE.md` ← 本仓库
5. **Project Local** → `./CLAUDE.local.md`

---

## 🔄 日常同步

```bash
# 拉取更新
cd ~/.claude && git pull

# 保存修改
cd ~/.claude && git add . && git commit -m "update: 描述" && git push

# 快捷别名 (添加到 ~/.zshrc)
alias claude-sync="cd ~/.claude && git pull"
alias claude-save="cd ~/.claude && git add . && git commit -m 'update config' && git push"
```

---

## ⚠️ 安全注意事项

| 文件 | 同步状态 | 说明 |
|------|---------|------|
| settings.json | ✅ 同步 | 共享配置 (已脱敏) |
| settings.local.json | ❌ 不同步 | 包含 API Key |
| skills/ | ✅ 同步 | 48 个自定义技能 |
| agents/ | ✅ 同步 | Sub-agents (空) |
| rules/ | ✅ 同步 | 模块化规则 (空) |

---

## 📊 当前配置统计

- **Skills**: 48 个
- **Commands**: 17 个
- **配置文件**: 351 个
- **最后更新**: 2025-01-09

---

## 🔗 参考资源

- [Claude Code 官方文档](https://code.claude.com/docs)
- [Skills 指南](https://code.claude.com/docs/en/skills)
- [Sub-agents 指南](https://code.claude.com/docs/en/sub-agents)
- [Settings 配置](https://code.claude.com/docs/en/settings)
- [Memory 系统](https://code.claude.com/docs/en/memory)
