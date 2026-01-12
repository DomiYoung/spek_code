# Context 优化技术

> 上下文优化通过战略性压缩、遮蔽、缓存和分区扩展有限上下文窗口的有效容量。有效优化可将有效上下文容量提升 2-3 倍。

---

## 触发条件

Use when:
- 上下文限制约束任务复杂度
- 优化成本（更少 token = 更低成本）
- 减少长对话延迟
- 实现长时间运行的 Agent 系统
- 需要处理更大的文档或对话

触发词：optimize context, reduce token costs, implement KV-cache, partition context, 上下文优化

---

## 四大优化策略

### 1. Compaction（压缩）

在接近限制时摘要上下文内容，然后用摘要重新初始化新上下文窗口。

**压缩优先级**：

| 优先级 | 内容类型 | 策略 |
|--------|----------|------|
| 1（最高）| 工具输出 | 替换为摘要 |
| 2 | 旧轮次 | 摘要早期对话 |
| 3 | 检索文档 | 如有最新版本则摘要 |
| ❌ 禁止 | System Prompt | 永不压缩 |

**摘要生成指南**：

| 消息类型 | 保留 | 移除 |
|----------|------|------|
| 工具输出 | 关键发现、指标、结论 | 冗长原始输出 |
| 对话轮次 | 关键决策、承诺、上下文转换 | 填充和来回 |
| 检索文档 | 关键事实和声明 | 支持证据和阐述 |

### 2. Observation Masking（观察遮蔽）

工具输出可占 Agent 轨迹 token 使用的 80%+。一旦 Agent 使用工具输出做出决策，保留完整输出价值递减但持续消耗上下文。

**遮蔽决策矩阵**：

| 类别 | 是否遮蔽 | 原因 |
|------|----------|------|
| 当前任务关键的观察 | ❌ 永不 | 仍在使用 |
| 最近一轮的观察 | ❌ 永不 | 可能需要 |
| 活跃推理中使用的观察 | ❌ 永不 | 正在引用 |
| 3+ 轮前的观察 | ⚠️ 考虑 | 可能已完成使用 |
| 可提取关键点的冗长输出 | ⚠️ 考虑 | 可压缩 |
| 目的已达成的观察 | ⚠️ 考虑 | 不再需要 |
| 重复输出 | ✅ 始终 | 冗余 |
| 样板头/尾 | ✅ 始终 | 无信息 |
| 已在对话中摘要的输出 | ✅ 始终 | 已捕获 |

**实现示例**：

```python
def mask_observation(observation, max_length=1000):
    if len(observation) > max_length:
        ref_id = store_observation(observation)  # 存储到外部
        key_info = extract_key_points(observation)
        return f"[Obs:{ref_id} elided. Key: {key_info}]"
    return observation
```

### 3. KV-Cache 优化

KV-cache 存储推理期间计算的 Key 和 Value 张量，随序列长度线性增长。缓存跨共享相同前缀的请求重用，避免重新计算。

**缓存友好的上下文排序**：

```python
# 稳定内容优先（可缓存）
context = [system_prompt, tool_definitions]
# 经常重用的元素
context += [reused_templates]
# 唯一内容最后
context += [unique_content]
```

**优化缓存的设计原则**：

| 做 ✅ | 不做 ❌ |
|-------|---------|
| 将稳定元素放在最前 | 动态内容（时间戳）放在开头 |
| 使用一致格式 | 频繁更改格式 |
| 跨会话保持结构稳定 | 每次重组结构 |

### 4. Context Partitioning（上下文分区）

最激进的优化形式：跨具有隔离上下文的 sub-agent 分区工作。

```
┌─────────────────────────────────────────────────────────┐
│                    Coordinator                          │
│  ├── 维护全局状态和目标                                   │
│  ├── 分解任务为子任务                                     │
│  └── 聚合结果（保持轻量上下文）                            │
├─────────────────────────────────────────────────────────┤
│  Sub-Agent A          Sub-Agent B          Sub-Agent C  │
│  ├── 隔离上下文        ├── 隔离上下文        ├── 隔离上下文 │
│  ├── 专注子任务        ├── 专注子任务        ├── 专注子任务 │
│  └── 返回摘要结果      └── 返回摘要结果      └── 返回摘要结果 │
└─────────────────────────────────────────────────────────┘
```

**优势**：详细搜索上下文保持隔离在 sub-agent 内，协调器专注于综合和分析

---

## 预算管理

### 上下文预算分配

```yaml
总预算: 100%
├── System Prompt: 10-15%
├── Tool Definitions: 5-10%
├── Retrieved Docs: 20-30%
├── Message History: 30-40%
└── Reserved Buffer: 10-15%
```

### 触发式优化

```python
def check_optimization_triggers(context):
    utilization = context.tokens / context.limit
    
    if utilization > 0.8:
        return "CRITICAL: 强制压缩"
    elif utilization > 0.7:
        return "WARNING: 触发优化"
    elif is_quality_degrading():
        return "PERFORMANCE: 应用选择性优化"
    else:
        return "OK: 继续正常运行"
```

---

## 优化决策框架

```
上下文利用率 > 70%？
├── 是 → 哪种内容主导？
│   ├── 工具输出主导 → 观察遮蔽
│   ├── 检索文档主导 → 摘要或分区
│   ├── 消息历史主导 → 带摘要的压缩
│   └── 多种组件 → 组合策略
└── 否 → 监控并继续
```

---

## 性能目标

| 策略 | 目标 Token 减少 | 目标质量保留 |
|------|-----------------|--------------|
| Compaction | 50-70% | > 95% |
| Observation Masking | 60-80%（被遮蔽观察） | > 90% |
| KV-Cache | 70%+ 命中率 | 100%（无损） |
| Partitioning | 取决于任务 | 取决于聚合质量 |

---

## 实践示例

### 示例 1：压缩触发

```python
def maybe_compact(context, limit, threshold=0.8):
    if context.tokens / limit > threshold:
        summary = generate_structured_summary(context)
        return reinitialize_context(summary)
    return context
```

### 示例 2：分层优化

```python
def optimize_context(context):
    # 层 1：遮蔽旧观察
    context = mask_old_observations(context, turns_ago=3)
    
    # 层 2：如果仍然太大，压缩历史
    if context.tokens > context.limit * 0.7:
        context = compact_history(context)
    
    # 层 3：如果仍然太大，分区到 sub-agent
    if context.tokens > context.limit * 0.8:
        context = partition_to_subagents(context)
    
    return context
```

---

## 指导原则

1. 优化前先测量——了解当前状态
2. 可能时先应用压缩再遮蔽
3. 用一致提示设计缓存稳定性
4. 在上下文变成问题前分区
5. 随时间监控优化有效性
6. 平衡 token 节省与质量保留
7. 在生产规模测试优化
8. 为边缘情况实现优雅降级

---

## 关联技能

| 技能 | 关系 |
|------|------|
| `context-fundamentals` | 基础概念 |
| `context-degradation` | 理解何时优化 |
| `context-compression` | 压缩策略细节 |
| `multi-agent-patterns` | 分区作为隔离 |
| `mem-orchestrator` | 将上下文卸载到记忆 |

---

**Version**: 1.0.0 | **Created**: 2026-01-12 | **Author**: domiyoung
