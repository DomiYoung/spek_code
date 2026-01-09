# Claude Code 配置同步指南

## 当前状态

✅ Git 仓库已初始化
✅ 敏感信息已脱敏 (settings.local.json)
✅ .gitignore 已配置
⏳ 需要推送到远程仓库

---

## 步骤 1: 登录 GitHub CLI (当前电脑)

```bash
# 登录 GitHub
gh auth login

# 创建私有仓库并推送
cd ~/.claude
gh repo create claude-config --private --source=. --push
```

**或者手动创建仓库：**

1. 访问 https://github.com/new
2. 仓库名: `claude-config`
3. 选择 **Private**
4. 不要勾选 "Add a README"
5. 创建后执行：

```bash
cd ~/.claude
git remote add origin git@github.com:你的用户名/claude-config.git
git push -u origin main
```

---

## 步骤 2: 第二台电脑设置

在第二台 Mac 上执行以下命令：

```bash
#!/bin/bash
# === Claude Code 配置同步脚本 ===

# 1. 备份现有配置
if [ -d ~/.claude ]; then
    mv ~/.claude ~/.claude.backup.$(date +%Y%m%d)
    echo "✅ 已备份现有配置"
fi

# 2. 克隆配置仓库
git clone git@github.com:你的用户名/claude-config.git ~/.claude
echo "✅ 已克隆配置仓库"

# 3. 创建本地敏感配置文件
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
echo "✅ 已创建 settings.local.json，请编辑填入 API Key"

# 4. 验证
ls -la ~/.claude/
echo ""
echo "🎉 配置同步完成！"
echo "📝 请编辑 ~/.claude/settings.local.json 填入你的 API Key"
```

---

## 日常同步命令

### 保存配置修改
```bash
cd ~/.claude
git add .
git commit -m "update: 描述你的修改"
git push
```

### 同步到本地
```bash
cd ~/.claude
git pull
```

### 快捷别名 (添加到 ~/.zshrc)
```bash
alias claude-sync="cd ~/.claude && git pull"
alias claude-save="cd ~/.claude && git add . && git commit -m 'update config' && git push"
```

---

## 目录结构说明

```
~/.claude/
├── .gitignore              # Git 忽略规则
├── settings.json           # 共享配置 (已脱敏)
├── settings.local.json     # 本地敏感配置 (不同步) ⚠️
├── CLAUDE.md               # 全局指令
├── COMMANDS.md             # 命令定义
├── FLAGS.md                # 标志定义
├── PERSONAS.md             # 角色定义
├── ...                     # 其他 SuperClaude 配置
├── commands/               # 自定义命令
└── skills/                 # 技能文件
```

---

## 注意事项

⚠️ **settings.local.json 不会同步**
- 每台电脑需要单独配置 API Key
- 这是故意设计的安全措施

⚠️ **避免冲突**
- 修改配置前先 `git pull`
- 使用有意义的 commit message

⚠️ **敏感信息检查**
- 提交前确认没有 API Key 泄露
- `git diff` 检查变更内容
