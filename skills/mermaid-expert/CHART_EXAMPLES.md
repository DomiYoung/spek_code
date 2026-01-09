# Mermaid 图表详细示例

> 📖 **本文件**: 包含 7 种图表类型的详细语法和项目实战示例
> **主文件**: [SKILL.md](./SKILL.md)

---

## 1. 流程图 (Flowchart)

**基础语法**
```mermaid
graph TD
    A[开始] --> B{判断条件}
    B -->|是| C[执行操作]
    B -->|否| D[跳过]
    C --> E[结束]
    D --> E
```

**方向选项**
- `graph TB` - 从上到下 (Top to Bottom)
- `graph TD` - 从上到下 (Top Down，同 TB)
- `graph LR` - 从左到右 (Left to Right)
- `graph RL` - 从右到左 (Right to Left)

**节点形状**
```mermaid
graph LR
    A[方形节点]
    B(圆角节点)
    C([体育场形])
    D[[子程序]]
    E[(数据库)]
    F((圆形))
    G>标签形]
    H{菱形}
    I{{六边形}}
    J[/平行四边形/]
    K[\平行四边形反向\]
    L[/梯形\]
    M[\梯形反向/]
```

**连接线样式**
```mermaid
graph LR
    A --> B      %% 实线箭头
    C --- D      %% 实线
    E -.-> F     %% 虚线箭头
    G -.- H      %% 虚线
    I ==> J      %% 粗线箭头
    K === L      %% 粗线
    M -->|标签| N  %% 带标签箭头
```

**项目实战：React 组件渲染流程**
```mermaid
graph TD
    A[用户访问页面] --> B{路由匹配}
    B -->|匹配成功| C[加载组件]
    B -->|404| D[显示错误页]
    C --> E{数据已缓存?}
    E -->|是| F[从 React Query 读取]
    E -->|否| G[API 请求]
    G --> H[更新缓存]
    H --> F
    F --> I[渲染组件]
    I --> J{用户交互}
    J -->|状态变更| K[Zustand 更新]
    K --> I
    J -->|路由跳转| B
```

---

## 2. 序列图 (Sequence Diagram)

**基础语法**
```mermaid
sequenceDiagram
    participant A as 用户
    participant B as 前端
    participant C as 后端
    participant D as 数据库

    A->>B: 点击按钮
    B->>C: API 请求
    activate C
    C->>D: 查询数据
    activate D
    D-->>C: 返回结果
    deactivate D
    C-->>B: JSON 响应
    deactivate C
    B->>A: 更新 UI
```

**高级特性**
```mermaid
sequenceDiagram
    autonumber  %% 自动编号
    actor U as 用户
    participant F as 前端
    participant B as 后端

    U->>+F: 登录请求
    Note over F: 验证表单
    F->>+B: POST /auth/login
    alt 成功
        B-->>F: {token, user}
        F->>F: 存储 token
        F-->>-U: 跳转主页
    else 失败
        B-->>F: {error}
        F-->>-U: 显示错误
    end

    par 并行操作
        F->>B: 获取用户信息
    and
        F->>B: 获取通知
    end

    loop 轮询
        F->>B: 检查新消息
        B-->>F: 消息列表
    end
```

**项目实战：SignalR 实时消息流程**
```mermaid
sequenceDiagram
    autonumber
    actor User
    participant UI as React 组件
    participant Store as Zustand Store
    participant Hub as SignalR Hub
    participant Server as 后端服务

    User->>UI: 发送消息
    UI->>Store: dispatch(sendMessage)
    Store->>Hub: invoke('SendMessage')
    activate Hub
    Hub->>Server: 转发消息
    activate Server
    Server->>Server: 处理业务逻辑
    Server->>Hub: 广播消息
    deactivate Server
    Hub-->>Store: on('ReceiveMessage')
    deactivate Hub
    Store->>UI: 更新消息列表
    UI->>User: 显示新消息

    Note over Hub,Server: WebSocket 持久连接
```

---

## 3. 类图 (Class Diagram)

**基础语法**
```mermaid
classDiagram
    class Animal {
        +String name
        +int age
        +makeSound()
    }
    class Dog {
        +String breed
        +bark()
    }
    class Cat {
        +meow()
    }

    Animal <|-- Dog : 继承
    Animal <|-- Cat : 继承
```

