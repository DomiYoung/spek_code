---
name: review-quality-gates
description: |
  最终质量审核门禁 - 提交前检查。
  Use when:
  - 任务完成、准备提交
  - 创建 PR、代码审核
  - lint、类型检查、构建测试
  触发词：完成、提交、PR、合并、审核、review
  Related Skills: code-quality-gates, smart-commit, speckit.checklist
allowed-tools: Bash, Read, Grep
---

# 最终质量审核门禁 (Review Quality Gates)

> **核心理念**：交付前的最后防线，确保每次提交都是生产级质量。
> **触发时机**：任务完成、git commit、创建 PR、请求审核。

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 禁止提交

### 自动化检查（必须全部通过）

| 检查项 | 命令 | 失败处理 |
|--------|------|---------|
| **TypeScript** | `pnpm exec tsc --noEmit` | 🛑 停止，修复类型错误 |
| **ESLint** | `pnpm lint` | 🛑 停止，修复 lint 错误 |
| **构建测试** | `pnpm build` | 🛑 停止，修复构建失败 |

### 代码质量（引用 code-quality-gates）

| 规则 | 标准 | 自动审计规则 |
|------|------|-------------|
| **函数长度** | ≤ 50 行 | 手动检查 |
| **文件长度** | ≤ 500 行 | `wc -l` |
| **无裸 any** | 必须有注释 | `grep -rn ": any" src/` |
| **无 console.log** | 生产代码禁止 | `grep -rn "console.log" src/` |
| **错误处理** | 必须有 try-catch | 代码审查 |

### 变更大小限制

| 维度 | 推荐 | 上限 | 超出处理 |
|------|-----|-----|---------|
| 单次 commit | ≤ 100 行 | ≤ 200 行 | ⚠️ 建议拆分 |
| 单个 PR | ≤ 200 行 | ≤ 500 行 | ❌ 必须拆分 |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 巨型提交 (Mega Commit) ⭐⭐⭐⭐⭐

**问题**: 一次提交包含多个不相关变更，难以回滚和审查
**检测**: `git diff --stat | tail -1` 显示 > 500 行
**修正**: 拆分为逻辑独立的小提交

```bash
# ❌ 禁止
git add .
git commit -m "feat: 完成所有功能"  # 800 行变更

# ✅ 正确
git add src/auth/
git commit -m "feat(auth): 实现用户登录"  # 150 行
git add src/chat/
git commit -m "feat(chat): 实现消息发送"  # 120 行
```

### ❌ 跳过检查提交 (Skipped Checks) ⭐⭐⭐⭐⭐

**问题**: 未运行 lint/tsc 就提交，将问题推给 CI
**检测**: 提交前未执行 `pnpm lint && pnpm exec tsc --noEmit`
**修正**: 始终在提交前运行完整检查

```bash
# ❌ 禁止
git commit -m "fix: 快速修复"  # 未检查

# ✅ 正确
pnpm lint && pnpm exec tsc --noEmit && git commit -m "fix(chat): 修复消息发送失败"
```

### ❌ 遗留调试代码 (Debug Leftovers) ⭐⭐⭐⭐

**问题**: console.log、debugger 语句残留在生产代码
**检测**: `grep -rn "console.log\|debugger" src/ --include="*.ts" --include="*.tsx"`
**修正**: 提交前清理所有调试代码

### ❌ 未完成的实现 (Incomplete Implementation) ⭐⭐⭐

**问题**: TODO、FIXME、临时代码被提交
**检测**: `grep -rn "TODO\|FIXME\|HACK\|XXX" src/ --include="*.ts"`
**修正**: 完成或创建 issue 跟踪

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准审核流程

### 审核流程图

```
任务完成
    ↓
┌─ 阶段1: 自动化检查 ──────────────────────────────┐
│   pnpm exec tsc --noEmit   # TypeScript          │
│   pnpm lint                # ESLint              │
│   pnpm build               # 构建测试            │
│   全部通过 → 继续                                │
│   任一失败 → 🛑 停止，修复问题                   │
└──────────────────────────────────────────────────┘
    ↓
┌─ 阶段2: 代码质量检查 ────────────────────────────┐
│   → 引用 code-quality-gates 规则                │
│   • 函数 ≤ 50 行 / 文件 ≤ 500 行                │
│   • 无裸 any / 无 console.log                   │
│   有问题 → ⚠️ 警告，建议修复                    │
└──────────────────────────────────────────────────┘
    ↓
┌─ 阶段3: 提交规范检查 ────────────────────────────┐
│   • 格式: <type>(<scope>): <用户价值>           │
│   • 禁止词检查                                  │
│   • 变更大小检查                                │
│   违反规范 → 🛑 停止，修正                      │
└──────────────────────────────────────────────────┘
    ↓
            ✅ 审核通过，可以提交
```

