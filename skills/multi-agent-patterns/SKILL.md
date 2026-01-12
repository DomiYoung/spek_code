# 多 Agent 架构模式

> 多 Agent 架构跨多个语言模型实例分配工作，每个实例有自己的上下文窗口。关键洞察：sub-agent 存在主要是为了隔离上下文，而非拟人化角色分工。

---

## 触发条件

Use when:
- 单 Agent 上下文限制约束任务复杂度
- 任务自然分解为并行子任务
- 不同子任务需要不同工具集或 system prompt
- 构建必须同时处理多个领域的系统
- 扩展 Agent 能力超越单上下文限制

触发词：design multi-agent system, implement supervisor pattern, create swarm architecture, coordinate multiple agents, 多 Agent 架构

---

## 为什么需要多 Agent

### 上下文瓶颈

单 Agent 面临固有上限：
- 上下文窗口被累积历史、检索文档、工具输出填满
- 性能按可预测模式退化：lost-in-middle、注意力稀缺、上下文污染

多 Agent 通过跨多个上下文窗口分区工作来解决这些限制。

### Token 经济学

| 架构 | Token 倍数 | 用例 |
|------|-----------|------|
| 单 Agent 聊天 | 1× 基准 | 简单查询 |
| 单 Agent + 工具 | ~4× 基准 | 工具使用任务 |
| 多 Agent 系统 | ~15× 基准 | 复杂研究/协调 |

**关键发现**：升级到更好模型通常比加倍 token 预算提供更大性能增益。

### 并行化优势

```
单 Agent（顺序）:
任务A → 任务B → 任务C → 任务D
总时间 = A + B + C + D

多 Agent（并行）:
任务A ─┐
任务B ─┼─→ 聚合
任务C ─┤
任务D ─┘
总时间 ≈ max(A, B, C, D)
```

---

## 三种架构模式

### 1. Supervisor/Orchestrator（监督者/编排者）

```
用户查询 → Supervisor → [Specialist, Specialist, Specialist] → 聚合 → 最终输出
```

**何时使用**：
- 有清晰分解的复杂任务
- 需要跨领域协调的任务
- 人工监督重要的场景

**优势**：
- 严格控制工作流
- 更容易实现 human-in-the-loop
- 确保遵守预定义计划

**劣势**：
- Supervisor 上下文成为瓶颈
- Supervisor 故障级联到所有 worker
- "电话游戏"问题：Supervisor 错误释义 sub-agent 响应

### "电话游戏"问题及解决方案

```python
def forward_message(message: str, to_user: bool = True):
    """
    直接转发 sub-agent 响应给用户，无需 supervisor 合成。
    
    Use when:
    - Sub-agent 响应是最终且完整的
    - Supervisor 合成会丢失重要细节
    - 响应格式必须精确保留
    """
    if to_user:
        return {"type": "direct_response", "content": message}
    return {"type": "supervisor_input", "content": message}
```

### 2. Peer-to-Peer/Swarm（点对点/群体）

```python
def transfer_to_agent_b():
    return agent_b  # 通过函数返回切换

agent_a = Agent(
    name="Agent A",
    functions=[transfer_to_agent_b]
)
```

**何时使用**：
- 需要灵活探索的任务
- 刚性规划适得其反的任务
- 有涌现需求难以预先分解的任务

**优势**：
- 无单点故障
- 有效扩展广度优先探索
- 启用涌现式问题解决行为

**劣势**：
- 协调复杂度随 Agent 数量增加
- 无中央状态管理者时存在发散风险
- 需要健壮的收敛约束

### 3. Hierarchical（层级式）

```
Strategy Layer（策略层）: 定义目标和约束
        ↓
Planning Layer（规划层）: 将目标分解为可操作计划
        ↓
Execution Layer（执行层）: 执行原子任务
```

**何时使用**：
- 有清晰层级结构的大型项目
- 有管理层的企业工作流
- 需要高层规划和细节执行的任务

**优势**：
- 镜像组织结构
- 清晰的关注点分离
- 不同层级启用不同上下文结构

**劣势**：
- 层间协调开销
- 策略和执行可能不对齐
- 复杂的错误传播

---

## 上下文隔离作为设计原则

**核心目的**：每个 sub-agent 在专注于其子任务的干净上下文窗口中运行，不携带其他子任务的累积上下文。

### 隔离机制

