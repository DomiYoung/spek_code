---
name: react-router-patterns
description: |
  React Router 6.x 路由最佳实践。当涉及路由守卫、权限控制、嵌套路由时自动触发。
  关键词：router、路由、route、navigate、权限、守卫、layout。
  【路由核心】包含路由守卫、权限控制、布局嵌套。
version: 2.0.0
allowed-tools: Read, Grep, Glob
---

# React Router 6.x 路由模式

## 项目架构

```
src/
├── router/
│   ├── index.tsx           # 路由配置
│   ├── guards/             # 路由守卫
│   │   ├── ProtectedRoute.tsx
│   │   └── RoleGuard.tsx
│   └── routes/             # 路由定义
│       ├── publicRoutes.ts
│       └── privateRoutes.ts
├── layouts/
│   ├── RootLayout.tsx      # 根布局
│   └── DashboardLayout.tsx # 仪表盘布局
└── pages/
    └── errors/
        ├── NotFound.tsx
        └── Forbidden.tsx

技术栈：
- React Router 6.x
- React 18.x
```

---

## 1. 硬性约束 (Hard Constraints)

### 路由配置约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| 必须配置 errorElement | 捕获路由级错误 | `grep -rln "createBrowserRouter" src/ --include="*.tsx" \| xargs grep -L "errorElement"` | 🔴 Critical |
| 必须使用 createBrowserRouter | v6.4+ 数据 API 支持 | `grep -rn "BrowserRouter" src/ --include="*.tsx" \| grep -v "createBrowserRouter"` | 🟡 Warning |
| 受保护路由必须处理 loading | 避免闪烁 | `grep -A10 "ProtectedRoute" src/ --include="*.tsx" \| grep -v "isLoading\|Loading"` | 🔴 Critical |
| Navigate 必须使用 replace | 登录/重定向场景 | `grep -rn "<Navigate" src/ --include="*.tsx" \| grep -v "replace"` | 🟡 Warning |

### 导航约束

| 约束 | 规则 | 审计命令 | 严重度 |
|------|------|----------|--------|
| useNavigate 禁止在渲染中调用 | 必须在 useEffect 或事件中 | `grep -B5 "navigate(" src/ --include="*.tsx" \| grep -v "useEffect\|onClick\|onSubmit"` | 🔴 Critical |
| useParams 必须有类型注解 | 保证类型安全 | `grep -rn "useParams()" src/ --include="*.tsx" \| grep -v "useParams<"` | 🟡 Warning |
| 路由路径禁止硬编码 | 使用常量定义 | `grep -rn "navigate(\"/\\|to=\"/" src/ --include="*.tsx" \| wc -l` | 🟡 Warning |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: useNavigate 在渲染中调用

**问题**：在组件渲染过程中直接调用 navigate()，导致渲染循环或警告。

**检测**：
```bash
# 检测渲染中的 navigate 调用
grep -B10 "navigate(" src/ -r --include="*.tsx" | \
  grep -v "useEffect\|onClick\|onSubmit\|onChange\|handleClick\|handle"

# 检测条件渲染中的 navigate
grep -rn "if.*{" src/ --include="*.tsx" -A3 | \
  grep "navigate(" | grep -v "useEffect"
```

**修正**：
```typescript
// ❌ 错误：渲染中直接调用
function MyComponent() {
  const navigate = useNavigate();
  const { isSuccess } = useMutation();

  if (isSuccess) {
    navigate('/success');  // 💥 渲染中调用
  }

  return <div>...</div>;
}

// ✅ 正确：在 useEffect 中调用
function MyComponent() {
  const navigate = useNavigate();
  const { isSuccess } = useMutation();

  useEffect(() => {
    if (isSuccess) {
      navigate('/success');
    }
  }, [isSuccess, navigate]);

  return <div>...</div>;
}

// ✅ 正确：在事件处理中调用
function MyComponent() {
  const navigate = useNavigate();

  const handleSubmit = async () => {
    await submitData();
    navigate('/success');  // ✅ 事件处理中
  };

  return <button onClick={handleSubmit}>提交</button>;
}
```

---

### 反模式 2.2: 忘记 replace 导致历史堆叠

