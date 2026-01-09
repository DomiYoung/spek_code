---
name: google-dev-quality
description: |
  Google 开发指南与质量标准。当涉及 Material Design、Android 开发、Web 性能、代码质量时自动触发。
  关键词：Material Design、Android、Google、性能、Core Web Vitals、代码审查、最佳实践。
  【开发质量】包含设计系统、性能优化、代码规范、测试策略、可访问性。
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# Google 开发指南与质量标准

## Material Design 3

### 设计原则

| 原则 | 说明 | 应用 |
|------|------|------|
| **个性化** | 用户自定义体验 | Dynamic Color |
| **适应性** | 跨设备一致 | Responsive Layout |
| **表达性** | 品牌可辨识 | 主题定制 |

### 颜色系统 (Dynamic Color)

```
Primary (主色)
├── Primary
├── On Primary
├── Primary Container
└── On Primary Container

Secondary (次色)
├── Secondary
├── On Secondary
├── Secondary Container
└── On Secondary Container

Tertiary (三级色)
├── Tertiary
├── On Tertiary
├── Tertiary Container
└── On Tertiary Container

Error (错误)
├── Error
├── On Error
├── Error Container
└── On Error Container

Surface (表面)
├── Surface
├── On Surface
├── Surface Variant
├── On Surface Variant
└── Outline
```

### 排版系统

| 角色 | 用途 | 规范 |
|------|------|------|
| Display Large | 英雄区 | 57sp |
| Display Medium | 大标题 | 45sp |
| Display Small | 次标题 | 36sp |
| Headline Large | 标题 | 32sp |
| Headline Medium | 区块标题 | 28sp |
| Headline Small | 小标题 | 24sp |
| Title Large | 强调 | 22sp |
| Title Medium | 列表标题 | 16sp, Medium |
| Title Small | 次级标题 | 14sp, Medium |
| Body Large | 正文 | 16sp |
| Body Medium | 次要正文 | 14sp |
| Body Small | 辅助文本 | 12sp |
| Label Large | 按钮 | 14sp, Medium |
| Label Medium | 标签 | 12sp, Medium |
| Label Small | 小标签 | 11sp, Medium |

### 组件规范

| 组件 | 高度 | 圆角 | 海拔 |
|------|------|------|------|
| FAB | 56dp | 16dp | 3dp |
| Extended FAB | 56dp | 16dp | 3dp |
| Button (Filled) | 40dp | 20dp | 0dp |
| Button (Outlined) | 40dp | 20dp | 0dp |
| Card (Filled) | 变化 | 12dp | 0dp |
| Card (Elevated) | 变化 | 12dp | 1dp |
| Dialog | 变化 | 28dp | 3dp |
| Navigation Bar | 80dp | 0dp | 0dp |

### 运动系统

```
Duration:
├── Short 1: 50ms   (微交互)
├── Short 2: 100ms  (简单动画)
├── Short 3: 150ms  (标准动画)
├── Short 4: 200ms  (复杂动画)
├── Medium 1: 250ms (页面过渡)
├── Medium 2: 300ms (模态展开)
├── Medium 3: 350ms (复杂过渡)
├── Medium 4: 400ms (全屏动画)
├── Long 1: 450ms   (大型动画)
├── Long 2: 500ms   (复杂场景)
├── Long 3: 550ms   (戏剧效果)
└── Long 4: 600ms   (叙事动画)

Easing:
├── Emphasized: 加速入场
├── Emphasized Decelerate: 减速出场
├── Standard: 常规运动
├── Standard Accelerate: 加速
└── Standard Decelerate: 减速
```

## Core Web Vitals

### 关键指标

| 指标 | 全称 | 目标 | 说明 |
|------|------|------|------|
| **LCP** | Largest Contentful Paint | < 2.5s | 最大内容绘制 |
| **INP** | Interaction to Next Paint | < 200ms | 交互响应 |
| **CLS** | Cumulative Layout Shift | < 0.1 | 布局稳定性 |

### LCP 优化

```
影响因素:
├── 服务器响应时间 (TTFB)
├── 资源加载时间
├── 客户端渲染时间
└── 关键渲染路径

优化策略:
├── 服务端优化
│   ├── CDN 分发
│   ├── 缓存策略
│   └── 预渲染/SSR
│
├── 资源优化
│   ├── 图片格式 (WebP/AVIF)
│   ├── 响应式图片
│   ├── 预加载关键资源
│   └── 字体优化 (font-display: swap)
│
└── 渲染优化
    ├── 减少 JavaScript 阻塞
    ├── CSS 内联关键路径
    └── 延迟非关键资源
```

