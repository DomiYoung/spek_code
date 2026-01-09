---
name: smart-commit
description: |
  Git 智能提交助手（知识图谱版）。当涉及 git commit、提交代码、推送变更时自动触发。
  【自动化】分析变更 → 推断 type/scope → 生成知识图谱格式 commit message。
  关键词：commit、提交、推送、git add、push、保存代码、提交代码。
  与 commit-quality-gates 协作，提供完整的提交自动化。
allowed-tools: Bash, Read, Grep, Glob
---

# Git 智能提交（知识图谱版）

## 🎯 核心原则

1. **全中文输出**：标题和正文均使用中文
2. **知识图谱视角**：分析节点、关系、影响
3. **用户价值导向**：说明 WHY 而非 HOW
4. **禁止敏感词**：绝对不出现 AI/agent/claude/bot/GPT 等

## 触发场景

- 用户说"提交"、"commit"、"推送"
- 完成功能开发后保存代码
- 修复 bug 后提交变更
- 用户说"帮我生成 commit message"

## 自动化流程

### Step 1: 环境检查

```bash
git status --short
git branch --show-current
git diff --stat
git log --oneline -3  # 参考最近提交风格
```

**验证**：
- 当前是 feature 分支（非 main/master/test）
- 有待提交的变更

### Step 2: 变更分析

**自动推断 Type**：

| 变更特征 | Type | 中文说明 |
|---------|------|---------|
| 新增功能代码/组件 | `feat` | 新功能 |
| 修复已知问题 | `fix` | 修复 |
| 代码重组/清理 | `refactor` | 重构 |
| 性能相关改进 | `perf` | 性能优化 |
| 仅 .md/.txt 文件 | `docs` | 文档 |
| 配置/构建/依赖 | `chore` | 构建/依赖 |
| 测试文件变更 | `test` | 测试 |
| 样式/格式调整 | `style` | 样式 |

**自动推断 Scope**（按路径）：

| 路径模式 | Scope |
|---------|-------|
| `components/editor/*` | `editor` |
| `components/chat/*` | `chat` |
| `components/app/*` | `app` |
| `components/_shared/*` | `ui` |
| `hooks/*` | `hooks` |
| `utils/*` | `utils` |
| `*Store.ts` | `store` |
| `api/*`, `services/*` | `api` |
| `*.config.*` | `config` |
| `package.json` | `deps` |
| `workflow*` | `workflow` |

### Step 3: 知识图谱分析

**必须分析以下维度**：

1. **节点识别**：变更涉及哪些组件/函数/类型
2. **关系描述**：节点之间建立或修改了什么关系
3. **影响范围**：对系统知识图谱的影响

### Step 4: Commit Message 生成

#### 📋 知识图谱格式（强制）

```
<type>(<scope>): <用户价值描述（中文）>

核心改动：<关键变更点，1-2句话>
影响范围：<涉及模块/组件>
技术背景：<为什么这样做>
相关文件：<主要修改文件统计>
```

#### 📝 格式规范

| 字段 | 要求 |
|------|------|
| **type** | 小写英文，见上表 |
| **scope** | 小写英文，见上表 |
| **标题** | 中文，≤50 字符，说明用户价值 |
| **核心改动** | 关键变更点，技术层面 |
| **影响范围** | 涉及的模块/文件/组件 |
| **技术背景** | 为什么做这个改动 |
| **相关文件** | 新增 X 文件，修改 Y 文件 |

#### 🔴 禁止词（绝对禁止）

```
AI, ai, Agent, agent, Claude, claude, Bot, bot, GPT, gpt,
Anthropic, anthropic, Copilot, copilot, Assistant, assistant,
自动生成, Generated, Co-Authored-By, noreply@anthropic.com
```

#### ✅ 正确示例

