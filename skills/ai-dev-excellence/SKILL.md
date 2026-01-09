---
name: ai-dev-excellence
description: |
  AI 辅助开发卓越指南。当涉及 AI 编程、Prompt 工程、Claude/GPT 最佳实践时自动触发。
  关键词：AI开发、Claude、OpenAI、GPT、Prompt工程、LLM、Agent、代码质量。
  【AI开发卓越】包含 Prompt 工程、AI 编程模式、代码质量、架构设计、20年资深水准。
allowed-tools: Read, Grep, Glob, WebFetch, WebSearch
---

# AI 辅助开发卓越指南

## 20年资深工程师标准

### 思维模式

```
初级工程师：完成任务
├── "它能工作"

中级工程师：完成正确
├── "它工作得很好"
├── "代码整洁"

高级工程师：完成优雅
├── "它解决了正确的问题"
├── "易于维护和扩展"
├── "考虑了边界情况"

资深工程师 (Staff+)：系统思维
├── "它如何影响整个系统"
├── "未来 3-5 年的可扩展性"
├── "团队效率和知识传承"
├── "技术债务和偿还策略"
└── "业务价值和技术权衡"
```

### 代码质量金字塔

```
                    /\
                   /  \
                  /可读\        代码能被其他人理解
                 /------\
                /        \
               /  可维护  \     变更成本可控
              /------------\
             /              \
            /    可测试     \   行为可验证
           /------------------\
          /                    \
         /      可扩展         \  功能可演进
        /------------------------\
       /                          \
      /         可靠性            \  错误可恢复
     /------------------------------\
    /                                \
   /           安全性                \ 数据受保护
  /------------------------------------\
```

## Prompt 工程原则

### 有效 Prompt 结构

```markdown
## 角色 (Role)
你是一位资深软件工程师，专注于 [领域]...

## 上下文 (Context)
- 项目背景: ...
- 技术栈: ...
- 约束条件: ...

## 任务 (Task)
请帮我 [具体任务]...

## 格式 (Format)
请按以下格式输出：
1. 分析
2. 方案
3. 代码
4. 测试

## 示例 (Examples)
输入: ...
期望输出: ...

## 约束 (Constraints)
- 不要 ...
- 确保 ...
```

### 迭代优化策略

| 策略 | 说明 | 示例 |
|------|------|------|
| **分解复杂任务** | 大任务拆小步骤 | 先设计 → 再实现 → 后测试 |
| **提供上下文** | 相关代码/文档 | 附上现有代码结构 |
| **明确约束** | 技术限制/风格 | "使用 TypeScript strict" |
| **请求解释** | 理解思路 | "解释为什么选择这个方案" |
| **迭代反馈** | 逐步完善 | "这里有问题，请修改..." |

### 高效协作模式

```
Plan → Review → Execute → Verify

1. 规划阶段
   - 明确需求和目标
   - AI 提供技术方案
   - 人类审核和调整

2. 审查阶段
   - AI 生成初步代码
   - 人类检查逻辑正确性
   - 讨论优化点

3. 执行阶段
   - 并行处理多个任务
   - 持续沟通和调整
   - 增量交付

4. 验证阶段
   - 运行测试
   - 代码审查
   - 性能评估
```

## AI 编程最佳实践

### 代码生成原则

| 原则 | 说明 | 检查项 |
|------|------|--------|
| **正确性优先** | 功能正确 > 优雅 | 逻辑验证、边界测试 |
| **可读性** | 清晰表达意图 | 命名、注释、结构 |
| **健壮性** | 处理异常情况 | 错误处理、类型安全 |
| **可维护性** | 易于修改 | 模块化、低耦合 |
| **安全性** | 防护攻击 | 输入验证、权限检查 |

### 代码审查清单

```markdown
## 功能性
- [ ] 实现了所有需求
- [ ] 边界条件处理正确
- [ ] 错误处理完备

## 代码质量
- [ ] 函数职责单一 (< 40 行)
- [ ] 命名清晰准确
- [ ] 无重复代码 (DRY)
- [ ] 无过度设计 (YAGNI)

## 类型安全
- [ ] 无 any 类型
- [ ] 类型定义完整
- [ ] 泛型使用合理

## 安全性
- [ ] 无 SQL 注入风险
- [ ] 无 XSS 风险
- [ ] 敏感信息加密

## 性能
- [ ] 无 N+1 查询
- [ ] 合理使用缓存
- [ ] 避免不必要的计算

## 测试
- [ ] 单元测试覆盖
- [ ] 关键路径测试
- [ ] 边界条件测试
```