### INP 优化

```
影响因素:
├── JavaScript 执行时间
├── 主线程阻塞
└── 事件处理复杂度

优化策略:
├── 代码分割
│   ├── 路由级分割
│   ├── 组件懒加载
│   └── 按需导入
│
├── 任务调度
│   ├── requestIdleCallback
│   ├── scheduler.postTask
│   └── Web Workers
│
└── 渲染优化
    ├── 虚拟滚动
    ├── 防抖/节流
    └── requestAnimationFrame
```

### CLS 优化

```
影响因素:
├── 图片/视频无尺寸
├── 动态注入内容
├── Web 字体加载
└── 异步加载广告

优化策略:
├── 预留空间
│   ├── 设置 width/height
│   ├── aspect-ratio
│   └── 骨架屏
│
├── 字体优化
│   ├── font-display: optional
│   ├── 预加载字体
│   └── size-adjust 回退
│
└── 动态内容
    ├── transform 动画
    ├── 固定位置容器
    └── 避免顶部插入
```

## 代码质量标准

### Google 代码审查指南

```
审查重点:
├── 设计 (Design)
│   ├── 代码是否应该属于这个代码库
│   ├── 是否与系统设计一致
│   └── 现在是否是合适的时机
│
├── 功能 (Functionality)
│   ├── 代码是否实现了预期功能
│   ├── 边界条件处理
│   └── 错误处理完备性
│
├── 复杂度 (Complexity)
│   ├── 代码是否过于复杂
│   ├── 是否容易理解
│   └── 未来是否易于维护
│
├── 测试 (Tests)
│   ├── 测试覆盖是否充分
│   ├── 测试是否有意义
│   └── 测试是否可维护
│
├── 命名 (Naming)
│   ├── 名称是否清晰表达意图
│   ├── 是否遵循命名规范
│   └── 是否避免误导
│
├── 注释 (Comments)
│   ├── 注释是否解释了 WHY
│   ├── 是否避免解释 WHAT
│   └── TODO 是否有跟踪
│
├── 风格 (Style)
│   ├── 是否遵循代码规范
│   ├── 格式是否一致
│   └── 导入是否有序
│
└── 文档 (Documentation)
    ├── API 是否有文档
    ├── 复杂逻辑是否有说明
    └── README 是否更新
```

### 代码复杂度控制

| 指标 | 阈值 | 说明 |
|------|------|------|
| 函数行数 | ≤ 40 行 | 单一职责 |
| 函数参数 | ≤ 4 个 | 使用对象传参 |
| 圈复杂度 | ≤ 10 | 减少分支 |
| 嵌套深度 | ≤ 3 层 | 提前返回 |
| 文件行数 | ≤ 300 行 | 拆分模块 |

### 命名规范

```javascript
// 变量：名词，表达内容
const userList = [];
const isLoading = false;
const hasPermission = true;

// 函数：动词，表达行为
function getUserById(id) {}
function validateEmail(email) {}
function calculateTotal(items) {}

// 类：PascalCase，名词
class UserService {}
class PaymentProcessor {}

// 常量：UPPER_SNAKE_CASE
const MAX_RETRY_COUNT = 3;
const API_BASE_URL = 'https://api.example.com';

// 私有成员：下划线前缀或 # 前缀
class User {
  #password;
  _internalState;
}

// 布尔值：is/has/can/should 前缀
const isVisible = true;
const hasChildren = false;
const canEdit = true;
const shouldUpdate = false;
```

## 测试策略

### 测试金字塔

```
         /\
        /  \
       / E2E \        10%  端到端测试
      /------\
     /        \
    / Integration \   20%  集成测试
   /--------------\
  /                \
 /    Unit Tests    \ 70%  单元测试
/--------------------\
```

### 测试原则

| 原则 | 说明 | 实践 |
|------|------|------|
| **FIRST** | Fast, Independent, Repeatable, Self-validating, Timely | 测试基本要求 |
| **AAA** | Arrange, Act, Assert | 测试结构 |
| **Given-When-Then** | 前置条件, 操作, 期望结果 | BDD 风格 |

### 单元测试规范

