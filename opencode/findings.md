# Findings & Decisions

## Requirements
<!-- 从用户请求和 Claude Code 扩展分析中提取 -->
- 复刻 Claude Code Cursor 扩展的视觉样式
- 包括品牌色彩系统
- 包括动画效果（Spinner、光标闪烁）
- 包括状态指示器（彩色圆点）
- 包括工具卡片样式

## Research Findings

### Claude Code Cursor 扩展样式分析

#### 1. 品牌色彩系统
| 变量名 | 值 | 用途 |
|--------|-----|------|
| --app-claude-orange | #D97757 | 核心品牌色 - 赤陶橙 |
| --app-claude-clay-button-orange | #C6613F | 按钮深橙色 |
| --app-claude-ivory | #FAF9F5 | 浅色背景/象牙白 |
| --app-claude-slate | #141413 | 深色背景/石板黑 |

#### 2. 状态点颜色
| 状态 | 颜色 | 用途 |
|------|------|------|
| 成功 | #74C991 | 工具执行成功 |
| 错误 | #C74E39 | 工具执行失败 |
| 警告 | #E1C08D | 警告/待确认 |
| 进行中 | #D97757 | 正在执行 + 闪烁 |

#### 3. 动画效果
| 效果 | 动画名 | 时长 | 用途 |
|------|--------|------|------|
| 淡入 | fadeIn | 0.15s | 消息出现 |
| 闪烁 | blink | 1s infinite | 进度指示点 |
| 旋转 | codicon-spin | 1.5s steps(30) | Spinner 加载 |
| 脉冲 | pulse | 1.5s ease-in-out | 录音/思考指示 |
| 滑入 | slideIn | 0.15s ease-out | 菜单弹出 |
| 光标 | cursor-phase | 0.5s × 20 | 流式输出光标 |

#### 4. 设计规格
| 类别 | 规格 |
|------|------|
| 间距 | 4px / 8px / 12px / 16px |
| 圆角 | 4px (小) / 6px (中) / 8px (大) |
| 字体 | 13px 主文字，0.9em 缩小 |
| 阴影 | 0 2px 8px rgba(0,0,0,0.15) |

#### 5. 组件结构
```
ChatContainer
├── Header (顶部栏)
│   ├── SessionSelector
│   ├── PermissionModeIndicator
│   └── HeaderButtons
├── MessagesContainer
│   ├── Message
│   │   ├── TimelineMessage (时间线 + 状态点)
│   │   ├── UserMessage
│   │   ├── ToolCall (工具卡片)
│   │   └── PermissionRequest
│   └── GradientOverlay (底部渐变)
├── InputArea
│   ├── InputContainer
│   ├── AttachedFiles
│   └── InputFooter
└── EmptyState (空状态欢迎页)
```

### OpenCode TUI 架构分析

#### 1. 技术栈
- **Bubble Tea**: TUI 框架 (Go)
- **Lipgloss**: 样式库
- **Glamour**: Markdown 渲染
- **bubbles/spinner**: 已有 Spinner 组件

#### 2. 文件结构
```
internal/tui/
├── tui.go              # 主应用入口
├── theme/
│   ├── theme.go        # Theme 接口
│   ├── manager.go      # 主题管理器
│   ├── opencode.go     # 默认主题
│   └── claudecode.go   # Claude 主题 (已创建)
├── styles/
│   ├── styles.go       # 样式函数
│   ├── icons.go        # 图标定义
│   └── markdown.go     # Markdown 渲染
└── components/
    ├── chat/
    │   ├── chat.go     # 聊天主视图
    │   ├── message.go  # 消息渲染 (核心)
    │   ├── editor.go   # 输入编辑器
    │   ├── list.go     # 消息列表 (Spinner)
    │   └── sidebar.go
    ├── dialog/
    └── core/
```

#### 3. 现有实现分析
- **Spinner**: 使用 `spinner.Pulse` 样式，已有完整实现
- **主题系统**: 完整的 Theme 接口，支持热切换
- **消息渲染**: 左边框样式，支持工具调用
- **状态显示**: 基于文字的 "Thinking..." 提示

### 差异对比
| 特性 | Claude Code | OpenCode 现状 | 需要改进 |
|------|-------------|---------------|----------|
| 主色 | #D97757 | #fab283 | ✅ 需修正 |
| 背景 | #141413 | #212121 | ✅ 需修正 |
| 状态点 | 彩色圆点 | 无 | ✅ 需添加 |
| 流式光标 | 闪烁 █ | 无 | ⚠️ 可选 |
| Spinner | 旋转动画 | Pulse 动画 | ⚠️ 可调整 |
| 工具卡片 | 可折叠+图标 | 简单边框 | ✅ 需增强 |

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| 修改 claudecode.go 而非创建新文件 | 已有基础结构，只需调整色值 |
| 使用 ASCII 状态点图标 | 终端兼容性优先，● ○ ◐ 等字符广泛支持 |
| 先完成色彩再处理动画 | 色彩是基础，动画可逐步增强 |
| 复用现有 Spinner | bubbles/spinner 已够用，只需调整样式 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| (暂无) | - |