### 快速审核命令

```bash
# 一键完整审核（复制执行）
pnpm exec tsc --noEmit && pnpm lint && pnpm build && git diff --stat

# 代码质量快速检查
grep -rn ": any" src/ --include="*.ts" --include="*.tsx"
grep -rn "console.log" src/ --include="*.ts" --include="*.tsx"
```

### 审核输出格式

#### ✅ 通过

```
╔══════════════════════════════════════════════════════════════╗
║  ✅ REVIEW PASSED                                            ║
╚══════════════════════════════════════════════════════════════╝

自动化检查:
  [✓] TypeScript  [✓] ESLint  [✓] Build

代码质量:
  [✓] 函数长度  [✓] 类型安全  [✓] 无 console.log

变更统计: 3 files, +45 -12

→ 可以提交！
```

#### ❌ 失败

```
╔══════════════════════════════════════════════════════════════╗
║  ❌ REVIEW FAILED                                            ║
╚══════════════════════════════════════════════════════════════╝

失败项:
  [✗] ESLint: 2 errors

详情:
  src/Chat.tsx:45 - 'useState' is defined but never used
  src/format.ts:23 - Unexpected console statement

必须修复后重新审核。
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交前必须运行

### 自动审核脚本

```bash
#!/bin/bash
# review-quality-audit.sh

echo "🔍 Review Quality Gates Audit..."

# 1. TypeScript 检查
echo "→ TypeScript 检查..."
pnpm exec tsc --noEmit
if [ $? -ne 0 ]; then
  echo "❌ TypeScript 类型检查失败"
  exit 1
fi

# 2. ESLint 检查
echo "→ ESLint 检查..."
pnpm lint
if [ $? -ne 0 ]; then
  echo "❌ ESLint 检查失败"
  exit 1
fi

# 3. 构建检查
echo "→ 构建检查..."
pnpm build
if [ $? -ne 0 ]; then
  echo "❌ 构建失败"
  exit 1
fi

# 4. 代码质量检查
echo "→ 代码质量检查..."
ANY_COUNT=$(grep -rn ": any" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)
if [ "$ANY_COUNT" -gt 0 ]; then
  echo "⚠️ 发现 $ANY_COUNT 处 any 类型（建议修复）"
fi

CONSOLE_COUNT=$(grep -rn "console.log" src/ --include="*.ts" --include="*.tsx" 2>/dev/null | wc -l)
if [ "$CONSOLE_COUNT" -gt 0 ]; then
  echo "❌ 发现 $CONSOLE_COUNT 处 console.log"
  grep -rn "console.log" src/ --include="*.ts" --include="*.tsx"
  exit 1
fi

# 5. 变更大小检查
LINES_CHANGED=$(git diff --stat | tail -1 | grep -oE '[0-9]+' | head -1)
if [ -n "$LINES_CHANGED" ] && [ "$LINES_CHANGED" -gt 500 ]; then
  echo "❌ 变更超过 500 行（当前 $LINES_CHANGED 行），请拆分提交"
  exit 1
fi

echo "✅ Review Quality Gates Passed"
```

### 交付检查清单

```
□ pnpm exec tsc --noEmit 通过
□ pnpm lint 通过
□ pnpm build 通过
□ 无 console.log（生产代码）
□ 无未注释的 any 类型
□ 函数 ≤ 50 行
□ 变更 ≤ 500 行（单 PR）
□ 提交信息符合规范
```

---

## 🔗 与其他 Skills 协作

| 阶段 | Skill |
|------|-------|
| 写代码时 | `code-quality-gates` 约束 |
| 提交信息 | `commit-quality-gates` 格式 |
| 最终交付 | 本 Skill (`review-quality-gates`) 审核 |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 代码示例区分 ❌ 错误 和 ✅ 正确
- [x] 检查失败有明确处理流程
- [x] 快速检查命令可直接复制使用