```typescript
describe('UserService', () => {
  describe('createUser', () => {
    it('should create a user with valid data', async () => {
      // Arrange
      const userData = { name: 'John', email: 'john@example.com' };

      // Act
      const user = await userService.createUser(userData);

      // Assert
      expect(user).toBeDefined();
      expect(user.name).toBe('John');
      expect(user.email).toBe('john@example.com');
    });

    it('should throw error when email is invalid', async () => {
      // Arrange
      const userData = { name: 'John', email: 'invalid' };

      // Act & Assert
      await expect(userService.createUser(userData))
        .rejects.toThrow('Invalid email format');
    });
  });
});
```

## 可访问性 (A11Y)

### ARIA 最佳实践

```html
<!-- 使用语义化 HTML -->
<nav aria-label="主导航">
  <ul>
    <li><a href="/" aria-current="page">首页</a></li>
    <li><a href="/about">关于</a></li>
  </ul>
</nav>

<!-- 动态内容通知 -->
<div role="status" aria-live="polite">
  已加载 10 条新消息
</div>

<!-- 表单无障碍 -->
<label for="email">邮箱</label>
<input
  id="email"
  type="email"
  aria-describedby="email-hint"
  aria-invalid="true"
  aria-errormessage="email-error"
>
<span id="email-hint">我们不会分享您的邮箱</span>
<span id="email-error" role="alert">请输入有效的邮箱地址</span>
```

### 焦点管理

```javascript
// 模态框焦点陷阱
function trapFocus(element) {
  const focusableElements = element.querySelectorAll(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
  );
  const firstElement = focusableElements[0];
  const lastElement = focusableElements[focusableElements.length - 1];

  element.addEventListener('keydown', (e) => {
    if (e.key !== 'Tab') return;

    if (e.shiftKey && document.activeElement === firstElement) {
      lastElement.focus();
      e.preventDefault();
    } else if (!e.shiftKey && document.activeElement === lastElement) {
      firstElement.focus();
      e.preventDefault();
    }
  });

  firstElement.focus();
}
```

## 安全最佳实践

### OWASP Top 10 防护

| 风险 | 防护措施 |
|------|---------|
| 注入攻击 | 参数化查询、输入验证 |
| 身份认证失败 | MFA、安全会话管理 |
| 敏感数据泄露 | 加密、最小权限 |
| XXE | 禁用外部实体 |
| 访问控制失效 | 基于角色的访问控制 |
| 安全配置错误 | 安全默认配置 |
| XSS | 输出编码、CSP |
| 不安全反序列化 | 完整性检查 |
| 使用已知漏洞组件 | 定期更新依赖 |
| 日志和监控不足 | 完善日志记录 |

### 安全编码原则

```typescript
// 输入验证
function validateInput(input: unknown): string {
  if (typeof input !== 'string') {
    throw new Error('Invalid input type');
  }

  const sanitized = input
    .trim()
    .slice(0, 1000)  // 限制长度
    .replace(/<[^>]*>/g, '');  // 移除 HTML 标签

  return sanitized;
}

// 参数化查询
const user = await db.query(
  'SELECT * FROM users WHERE id = $1',
  [userId]  // 参数化，防止 SQL 注入
);

// Content Security Policy
const csp = {
  'default-src': ["'self'"],
  'script-src': ["'self'", "'strict-dynamic'"],
  'style-src': ["'self'", "'unsafe-inline'"],
  'img-src': ["'self'", 'data:', 'https:'],
  'font-src': ["'self'"],
  'connect-src': ["'self'", 'https://api.example.com'],
  'frame-ancestors': ["'none'"],
  'base-uri': ["'self'"],
  'form-action': ["'self'"],
};
```

## 性能预算

### 资源预算

| 资源类型 | 预算 | 说明 |
|---------|------|------|
| HTML | < 50 KB | 压缩后 |
| CSS | < 100 KB | 关键 CSS 内联 |
| JavaScript | < 300 KB | 首屏 JS |
| 图片 | < 500 KB | 首屏图片 |
| 字体 | < 100 KB | 子集化 |
| 总计 | < 1 MB | 首屏资源 |

### 时间预算

| 指标 | 3G 网络 | 4G 网络 |
|------|---------|---------|
| FCP | < 3s | < 1.5s |
| LCP | < 4s | < 2.5s |
| TTI | < 7.5s | < 3.5s |
| TBT | < 600ms | < 300ms |

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `apple-hig-design` | 跨平台设计对比 |
| `interaction-design-science` | 交互设计理论 |
| `tailwindcss-patterns` | Web 样式实现 |

### 参考资源

- [Material Design 3](https://m3.material.io/)
- [web.dev](https://web.dev/)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [Android Developers](https://developer.android.com/)
