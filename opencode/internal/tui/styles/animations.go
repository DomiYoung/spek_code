package styles

import (
	"github.com/charmbracelet/lipgloss"
	"github.com/opencode-ai/opencode/internal/tui/theme"
)

// Claude Code 2.1.5 Animation & Spacing Constants
// Based on: ~/.cursor/extensions/anthropic.claude-code-2.1.5-darwin-arm64/webview/index.css

// Spacing constants (Claude Code style)
const (
	SpacingSmall  = 4  // --app-spacing-small: 4px
	SpacingMedium = 8  // --app-spacing-medium: 8px
	SpacingLarge  = 12 // --app-spacing-large: 12px
	SpacingXLarge = 16 // --app-spacing-xlarge: 16px
)

// Corner radius constants (Claude Code style)
const (
	CornerRadiusSmall  = 4 // --corner-radius-small: 4px
	CornerRadiusMedium = 6 // --corner-radius-medium: 6px
	CornerRadiusLarge  = 8 // --corner-radius-large: 8px
)

// Status dot size (Claude Code style)
const (
	StatusDotSize = 7 // width: 7px, height: 7px, border-radius: 50%
)

// Animation frame characters for terminal animations
// Since terminal doesn't support CSS animations, we use character sequences

// BlinkFrames for status dot blinking animation
// Based on: @keyframes fo { 0%,100%{opacity:1} 50%{opacity:0} }
var BlinkFrames = []string{"●", " ", "●"}

// SpinnerFrames for loading spinner
// Based on: @keyframes codicon-spin { to{transform:rotate(360deg)} }
var SpinnerFrames = []string{"⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"}

// DotSpinnerFrames - alternative dot spinner (Claude Code style)
var DotSpinnerFrames = []string{"⣾", "⣽", "⣻", "⢿", "⡿", "⣟", "⣯", "⣷"}

// PulseFrames for pulse animation
// Based on: @keyframes Jo { 0%{opacity:1} 50%{opacity:0.4} 100%{opacity:1} }
var PulseFrames = []string{"◉", "◎", "○", "◎", "◉"}

// ProgressFrames for progress indicator
var ProgressFrames = []string{"▰▱▱▱▱", "▰▰▱▱▱", "▰▰▰▱▱", "▰▰▰▰▱", "▰▰▰▰▰"}

// Border characters (Claude Code style)
const (
	BorderVertical       = "│" // Connection line
	BorderVerticalDashed = "┊" // Thinking/reasoning border
	BorderVerticalThick  = "┃" // Message border
	BorderHorizontal     = "─"
	BorderCornerTL       = "┌"
	BorderCornerTR       = "┐"
	BorderCornerBL       = "└"
	BorderCornerBR       = "┘"
	BorderTeeLeft        = "├"
	BorderTeeRight       = "┤"
	BorderCross          = "┼"
)

// Claude Code style border configurations
func ClaudeCodeBorder() lipgloss.Border {
	return lipgloss.Border{
		Top:         BorderHorizontal,
		Bottom:      BorderHorizontal,
		Left:        BorderVertical,
		Right:       BorderVertical,
		TopLeft:     BorderCornerTL,
		TopRight:    BorderCornerTR,
		BottomLeft:  BorderCornerBL,
		BottomRight: BorderCornerBR,
	}
}

// ConnectionLineBorder for tool chain connection
func ConnectionLineBorder() lipgloss.Border {
	return lipgloss.Border{
		Left: BorderVertical,
	}
}

// ThinkingBorder for thinking/reasoning content (dashed style)
func ThinkingBorder() lipgloss.Border {
	return lipgloss.Border{
		Left: BorderVerticalDashed,
	}
}

// MessageBorder for regular messages (thick style)
func MessageBorder() lipgloss.Border {
	return lipgloss.Border{
		Left: BorderVerticalThick,
	}
}

// ToolCardStyle returns Claude Code style for tool cards
// CSS: background: var(--app-tool-background), border-radius: 5px
func ToolCardStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundTool()). // Claude Code: --app-tool-background
		Foreground(t.Text()).
		Padding(0, 1).
		MarginTop(0).
		MarginBottom(0)
}