**问题**：登录成功后跳转不使用 replace，用户可以返回登录页。

**检测**：
```bash
# 检测登录/认证后的导航
grep -A5 "isAuthenticated\|isSuccess\|login" src/ -r --include="*.tsx" | \
  grep "navigate(" | grep -v "replace"

# 检测 Navigate 组件不带 replace
grep -rn "<Navigate" src/ --include="*.tsx" | grep -v "replace"
```

**修正**：
```typescript
// ❌ 错误：登录后不替换历史
function LoginPage() {
  const navigate = useNavigate();

  const onLoginSuccess = () => {
    navigate('/dashboard');  // 💥 登录页还在历史中
  };
}

// ✅ 正确：替换历史记录
function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const from = location.state?.from?.pathname || '/dashboard';

  const onLoginSuccess = () => {
    navigate(from, { replace: true });  // ✅ 替换，无法返回登录页
  };
}

// ✅ 正确：Navigate 组件也要 replace
function ProtectedRoute({ children }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }
  return children;
}
```

---

### 反模式 2.3: 守卫未处理加载状态

**问题**：路由守卫在验证过程中未显示加载状态，导致闪烁。

**检测**：
```bash
# 检测 ProtectedRoute 但无 loading 处理
grep -A20 "ProtectedRoute\|AuthGuard\|RouteGuard" src/ -r --include="*.tsx" | \
  grep -v "isLoading\|loading\|Loading\|Spinner"

# 检测守卫组件
grep -rln "isAuthenticated" src/ --include="*.tsx" | \
  xargs grep -L "isLoading"
```

**修正**：
```typescript
// ❌ 错误：无加载状态
function ProtectedRoute({ children }) {
  const { isAuthenticated } = useAuth();  // 可能正在检查中

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;  // 💥 可能误判为未登录
  }
  return children;
}

// ✅ 正确：处理加载状态
function ProtectedRoute({ children }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;  // ✅ 等待验证完成
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return children;
}
```

---

### 反模式 2.4: useParams 缺少类型注解

**问题**：useParams 不带类型参数，返回值全部是 string | undefined。

**检测**：
```bash
# 检测无类型的 useParams
grep -rn "useParams()" src/ --include="*.tsx" | grep -v "useParams<"

# 检测 params 后直接使用无类型断言
grep -rn "const.*=.*useParams()" src/ --include="*.tsx"
```

**修正**：
```typescript
// ❌ 错误：无类型注解
function WorkflowEditor() {
  const { id } = useParams();  // id: string | undefined

  // 需要处理 undefined
  if (!id) return null;

  return <Editor id={id} />;
}

// ✅ 正确：带类型注解
interface WorkflowParams {
  id: string;
}

function WorkflowEditor() {
  const { id } = useParams<WorkflowParams>();  // 类型明确

  // 仍需处理可能的 undefined（路由不匹配时）
  if (!id) return <Navigate to="/404" replace />;

  return <Editor id={id} />;
}

// ✅ 更好：使用 invariant 断言
import invariant from 'tiny-invariant';

function WorkflowEditor() {
  const { id } = useParams<WorkflowParams>();
  invariant(id, 'Workflow ID is required');  // 运行时保护

  return <Editor id={id} />;  // id 是 string
}
```

---

### 反模式 2.5: 路由路径硬编码

**问题**：路由路径散落在各处，修改时容易遗漏，导致链接失效。

**检测**：
```bash
# 统计硬编码路径数量
grep -rn "navigate(\"/\\|to=\"/" src/ --include="*.tsx" | wc -l

# 检测非常量路径
grep -rn "navigate(\"/" src/ --include="*.tsx" | head -10
```