**关系类型**
```mermaid
classDiagram
    classA <|-- classB : 继承 (Inheritance)
    classC *-- classD : 组合 (Composition)
    classE o-- classF : 聚合 (Aggregation)
    classG <-- classH : 关联 (Association)
    classI -- classJ : 链接 (Link - 实线)
    classK <.. classL : 依赖 (Dependency)
    classM <|.. classN : 实现 (Realization)
    classO .. classP : 虚线 (Dashed Link)
```

**项目实战：Zustand Store 架构**
```mermaid
classDiagram
    class BaseStore {
        <<interface>>
        +state: State
        +actions: Actions
    }

    class WorkflowStore {
        +nodes: Node[]
        +edges: Edge[]
        +addNode(node)
        +updateNode(id, data)
        +deleteNode(id)
    }

    class DifyStore {
        +conversations: Map
        +currentConversationId: string
        +createConversation()
        +addMessage()
    }

    class AuthStore {
        +user: User | null
        +token: string
        +login(credentials)
        +logout()
    }

    BaseStore <|.. WorkflowStore : implements
    BaseStore <|.. DifyStore : implements
    BaseStore <|.. AuthStore : implements

    WorkflowStore --> Node : uses
    WorkflowStore --> Edge : uses
    DifyStore --> Conversation : contains
```

---

## 4. 状态图 (State Diagram)

**基础语法**
```mermaid
stateDiagram-v2
    [*] --> 待机
    待机 --> 运行 : 启动
    运行 --> 暂停 : 暂停
    暂停 --> 运行 : 继续
    运行 --> 停止 : 停止
    停止 --> [*]
```

**复合状态**
```mermaid
stateDiagram-v2
    [*] --> Active

    state Active {
        [*] --> NumLockOff
        NumLockOff --> NumLockOn : EvNumLockPressed
        NumLockOn --> NumLockOff : EvNumLockPressed
        --
        [*] --> CapsLockOff
        CapsLockOff --> CapsLockOn : EvCapsLockPressed
        CapsLockOn --> CapsLockOff : EvCapsLockPressed
    }
```

**项目实战：Workflow 执行状态**
```mermaid
stateDiagram-v2
    [*] --> Idle : 初始化

    Idle --> Validating : 点击运行
    Validating --> Running : 验证通过
    Validating --> Error : 验证失败

    state Running {
        [*] --> ExecutingNode
        ExecutingNode --> WaitingForAPI : API 调用
        WaitingForAPI --> ExecutingNode : 响应返回
        ExecutingNode --> NextNode : 节点完成
        NextNode --> ExecutingNode : 有下一节点
        NextNode --> [*] : 无下一节点
    }

    Running --> Paused : 用户暂停
    Paused --> Running : 用户继续
    Running --> Completed : 所有节点完成
    Running --> Error : 执行异常

    Error --> Idle : 重置
    Completed --> Idle : 重新运行
```

---

## 5. ER 图 (Entity Relationship Diagram)

**基础语法**
```mermaid
erDiagram
    CUSTOMER ||--o{ ORDER : places
    CUSTOMER {
        string name
        string custNumber
        string sector
    }
    ORDER ||--|{ LINE-ITEM : contains
    ORDER {
        int orderNumber
        string deliveryAddress
    }
    LINE-ITEM {
        string productCode
        int quantity
        float pricePerUnit
    }
```

**关系类型**
- `||--||` : 一对一 (One to One)
- `||--o{` : 一对多 (One to Many)
- `}o--o{` : 多对多 (Many to Many)

**项目实战：数据库模型**
```mermaid
erDiagram
    USER ||--o{ WORKFLOW : creates
    USER {
        uuid id PK
        string email UK
        string name
        timestamp created_at
    }

    WORKFLOW ||--o{ NODE : contains
    WORKFLOW {
        uuid id PK
        uuid user_id FK
        string title
        json metadata
        timestamp updated_at
    }

    NODE ||--o{ EDGE : connects
    NODE {
        uuid id PK
        uuid workflow_id FK
        string type
        json data
        json position
    }

    EDGE {
        uuid id PK
        uuid workflow_id FK
        uuid source_node_id FK
        uuid target_node_id FK
        json style
    }
```

---

## 6. 甘特图 (Gantt Chart)

**基础语法**
```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD
    section 需求分析
    需求调研           :a1, 2024-01-01, 7d
    需求文档           :after a1, 5d
    section 设计
    架构设计           :2024-01-13, 10d
    UI 设计            :2024-01-15, 8d
    section 开发
    前端开发           :2024-01-23, 20d
    后端开发           :2024-01-23, 20d
    section 测试
    集成测试           :2024-02-12, 10d
    上线部署           :2024-02-22, 3d
```

