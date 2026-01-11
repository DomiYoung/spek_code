---
name: product-expert
description: |
  产品经理专家 - PRD、需求分析。
  Use when:
  - PRD 撰写、需求分析
  - 用户故事、验收标准
  - 优先级排序（MoSCoW、RICE）
  触发词：PRD、需求、用户故事、验收标准、AC、优先级、JTBD
  Related Skills: speckit.specify, brainstorm, experts/architect
allowed-tools: "*"
---

# Product Expert（产品经理专家）

> **核心理念**：用户价值驱动，可验证的需求，拒绝模糊规范。
> **来源**：[Inspired by Marty Cagan](https://www.svpg.com/)、[Shape Up by Basecamp](https://basecamp.com/shapeup)、[JTBD 理论](https://jtbd.info/)

---

## 1. 硬性约束 (Hard Constraints)

> ❌ **Blocker**: 违反这些规则 → 需求文档被拒绝

| 维度 | 要求 | 自动审计规则 |
|------|------|-------------|
| **验收标准必须存在** | 每个功能点必须有 AC | `grep -E "^AC-[0-9]+:" spec.md \| wc -l` 必须 > 0 |
| **AC 格式规范** | 必须使用 Given-When-Then | `grep -E "Given.*When.*Then" spec.md` |
| **优先级必须标注** | 每个需求有 P0/P1/P2 | `grep -E "\[P[0-2]\]" spec.md \| wc -l` |
| **成功指标必须量化** | 禁止模糊目标 | `grep -E "[0-9]+%" spec.md` 或 `grep -E "<\s*[0-9]+" spec.md` |
| **用户故事格式** | 必须符合 INVEST | 检查 "作为...我想要...以便..." 格式 |
| **禁止功能蔓延** | 必须有 Won't Have 列表 | `grep -E "Won't Have\|不做" spec.md` |
| **依赖项明确** | 列出外部/团队依赖 | `grep -E "依赖\|Dependency" spec.md` |

---

## 2. 反模式 (Anti-Patterns)

> ⚠️ **Warning**: 检测到这些坏习惯需立即修正

### ❌ 模糊验收标准 ⭐⭐⭐⭐⭐

**问题**: "用户体验要好"、"性能要快" → 无法验收，开发返工
**检测**: `grep -E "要好|要快|应该|尽量|适当" spec.md`
**修正**: 使用 Given-When-Then + 量化指标

```markdown
# ❌ 错误 - 无法验收
AC: 页面加载要快

# ✅ 正确 - 可验证
AC-001: Given 用户首次访问，When 点击进入页面，Then 首屏内容在 2 秒内可见（LCP < 2s）
```

### ❌ 需求无优先级 ⭐⭐⭐⭐⭐

**问题**: 一切都是 P0 → 资源冲突，延期交付
**检测**: `grep -c "\[P0\]" spec.md` 如果 > 总需求数的 30%
**修正**: 使用 MoSCoW 或 RICE 强制排序

```markdown
# ❌ 错误 - 全是 P0
- [P0] 用户登录
- [P0] 密码找回
- [P0] 头像上传
- [P0] 个性签名

# ✅ 正确 - 分层优先级
- [P0] 用户登录 (Must Have - 核心功能)
- [P1] 密码找回 (Should Have - 重要但可推迟)
- [P2] 头像上传 (Could Have - 锦上添花)
- [P3] 个性签名 (Won't Have - 明确排除)
```

### ❌ 用户故事不符合 INVEST ⭐⭐⭐⭐

**问题**: 故事太大无法估算，或缺乏用户价值
**检测**: 用户故事没有 "以便" 部分
**修正**: 检查 INVEST 六原则

```markdown
# ❌ 错误 - 缺乏价值描述
作为用户，我想要上传文件

# ✅ 正确 - 完整 INVEST
作为项目成员，我想要上传设计稿附件，以便团队成员可以在线预览和评审设计方案
```

### ❌ 功能蔓延（Scope Creep）⭐⭐⭐⭐

**问题**: 不断添加功能，无法交付
**检测**: 没有 "Won't Have" 或 "不做" 部分
**修正**: 明确边界，列出排除项

```markdown
# ❌ 错误 - 无边界
## 功能列表
1. 用户注册
2. 社交登录
3. 手机验证
4. 邮箱验证
5. 人脸识别...（无止境）

# ✅ 正确 - 明确边界
## Must Have (P0)
1. 邮箱密码注册

## Won't Have (本期不做)
- 社交登录 → 下期规划
- 人脸识别 → 无业务场景
```

### ❌ 假设驱动而非数据驱动 ⭐⭐⭐

**问题**: "我觉得用户需要..." → 上线后无人使用
**检测**: 没有用户研究/数据支撑
**修正**: 添加数据来源和验证方式

```markdown
# ❌ 错误 - 纯假设
背景：用户应该需要批量导出功能

# ✅ 正确 - 数据支撑
背景：
- 数据来源：客服工单分析（2024 Q3）
- 痛点频次：47 次/月请求批量导出
- 影响用户：企业版用户占比 80%
- 验证方式：灰度发布 → A/B 测试
```

### ❌ PRD 缺少非功能需求 ⭐⭐⭐

**问题**: 只写功能，忽略性能/安全/可用性
**检测**: `grep -E "性能|安全|可用性|NFR" spec.md`
**修正**: 必须包含 NFR 章节

```markdown
# ❌ 错误 - 只有功能
## 功能需求
1. 用户可以上传文件

# ✅ 正确 - 包含 NFR
## 功能需求
1. 用户可以上传文件

## 非功能需求 (NFR)
- 性能：单文件上传 < 5s（100MB 以内）
- 安全：文件类型白名单（jpg/png/pdf）
- 可用性：99.9% SLA
- 容量：单用户存储上限 10GB
```

---

## 3. 最佳实践 (Golden Paths)

> ✅ **Recommended**: 标准文档模板

### PRD 模板

```markdown
# PRD: [功能名称]

## 1. 概述
- **背景**: 为什么做这个功能？（数据/用户反馈支撑）
- **目标**: 解决什么问题？
- **成功指标**: 如何衡量成功？（量化）
  - 主指标：注册转化率提升 15%
  - 辅助指标：页面跳出率下降 10%

## 2. 用户故事
作为 [用户角色]，我想要 [功能]，以便 [价值]

## 3. 功能需求

### 3.1 Must Have (P0)
| ID | 功能描述 | 验收标准 |
|----|----------|----------|
| FR-001 | 用户邮箱注册 | AC-001, AC-002 |

### 3.2 Should Have (P1)
...

### 3.3 Could Have (P2)
...

### 3.4 Won't Have (明确不做)
- 社交登录 - 原因：本期聚焦核心流程

## 4. 验收标准 (AC)
AC-001: Given 用户在注册页，When 输入有效邮箱和密码，Then 注册成功并跳转首页
AC-002: Given 用户输入已注册邮箱，When 提交注册，Then 显示"邮箱已被使用"

## 5. 非功能需求
- 性能：注册接口响应 < 500ms
- 安全：密码强度校验（8位+大小写+数字）
- 可用性：99.9% SLA

## 6. 设计约束
- 技术栈：React + Node.js
- 时间约束：2 周内上线

## 7. 依赖项
- [ ] 邮件服务配置 - @运维
- [ ] UI 设计稿 - @设计团队

## 8. 风险与缓解
| 风险 | 概率 | 影响 | 缓解策略 |
|------|------|------|----------|
| 邮件服务不稳定 | 中 | 高 | 备用 SMTP 服务商 |
```

### 验收标准 (AC) 模板

```markdown
## Given-When-Then 格式

AC-[编号]: Given [前提条件], When [用户操作], Then [预期结果]

## 示例集

### 正向场景
AC-001: Given 用户在登录页且未登录，When 输入正确邮箱密码并点击登录，Then 登录成功跳转到首页

### 边界场景
AC-002: Given 用户输入密码，When 密码少于 8 位，Then 显示"密码至少 8 位"且登录按钮禁用

### 异常场景
AC-003: Given 用户连续输错密码 5 次，When 再次尝试登录，Then 显示"账户已锁定，请 30 分钟后重试"

### 性能场景
AC-004: Given 用户提交登录，When 服务正常，Then 登录响应时间 < 500ms (P99)
```

### RICE 优先级评分

```markdown
## RICE 评分公式

Score = (Reach × Impact × Confidence) / Effort

| 维度 | 说明 | 取值 |
|------|------|------|
| Reach | 每季度影响用户数 | 实际数字 |
| Impact | 影响程度 | 0.25(低) / 0.5(中) / 1(高) / 2(很高) / 3(极高) |
| Confidence | 把握程度 | 100% / 80% / 50% |
| Effort | 工作量 | 人周 |

## 示例

| 功能 | Reach | Impact | Confidence | Effort | Score |
|------|-------|--------|------------|--------|-------|
| 一键登录 | 10000 | 2 | 80% | 2 | 8000 |
| 头像编辑 | 5000 | 0.5 | 100% | 1 | 2500 |
| 批量导出 | 500 | 3 | 50% | 4 | 187.5 |

→ 优先级：一键登录 > 头像编辑 > 批量导出
```

### 双清单验收机制

```markdown
## 验收流程

1️⃣ 需求阶段：spec.md 定义 AC 清单
2️⃣ 开发阶段：按 AC 逐项实现
3️⃣ 完成阶段：生成 completion.md
4️⃣ 验收阶段：spec.md vs completion.md 核对

## completion.md 模板

| AC ID | 状态 | 实现说明 | 测试证据 |
|-------|------|----------|----------|
| AC-001 | ✅ | LoginForm.tsx:45 | test/login.spec.ts |
| AC-002 | ⚠️ | 部分实现，缺少边界处理 | - |
| AC-003 | ❌ | 未实现 | - |

## 验收判定

| 条件 | 结论 |
|------|------|
| P0 完成率 100% + P1 ≥ 80% | ✅ **通过** |
| P0 ≥ 80% + 有后续计划 | ⚠️ **条件通过** |
| P0 < 80% | ❌ **不通过** |
```

---

## 4. 自我验证 (Self-Verification)

> 🛡️ **Self-Audit**: 提交 PRD 前运行

### 自动审计脚本

```bash
#!/bin/bash
# prd-audit.sh

echo "🔍 Product Expert Audit..."

SPEC_FILE=${1:-"spec.md"}

# 1. 检查 AC 存在
AC_COUNT=$(grep -cE "^AC-[0-9]+:" "$SPEC_FILE" 2>/dev/null || echo 0)
if [ "$AC_COUNT" -eq 0 ]; then
  echo "❌ 未找到验收标准 (AC-xxx)"
  exit 1
fi
echo "✅ 找到 $AC_COUNT 条验收标准"

# 2. 检查 Given-When-Then 格式
GWT_COUNT=$(grep -cE "Given.*When.*Then" "$SPEC_FILE" 2>/dev/null || echo 0)
if [ "$GWT_COUNT" -eq 0 ]; then
  echo "⚠️ AC 未使用 Given-When-Then 格式"
fi

# 3. 检查优先级标注
P0_COUNT=$(grep -cE "\[P0\]|Must Have" "$SPEC_FILE" 2>/dev/null || echo 0)
if [ "$P0_COUNT" -eq 0 ]; then
  echo "❌ 未找到优先级标注"
  exit 1
fi

# 4. 检查 Won't Have
WONT_COUNT=$(grep -cE "Won't Have|不做|排除" "$SPEC_FILE" 2>/dev/null || echo 0)
if [ "$WONT_COUNT" -eq 0 ]; then
  echo "⚠️ 未定义 Won't Have，可能存在功能蔓延风险"
fi

# 5. 检查模糊词汇
VAGUE=$(grep -E "要好|要快|应该|尽量|适当|大概" "$SPEC_FILE" 2>/dev/null)
if [ -n "$VAGUE" ]; then
  echo "⚠️ 发现模糊词汇："
  echo "$VAGUE"
fi

# 6. 检查量化指标
METRICS=$(grep -cE "[0-9]+%|<\s*[0-9]+|>\s*[0-9]+" "$SPEC_FILE" 2>/dev/null || echo 0)
if [ "$METRICS" -eq 0 ]; then
  echo "⚠️ 未找到量化指标，建议添加可测量的成功标准"
fi

echo "✅ PRD Audit Passed"
```

### 交付检查清单

```
□ 每个功能点有验收标准 (AC)
□ AC 使用 Given-When-Then 格式
□ 优先级使用 MoSCoW 或 RICE 排序
□ P0 需求不超过总需求的 30%
□ 明确列出 Won't Have（不做）列表
□ 成功指标可量化（数字/百分比）
□ 非功能需求（性能/安全/可用性）已定义
□ 依赖项和风险已识别
□ 用户故事符合 INVEST 原则
□ 已与开发团队评审
```

### INVEST 检查表

| 原则 | 检查问题 | 通过标准 |
|------|----------|----------|
| **I**ndependent | 是否依赖其他故事？ | 可独立开发交付 |
| **N**egotiable | 是否过于详细？ | 有讨论空间 |
| **V**aluable | 用户价值是什么？ | 有明确的"以便" |
| **E**stimable | 能估算工作量吗？ | 团队可评估 |
| **S**mall | 一个迭代能完成吗？ | ≤ 5 人天 |
| **T**estable | 如何验证完成？ | 有明确 AC |

---

**QA Audit Checklist** (Do not remove):
- [x] "Hard Constraints" 包含具体拒绝标准和审计规则
- [x] "Anti-Patterns" 包含检测逻辑和修正方案
- [x] 无泛泛而谈的建议（"小心"、"注意"等）
- [x] 代码块可直接复制使用
