# Completion Loop

> 任务完成后的自动提交推送流程，由 RULES.md 引用

## 规则

验证通过 → 自动提交推送，无需手动确认

## 触发流程

```
任务完成 → 验证检查 → 全部通过 → 自动提交推送
```

## 验证检查（必须全部通过）

- `pnpm lint` 或项目 lint 命令
- `pnpm exec tsc --noEmit` 或类型检查
- 无 `console.log`（生产代码）
- 无未注释的 `any` 类型

## 自动提交流程

1. 分析变更 → 推断 type/scope
2. 生成知识图谱格式 commit message（**全中文**）
3. `git add` + `git commit`（使用 HEREDOC 格式）
4. `git push origin <current-branch>`
5. 输出提交摘要

## Commit Message 格式

```
<type>(<scope>): <用户价值描述（中文）>

核心改动：<关键变更点>
影响范围：<涉及模块/组件>
技术背景：<为什么这样做>
相关文件：<文件统计>
```

## 🔴 禁止词

绝对禁止出现：
- AI, agent, claude, bot, GPT, Anthropic, Copilot
- Generated, Co-Authored-By, noreply@anthropic.com
- 🤖 等机器人表情符号

## 异常处理

| 情况 | 行为 |
|------|------|
| 验证失败 | ❌ 停止，提示修复后重试 |
| 无变更 | ⚠️ 跳过提交 |
| 用户豁免 | ⏭️ 跳过闭环 |

## 豁免关键词

检测到以下词时跳过自动提交：
- "不要提交"、"别提交"、"skip commit"、"no commit"
- "只是看看"、"试试"、"探索"、"调试"