**项目实战：Sprint 计划**
```mermaid
gantt
    title Sprint 3 - Dify 集成
    dateFormat YYYY-MM-DD
    section 准备阶段
    Dify API 调研      :done, prep1, 2024-01-01, 2d
    技术方案设计        :done, prep2, after prep1, 3d
    section 开发阶段
    API Service 封装   :active, dev1, 2024-01-06, 3d
    React Hook 开发    :dev2, after dev1, 2d
    Zustand Store 集成 :dev3, after dev2, 2d
    ReactFlow 节点     :dev4, after dev3, 3d
    section 测试阶段
    单元测试           :test1, after dev4, 2d
    集成测试           :test2, after test1, 2d
    section 部署
    上线准备           :deploy, after test2, 1d
```

---

## 7. 用户旅程图 (User Journey)

**基础语法**
```mermaid
journey
    title 用户购物旅程
    section 浏览
      访问首页: 5: 用户
      搜索商品: 3: 用户
      查看详情: 4: 用户
    section 购买
      加入购物车: 4: 用户
      填写地址: 2: 用户
      支付: 3: 用户, 系统
    section 售后
      查看订单: 5: 用户
      评价商品: 4: 用户
```

**项目实战：Workflow 编辑旅程**
```mermaid
journey
    title Workflow 编辑器使用旅程
    section 初始化
      创建 Workflow: 5: 用户
      选择模板: 4: 用户
    section 编辑阶段
      添加节点: 5: 用户
      连接节点: 4: 用户
      配置参数: 3: 用户
      调试运行: 2: 用户, 系统
    section 优化阶段
      性能分析: 3: 系统
      调整节点: 4: 用户
      重新测试: 4: 用户, 系统
    section 完成
      保存 Workflow: 5: 用户
      部署上线: 4: 用户, 系统
```

---

## 高级技巧

### 1. 主题定制

```mermaid
%%{init: {'theme':'dark', 'themeVariables': { 'primaryColor':'#ff6b6b'}}}%%
graph TD
    A[深色主题] --> B[自定义颜色]
```

**可用主题**
- `default` - 默认主题
- `dark` - 深色主题
- `forest` - 森林主题
- `neutral` - 中性主题

### 2. 子图 (Subgraph)

```mermaid
graph TB
    subgraph 前端层
        A[React 组件]
        B[Zustand Store]
    end
    subgraph 数据层
        C[React Query]
        D[IndexedDB]
    end
    subgraph 后端层
        E[API Gateway]
        F[业务服务]
    end

    A --> B
    B --> C
    C --> E
    E --> F
    C --> D
```

### 3. 样式定制

```mermaid
graph LR
    A[节点 A]:::classA --> B[节点 B]:::classB
    B --> C[节点 C]:::classC

    classDef classA fill:#f9f,stroke:#333,stroke-width:4px
    classDef classB fill:#bbf,stroke:#f66,stroke-width:2px,stroke-dasharray: 5 5
    classDef classC fill:#ff6,stroke:#333,stroke-width:2px
```

---

## 与项目集成

### 1. Markdown 文档中使用

```markdown
## 系统架构

\`\`\`mermaid
graph TD
    A[用户] --> B[React App]
    B --> C[API]
\`\`\`
```

### 2. React 组件渲染

```typescript
// 使用 react-mermaid 库
import { Mermaid } from 'react-mermaid';

function FlowchartViewer() {
  const chart = `
    graph TD
      A[开始] --> B[处理]
      B --> C[结束]
  `;

  return <Mermaid chart={chart} />;
}
```

### 3. 动态生成图表

```typescript
function generateWorkflowDiagram(nodes: Node[], edges: Edge[]): string {
  let mermaid = 'graph TD\n';

  nodes.forEach(node => {
    mermaid += `  ${node.id}[${node.data.label}]\n`;
  });

  edges.forEach(edge => {
    mermaid += `  ${edge.source} --> ${edge.target}\n`;
  });

  return mermaid;
}
```

---

## 快速参考

| 图表类型 | 关键字 | 用途 |
|---------|--------|------|
| 流程图 | `graph` | 流程、决策、系统架构 |
| 序列图 | `sequenceDiagram` | 时序交互、API 调用 |
| 类图 | `classDiagram` | 类结构、对象关系 |
| 状态图 | `stateDiagram-v2` | 状态转换、生命周期 |
| ER 图 | `erDiagram` | 数据库设计、实体关系 |
| 甘特图 | `gantt` | 项目计划、时间线 |
| 旅程图 | `journey` | 用户体验、流程分析 |