**修正**：
```typescript
// ❌ 错误：路径硬编码
function NavBar() {
  return (
    <nav>
      <Link to="/dashboard">仪表盘</Link>
      <Link to="/workflow">工作流</Link>
      <Link to="/settings/profile">个人设置</Link>
    </nav>
  );
}

function handleClick() {
  navigate('/workflow/123/edit');
}

// ✅ 正确：集中定义路由常量
// routes/paths.ts
export const ROUTES = {
  HOME: '/',
  DASHBOARD: '/dashboard',
  WORKFLOW: {
    LIST: '/workflow',
    DETAIL: (id: string) => `/workflow/${id}`,
    EDIT: (id: string) => `/workflow/${id}/edit`,
  },
  SETTINGS: {
    PROFILE: '/settings/profile',
    SECURITY: '/settings/security',
  },
} as const;

// 使用
function NavBar() {
  return (
    <nav>
      <Link to={ROUTES.DASHBOARD}>仪表盘</Link>
      <Link to={ROUTES.WORKFLOW.LIST}>工作流</Link>
      <Link to={ROUTES.SETTINGS.PROFILE}>个人设置</Link>
    </nav>
  );
}

function handleClick(id: string) {
  navigate(ROUTES.WORKFLOW.EDIT(id));
}
```

---

## 3. 最佳实践 (Golden Paths)

### 3.1 路由配置

```typescript
// src/router/index.tsx
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import { ROUTES } from './paths';
import { ProtectedRoute } from './guards/ProtectedRoute';
import { RootLayout } from '@/layouts/RootLayout';
import { ErrorPage } from '@/pages/errors/ErrorPage';

const router = createBrowserRouter([
  {
    path: ROUTES.HOME,
    element: <RootLayout />,
    errorElement: <ErrorPage />,  // ⚠️ 必须配置
    children: [
      { index: true, element: <Home /> },
      { path: 'about', element: <About /> },
      {
        path: 'workflow',
        element: (
          <ProtectedRoute requiredPermissions={['workflow:read']}>
            <WorkflowLayout />
          </ProtectedRoute>
        ),
        children: [
          { index: true, element: <WorkflowList /> },
          { path: ':id', element: <WorkflowEditor /> },
          { path: ':id/edit', element: <WorkflowEditor mode="edit" /> },
        ],
      },
      {
        path: 'settings',
        element: <ProtectedRoute><SettingsLayout /></ProtectedRoute>,
        children: [
          { path: 'profile', element: <Profile /> },
          { path: 'security', element: <Security /> },
        ],
      },
    ],
  },
  { path: '/login', element: <Login /> },
  { path: '/auth/callback', element: <AuthCallback /> },
  { path: '/403', element: <Forbidden /> },
  { path: '*', element: <NotFound /> },
]);

export function AppRouter() {
  return <RouterProvider router={router} />;
}
```

### 3.2 完整路由守卫

```typescript
// src/router/guards/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '@/features/auth/hooks/useAuth';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ROUTES } from '../paths';

interface ProtectedRouteProps {
  children: React.ReactNode;
  requiredPermissions?: string[];
  requiredRoles?: string[];
}

export function ProtectedRoute({
  children,
  requiredPermissions = [],
  requiredRoles = [],
}: ProtectedRouteProps) {
  const { isAuthenticated, isLoading, user } = useAuth();
  const location = useLocation();

  // 1. 加载状态
  if (isLoading) {
    return <LoadingSpinner fullScreen />;
  }

  // 2. 未认证 → 登录页（保存来源）
  if (!isAuthenticated) {
    return (
      <Navigate
        to="/login"
        state={{ from: location }}
        replace
      />
    );
  }

  // 3. 角色检查
  if (requiredRoles.length > 0) {
    const hasRole = requiredRoles.some(role =>
      user?.roles?.includes(role)
    );
    if (!hasRole) {
      return <Navigate to="/403" replace />;
    }
  }

  // 4. 权限检查
  if (requiredPermissions.length > 0) {
    const hasPermission = requiredPermissions.every(
      perm => user?.permissions?.includes(perm)
    );
    if (!hasPermission) {
      return <Navigate to="/403" replace />;
    }
  }

  return <>{children}</>;
}
```

### 3.3 路由常量定义

