## RAGFlow 核心知识库

### 1. 架构概述
- **定位**: 基于深度文档理解的开源 RAG 引擎
- **核心优势**:
  - DeepDoc 深度文档解析（PDF/Word/Excel/PPT/图片）
  - 可视化 Chunk 编辑与质量控制
  - 多种 Embedding 模型支持
  - GraphRAG 知识图谱增强
  - Agent 工作流编排

### 2. 部署架构

```
┌─────────────────────────────────────────────────┐
│                   RAGFlow                        │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │ Web UI  │  │   API   │  │ Agent Workflow  │ │
│  └────┬────┘  └────┬────┘  └────────┬────────┘ │
│       │            │                │          │
│  ┌────▼────────────▼────────────────▼────┐    │
│  │           RAGFlow Core                 │    │
│  │  ┌──────────┐  ┌──────────────────┐   │    │
│  │  │ DeepDoc  │  │ Retrieval Engine │   │    │
│  │  │ Parser   │  │ (Hybrid Search)  │   │    │
│  │  └──────────┘  └──────────────────┘   │    │
│  └───────────────────────────────────────┘    │
├─────────────────────────────────────────────────┤
│  ┌─────────┐  ┌─────────┐  ┌─────────────────┐ │
│  │ MinIO   │  │ Redis   │  │ Elasticsearch   │ │
│  │(文件存储)│  │ (缓存)  │  │ (向量+全文检索) │ │
│  └─────────┘  └─────────┘  └─────────────────┘ │
│  ┌─────────────────────────────────────────────┐│
│  │              MySQL (元数据)                  ││
│  └─────────────────────────────────────────────┘│
└─────────────────────────────────────────────────┘
```

### 3. 知识库配置最佳实践

| 文档类型 | 推荐 Chunk 方法 | Chunk 大小 | 说明 |
|---------|----------------|-----------|------|
| 技术文档 | Naive (递归) | 512-1024 | 保持段落完整性 |
| 法律合同 | Book (章节) | 1024-2048 | 按章节结构分块 |
| 论文/报告 | Paper | 自动 | 识别标题/摘要/正文 |
| 表格数据 | Table | 行级 | 保持表格结构 |
| QA 对 | QA | 问答对 | 一问一答为单位 |

### 4. Embedding 模型选择

| 模型 | 维度 | 适用场景 | 性能 |
|------|------|---------|------|
| BAAI/bge-large-zh-v1.5 | 1024 | 中文通用 | ⭐⭐⭐⭐ |
| BAAI/bge-m3 | 1024 | 多语言 | ⭐⭐⭐⭐⭐ |
| text-embedding-3-large | 3072 | 英文高精度 | ⭐⭐⭐⭐⭐ |
| nomic-embed-text | 768 | 本地部署 | ⭐⭐⭐ |

### 5. 检索策略优化

```yaml
retrieval_config:
  # 混合检索权重
  similarity_weight: 0.7      # 向量相似度
  keyword_weight: 0.3         # 关键词匹配

  # 检索参数
  top_k: 10                   # 召回数量
  similarity_threshold: 0.2   # 相似度阈值
  rerank: true                # 启用重排序
  rerank_model: "bge-reranker-v2-m3"
```

### 6. GraphRAG 配置

- **实体提取**: 使用 LLM 抽取实体和关系
- **知识图谱**: 构建实体-关系-实体三元组
- **混合检索**: 向量检索 + 图遍历结合
- **适用场景**: 复杂问答、多跳推理、因果分析

### 7. 常见问题与解决方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 检索结果不相关 | Chunk 过大/过小 | 调整 Chunk 大小，启用重排序 |
| 中文分词不准 | 分词器问题 | 使用 jieba 自定义词典 |
| 响应速度慢 | 模型过大 | 使用量化模型或更小的 Embedding |
| 表格识别差 | 解析器限制 | 使用 Table Chunk 方法 |
| 图片内容丢失 | OCR 未启用 | 启用 OCR 并选择合适模型 |

### 8. API 集成示例

```python
from ragflow_sdk import RAGFlow

# 初始化客户端
rag = RAGFlow(api_key="your-api-key", base_url="http://localhost")

# 创建知识库
dataset = rag.create_dataset(name="tech-docs")

# 上传文档
dataset.upload_documents(["doc1.pdf", "doc2.docx"])

# 等待解析完成
dataset.async_parse_documents()

# 创建 Chat Assistant
assistant = rag.create_chat(
    name="Tech Assistant",
    dataset_ids=[dataset.id],
    llm={"model_name": "gpt-4", "temperature": 0.1}
)

# 对话
response = assistant.chat("如何部署 RAGFlow?")
print(response.content)
```

### 9. 生产部署清单

- [ ] Docker Compose 配置优化（资源限制）
- [ ] Elasticsearch 集群配置（分片/副本）
- [ ] MinIO 持久化存储配置
- [ ] Redis 哨兵/集群模式
- [ ] Nginx 反向代理 + SSL
- [ ] 监控告警（Prometheus + Grafana）
- [ ] 日志收集（ELK/Loki）
- [ ] 备份策略（数据库 + 向量索引）
```
