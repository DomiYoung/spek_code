---
name: smart-commit
description: |
  Git 智能提交助手 - 自动生成 commit message。
  Use when:
  - git commit、提交代码
  - 分析变更生成提交信息
  - 推送代码
  触发词：commit、提交、推送、git add、push
  Related Skills: code-quality-gates, review-quality-gates, speckit.taskstoissues
allowed-tools: Bash, Read, Grep, Glob
---

# Git 智能提交（RAG 友好版 v2.0）

> 基于 [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) 官方规范，增强 RAG/语义检索支持

## 🔴 强制规则（全局生效）

**无论任何项目，执行 git commit 时必须：**

1. 使用 RAG 友好格式（见下方模板）
2. 包含 `[tags]` 和 `[files]` 元数据
3. 中文描述用户价值
4. 禁止敏感词

**如果发现 commit 未遵循此格式，必须：**
1. 使用 `git commit --amend` 修正
2. 或 `git reset --soft HEAD~1` 后重新提交

## 🎯 核心原则

1. **Conventional Commits 兼容**：严格遵循官方规范
2. **RAG 友好**：结构化元数据便于语义检索和知识图谱构建
3. **全中文描述**：标题和正文使用中文（type/scope 保持英文小写）
4. **用户价值导向**：说明 WHY 而非 HOW
5. **禁止敏感词**：绝对不出现 AI/agent/claude/bot/GPT 等

## 触发场景

**自动触发（无需用户显式调用）：**
- 执行任何 `git commit` 命令
- 执行任何 `git push` 命令
- 用户说"提交"、"推送"

**手动触发：**
- 用户说"帮我生成 commit message"
- 完成功能开发后保存代码
- 修复 bug 后提交变更

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

#### 📋 官方规范格式（Conventional Commits 1.0.0）

```
<type>[optional scope][!]: <description>

[optional body]

[optional footer(s)]
```