```bash
git commit -m "$(cat <<'EOF'
feat(ui): 添加测试环境标识组件，帮助用户区分测试和正式环境

核心改动：创建 EnvBadge 组件，通过 VITE_APP_BASE_URL 检测环境类型
影响范围：App.tsx 入口 + 新增 env-badge 组件目录
技术背景：appflowytest 和 appflowy 两个部署地址需要视觉区分
相关文件：新增 EnvBadge.tsx，修改 App.tsx (2 files)
EOF
)"
```

```bash
git commit -m "$(cat <<'EOF'
fix(editor): 修复刷新后子节点丢失问题，确保数据持久化

核心改动：在 refreshNodes 函数中添加子节点状态恢复逻辑
影响范围：IterationNode 组件 + workflowStore
技术背景：刷新时 Yjs 同步未包含子节点状态导致数据丢失
相关文件：修改 IterationNode.tsx, workflowStore.ts (2 files)
EOF
)"
```

```bash
git commit -m "$(cat <<'EOF'
style(ui): 优化环境标识为顶部居中横幅样式，提升可见性

核心改动：将右下角胶囊改为顶部居中横幅，添加🔧图标和"环境"文字
影响范围：EnvBadge 组件样式
技术背景：右下角标识太小容易被忽略，顶部横幅更醒目
相关文件：EnvBadge.tsx (1 file)
EOF
)"
```

#### ❌ 错误示例

```bash
# 错误：英文标题
feat(ui): add environment badge component

# 错误：没有知识图谱格式
feat(ui): 添加环境标识

# 错误：包含禁止词
feat(ui): 添加环境标识

🤖 Generated with Claude Code
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>

# 错误：说 HOW 而不是 WHY
fix(editor): 添加 if 判断修复空指针
```

### Step 5: 执行提交

```bash
# 1. 暂存相关文件
git add <相关文件>

# 2. 使用 HEREDOC 确保格式正确
git commit -m "$(cat <<'EOF'
<type>(<scope>): <中文用户价值描述>

核心改动：<关键变更点>
影响范围：<涉及模块>
技术背景：<为什么这样做>
相关文件：<文件统计>
EOF
)" --author="YOUR_USERNAME <YOUR_USERNAME@gmail.com>"

# 3. 验证提交
git log -1 --pretty=full
```

### Step 6: 可选推送

用户说"推送"、"push"时：

```bash
git push origin $(git branch --show-current)
```

## 安全检查

**提交前验证**：
- [ ] 无 `.env`、`credentials` 等敏感文件
- [ ] 无生产代码中的 `console.log`
- [ ] 无未注释的 `any` 类型
- [ ] 无超大文件（>1MB）
- [ ] 无禁止词

## 输出格式

```markdown
## ✅ Git 提交完成

| Commit | Type | Scope | 描述 |
|--------|------|-------|------|
| `abc123` | feat | ui | 添加环境标识组件 |

**分支**: feature/xxx
**推送**: ✅ 已推送 / ⏳ 待推送

### Commit Message 预览
```
<完整的 commit message>
```
```

## 与其他 Skills 协作

| Skill | 协作 |
|-------|------|
| `commit-quality-gates` | 格式验证 |
| `code-quality-gates` | 代码质量检查 |
| `workflow-router` | 工作流路由 |

## 变更大小控制

| 维度 | 推荐 | 上限 | 超出处理 |
|------|-----|-----|---------|
| 单次 commit | ≤ 100 行 | ≤ 200 行 | 拆分 commit |
| 修改文件数 | ≤ 5 个 | ≤ 10 个 | 拆分 commit |

## 智能分组策略

**判断拆分策略**：

| 条件 | 行为 |
|------|------|
| 同一功能域变更 | 合并 1 个 commit |
| 跨多个功能域 | 拆分多个 commit |
| 删除 + 新增 | 先清理后新增 |

**分组优先级**：
1. `refactor`: 删除/清理代码
2. `refactor`: 重构/优化代码
3. `feat`: 新增功能
4. `fix`: 修复问题
