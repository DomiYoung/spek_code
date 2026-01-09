---
name: mermaid-diagrams
description: |
  Mermaid 代码生成图表最佳实践。当涉及流程图、时序图、类图、架构图时自动触发。
  关键词：mermaid、flowchart、sequenceDiagram、classDiagram、架构图、流程图、时序图。
  【代码绘图】包含流程图、时序图、类图、状态图、ER图、甘特图。
allowed-tools: Read, Grep, Glob, Write
---

# Mermaid 代码生成图表

## 流程图 (Flowchart)

### 基础语法

```mermaid
flowchart TD
    A[开始] --> B{条件判断}
    B -->|是| C[执行操作A]
    B -->|否| D[执行操作B]
    C --> E[结束]
    D --> E
```

### 节点形状

```mermaid
flowchart LR
    A[矩形] --> B(圆角矩形)
    B --> C([体育场形])
    C --> D[[子程序]]
    D --> E[(数据库)]
    E --> F((圆形))
    F --> G>旗帜形]
    G --> H{菱形}
    H --> I{{六边形}}
    I --> J[/平行四边形/]
    J --> K[\反向平行四边形\]
```

### 子图分组

```mermaid
flowchart TB
    subgraph 前端
        A[React] --> B[Redux]
        B --> C[Components]
    end

    subgraph 后端
        D[Node.js] --> E[Express]
        E --> F[Database]
    end

    C --> D
```

### 方向控制

```
TB - 从上到下 (Top to Bottom)
TD - 从上到下 (Top Down)
BT - 从下到上 (Bottom to Top)
RL - 从右到左 (Right to Left)
LR - 从左到右 (Left to Right)
```

## 时序图 (Sequence Diagram)

### 基础交互

```mermaid
sequenceDiagram
    participant U as 用户
    participant F as 前端
    participant B as 后端
    participant D as 数据库

    U->>F: 点击登录
    F->>B: POST /api/login
    B->>D: 查询用户
    D-->>B: 返回用户数据
    B-->>F: 返回 Token
    F-->>U: 跳转首页
```

### 高级特性

```mermaid
sequenceDiagram
    autonumber

    participant C as Client
    participant S as Server

    rect rgb(200, 220, 255)
        Note over C,S: 认证流程
        C->>+S: 请求登录
        S-->>-C: 返回 Token
    end

    alt 成功
        C->>S: 携带 Token 请求
        S-->>C: 返回数据
    else 失败
        C->>S: 无效 Token
        S-->>C: 401 Unauthorized
    end

    loop 每5秒
        C->>S: 心跳检测
        S-->>C: pong
    end
```

### 消息类型

```
->   实线箭头
-->  虚线箭头
->>  实线带箭头
-->> 虚线带箭头
-x   实线带叉
--x  虚线带叉
-)   实线带开放箭头
--)  虚线带开放箭头
```

## 类图 (Class Diagram)

### 类定义

```mermaid
classDiagram
    class User {
        +String id
        +String name
        -String password
        +login() boolean
        +logout() void
        #validatePassword(pwd) boolean
    }

    class Admin {
        +String role
        +manageUsers() void
    }

    class Order {
        +String orderId
        +Date createTime
        +calculateTotal() number
    }

    User <|-- Admin : 继承
    User "1" --> "*" Order : 拥有
```

### 关系类型

```
<|-- 继承
*--  组合
o--  聚合
-->  关联
--   链接
..>  依赖
..|> 实现
```

## 状态图 (State Diagram)

```mermaid
stateDiagram-v2
    [*] --> 待提交
    待提交 --> 审核中: 提交
    审核中 --> 已通过: 通过
    审核中 --> 已拒绝: 拒绝
    已拒绝 --> 待提交: 重新编辑
    已通过 --> [*]

    state 审核中 {
        [*] --> 初审
        初审 --> 复审: 初审通过
        复审 --> [*]: 复审通过
    }
```

## ER 图 (Entity Relationship)

```mermaid
erDiagram
    USER ||--o{ ORDER : places
    USER {
        string id PK
        string name
        string email UK
        date created_at
    }
    ORDER ||--|{ ORDER_ITEM : contains
    ORDER {
        string id PK
        string user_id FK
        date order_date
        decimal total
    }
    ORDER_ITEM {
        string id PK
        string order_id FK
        string product_id FK
        int quantity
    }
    PRODUCT ||--o{ ORDER_ITEM : "ordered in"
    PRODUCT {
        string id PK
        string name
        decimal price
    }
```

## 甘特图 (Gantt)

```mermaid
gantt
    title 项目开发计划
    dateFormat YYYY-MM-DD

    section 需求阶段
    需求分析     :a1, 2024-01-01, 7d
    原型设计     :a2, after a1, 5d
    需求评审     :a3, after a2, 2d

    section 开发阶段
    后端开发     :b1, after a3, 14d
    前端开发     :b2, after a3, 14d
    接口联调     :b3, after b1, 5d

    section 测试阶段
    功能测试     :c1, after b3, 7d
    性能测试     :c2, after c1, 3d
    上线部署     :milestone, after c2, 0d
```

## 饼图 (Pie Chart)

```mermaid
pie showData
    title 浏览器市场份额
    "Chrome" : 65
    "Safari" : 19
    "Firefox" : 8
    "Edge" : 5
    "其他" : 3
```

## 架构图模板

### 微服务架构

```mermaid
flowchart TB
    subgraph 客户端
        Web[Web 应用]
        Mobile[移动端]
    end

    subgraph 网关层
        Gateway[API Gateway]
        Auth[认证服务]
    end

    subgraph 业务层
        UserSvc[用户服务]
        OrderSvc[订单服务]
        ProductSvc[商品服务]
    end

    subgraph 数据层
        MySQL[(MySQL)]
        Redis[(Redis)]
        MQ[消息队列]
    end

    Web --> Gateway
    Mobile --> Gateway
    Gateway --> Auth
    Gateway --> UserSvc
    Gateway --> OrderSvc
    Gateway --> ProductSvc

    UserSvc --> MySQL
    UserSvc --> Redis
    OrderSvc --> MySQL
    OrderSvc --> MQ
    ProductSvc --> MySQL
```

### 前端架构

```mermaid
flowchart TD
    subgraph View[视图层]
        Pages[页面组件]
        Components[通用组件]
    end

    subgraph State[状态层]
        Store[全局状态]
        Hooks[自定义 Hooks]
    end

    subgraph Service[服务层]
        API[API 请求]
        Utils[工具函数]
    end

    Pages --> Components
    Pages --> Hooks
    Hooks --> Store
    Hooks --> API
    API --> Utils
```

## 在 Markdown 中使用

````markdown
```mermaid
flowchart LR
    A --> B --> C
```
````

## 样式定制

```mermaid
flowchart LR
    A[开始]:::startNode --> B[处理]:::processNode --> C[结束]:::endNode

    classDef startNode fill:#90EE90,stroke:#228B22
    classDef processNode fill:#87CEEB,stroke:#4169E1
    classDef endNode fill:#FFB6C1,stroke:#DC143C
```

## 🔗 与其他 Skills 协作

| Skill | 协作方式 |
|-------|----------|
| `bpmn-workflow-patterns` | 流程图替代方案 |
| `drawio-diagrams` | 复杂图表补充 |

### 常用场景

- 技术文档中的架构图
- README 中的流程说明
- 代码注释中的逻辑图
- PR 描述中的变更说明
