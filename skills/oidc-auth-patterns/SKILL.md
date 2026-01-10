---
name: oidc-auth-patterns
description: |
  OIDC/SSO 认证最佳实践。当涉及登录、Token 刷新、401 处理、跨标签页同步时自动触发。
  关键词：OIDC、SSO、Token、认证、登录、401、刷新、oauth、jwt。
  【认证核心】包含 Token 管理、请求队列、跨标签页同步。
allowed-tools: Read, Grep, Glob
---

# OIDC/SSO 认证模式

## 项目架构

```
src/features/auth/
├── components/
│   ├── AuthCallback.tsx      # OIDC 回调处理
│   └── ProtectedRoute.tsx    # 路由守卫
├── hooks/
│   ├── useAuth.ts            # 认证 Hook
│   └── useTokenRefresh.ts    # Token 刷新
├── services/
│   └── authService.ts        # 认证服务
└── store/
    └── authStore.ts          # 认证状态
```

## 核心模式

### 1. Token 管理

```typescript
// src/features/auth/services/authService.ts
import { UserManager, User } from 'oidc-client-ts';

class AuthService {
  private userManager: UserManager;
  private refreshPromise: Promise<User> | null = null;

  constructor() {
    this.userManager = new UserManager({
      authority: import.meta.env.VITE_OIDC_SSO_URL,
      client_id: 'moss-ai',
      redirect_uri: `${window.location.origin}/auth/callback`,
      response_type: 'code',
      scope: 'openid profile',
      automaticSilentRenew: true,
      silent_redirect_uri: `${window.location.origin}/silent-renew.html`,
    });

    // 监听 Token 过期
    this.userManager.events.addAccessTokenExpiring(() => {
      console.log('Token 即将过期，静默刷新...');
      this.silentRenew();
    });
  }

  async getAccessToken(): Promise<string | null> {
    const user = await this.userManager.getUser();
    if (!user || user.expired) {
      return null;
    }
    return user.access_token;
  }

  async silentRenew(): Promise<User> {
    // 防止并发刷新
    if (this.refreshPromise) {
      return this.refreshPromise;
    }

    this.refreshPromise = this.userManager.signinSilent();

    try {
      const user = await this.refreshPromise;
      return user;
    } finally {
      this.refreshPromise = null;
    }
  }

  async login(): Promise<void> {
    await this.userManager.signinRedirect();
  }

  async logout(): Promise<void> {
    await this.userManager.signoutRedirect();
  }
}

export const authService = new AuthService();
```

### 2. 401 请求队列（核心）

