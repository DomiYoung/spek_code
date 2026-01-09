# 强制自动化行为

> 由 AGENTS.md 引用的自动化行为规则

## 会话启动时（自动执行）

1. **读取 KI 踩坑记录**（避免重复踩坑）
   ```
   ~/.ai-knowledge/projects/{project}/pitfalls.md
   ```

2. **读取 Serena Memory** - 恢复上次工作进度

3. **检查 Task Master** - 获取待办任务

## 开发新功能前（自动执行）

1. **触发 component-reuse-expert** 检查复用机会
   - 检查 `src/components/` 是否有类似组件
   - 检查 `src/services/` 是否有可复用服务
   - 检查 `src/hooks/` 是否有可复用 Hook

2. **生成可复用组件清单** 到 plan.md

## 功能完成后（自动执行）

1. **触发 code-quality-gates** 质量检查
2. **触发 ki-manager** 反思沉淀
   - 检查是否踩坑需记录
   - 检查是否有架构决策
   - 检查是否有组件模式
3. **更新 KI 文件**（pitfalls.md / component_patterns.md / decisions.md）
4. **更新 Serena Memory** 记录完成状态
5. **自动提交推送**（验证通过后）
