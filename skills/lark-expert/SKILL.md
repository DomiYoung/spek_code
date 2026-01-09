---
name: lark-expert
description: "飞书/Lark 专家。当用户需要：(1) 开发飞书机器人 (2) 发送消息卡片 Interactive (3) 操作多维表格 Bitable (4) 创建审批流 (5) 订阅 Webhook 事件时触发。"
---

# Lark/飞书 Expert

## 消息卡片

```json
{
  "msg_type": "interactive",
  "card": {
    "header": {
      "title": { "tag": "plain_text", "content": "标题" },
      "template": "blue"
    },
    "elements": [{
      "tag": "div",
      "text": { "tag": "lark_md", "content": "**内容**" }
    }]
  }
}
```

模板色：`blue` 信息 | `green` 成功 | `red` 警告 | `orange` 提醒

## 多维表格 API

```typescript
// 读取记录
GET /open-apis/bitable/v1/apps/:app_token/tables/:table_id/records

// 新增记录
POST /open-apis/bitable/v1/apps/:app_token/tables/:table_id/records
{ "fields": { "标题": "值", "日期": 1703347200000 } }
```

## Webhook 事件

| 事件 | 用途 |
|------|------|
| `im.message.receive_v1` | 接收消息 |
| `bitable.record.changed_v1` | 多维表格变更 |

验证：
```typescript
if (body.type === "url_verification") return { challenge: body.challenge };
```

## 鉴权

```typescript
POST /open-apis/auth/v3/tenant_access_token/internal
{ "app_id": "cli_xxx", "app_secret": "xxx" }
// token 有效期 2h，需缓存
```
