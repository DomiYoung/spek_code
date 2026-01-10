---
name: architect
description: |
  高级系统架构师专家。当涉及系统设计、架构决策、模块划分、技术选型、
  可扩展性设计、SOLID 原则时自动触发。
  关键词：架构、设计、SOLID、模块、扩展性、ADR、技术选型、微服务。
  【架构核心】包含 SOLID 原则、架构模式、边界划分、性能设计。
allowed-tools: Read, Grep, Glob, Task, mcp__sequential-thinking__sequentialthinking
---

# 高级系统架构师知识库

> 基于 [Martin Fowler](https://martinfowler.com/)、[System Design Primer](https://github.com/donnemartin/system-design-primer)、[AWS Well-Architected](https://aws.amazon.com/architecture/well-architected/)

---

## 1. 硬性约束 (Hard Constraints)

### SOLID 原则违反检测

| 约束 | 阈值 | 审计规则 | 严重度 |
|------|------|----------|--------|
| 单一职责 (S) | 文件 ≤ 500 行 | `wc -l *.ts \| awk '$1>500'` | 🔴 Critical |
| 开闭原则 (O) | switch/if-else ≤ 5 分支 | `grep -c "case\|else if" file.ts` | 🟡 Warning |
| 里氏替换 (L) | 继承层级 ≤ 3 | `grep -r "extends.*extends" src/` | 🟡 Warning |
| 接口隔离 (I) | 接口方法 ≤ 7 个 | 手动审查接口定义 | 🟡 Warning |
| 依赖倒置 (D) | 禁止高层直接 new 低层 | `grep -r "new [A-Z].*Repository\|new [A-Z].*Service" src/` | 🔴 Critical |

### 架构边界约束

| 约束 | 规则 | 审计命令 |
|------|------|----------|
| 循环依赖 | 模块间禁止循环引用 | `madge --circular src/` |
| 层级穿透 | UI 层禁止直接访问数据层 | `grep -r "Repository\|DataSource" src/components/` |
| 耦合度 | 跨模块依赖 < 30% | `dependency-cruiser --validate .dependency-cruiser.js src/` |

---

## 2. 反模式 (Anti-Patterns)

### 反模式 2.1: 上帝类 (God Class)

**问题**：单个类/文件承担过多职责，难以维护和测试。

**检测**：
```bash
# 检测超过 500 行的 TypeScript 文件
find src/ -name "*.ts" -exec wc -l {} \; | awk '$1 > 500 {print}'

# 检测单文件导出超过 10 个函数/类
grep -l "export" src/**/*.ts | xargs -I {} sh -c 'echo "{}:"; grep -c "^export" {}'
```

**修正**：
```typescript
// ❌ 错误：上帝类
class UserManager {
  createUser() { /* ... */ }
  validateEmail() { /* ... */ }
  sendNotification() { /* ... */ }
  generateReport() { /* ... */ }
  handlePayment() { /* ... */ }
}

// ✅ 正确：职责分离
class UserService { createUser() { /* ... */ } }
class EmailValidator { validate() { /* ... */ } }
class NotificationService { send() { /* ... */ } }
class ReportGenerator { generate() { /* ... */ } }
class PaymentProcessor { process() { /* ... */ } }
```

---

### 反模式 2.2: 紧耦合依赖

**问题**：高层模块直接实例化低层模块，违反依赖倒置原则。

**检测**：
```bash
# 检测直接 new Repository/Service 的代码
grep -rn "new [A-Z][a-zA-Z]*Repository\|new [A-Z][a-zA-Z]*Service" src/ --include="*.ts"

# 检测组件直接导入数据层
grep -rn "import.*from.*repository\|import.*from.*datasource" src/components/
```

**修正**：
```typescript
// ❌ 错误：直接依赖具体实现
class OrderService {
  private repo = new OrderRepository();  // 紧耦合
}

// ✅ 正确：依赖注入
interface IOrderRepository {
  save(order: Order): Promise<void>;
}

class OrderService {
  constructor(private repo: IOrderRepository) {}  // 依赖抽象
}
```

---

### 反模式 2.3: 分布式单体

**问题**：微服务架构但服务间强耦合，失去独立部署能力。

**检测**：
```bash
# 检测同步跨服务调用链
grep -rn "await.*Service.*await.*Service" src/ --include="*.ts"

# 检测共享数据库表
grep -rn "SELECT.*JOIN.*other_service" src/ --include="*.sql"
```

**修正**：
- 使用事件驱动解耦同步调用
- 每个服务独立数据库
- 通过 API 契约而非共享模型通信

---

### 反模式 2.4: 过早优化

**问题**：在没有性能数据支撑的情况下进行复杂优化。

**检测**：
```bash
# 检测没有性能测试就引入缓存
grep -rn "cache\|memoize\|useMemo" src/ | head -20
# 然后检查是否有对应的性能基准测试
ls tests/performance/ 2>/dev/null || echo "⚠️ 无性能测试目录"
```

**修正**：
1. 先测量，后优化
2. 使用 profiler 定位瓶颈
3. 记录优化前后的性能指标

---

## 3. 最佳实践 (Golden Paths)

### 3.1 架构模式选择

| 模式 | 适用场景 | 优势 | 劣势 |
|------|---------|------|------|
| **Monolith** | 初创/MVP | 简单、部署快 | 扩展难、耦合高 |
| **Modular Monolith** | 中型项目 | 模块清晰、可演进 | 需严格边界 |
| **Microservices** | 大型团队 | 独立部署、技术异构 | 复杂度高 |
| **Event-Driven** | 异步处理 | 解耦、可扩展 | 最终一致性 |
| **CQRS** | 读写分离 | 性能优化 | 复杂度高 |

### 3.2 ADR (Architecture Decision Record) 模板

```markdown
# ADR-{编号}: {决策标题}

## 状态
[Proposed | Accepted | Deprecated | Superseded by ADR-XXX]

## 背景
[描述问题背景和约束条件]

## 决策
[描述做出的决策]

## 备选方案
| 方案 | 优势 | 劣势 | 评分 |
|------|------|------|------|
| 方案 A | ... | ... | ⭐⭐⭐ |
| 方案 B | ... | ... | ⭐⭐ |

## 影响
- 正面：[列出正面影响]
- 负面：[列出负面影响]
- 风险：[列出潜在风险]

## 后续行动
- [ ] 行动项 1
- [ ] 行动项 2
```

### 3.3 模块边界划分

**高内聚低耦合目标**：
```
内聚度 = 模块内部依赖数 / 模块总依赖数 > 0.7
耦合度 = 跨模块依赖数 / 模块总依赖数 < 0.3
```

**依赖方向规则**：
```
UI Layer → Application Layer → Domain Layer → Infrastructure Layer
   ↓              ↓                 ↓                 ↓
  View          UseCase           Entity            Repository
```

### 3.4 技术选型评估框架

| 维度 | 权重 | 考量点 |
|------|------|--------|
| **团队熟悉度** | 25% | 学习曲线、现有经验 |
| **生态成熟度** | 20% | 社区活跃度、第三方库 |
| **性能匹配度** | 20% | 满足 SLA 要求 |
| **可维护性** | 15% | 代码质量、文档完善度 |
| **成本** | 10% | 许可证、基础设施成本 |
| **风险** | 10% | 厂商锁定、技术过时风险 |

### 3.5 性能黄金指标

| 指标 | 说明 | 目标值 |
|------|------|--------|
| **Latency** | 响应时间 | P99 < 500ms |
| **Traffic** | 吞吐量 | 根据业务定 |
| **Errors** | 错误率 | < 0.1% |
| **Saturation** | 资源饱和度 | CPU < 70%, Memory < 80% |

---

## 4. 自我验证 (Self-Verification)

### 架构合规审计脚本

```bash
#!/bin/bash
# architect-audit.sh - 架构合规检查

echo "🏗️ 架构合规审计"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

ERRORS=0

# 1. 检测上帝类（>500行）
echo -e "\n📏 检测上帝类..."
GOD_CLASSES=$(find src/ -name "*.ts" -exec wc -l {} \; 2>/dev/null | awk '$1 > 500 {print $2 ": " $1 " 行"}')
if [ -n "$GOD_CLASSES" ]; then
    echo "❌ 发现上帝类:"
    echo "$GOD_CLASSES"
    ((ERRORS++))
else
    echo "✅ 无上帝类"
fi

# 2. 检测紧耦合依赖
echo -e "\n🔗 检测紧耦合..."
TIGHT_COUPLING=$(grep -rn "new [A-Z][a-zA-Z]*Repository\|new [A-Z][a-zA-Z]*Service" src/ --include="*.ts" 2>/dev/null | head -5)
if [ -n "$TIGHT_COUPLING" ]; then
    echo "❌ 发现紧耦合:"
    echo "$TIGHT_COUPLING"
    ((ERRORS++))
else
    echo "✅ 无紧耦合"
fi

# 3. 检测层级穿透
echo -e "\n📊 检测层级穿透..."
LAYER_VIOLATION=$(grep -rn "import.*Repository\|import.*DataSource" src/components/ --include="*.ts" 2>/dev/null | head -5)
if [ -n "$LAYER_VIOLATION" ]; then
    echo "❌ UI层直接访问数据层:"
    echo "$LAYER_VIOLATION"
    ((ERRORS++))
else
    echo "✅ 层级隔离正常"
fi

# 4. 检测循环依赖（需要 madge）
echo -e "\n🔄 检测循环依赖..."
if command -v madge &> /dev/null; then
    CIRCULAR=$(madge --circular src/ 2>/dev/null | grep -v "No circular")
    if [ -n "$CIRCULAR" ]; then
        echo "❌ 发现循环依赖:"
        echo "$CIRCULAR"
        ((ERRORS++))
    else
        echo "✅ 无循环依赖"
    fi
else
    echo "⚠️ madge 未安装，跳过循环依赖检测"
fi

echo -e "\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ]; then
    echo "✅ 架构审计通过"
    exit 0
else
    echo "❌ 发现 $ERRORS 个架构问题"
    exit 1
fi
```

### 架构评审检查清单

**功能性**：
- [ ] 满足所有功能需求
- [ ] 边界场景已考虑
- [ ] 错误处理完备

**非功能性**：
- [ ] 性能满足 SLA
- [ ] 可扩展至预期规模
- [ ] 高可用设计（无单点故障）
- [ ] 安全威胁已识别并缓解
- [ ] 可观测性（日志/指标/追踪）

**可维护性**：
- [ ] 符合 SOLID 原则
- [ ] 模块边界清晰
- [ ] 技术债务可控
- [ ] 文档完整（ADR、API 文档）

---

**✅ Architect Skill v2.0.0** | **标准 4 Section 已集成**