| 机制 | 说明 | 使用时机 |
|------|------|----------|
| 完整上下文委托 | Planner 共享整个上下文 | 复杂任务，sub-agent 需要完整理解 |
| 指令传递 | Planner 通过函数调用创建指令 | 简单、定义明确的子任务 |
| 文件系统记忆 | Agent 读写持久存储 | 需要共享状态的复杂任务 |

### 权衡

- **完整上下文委托**：最大能力但违背 sub-agent 目的
- **指令传递**：保持隔离但限制 sub-agent 灵活性
- **文件系统记忆**：启用共享状态但引入延迟和一致性挑战

---

## 共识与协调

### 投票问题

简单多数投票将弱模型的幻觉与强模型的推理等同对待。没有干预，多 Agent 讨论会因固有的同意偏见而陷入对错误前提的共识。

### 解决方案

| 方法 | 说明 |
|------|------|
| **加权投票** | 按置信度或专业知识加权 Agent 投票 |
| **辩论协议** | 要求 Agent 在多轮中相互批评输出 |
| **触发式干预** | 监控停滞触发器、谄媚触发器 |

---

## 故障模式与缓解

### 故障 1：Supervisor 瓶颈

Supervisor 累积所有 worker 的上下文，容易饱和和退化。

**缓解**：
- 实施输出 schema 约束，worker 只返回精炼摘要
- 使用检查点持久化 supervisor 状态而不携带完整历史

### 故障 2：协调开销

Agent 通信消耗 token 并引入延迟。复杂协调可能抵消并行化收益。

**缓解**：
- 通过清晰切换协议最小化通信
- 尽可能批量处理结果
- 使用异步通信模式

### 故障 3：发散

没有中央协调的 Agent 追求不同目标可能偏离预期目标。

**缓解**：
- 为每个 Agent 定义清晰的目标边界
- 实施收敛检查验证朝向共享目标的进展
- 对 Agent 执行使用 TTL（生存时间）限制

### 故障 4：错误传播

一个 Agent 输出中的错误传播到消费该输出的下游 Agent。

**缓解**：
- 传递给消费者前验证 Agent 输出
- 实施带断路器的重试逻辑
- 尽可能使用幂等操作

---

## 实践示例

### 示例 1：研究团队架构

```
Supervisor
├── Researcher（网络搜索、文档检索）
├── Analyzer（数据分析、统计）
├── Fact-checker（验证、校验）
└── Writer（报告生成、格式化）
```

### 示例 2：切换协议

```python
def handle_customer_request(request):
    if request.type == "billing":
        return transfer_to(billing_agent)
    elif request.type == "technical":
        return transfer_to(technical_agent)
    elif request.type == "sales":
        return transfer_to(sales_agent)
    else:
        return handle_general(request)
```

### 示例 3：带直接响应的 Supervisor

```python
class SupervisorAgent:
    def process(self, task):
        # 分解任务
        subtasks = self.decompose(task)
        
        # 分发到 worker
        results = []
        for subtask in subtasks:
            worker = self.select_worker(subtask)
            result = worker.execute(subtask)
            
            # 决定是否直接转发
            if result.is_final and result.high_fidelity:
                return self.forward_direct(result)
            else:
                results.append(result)
        
        # 合成非直接转发的结果
        return self.synthesize(results)
```

---

## 指导原则

1. 将上下文隔离作为多 Agent 系统的主要收益来设计
2. 基于协调需求选择架构模式，而非组织隐喻
3. 实施带状态传递的显式切换协议
4. 使用加权投票或辩论协议达成共识
5. 监控 supervisor 瓶颈并实施检查点
6. 在 Agent 间传递前验证输出
7. 设置 TTL 限制防止无限循环
8. 显式测试故障场景

---

## 关联技能

| 技能 | 关系 |
|------|------|
| `context-fundamentals` | 上下文基础 |
| `context-optimization` | 分区策略 |
| `mem-orchestrator` | 跨 Agent 共享状态管理 |
| `llm-evaluation` | 评估多 Agent 输出质量 |

---

## 框架参考

| 框架 | 模式 | 特点 |
|------|------|------|
| LangGraph | 基于图的状态机 | 显式节点和边 |
| AutoGen | 对话/事件驱动 | GroupChat |
| CrewAI | 基于角色的流程 | 层级 crew 结构 |

---

**Version**: 1.0.0 | **Created**: 2026-01-12 | **Author**: domiyoung