```typescript
// src/router/paths.ts
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  AUTH_CALLBACK: '/auth/callback',
  FORBIDDEN: '/403',
  NOT_FOUND: '/404',

  DASHBOARD: '/dashboard',

  WORKFLOW: {
    LIST: '/workflow',
    DETAIL: (id: string) => `/workflow/${id}` as const,
    EDIT: (id: string) => `/workflow/${id}/edit` as const,
    CREATE: '/workflow/new',
  },

  SETTINGS: {
    ROOT: '/settings',
    PROFILE: '/settings/profile',
    SECURITY: '/settings/security',
    NOTIFICATIONS: '/settings/notifications',
  },
} as const;

// 类型安全的路由参数
export type WorkflowParams = {
  id: string;
};

export type SettingsParams = {
  tab?: 'profile' | 'security' | 'notifications';
};
```

### 3.4 动态路由与 searchParams

```typescript
import { useParams, useSearchParams, useNavigate } from 'react-router-dom';
import type { WorkflowParams } from '@/router/paths';

function WorkflowEditor() {
  const { id } = useParams<WorkflowParams>();
  const [searchParams, setSearchParams] = useSearchParams();
  const navigate = useNavigate();

  // 读取 query 参数
  const nodeId = searchParams.get('nodeId');
  const tab = searchParams.get('tab') || 'canvas';

  // 更新 query 参数（不刷新页面）
  const selectNode = (nodeId: string) => {
    setSearchParams(prev => {
      prev.set('nodeId', nodeId);
      return prev;
    });
  };

  // 清除 query 参数
  const clearSelection = () => {
    setSearchParams(prev => {
      prev.delete('nodeId');
      return prev;
    });
  };

  // 切换 tab（保留其他参数）
  const switchTab = (newTab: string) => {
    setSearchParams(prev => {
      prev.set('tab', newTab);
      return prev;
    });
  };

  return (
    <Editor
      workflowId={id!}
      selectedNodeId={nodeId}
      activeTab={tab}
      onNodeSelect={selectNode}
      onTabChange={switchTab}
    />
  );
}
```

### 3.5 登录重定向

```typescript
// src/pages/Login.tsx
import { useNavigate, useLocation } from 'react-router-dom';
import { ROUTES } from '@/router/paths';

function LoginPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const { login } = useAuth();

  // 获取来源页面
  const from = (location.state as { from?: Location })?.from?.pathname
    || ROUTES.DASHBOARD;

  const handleLogin = async (credentials: LoginCredentials) => {
    try {
      await login(credentials);
      // 登录成功，跳转回原页面（replace 防止返回登录页）
      navigate(from, { replace: true });
    } catch (error) {
      // 处理错误
    }
  };

  return (
    <LoginForm
      onSubmit={handleLogin}
      redirectHint={from !== ROUTES.DASHBOARD ? `登录后返回 ${from}` : undefined}
    />
  );
}
```

---

## 4. 自我验证 (Self-Verification)

### React Router 合规审计脚本

