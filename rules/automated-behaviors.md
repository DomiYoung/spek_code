# 强制自动化行为

> 由 AGENTS.md 引用的自动化行为规则

## 会话启动时（自动执行）

1. **检查 Task Master** - 获取待办任务
2. **检查项目 SESSION.md** - 恢复上次进度

## 开发新功能前（自动执行）

1. **触发 component-reuse-expert** 检查复用机会
   - 检查 `src/components/` 是否有类似组件
   - 检查 `src/services/` 是否有可复用服务
   - 检查 `src/hooks/` 是否有可复用 Hook

2. **生成可复用组件清单** 到 plan.md

## 功能完成后（自动执行）

1. **触发 code-quality-gates** 质量检查
2. **知识价值评估**（知识四问）
   - 可复用？费力？有帮助？未文档化？
   - 2+ YES → 写入对应 `skills/{tech}-patterns/SKILL.md` + Evolution Marker
3. **自动提交推送**（验证通过后）
