package styles

const (
	OpenCodeIcon string = "⌬"

	CheckIcon    string = "✓"
	ErrorIcon    string = "✖"
	WarningIcon  string = "⚠"
	InfoIcon     string = ""
	HintIcon     string = "i"
	SpinnerIcon  string = "..."
	LoadingIcon  string = "⟳"
	DocumentIcon string = "🖼"

	// Status dot icons (Claude Code style)
	DotIcon      string = "●" // Solid dot for status indicators
	DotEmptyIcon string = "○" // Empty dot
	DotHalfIcon  string = "◐" // Half-filled dot (in progress)

	// Streaming cursor
	CursorBlock string = "█" // Block cursor for streaming
	CursorLine  string = "▌" // Line cursor alternative

	// Tool type icons (Claude Code style)
	ToolBashIcon        string = "$"  // Terminal/bash
	ToolEditIcon        string = "✎"  // Edit file
	ToolViewIcon        string = "◉"  // View/read file
	ToolWriteIcon       string = "✍"  // Write file
	ToolGlobIcon        string = "✱"  // Glob/search files
	ToolGrepIcon        string = "⌕"  // Search content
	ToolFetchIcon       string = "↓"  // Web fetch
	ToolTaskIcon        string = "▶"  // Task/agent
	ToolTodoIcon        string = "☐"  // Todo
	ToolSkillIcon       string = "◆"  // Skill
	ToolDiagnosticsIcon string = "⚕"  // Diagnostics/health check
	ToolMcpIcon         string = "⬡"  // MCP external tool
	ToolListIcon        string = "☰"  // List/directory

	// Chevron icons for collapsible content
	ChevronDown  string = "▼"
	ChevronRight string = "▶"
	ChevronUp    string = "▲"

	// Message type indicators
	UserIcon      string = "›" // User message prefix
	AssistantIcon string = "◇" // Assistant message prefix
	SystemIcon    string = "◈" // System message prefix
)