**官方规范要点**：
- `type` 和 `scope` 必须小写英文
- `!` 表示 Breaking Change（可选）
- `body` 与 header 之间必须空一行
- `footer` 遵循 [git trailer 格式](https://git-scm.com/docs/git-interpret-trailers)

#### 📋 RAG 友好扩展格式（推荐）

```
<type>(<scope>): <用户价值描述（中文）>

[tags]: <关键词1>, <关键词2>, <关键词3>
[refs]: #<issue-id> (可选)
[files]:
  + <新增文件路径>
  ~ <修改文件路径>
  - <删除文件路径>

核心改动：<关键变更点，1-2句话>
影响范围：<涉及模块/组件>
技术背景：<为什么这样做>

BREAKING CHANGE: <破坏性变更说明> (可选)
```

**RAG 元数据字段说明**：

| 字段 | 格式 | 用途 | 示例 |
|------|------|------|------|
| `[tags]` | 逗号分隔关键词 | 语义检索、分类过滤 | `attachment, video, clipboard` |
| `[refs]` | `#issue-id` 或 URL | 关联追溯 | `#123`, `JIRA-456` |
| `[files]` | `+`新增 `~`修改 `-`删除 | 变更可视化、影响分析 | `+ utils/helper.ts` |

#### 📝 格式规范

| 字段 | 要求 |
|------|------|
| **type** | 小写英文，见上表 |
| **scope** | 小写英文，见上表，可选 |
| **description** | 中文，≤50 字符，说明用户价值 |
| **[tags]** | 3-5 个语义关键词，便于 RAG 检索 |
| **[refs]** | 关联的 Issue/PR/Ticket |
| **[files]** | 结构化文件清单，`+/-/~` 符号 |
| **核心改动** | 关键变更点，技术层面 |
| **影响范围** | 涉及的模块/文件/组件 |
| **技术背景** | 为什么做这个改动 |
| **BREAKING CHANGE** | 破坏性变更说明（官方 footer）|

#### 🔴 禁止词（绝对禁止）

```
AI, ai, Agent, agent, Claude, claude, Bot, bot, GPT, gpt,
Anthropic, anthropic, Copilot, copilot, Assistant, assistant,
自动生成, Generated, Co-Authored-By, noreply@anthropic.com
```

#### ✅ 正确示例

**示例 1: 新功能（RAG 友好格式）**

```bash
git commit -m "$(cat <<'EOF'
feat(chat): 增强附件系统，支持视频预览与剪贴板复制

[tags]: attachment, video, clipboard, preview, copy
[refs]: #issue-123
[files]:
  + src/features/chat/utils/attachmentMapper.ts
  + src/features/chat/utils/clipboardUtils.ts
  ~ src/features/chat/components/AttachmentCard.tsx
  ~ src/features/chat/components/MessageBubble.tsx

核心改动：附件卡片视频预览 + 消息复制支持附件文件
影响范围：moss-chat-signalr, runlog, api
技术背景：提升聊天附件交互体验，完善任务链控制能力
EOF
)"
```

**示例 2: Bug 修复**

```bash
git commit -m "$(cat <<'EOF'
fix(editor): 修复刷新后子节点丢失问题，确保数据持久化

[tags]: refresh, node, persistence, yjs, sync
[files]:
  ~ src/components/IterationNode.tsx
  ~ src/stores/workflowStore.ts

核心改动：在 refreshNodes 函数中添加子节点状态恢复逻辑
影响范围：IterationNode 组件 + workflowStore
技术背景：刷新时 Yjs 同步未包含子节点状态导致数据丢失
EOF
)"
```

**示例 3: Breaking Change**

```bash
git commit -m "$(cat <<'EOF'
feat(api)!: 重构任务链 API，优化继续运行接口

[tags]: api, taskchain, breaking, refactor
[files]:
  ~ src/api/workflowEditor/list.ts

核心改动：continueTaskChainRun 路径从 body 传参改为 URL 路径参数
影响范围：workflowEditor API
技术背景：RESTful 规范要求资源 ID 放在 URL 路径中

BREAKING CHANGE: continueTaskChainRun(logId) API 签名变更，logId 不再可选
EOF
)"
```

**示例 4: 简洁格式（小改动）**

```bash
git commit -m "docs: 更新 README 安装说明"
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

## 🔍 RAG 检索优化指南

### 为什么需要 RAG 友好格式？

| 场景 | 传统格式问题 | RAG 友好格式优势 |
|------|-------------|-----------------|
| **语义搜索** | "附件" 搜不到 "attachment" | `[tags]` 统一关键词 |
| **影响分析** | 不知道改了哪些文件 | `[files]` 结构化清单 |
| **变更追溯** | 无法关联 Issue | `[refs]` 直接链接 |
| **知识图谱** | 缺少节点关系 | 核心改动/影响范围 明确描述 |

### [tags] 关键词选择原则

1. **领域词汇**：`attachment`, `workflow`, `auth`, `permission`
2. **技术栈**：`react`, `zustand`, `signalr`, `yjs`
3. **变更类型**：`breaking`, `deprecate`, `migrate`
4. **功能特性**：`clipboard`, `preview`, `upload`, `cache`

### 解析正则（供工具使用）

```javascript
// 解析 commit message 的 RAG 元数据
const COMMIT_REGEX = {
  header: /^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)$/,
  tags: /^\[tags\]:\s*(.+)$/m,
  refs: /^\[refs\]:\s*(.+)$/m,
  files: /^\[files\]:\n((?:\s+[+~-]\s+.+\n?)+)/m,
  breaking: /^BREAKING CHANGE:\s*(.+)$/m,
};

// 文件变更类型
const FILE_CHANGE_TYPE = {
  '+': 'added',
  '~': 'modified', 
  '-': 'deleted',
};
```

## 📅 版本历史

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v2.0 | 2026-01-11 | RAG 友好格式，增加 `[tags]`/`[refs]`/`[files]` 元数据 |
| v1.0 | 2025-12-01 | 知识图谱版，核心改动/影响范围/技术背景 |
