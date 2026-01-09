## Dify 核心知识库

### 1. 平台概述
- **定位**: 开源 LLM 应用开发平台，支持可视化编排
- **核心能力**:
  - Workflow 工作流编排（DAG 有向无环图）
  - Chatflow 对话流编排
  - Agent 智能体（ReAct / Function Call）
  - RAG 知识库管理
  - 多模型接入（OpenAI/Claude/本地模型）

### 2. 应用类型

| 类型 | 适用场景 | 特点 |
|------|---------|------|
| **Chatbot** | 对话助手 | 简单配置，快速上线 |
| **Completion** | 文本生成 | 单次输入输出 |
| **Workflow** | 复杂流程 | 可视化编排，多节点协作 |
| **Agent** | 智能代理 | 自主决策，工具调用 |

### 3. Workflow 核心节点

| 节点类型 | 用途 | 关键配置 |
|---------|------|---------|
| **Start** | 入口 | 定义输入变量 |
| **LLM** | 大模型调用 | 模型、Prompt、变量 |
| **Knowledge Retrieval** | 知识库检索 | 数据集、Top-K、阈值 |
| **Code** | 代码执行 | Python/JavaScript |
| **HTTP Request** | API 调用 | URL、Headers、Body |
| **IF/ELSE** | 条件分支 | 条件表达式 |
| **Iteration** | 循环处理 | 数组遍历 |
| **Variable Aggregator** | 变量聚合 | 多分支合并 |
| **Template Transform** | 模板转换 | Jinja2 语法 |
| **End** | 输出 | 返回结果 |

### 4. 变量与模板语法

```jinja2
{# 基础变量引用 #}
{{ 变量名 }}

{# 系统变量 #}
{{ sys.query }}           {# 用户输入 #}
{{ sys.conversation_id }} {# 会话ID #}
{{ sys.user_id }}         {# 用户ID #}

{# 节点输出引用 #}
{{ node_name.output }}
{{ llm_node.text }}
{{ code_node.result }}

{# Jinja2 过滤器 #}
{{ text | upper }}
{{ text | replace("a", "b") }}
{{ list | join(", ") }}
{{ json_str | tojson }}

{# 条件判断 #}
{% if condition %}
  内容A
{% else %}
  内容B
{% endif %}

{# 循环 #}
{% for item in items %}
  {{ item }}
{% endfor %}
```

### 5. Code 节点模板

**Python 格式**:
```python
def main(inputs: dict) -> dict:
    # inputs 包含上游变量
    question = inputs.get("question", "")

    # 处理逻辑
    result = question.upper()

    # 返回字典
    return {"output": result}
```

**JavaScript 格式**:
```javascript
function main(inputs) {
    const question = inputs.question || "";
    const result = question.toUpperCase();
    return { output: result };
}
```

### 6. HTTP Request 节点配置

```yaml
Method: POST
URL: https://api.example.com/endpoint
Headers:
  Content-Type: application/json
  Authorization: Bearer {{api_key}}
Body (JSON):
  {
    "query": "{{user_input}}",
    "options": {
      "temperature": 0.7
    }
  }
```

### 7. 知识库配置最佳实践

| 配置项 | 推荐值 | 说明 |
|-------|-------|------|
| Embedding 模型 | text-embedding-3-small | 性价比高 |
| Chunk 大小 | 500-1000 | 按文档类型调整 |
| Top-K | 3-5 | 召回数量 |
| Score 阈值 | 0.5-0.7 | 过滤低质量结果 |
| Rerank | 开启 | 提升相关性 |

### 8. Agent 工具开发

**自定义工具 Schema**:
```yaml
name: search_database
description: 搜索内部数据库
parameters:
  type: object
  properties:
    query:
      type: string
      description: 搜索关键词
    limit:
      type: integer
      description: 返回数量
      default: 10
  required:
    - query
```

### 9. 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 变量未定义 | 节点未连接或命名错误 | 检查节点连线和变量名 |
| HTTP 超时 | 外部 API 响应慢 | 增加超时时间或异步处理 |
| 中文引号报错 | JSON 解析失败 | 使用 Jinja2 replace 过滤 |
| 知识库召回差 | Chunk 或阈值不当 | 调整分块策略和阈值 |
| Token 超限 | 上下文过长 | 截断或压缩历史消息 |

### 10. 部署架构

```
┌─────────────────────────────────────────────────┐
│                    Dify                          │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │ Web UI  │  │   API   │  │ Workflow Engine │ │
│  └────┬────┘  └────┬────┘  └────────┬────────┘ │
│       │            │                │          │
│  ┌────▼────────────▼────────────────▼────┐    │
│  │              Dify Core                 │    │
│  │  ┌──────────┐  ┌──────────────────┐   │    │
│  │  │  Agent   │  │  RAG Pipeline    │   │    │
│  │  │  Engine  │  │  (Retrieval)     │   │    │
│  │  └──────────┘  └──────────────────┘   │    │
│  └───────────────────────────────────────┘    │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │ Redis   │  │ Weaviate│  │   PostgreSQL    │ │
│  │ (缓存)  │  │ (向量库) │  │   (元数据)      │ │
│  └─────────┘  └─────────┘  └─────────────────┘ │
└─────────────────────────────────────────────────┘
```

### 11. API 集成示例

```python
import requests

# 调用已发布的 Dify 应用
response = requests.post(
    "https://api.dify.ai/v1/chat-messages",
    headers={
        "Authorization": "Bearer app-xxx",
        "Content-Type": "application/json"
    },
    json={
        "inputs": {},
        "query": "你好",
        "user": "user-123",
        "response_mode": "streaming"  # 或 "blocking"
    }
)
```

### 12. 生产部署清单

- [ ] Docker Compose 配置优化
- [ ] PostgreSQL 持久化存储
- [ ] Redis 集群配置
- [ ] Weaviate/Qdrant 向量数据库
- [ ] Nginx 反向代理 + SSL
- [ ] 环境变量安全管理
- [ ] 日志收集与监控
- [ ] API 限流配置
```