```typescript
// src/utils/request.ts
import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { authService } from '@/features/auth/services/authService';

interface FailedRequest {
  config: InternalAxiosRequestConfig;
  resolve: (value: any) => void;
  reject: (error: any) => void;
}

class RequestQueue {
  private isRefreshing = false;
  private failedQueue: FailedRequest[] = [];
  private lockKey = 'token_refresh_lock';

  // 跨标签页锁
  private async acquireLock(): Promise<boolean> {
    const lockValue = Date.now().toString();
    const existingLock = localStorage.getItem(this.lockKey);

    if (existingLock) {
      const lockTime = parseInt(existingLock, 10);
      // 锁超时 30 秒
      if (Date.now() - lockTime < 30000) {
        return false;
      }
    }

    localStorage.setItem(this.lockKey, lockValue);
    return true;
  }

  private releaseLock(): void {
    localStorage.removeItem(this.lockKey);
  }

  async handle401(error: AxiosError): Promise<any> {
    const originalRequest = error.config!;

    // 已经在刷新中，加入队列
    if (this.isRefreshing) {
      return new Promise((resolve, reject) => {
        this.failedQueue.push({
          config: originalRequest,
          resolve,
          reject,
        });
      });
    }

    // 尝试获取锁
    const hasLock = await this.acquireLock();
    if (!hasLock) {
      // 其他标签页在刷新，等待
      return new Promise((resolve) => {
        const listener = (event: StorageEvent) => {
          if (event.key === 'access_token' && event.newValue) {
            window.removeEventListener('storage', listener);
            originalRequest.headers.Authorization = `Bearer ${event.newValue}`;
            resolve(axios(originalRequest));
          }
        };
        window.addEventListener('storage', listener);
      });
    }

    this.isRefreshing = true;

    try {
      const user = await authService.silentRenew();
      const newToken = user.access_token;

      // 广播新 Token
      localStorage.setItem('access_token', newToken);

      // 处理队列
      this.failedQueue.forEach(({ config, resolve }) => {
        config.headers.Authorization = `Bearer ${newToken}`;
        resolve(axios(config));
      });
      this.failedQueue = [];

      // 重试原请求
      originalRequest.headers.Authorization = `Bearer ${newToken}`;
      return axios(originalRequest);

    } catch (refreshError) {
      // 刷新失败，拒绝所有队列
      this.failedQueue.forEach(({ reject }) => {
        reject(refreshError);
      });
      this.failedQueue = [];

      // 跳转登录
      authService.login();
      throw refreshError;

    } finally {
      this.isRefreshing = false;
      this.releaseLock();
    }
  }
}

const requestQueue = new RequestQueue();

// Axios 拦截器
axios.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    if (error.response?.status === 401) {
      return requestQueue.handle401(error);
    }
    return Promise.reject(error);
  }
);
```

### 3. 路由守卫

```typescript
// src/features/auth/components/ProtectedRoute.tsx
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

export function ProtectedRoute({ children }: { children: React.ReactNode }) {
  const { isAuthenticated, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  return <>{children}</>;
}
```

### 4. 跨标签页同步

```typescript
// src/features/auth/hooks/useTokenSync.ts
import { useEffect } from 'react';
import { useAuthStore } from '../store/authStore';

export function useTokenSync() {
  const { setToken, logout } = useAuthStore();

  useEffect(() => {
    const handleStorageChange = (event: StorageEvent) => {
      if (event.key === 'access_token') {
        if (event.newValue) {
          setToken(event.newValue);
        } else {
          // Token 被清除，其他标签页登出
          logout();
        }
      }
    };

    window.addEventListener('storage', handleStorageChange);
    return () => window.removeEventListener('storage', handleStorageChange);
  }, [setToken, logout]);
}
```

## 常见陷阱

### ❌ 陷阱 1：并发刷新 Token

```typescript
// ❌ 错误：每个 401 都触发刷新
interceptors.response.use(null, async (error) => {
  if (error.response?.status === 401) {
    await authService.silentRenew();  // 多个请求同时刷新！
  }
});

// ✅ 正确：使用队列和锁
if (this.isRefreshing) {
  return new Promise((resolve, reject) => {
    this.failedQueue.push({ config, resolve, reject });
  });
}
```

### ❌ 陷阱 2：跨标签页竞争

```typescript
// ❌ 错误：不考虑其他标签页
await authService.silentRenew();

// ✅ 正确：使用 localStorage 锁
const hasLock = await this.acquireLock();
if (!hasLock) {
  // 等待其他标签页刷新
  return this.waitForRefresh();
}
```

### ❌ 陷阱 3：忘记清理监听器

```typescript
// ❌ 错误：内存泄漏
useEffect(() => {
  window.addEventListener('storage', handleStorageChange);
}, []);

// ✅ 正确：清理
useEffect(() => {
  window.addEventListener('storage', handleStorageChange);
  return () => window.removeEventListener('storage', handleStorageChange);
}, []);
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `signalr-patterns` | SignalR 连接使用 accessTokenFactory |
| `react-query-patterns` | 401 时触发重试 |
| `zustand-patterns` | 认证状态存储 |

---

**✅ OIDC 认证 Skill 已集成**