## Resources
- Claude Code 扩展路径: `/Users/jinjia/.cursor/extensions/anthropic.claude-code-2.1.5-darwin-arm64/`
- 核心 CSS: `webview/index.css`
- OpenCode 主题: `internal/tui/theme/claudecode.go`
- 消息渲染: `internal/tui/components/chat/message.go`
- 消息列表: `internal/tui/components/chat/list.go`
- Claude Code 开源仓库: `https://github.com/anthropics/claude-code`

## Claude Code 2.1.5 精确 CSS 规则

### 状态点系统 (Status Dot)
```css
/* 基础状态点 - 圆形指示器 */
.e:before {
  content: "";
  position: absolute;
  left: 9px;
  top: 15px;
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background-color: var(--app-secondary-foreground);
  z-index: 1;
}

/* 成功状态 - 绿色 */
.e.fr:before { background-color: #74c991; }

/* 错误状态 - 红色 */
.e.vr:before { background-color: #c74e39; }

/* 警告状态 - 黄色 */
.e.wr:before { background-color: #e1c08d; }

/* 加载中 - 闪烁动画 */
.e.kr:before { animation: fo 1s linear infinite; }
```

### 连接线系统 (Connection Line)
```css
/* 基础连接线 - 垂直线连接多个工具 */
.e:after {
  content: "";
  position: absolute;
  left: 12px;
  top: 0;
  bottom: 0;
  width: 1px;
  background-color: var(--app-primary-border-color);
}

/* 第一个元素: 连接线从状态点下方开始 (18px) */
.e:not(.e+.e):after { top: 18px; }

/* 最后一个元素: 连接线只到状态点位置 (18px 高度) */
.e:not(:has(+.e)):after { height: 18px; }

/* 单独元素: 不显示连接线 */
.e:not(.e+.e):not(:has(+.e)):after { display: none; }

/* 折叠状态: 连接线半透明 */
.e.Y:after { opacity: 0.4; }
```

### Badge 样式
```css
/* 成功 badge - 绿底白字 */
.k.ga { background-color: #74c991; color: #fff; }

/* 错误 badge - 红底白字 */
.k.ma { background-color: #c74e39; color: #fff; }

/* 警告 badge - 黄底黑字 */
.k.ba { background-color: #e1c08d; color: #000; }
```

### 输入框样式
```css
/* 输入框容器 */
.t {
  display: flex;
  flex-direction: column;
  padding: 8px;
  background-color: var(--app-input-secondary-background);
  border: 1px solid var(--app-input-border);
  border-radius: var(--corner-radius-large); /* 8px */
  max-height: 70vh;
  outline: 0;
  position: relative;
  margin-bottom: 6px;
}
```

### Claude 品牌按钮
```css
/* 橙色边框按钮 */
.Ee {
  position: relative;
  width: 16px;
  height: 16px;
  flex-shrink: 0;
  padding: 2px;
  border: 1px solid var(--app-claude-orange);
  border-radius: var(--corner-radius-small); /* 4px */
  background: #d977571a; /* 10% 透明橙色 */
  cursor: pointer;
}

.Ee:hover { background: #d9775733; } /* 20% 透明橙色 */

/* 圆形橙色按钮 */
.Nt {
  width: 19px;
  height: 19px;
  flex-shrink: 0;
  border: 1px solid var(--app-claude-orange);
  border-radius: 23px;
  background: #d97757cc; /* 80% 透明橙色 */
}
```

## Visual/Browser Findings
- Claude Code 使用 SVG Logo 作为欢迎页图标
- 消息使用时间线样式，左侧有状态点指示器
- 工具调用有专门的卡片样式，支持折叠/展开
- 底部有渐变遮罩覆盖消息列表边缘
- **状态点位置**: left:9px, top:15px, 尺寸 7x7px
- **连接线位置**: left:12px, width:1px
- **单独工具不显示连接线，多个工具才显示**

## OpenCode TUI 映射

| Claude Code CSS | OpenCode Go | 说明 |
|-----------------|-------------|------|
| `.e:before` 状态点 | `renderStatusDot()` | ● ○ ◐ 字符 |
| `.e.fr` 成功 | `t.Success()` #74c991 | 绿色点 |
| `.e.vr` 错误 | `t.Error()` #c74e39 | 红色点 |
| `.e.wr` 警告 | `t.Warning()` #e1c08d | 黄色点 |
| `.e:after` 连接线 | `│` BorderVertical | 连接多个工具 |
| 单独工具无连接线 | `isSingle → " "` | 空格替代 |

---
*Update this file after every 2 view/browser/search operations*