### 常见陷阱与防护

```typescript
// ❌ 陷阱 1: 过度依赖 AI 生成的代码
// AI 可能生成看起来正确但有微妙 bug 的代码
function processData(data) {
  return data.map(item => item.value); // data 可能为 null
}

// ✅ 防护: 始终添加防御性检查
function processData(data: Item[] | null): number[] {
  if (!data || data.length === 0) {
    return [];
  }
  return data.map(item => item.value ?? 0);
}

// ❌ 陷阱 2: 忽略边界条件
function divide(a, b) {
  return a / b; // b 可能为 0
}

// ✅ 防护: 显式处理边界
function divide(a: number, b: number): number {
  if (b === 0) {
    throw new Error('Division by zero');
  }
  return a / b;
}

// ❌ 陷阱 3: 不验证 AI 的假设
// AI: "这个 API 返回 JSON 数组"
const users = await fetch('/api/users').then(r => r.json());
users.forEach(u => console.log(u.name)); // users 可能不是数组

// ✅ 防护: 验证数据结构
const response = await fetch('/api/users');
const data = await response.json();

if (!Array.isArray(data)) {
  throw new Error('Expected array response');
}

const users = data as User[];
```

## 架构设计原则

### 系统设计思维

```
需求分析
├── 功能需求: 系统应该做什么
├── 非功能需求: 性能、可用性、安全性
├── 约束条件: 时间、预算、技术栈
└── 未来演进: 可扩展性考量

架构决策
├── 分层架构 vs 微服务
├── 同步 vs 异步
├── 一致性 vs 可用性
└── 简单性 vs 灵活性

权衡分析
├── 短期收益 vs 长期维护
├── 开发效率 vs 运行效率
├── 团队能力 vs 技术理想
└── 业务需求 vs 技术债务
```

### 模块设计准则

| 准则 | 说明 | 实践 |
|------|------|------|
| **高内聚** | 相关功能聚合 | 按领域划分模块 |
| **低耦合** | 模块间松散依赖 | 依赖注入、接口隔离 |
| **单一职责** | 一个模块一个变化原因 | 拆分大模块 |
| **开闭原则** | 对扩展开放，对修改关闭 | 策略模式、插件架构 |
| **依赖倒置** | 依赖抽象不依赖具体 | 接口编程 |

### API 设计规范

```typescript
// RESTful API 设计

// 1. 资源命名：名词复数
GET    /api/users        // 获取用户列表
GET    /api/users/:id    // 获取单个用户
POST   /api/users        // 创建用户
PUT    /api/users/:id    // 更新用户
DELETE /api/users/:id    // 删除用户

// 2. 查询参数：过滤、排序、分页
GET /api/users?role=admin&sort=-createdAt&page=1&limit=20

// 3. 响应格式：一致的结构
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    code: string;
    message: string;
    details?: unknown;
  };
  meta?: {
    page: number;
    limit: number;
    total: number;
  };
}

// 4. HTTP 状态码
// 200 OK - 成功
// 201 Created - 创建成功
// 400 Bad Request - 请求参数错误
// 401 Unauthorized - 未认证
// 403 Forbidden - 无权限
// 404 Not Found - 资源不存在
// 422 Unprocessable Entity - 验证失败
// 500 Internal Server Error - 服务器错误
```

## 错误处理哲学

### 错误分类与处理

```typescript
// 1. 可预期错误：业务逻辑错误
class BusinessError extends Error {
  constructor(
    message: string,
    public code: string,
    public statusCode: number = 400
  ) {
    super(message);
    this.name = 'BusinessError';
  }
}

// 使用
throw new BusinessError('用户不存在', 'USER_NOT_FOUND', 404);

// 2. 编程错误：开发者错误
// 使用断言，在开发阶段发现
function processUser(user: User) {
  console.assert(user != null, 'User must not be null');
  // ...
}

// 3. 外部错误：第三方服务错误
async function fetchExternalData() {
  try {
    return await externalApi.getData();
  } catch (error) {
    // 记录原始错误
    logger.error('External API failed', { error });
    // 转换为应用错误
    throw new BusinessError('服务暂时不可用', 'SERVICE_UNAVAILABLE', 503);
  }
}

// 4. 全局错误处理
app.use((error: Error, req: Request, res: Response, next: NextFunction) => {
  if (error instanceof BusinessError) {
    return res.status(error.statusCode).json({
      success: false,
      error: {
        code: error.code,
        message: error.message,
      },
    });
  }

  // 未预期错误
  logger.error('Unexpected error', { error });
  return res.status(500).json({
    success: false,
    error: {
      code: 'INTERNAL_ERROR',
      message: '服务器内部错误',
    },
  });
});
```

