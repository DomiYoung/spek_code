---
name: component-reuse-expert
description: "组件复用专家。在开发新功能前自动检查已有组件/API/工具函数/数据库表，防止重复开发。触发：用户说'我想做'、'开发新功能'、'做个组件'、'加个API'、'新增功能'、brainstorming 或 write-plan 阶段。输出可复用组件清单。"
---

# Component Reuse Expert

> **核心职责**: 在新功能开发前，检查项目中已有的可复用资源，防止重复开发。

## 触发条件

自动激活当用户说：
- "我想做 XX"
- "开发新功能"
- "做个组件"
- "加个 API"
- "新增功能"
- 进入 brainstorming 或 write-plan 阶段

## 检查范围

### 1. 前端组件
**位置**:
- `frontend/src/components/`
- `frontend/src/views/`

**检查**:
```bash
# 搜索已有组件
Glob: frontend/src/components/**/*.tsx
Grep: "export (default |const |function )" in *.tsx
```

**输出**: 组件名称、Props 接口、功能描述

### 2. 后端 API
**位置**: `backend/main.py`

**检查**:
```bash
# 搜索已有路由
Grep: "@app\.(get|post|put|delete|patch)" in backend/main.py
```

**输出**: 路由路径、HTTP 方法、功能描述

### 3. 工具函数
**位置**:
- `frontend/src/lib/`
- `frontend/src/hooks/`

**检查**:
```bash
# 搜索已有函数
Grep: "export (const|function|async function)" in frontend/src/lib/*.ts
Grep: "export (const|function) use" in frontend/src/hooks/*.ts
```

**输出**: 函数名、用途、参数

### 4. 数据库表
**位置**: `backend/database.py`

**检查**:
```bash
# 搜索已有模型
Grep: "class .* \(Base\)" in backend/database.py
```

**输出**: 表名、字段、关系

---

## 工作流

### Step 1: 理解需求
从用户描述中提取：
- 需要的前端组件类型
- 需要的后端 API 端点
- 需要的工具函数
- 需要的数据库表

### Step 2: 扫描现有资源
使用 Glob 和 Grep 工具检查上述4个范围

### Step 3: 匹配分析
对每个需求，评估：
- ✅ **完全匹配**: 已有组件可直接使用
- ⚠️ **部分匹配**: 扩展现有组件即可满足
- ❌ **无匹配**: 需新建

### Step 4: 输出清单
生成可复用组件清单：

```markdown
## 可复用组件清单

### 前端组件
- ✅ `BottomNav` (frontend/src/components/BottomNav.tsx) - 添加新 Tab 即可
- ⚠️ `Card` (frontend/src/components/ui/Card.tsx) - 需扩展样式
- ❌ `FollowButton` - 需新建

### 后端 API
- ✅ `/api/users` (backend/main.py:45) - 扩展返回关注状态字段
- ❌ `/api/follow` - 需新建

### 工具函数
- ✅ `fetchWithCache` (frontend/src/lib/api.ts) - 可复用缓存逻辑
- ✅ `triggerHaptic` (frontend/src/lib/haptic.ts) - 可复用触觉反馈

### 数据库表
- ⚠️ `users` 表 - 需添加 following_count 字段
- ❌ `user_follows` 表 - 需新建
```

---

## 输出位置

如果在 brainstorming/write-plan 阶段：
- 将清单写入 `specs/{feature_id}/plan.md` 的 "可复用组件清单" 节

如果是独立检查：
- 直接在对话中输出清单

---

## 复用决策原则

1. **优先扩展而非新建**: 如果现有组件覆盖 60%+ 需求，优先扩展
2. **保持接口兼容**: 扩展时不破坏现有调用方
3. **避免过度抽象**: 如果只用一次，不要强行抽象
4. **记录复用决策**: 在 plan.md 中说明为什么选择复用/新建

---

## 与其他 Skills 的协作

- **brainstorming**: 在设计阶段提前识别复用机会
- **product-manager**: 验收时确认复用组件是否正确使用
- **ki-manager**: 将新建的可复用组件记录到 component_patterns.md

---

## 示例

**用户输入**: "我想做用户关注功能"

**检查结果**:
```
扫描 frontend/src/components/...
  发现: BottomNav, Card, ArticleCard, TheBrain...

扫描 backend/main.py...
  发现: /api/articles, /api/users, /api/intelligence...

扫描 frontend/src/lib/...
  发现: fetchWithCache, triggerHaptic, formatDate...

扫描 backend/database.py...
  发现: User, RawArticle, UserProfile...
```

**输出**:
```markdown
## 可复用组件清单（用户关注功能）

### 前端组件
- ✅ `BottomNav` - 可添加"关注"Tab
- ✅ `Card` - 可复用卡片样式
- ❌ `FollowButton` - 需新建关注按钮
- ❌ `FollowerList` - 需新建关注者列表

### 后端 API
- ⚠️ `/api/users` - 扩展返回 is_following 字段
- ❌ `/api/follow` - 需新建关注/取消关注
- ❌ `/api/followers` - 需新建获取关注者列表

### 工具函数
- ✅ `fetchWithCache` - 复用API缓存逻辑
- ✅ `triggerHaptic` - 复用关注按钮触觉反馈

### 数据库表
- ⚠️ `users` - 添加 followers_count, following_count
- ❌ `user_follows` - 新建关注关系表

### 复用比例
- 前端: 2/4 (50%)
- 后端: 1/3 (33%)
- 工具: 2/2 (100%)
- 数据库: 0/2 (0%)

**总体复用率**: 41.6%
```
