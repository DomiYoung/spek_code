# Task Plan: Claude Code 样式迁移到 OpenCode TUI

## Goal
将 OpenCode 终端界面的视觉样式完全复刻为 Claude Code Cursor 扩展的风格，包括品牌色彩、动画效果、状态指示器和组件样式。

## Current Phase
Phase 11 - Complete (等待编译验证)

## Phases

### Phase 1: 样式分析与需求确认
- [x] 分析 Claude Code Cursor 扩展的 CSS 样式
- [x] 提取核心色彩系统
- [x] 识别动画效果和交互模式
- [x] 分析 OpenCode 现有 TUI 架构
- [x] 确认最终需求范围
- **Status:** complete

### Phase 2: 主题色彩系统修正
- [x] 修改 claudecode.go 主题文件
- [x] 调整核心品牌色 (#D97757 赤陶橙)
- [x] 调整背景色 (#141413 深黑)
- [x] 添加次要橙色 (#C6613F)
- **Status:** complete

### Phase 3: 图标与状态指示器
- [x] 扩展 icons.go 添加状态点图标
- [x] 添加工具类型图标
- [x] 实现状态点颜色系统
- [x] 集成到消息渲染
- **Status:** complete

### Phase 4: 动画效果实现
- [x] 优化 Spinner 样式 (改为 Dot 样式)
- [x] 优化思考状态显示 (添加状态点)
- [ ] 流式光标闪烁 (可选，需要更复杂实现)
- **Status:** complete

### Phase 5: 组件样式增强
- [x] 增强工具调用卡片样式 (添加状态点+图标)
- [x] 优化输入框样式 (使用 UserIcon 提示符)
- [x] 优化 Logo 样式 (使用 Primary 颜色)
- **Status:** complete

### Phase 6: 测试与验证
- [ ] 编译测试 (需用户本地执行)
- [ ] 主题切换测试
- [ ] 各组件视觉验证
- **Status:** in_progress

## Key Questions
1. 是否需要支持浅色主题？（Claude Code 有 Light/Dark 两种）
2. 流式光标闪烁是否为必需功能？（实现复杂度较高）
3. 工具图标是否使用 emoji 还是 ASCII 字符？（终端兼容性考虑）
4. 是否需要完全替换默认主题，还是作为可选主题？

## Decisions Made
| Decision | Rationale |
|----------|-----------|
| 使用 planning-with-files 方法 | 任务复杂度 ≥7，需要系统化规划 |
| 先完成分析再实施 | 避免盲目修改，确保完整理解需求 |
| 保留现有主题作为选项 | claudecode 作为新增主题，不影响其他用户 |

## Errors Encountered
| Error | Attempt | Resolution |
|-------|---------|------------|
| (暂无) | - | - |

## Notes
- Claude Code 核心色: #D97757 (赤陶橙), #C6613F (按钮深橙)
- Claude Code 背景色: #141413 (Slate), #FAF9F5 (Ivory)
- 关键动画: Spinner 1.5s, 光标闪烁 0.5s, 淡入 0.15s
- OpenCode 使用 Bubble Tea + Lipgloss 框架