### 优雅降级策略

```typescript
// 多层降级策略
async function getData(id: string): Promise<Data> {
  // 1. 尝试从缓存获取
  const cached = await cache.get(id);
  if (cached) {
    return cached;
  }

  try {
    // 2. 尝试从主数据源获取
    const data = await primaryDb.findById(id);
    await cache.set(id, data);
    return data;
  } catch (primaryError) {
    logger.warn('Primary DB failed, trying replica', { primaryError });

    try {
      // 3. 尝试从只读副本获取
      return await replicaDb.findById(id);
    } catch (replicaError) {
      logger.error('All sources failed', { primaryError, replicaError });

      // 4. 返回降级数据
      return getDefaultData(id);
    }
  }
}
```

## 测试策略

### 测试设计原则

```typescript
// 1. 测试行为，而非实现
// ❌ 测试实现细节
it('should call validateEmail function', () => {
  const spy = jest.spyOn(utils, 'validateEmail');
  userService.createUser({ email: 'test@example.com' });
  expect(spy).toHaveBeenCalled();
});

// ✅ 测试行为
it('should reject invalid email', async () => {
  await expect(
    userService.createUser({ email: 'invalid' })
  ).rejects.toThrow('Invalid email format');
});

// 2. 测试边界条件
describe('divide', () => {
  it('should divide two positive numbers', () => {
    expect(divide(10, 2)).toBe(5);
  });

  it('should handle zero numerator', () => {
    expect(divide(0, 5)).toBe(0);
  });

  it('should throw on zero denominator', () => {
    expect(() => divide(10, 0)).toThrow('Division by zero');
  });

  it('should handle negative numbers', () => {
    expect(divide(-10, 2)).toBe(-5);
  });

  it('should handle floating point', () => {
    expect(divide(1, 3)).toBeCloseTo(0.333, 2);
  });
});

// 3. 使用测试工厂
function createUser(overrides: Partial<User> = {}): User {
  return {
    id: 'user-123',
    name: 'Test User',
    email: 'test@example.com',
    role: 'user',
    createdAt: new Date(),
    ...overrides,
  };
}

it('should update admin user', async () => {
  const admin = createUser({ role: 'admin' });
  // ...
});
```

## 文档与知识传承

### 代码即文档

```typescript
/**
 * 计算订单总价
 *
 * @description
 * 根据商品列表计算总价，包含以下计算规则：
 * 1. 基础价格 = 单价 × 数量
 * 2. 折扣 = 基础价格 × 折扣率
 * 3. 税费 = (基础价格 - 折扣) × 税率
 *
 * @param items - 订单商品列表
 * @param taxRate - 税率 (0-1)，默认 0.1 (10%)
 * @returns 订单总价（单位：分）
 *
 * @example
 * const total = calculateOrderTotal([
 *   { price: 1000, quantity: 2, discount: 0.1 },
 *   { price: 500, quantity: 1, discount: 0 },
 * ]);
 * // total = (1000 * 2 * 0.9 + 500 * 1) * 1.1 = 2530
 *
 * @throws {ValidationError} 当商品价格或数量为负数时
 */
function calculateOrderTotal(
  items: OrderItem[],
  taxRate: number = 0.1
): number {
  // 实现...
}
```

### ADR (Architecture Decision Records)

```markdown
# ADR-001: 选择 PostgreSQL 作为主数据库

## 状态
已采纳

## 上下文
我们需要为新项目选择主数据库。团队考虑了 PostgreSQL、MySQL 和 MongoDB。

## 决策
选择 PostgreSQL 作为主数据库。

## 理由
1. 强大的 JSON 支持，兼顾关系型和文档型
2. 高级索引特性（GiST, GIN）
3. 强一致性保证
4. 团队有 PostgreSQL 经验

## 后果
- 正面：高性能复杂查询，强数据一致性
- 负面：水平扩展相对困难
- 缓解：使用读写分离，必要时分库分表

## 记录
- 日期：2024-01-15
- 决策者：技术负责人, 后端团队
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `google-dev-quality` | 代码质量标准 |
| `apple-hig-design` | 用户体验设计 |
| `interaction-design-science` | 交互设计理论 |

### 参考资源

- [Anthropic Claude Documentation](https://docs.anthropic.com/)
- [OpenAI Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
- [Google Engineering Practices](https://google.github.io/eng-practices/)
- [The Pragmatic Programmer](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/)
