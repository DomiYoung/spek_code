package theme

import (
	"github.com/charmbracelet/lipgloss"
)

// ClaudeCodeTheme implements the Theme interface with Claude Code brand colors.
// Matches the style of Claude Code extension in Cursor IDE.
type ClaudeCodeTheme struct {
	BaseTheme
}

// NewClaudeCodeTheme creates a new instance of the Claude Code theme.
func NewClaudeCodeTheme() *ClaudeCodeTheme {
	// Claude Code color palette - Dark mode focused
	// Based on the Claude Code Cursor extension aesthetic
	
	// Dark mode colors (primary)
	// Based on Claude Code Cursor extension official colors
	darkBackground := "#141413"       // Claude Slate - official dark background
	darkCurrentLine := "#1c1c1b"      // Slightly lighter for current line
	darkSelection := "#2a2a28"        // Selection background
	darkForeground := "#e5e5e5"       // Light gray text
	darkComment := "#6b7280"          // Muted gray for comments
	darkPrimary := "#D97757"          // Claude Orange - official brand color (赤陶橙)
	darkSecondary := "#C6613F"        // Claude Clay Button Orange
	darkAccent := "#D97757"           // Keep consistent with primary
	darkRed := "#C74E39"              // Claude error red
	darkOrange := "#E1C08D"           // Claude warning (warm yellow)
	darkGreen := "#74C991"            // Claude success green
	darkCyan := "#06b6d4"             // Info cyan
	darkYellow := "#E1C08D"           // Emphasized text (warm)
	darkBorder := "#2a2a28"           // Border color (subtle)

	// Light mode colors
	// Based on Claude Code Cursor extension official colors
	lightBackground := "#FAF9F5"      // Claude Ivory - official light background
	lightCurrentLine := "#F5F4F0"     // Slightly darker for current line
	lightSelection := "#EBE9E4"       // Selection background
	lightForeground := "#141413"      // Claude Slate for text
	lightComment := "#6b7280"         // Muted gray for comments
	lightPrimary := "#D97757"         // Claude Orange - same as dark mode
	lightSecondary := "#C6613F"       // Claude Clay Button Orange
	lightAccent := "#D97757"          // Keep consistent with primary
	lightRed := "#C74E39"             // Claude error red
	lightOrange := "#B8860B"          // Warning (darker for light bg)
	lightGreen := "#2E7D32"           // Success green (darker for light bg)
	lightCyan := "#0891b2"            // Info cyan
	lightYellow := "#8B7355"          // Emphasized text (warm brown)
	lightBorder := "#E0DED9"          // Border color (subtle warm gray)

	theme := &ClaudeCodeTheme{}

	// Base colors
	theme.PrimaryColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.SecondaryColor = lipgloss.AdaptiveColor{
		Dark:  darkSecondary,
		Light: lightSecondary,
	}
	theme.AccentColor = lipgloss.AdaptiveColor{
		Dark:  darkAccent,
		Light: lightAccent,
	}

	// Status colors
	theme.ErrorColor = lipgloss.AdaptiveColor{
		Dark:  darkRed,
		Light: lightRed,
	}
	theme.WarningColor = lipgloss.AdaptiveColor{
		Dark:  darkOrange,
		Light: lightOrange,
	}
	theme.SuccessColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.InfoColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}

	// Text colors
	theme.TextColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}
	theme.TextMutedColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.TextEmphasizedColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}

	// Background colors
	theme.BackgroundColor = lipgloss.AdaptiveColor{
		Dark:  darkBackground,
		Light: lightBackground,
	}
	theme.BackgroundSecondaryColor = lipgloss.AdaptiveColor{
		Dark:  darkCurrentLine,
		Light: lightCurrentLine,
	}
	theme.BackgroundDarkerColor = lipgloss.AdaptiveColor{
		Dark:  "#000000",
		Light: "#f9fafb",
	}
	// Claude Code: --app-tool-background for tool cards
	theme.BackgroundToolColor = lipgloss.AdaptiveColor{
		Dark:  "#1a1a19", // Slightly lighter than slate for tool cards
		Light: "#F0EFEB", // Slightly darker than ivory for tool cards
	}

	// Border colors
	theme.BorderNormalColor = lipgloss.AdaptiveColor{
		Dark:  darkBorder,
		Light: lightBorder,
	}
	theme.BorderFocusedColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.BorderDimColor = lipgloss.AdaptiveColor{
		Dark:  darkSelection,
		Light: lightSelection,
	}

	// Diff view colors
	theme.DiffAddedColor = lipgloss.AdaptiveColor{
		Dark:  "#22c55e",
		Light: "#16a34a",
	}
	theme.DiffRemovedColor = lipgloss.AdaptiveColor{
		Dark:  "#ef4444",
		Light: "#dc2626",
	}
	theme.DiffContextColor = lipgloss.AdaptiveColor{
		Dark:  "#9ca3af",
		Light: "#6b7280",
	}
	theme.DiffHunkHeaderColor = lipgloss.AdaptiveColor{
		Dark:  "#6b7280",
		Light: "#9ca3af",
	}
	theme.DiffHighlightAddedColor = lipgloss.AdaptiveColor{
		Dark:  "#86efac",
		Light: "#bbf7d0",
	}
	theme.DiffHighlightRemovedColor = lipgloss.AdaptiveColor{
		Dark:  "#fca5a5",
		Light: "#fecaca",
	}
	theme.DiffAddedBgColor = lipgloss.AdaptiveColor{
		Dark:  "#14532d",
		Light: "#dcfce7",
	}
	theme.DiffRemovedBgColor = lipgloss.AdaptiveColor{
		Dark:  "#7f1d1d",
		Light: "#fee2e2",
	}
	theme.DiffContextBgColor = lipgloss.AdaptiveColor{
		Dark:  darkBackground,
		Light: lightBackground,
	}
	theme.DiffLineNumberColor = lipgloss.AdaptiveColor{
		Dark:  "#6b7280",
		Light: "#9ca3af",
	}
	theme.DiffAddedLineNumberBgColor = lipgloss.AdaptiveColor{
		Dark:  "#166534",
		Light: "#bbf7d0",
	}
	theme.DiffRemovedLineNumberBgColor = lipgloss.AdaptiveColor{
		Dark:  "#991b1b",
		Light: "#fecaca",
	}

	// Markdown colors - Claude orange theme
	theme.MarkdownTextColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}
	theme.MarkdownHeadingColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.MarkdownLinkColor = lipgloss.AdaptiveColor{
		Dark:  darkAccent,
		Light: lightAccent,
	}
	theme.MarkdownLinkTextColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownCodeColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.MarkdownBlockQuoteColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.MarkdownEmphColor = lipgloss.AdaptiveColor{
		Dark:  darkYellow,
		Light: lightYellow,
	}
	theme.MarkdownStrongColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.MarkdownHorizontalRuleColor = lipgloss.AdaptiveColor{
		Dark:  darkBorder,
		Light: lightBorder,
	}
	theme.MarkdownListItemColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.MarkdownListEnumerationColor = lipgloss.AdaptiveColor{
		Dark:  darkSecondary,
		Light: lightSecondary,
	}
	theme.MarkdownImageColor = lipgloss.AdaptiveColor{
		Dark:  darkAccent,
		Light: lightAccent,
	}
	theme.MarkdownImageTextColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.MarkdownCodeBlockColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}

	// Syntax highlighting colors
	theme.SyntaxCommentColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}
	theme.SyntaxKeywordColor = lipgloss.AdaptiveColor{
		Dark:  "#c084fc", // Purple for keywords
		Light: "#9333ea",
	}
	theme.SyntaxFunctionColor = lipgloss.AdaptiveColor{
		Dark:  darkPrimary,
		Light: lightPrimary,
	}
	theme.SyntaxVariableColor = lipgloss.AdaptiveColor{
		Dark:  "#f472b6", // Pink for variables
		Light: "#db2777",
	}
	theme.SyntaxStringColor = lipgloss.AdaptiveColor{
		Dark:  darkGreen,
		Light: lightGreen,
	}
	theme.SyntaxNumberColor = lipgloss.AdaptiveColor{
		Dark:  darkAccent,
		Light: lightAccent,
	}
	theme.SyntaxTypeColor = lipgloss.AdaptiveColor{
		Dark:  darkCyan,
		Light: lightCyan,
	}
	theme.SyntaxOperatorColor = lipgloss.AdaptiveColor{
		Dark:  darkForeground,
		Light: lightForeground,
	}
	theme.SyntaxPunctuationColor = lipgloss.AdaptiveColor{
		Dark:  darkComment,
		Light: lightComment,
	}

	return theme
}

func init() {
	// Register the Claude Code theme with the theme manager
	RegisterTheme("claudecode", NewClaudeCodeTheme())
}
