# Context 压缩策略

> 当 Agent 会话生成数百万 token 的对话历史时，压缩成为必须。正确的优化目标是 tokens-per-task（每任务 token），而非 tokens-per-request。

---

## 触发条件

Use when:
- Agent 会话超出上下文窗口限制
- 代码库超出上下文窗口（5M+ token 系统）
- 设计对话摘要策略
- 调试 Agent "忘记"它修改了哪些文件的情况
- 构建压缩质量评估框架

触发词：compress context, summarize conversation, implement compaction, reduce token usage, 上下文压缩

---

## 核心洞察

### Tokens-per-Task vs Tokens-per-Request

```yaml
错误优化: 最小化每次请求的 token 数
正确优化: 最小化完成任务的总 token 数（包括重新获取成本）
```

当压缩丢失关键细节（如文件路径、错误消息）时：
- Agent 必须重新获取信息
- 重新探索方法
- 浪费 token 恢复上下文

**结论**：节省 0.5% token 但导致 20% 更多重新获取 = 总成本更高

---

## 三种生产就绪方法

### 1. 锚定迭代摘要（Anchored Iterative Summarization）

**最佳质量** | 压缩比 98.6% | 质量分 3.70/5.0

```markdown
## Session Intent（会话意图）
[用户试图完成什么]

## Files Modified（修改的文件）
- auth.controller.ts: 修复 JWT token 生成
- config/redis.ts: 更新连接池配置
- tests/auth.test.ts: 添加新配置的 mock 设置

## Decisions Made（做出的决策）
- 使用 Redis 连接池而非每请求连接
- 瞬态故障的指数退避重试逻辑

## Current State（当前状态）
- 14 测试通过，2 失败
- 剩余：session service 测试的 mock 设置

## Next Steps（下一步）
1. 修复剩余测试失败
2. 运行完整测试套件
3. 更新文档
```

**原理**：结构强制保留——专用章节充当检查清单，防止静默信息漂移

**使用时机**：
- 长时间运行会话（100+ 消息）
- 文件跟踪重要（编码、调试）
- 需要验证保留了什么

### 2. 不透明压缩（Opaque Compression）

**最高压缩** | 压缩比 99.3% | 质量分 3.35/5.0

- 产生为重建保真度优化的压缩表示
- 牺牲可解释性
- 无法验证保留了什么

**使用时机**：
- 需要最大 token 节省
- 会话相对较短
- 重新获取成本低

### 3. 再生完整摘要（Regenerative Full Summary）

**中等质量** | 压缩比 98.7% | 质量分 3.44/5.0

- 每次压缩时生成详细结构化摘要
- 产生可读输出
- 可能因完全重新生成而非增量合并丢失细节

**使用时机**：
- 摘要可解释性关键
- 会话有清晰的阶段边界
- 每次压缩可接受完整上下文审查

---

## Artifact Trail 问题

**普遍弱项**：工件追踪完整性在所有方法中得分最低（2.2-2.5/5.0）

编码 Agent 需要知道：
- 创建了哪些文件
- 修改了哪些文件及更改内容
- 读取但未更改哪些文件
- 函数名、变量名、错误消息

**解决方案**：可能需要超越通用摘要的专门处理：
- 单独的工件索引
- Agent 脚手架中的显式文件状态跟踪

---

## 压缩触发策略

| 策略 | 触发点 | 权衡 |
|------|--------|------|
| 固定阈值 | 70-80% 上下文利用率 | 简单但可能过早压缩 |
| 滑动窗口 | 保留最后 N 轮 + 摘要 | 可预测上下文大小 |
| 重要性优先 | 先压缩低相关性部分 | 复杂但保留信号 |
| 任务边界 | 在逻辑任务完成时压缩 | 干净摘要但时机不可预测 |

**推荐**：带结构化摘要的滑动窗口，为大多数编码 Agent 用例提供最佳平衡

---

## 基于探针的评估

传统指标（ROUGE、embedding 相似度）无法捕捉功能性压缩质量。

**探针类型**：

| 类型 | 测试内容 | 示例问题 |
|------|----------|----------|
| Recall | 事实保留 | "原始错误消息是什么？" |
| Artifact | 文件跟踪 | "我们修改了哪些文件？" |
| Continuation | 任务规划 | "我们下一步应该做什么？" |
| Decision | 推理链 | "我们对 Redis 问题决定了什么？" |

**六个评估维度**：

1. **Accuracy**：技术细节正确吗？
2. **Context Awareness**：响应反映当前对话状态吗？
3. **Artifact Trail**：Agent 知道读取/修改了哪些文件吗？
4. **Completeness**：响应解决了问题的所有部分吗？
5. **Continuity**：工作可以继续而不重新获取信息吗？
6. **Instruction Following**：响应遵守了声明的约束吗？

---

## 三阶段压缩工作流（大型代码库）

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Research（研究）                               │
│  ├── 输入：架构图、文档、关键接口                         │
│  ├── 压缩：结构化分析组件和依赖                           │
│  └── 输出：单个研究文档                                   │
├─────────────────────────────────────────────────────────┤
│  Phase 2: Planning（规划）                               │
│  ├── 输入：研究文档                                       │
│  ├── 转换：函数签名、类型定义、数据流                      │
│  └── 输出：~2000 词规格（5M token 代码库）                │
├─────────────────────────────────────────────────────────┤
│  Phase 3: Implementation（实现）                         │
│  ├── 输入：规格文档                                       │
│  └── 上下文：聚焦于规格而非原始代码库探索                   │
└─────────────────────────────────────────────────────────┘
```

---

## 实施锚定迭代摘要

```python
# 伪代码
def anchored_summarize(context, existing_summary):
    # 1. 定义显式摘要章节
    sections = ["Session Intent", "Files Modified", 
                "Decisions Made", "Current State", "Next Steps"]
    
    # 2. 首次压缩：将截断历史摘要到章节
    if not existing_summary:
        return summarize_to_sections(context, sections)
    
    # 3. 后续压缩：仅摘要新截断内容
    new_content = get_truncated_content(context)
    new_summary = summarize_to_sections(new_content, sections)
    
    # 4. 合并到现有章节而非重新生成
    return merge_summaries(existing_summary, new_summary)
```

---

## 指导原则

1. 优化 tokens-per-task，而非 tokens-per-request
2. 使用带文件跟踪显式章节的结构化摘要
3. 在 70-80% 上下文利用率时触发压缩
4. 实施增量合并而非完全重新生成
5. 用基于探针的评估测试压缩质量
6. 如果文件跟踪关键，单独跟踪工件追踪
7. 接受略低压缩比以获得更好质量保留
8. 监控重新获取频率作为压缩质量信号

---

## 关联技能

| 技能 | 关系 |
|------|------|
| `context-degradation` | 压缩是退化的缓解策略 |
| `context-optimization` | 压缩是优化技术之一 |
| `llm-evaluation` | 探针评估适用于压缩测试 |
| `mem-orchestrator` | 压缩与 scratchpad 和摘要记忆模式相关 |

---

**Version**: 1.0.0 | **Created**: 2026-01-12 | **Author**: domiyoung