```bash
#!/bin/bash
# router-audit.sh - React Router 代码合规检查

echo "🛤️ React Router 合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测渲染中的 navigate 调用
echo -e "\n🚫 检测渲染中的 navigate..."
RENDER_NAV=$(grep -B5 "navigate(" src/ -r --include="*.tsx" 2>/dev/null | \
  grep -c "if.*{" || echo "0")

if [ "$RENDER_NAV" -gt 0 ]; then
    echo "⚠️ 可能在渲染中调用 navigate ($RENDER_NAV 处)"
    echo "   建议检查是否应该移到 useEffect 中"
else
    echo "✅ navigate 调用位置正常"
fi

# 2. 检测缺少 replace 的 Navigate
echo -e "\n🔄 检测 Navigate replace..."
MISSING_REPLACE=$(grep -rn "<Navigate" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "replace" | wc -l | tr -d ' ')

if [ "$MISSING_REPLACE" -gt 0 ]; then
    echo "❌ Navigate 组件缺少 replace:"
    grep -rn "<Navigate" src/ --include="*.tsx" 2>/dev/null | \
      grep -v "replace" | head -5
    ((ERRORS++))
else
    echo "✅ Navigate 都使用了 replace"
fi

# 3. 检测 ProtectedRoute 加载状态
echo -e "\n⏳ 检测守卫加载状态..."
GUARD_FILES=$(grep -rln "ProtectedRoute\|AuthGuard\|RouteGuard" src/ --include="*.tsx" 2>/dev/null)
MISSING_LOADING=""

for file in $GUARD_FILES; do
    if ! grep -q "isLoading\|Loading" "$file" 2>/dev/null; then
        MISSING_LOADING="$MISSING_LOADING\n  - $file"
    fi
done

if [ -n "$MISSING_LOADING" ]; then
    echo "❌ 守卫组件缺少加载状态:$MISSING_LOADING"
    ((ERRORS++))
else
    echo "✅ 守卫组件有加载状态"
fi

# 4. 检测 useParams 类型
echo -e "\n📝 检测 useParams 类型..."
UNTYPED_PARAMS=$(grep -rn "useParams()" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "useParams<" | wc -l | tr -d ' ')

if [ "$UNTYPED_PARAMS" -gt 0 ]; then
    echo "⚠️ useParams 缺少类型注解 ($UNTYPED_PARAMS 处):"
    grep -rn "useParams()" src/ --include="*.tsx" 2>/dev/null | \
      grep -v "useParams<" | head -5
else
    echo "✅ useParams 都有类型注解"
fi

# 5. 检测 errorElement 配置
echo -e "\n🚨 检测 errorElement..."
ROUTER_FILES=$(grep -rln "createBrowserRouter" src/ --include="*.tsx" 2>/dev/null)
MISSING_ERROR=""

for file in $ROUTER_FILES; do
    if ! grep -q "errorElement" "$file" 2>/dev/null; then
        MISSING_ERROR="$MISSING_ERROR\n  - $file"
    fi
done

if [ -n "$MISSING_ERROR" ]; then
    echo "❌ 路由配置缺少 errorElement:$MISSING_ERROR"
    ((ERRORS++))
else
    echo "✅ 已配置 errorElement"
fi

# 6. 检测硬编码路径
echo -e "\n🔗 检测硬编码路径..."
HARDCODED=$(grep -rn "navigate(\"/\\|to=\"/" src/ --include="*.tsx" 2>/dev/null | wc -l | tr -d ' ')

if [ "$HARDCODED" -gt 10 ]; then
    echo "⚠️ 发现 $HARDCODED 处硬编码路径"
    echo "   建议使用路由常量 (ROUTES.xxx)"
else
    if [ "$HARDCODED" -gt 0 ]; then
        echo "💡 发现 $HARDCODED 处硬编码路径（可接受）"
    else
        echo "✅ 未发现硬编码路径"
    fi
fi

# 7. 检测旧版 BrowserRouter
echo -e "\n📦 检测 Router 版本..."
OLD_ROUTER=$(grep -rn "BrowserRouter" src/ --include="*.tsx" 2>/dev/null | \
  grep -v "createBrowserRouter" | wc -l | tr -d ' ')

if [ "$OLD_ROUTER" -gt 0 ]; then
    echo "⚠️ 发现旧版 BrowserRouter ($OLD_ROUTER 处)"
    echo "   建议升级到 createBrowserRouter"
else
    echo "✅ 使用 createBrowserRouter"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ React Router 审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个问题"
    exit 1
fi
```

### 快速检查清单

- [ ] 使用 `createBrowserRouter`（v6.4+ 数据 API）
- [ ] 配置了 `errorElement` 捕获路由错误
- [ ] `Navigate` 组件使用了 `replace` 属性
- [ ] 路由守卫处理了 `isLoading` 加载状态
- [ ] `useNavigate` 在 `useEffect` 或事件中调用
- [ ] `useParams` 带类型注解 `useParams<Params>()`
- [ ] 路由路径使用常量定义（`ROUTES.xxx`）
- [ ] 登录成功后使用 `replace: true` 跳转

---

## 🔗 与全局 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `oidc-auth-patterns` | 认证状态驱动路由守卫 |
| `zustand-patterns` | 路由状态持久化 |
| `react-query-patterns` | 路由 loader 数据预取 |
| `code-quality-gates` | 检查路由配置完整性 |

### 关联文件

- `src/router/index.tsx`
- `src/router/paths.ts`
- `src/router/guards/*.tsx`
- `src/layouts/*.tsx`

---

**✅ React Router Patterns v2.0.0** | **标准 4 Section 已集成**