// InputBoxStyle returns Claude Code style for input boxes
// CSS: border-radius: 8px, focus: border-color: var(--app-claude-orange)
func InputBoxStyle(focused bool) lipgloss.Style {
	t := theme.CurrentTheme()
	style := lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Text()).
		Padding(0, 1).
		Border(lipgloss.RoundedBorder())

	if focused {
		// Claude Code: focus state uses orange border
		style = style.BorderForeground(t.Primary()) // --app-claude-orange
	} else {
		style = style.BorderForeground(t.BorderNormal())
	}

	return style
}

// ButtonStyle returns Claude Code style for buttons
func ButtonStyle(primary bool) lipgloss.Style {
	t := theme.CurrentTheme()
	if primary {
		return lipgloss.NewStyle().
			Background(t.Primary()).
			Foreground(lipgloss.AdaptiveColor{Light: "#ffffff", Dark: "#ffffff"}).
			Padding(0, 2).
			Bold(true)
	}
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Text()).
		Padding(0, 2)
}

// BadgeStyle returns Claude Code style for badges
func BadgeStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.Primary()).
		Foreground(lipgloss.AdaptiveColor{Light: "#ffffff", Dark: "#ffffff"}).
		Padding(0, 1)
}

// HeaderStyle returns Claude Code style for headers
func HeaderStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.Background()).
		Foreground(t.Text()).
		Padding(0, 1).
		BorderBottom(true).
		BorderStyle(lipgloss.NormalBorder()).
		BorderForeground(t.BorderNormal())
}

// ListItemStyle returns Claude Code style for list items
func ListItemStyle(selected bool, hovered bool) lipgloss.Style {
	t := theme.CurrentTheme()
	style := lipgloss.NewStyle().
		Padding(0, 1)

	if selected {
		style = style.
			Background(t.Primary()).
			Foreground(lipgloss.AdaptiveColor{Light: "#ffffff", Dark: "#ffffff"})
	} else if hovered {
		style = style.
			Background(t.BackgroundSecondary()).
			Foreground(t.Text())
	} else {
		style = style.
			Background(t.Background()).
			Foreground(t.Text())
	}

	return style
}

// CodeBlockStyle returns Claude Code style for code blocks
func CodeBlockStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Text()).
		Padding(1, 2).
		Border(ConnectionLineBorder()).
		BorderForeground(t.BorderNormal())
}

// InlineCodeStyle returns Claude Code style for inline code
func InlineCodeStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.MarkdownCode()).
		Padding(0, 1)
}

// TableStyle returns Claude Code style for tables
func TableStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Border(ClaudeCodeBorder()).
		BorderForeground(t.BorderNormal())
}

// WarningBoxStyle returns Claude Code style for warning boxes
func WarningBoxStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Warning()).
		Padding(0, 1).
		Border(lipgloss.RoundedBorder()).
		BorderForeground(t.Warning())
}

// ErrorBoxStyle returns Claude Code style for error boxes
func ErrorBoxStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Error()).
		Padding(0, 1).
		Border(lipgloss.RoundedBorder()).
		BorderForeground(t.Error())
}

// SuccessBoxStyle returns Claude Code style for success boxes
func SuccessBoxStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Background(t.BackgroundSecondary()).
		Foreground(t.Success()).
		Padding(0, 1).
		Border(lipgloss.RoundedBorder()).
		BorderForeground(t.Success())
}

// ModalBackgroundStyle returns Claude Code style for modal backgrounds
func ModalBackgroundStyle() lipgloss.Style {
	return lipgloss.NewStyle().
		Background(lipgloss.AdaptiveColor{Light: "rgba(0,0,0,0.5)", Dark: "rgba(0,0,0,0.75)"})
}

// ShadowStyle adds a shadow effect (simulated in terminal)
func ShadowStyle() lipgloss.Style {
	t := theme.CurrentTheme()
	return lipgloss.NewStyle().
		Border(lipgloss.RoundedBorder()).
		BorderForeground(t.BorderNormal()).
		Padding(1, 2)
}
