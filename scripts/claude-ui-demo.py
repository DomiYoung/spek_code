#!/usr/bin/env python3
"""
Claude Code UI 风格终端输出演示
模拟 Claude Code 原版界面效果
"""

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich import box
import time

console = Console()

# ═══════════════════════════════════════════════════════════════
# 状态指示器
# ═══════════════════════════════════════════════════════════════

def dot(status: str) -> str:
    """状态圆点 - 完全匹配 Claude Code 原版"""
    colors = {
        "success": "[green]●[/green]",
        "error": "[red]●[/red]", 
        "warning": "[yellow]●[/yellow]",
        "pending": "[dim]○[/dim]",
        "running": "[#888888]●[/#888888]",
    }
    return colors.get(status, "[dim]○[/dim]")

# ═══════════════════════════════════════════════════════════════
# 工具调用卡片 - Claude Code 风格
# ═══════════════════════════════════════════════════════════════

def tool_call(tool_name: str, description: str, input_text: str, output_text: str, status: str = "success"):
    """工具调用块 - 无边框，纯文本风格"""
    console.print()
    # 标题行: ● Bash Read Claude settings
    console.print(f"{dot(status)} [bold]{tool_name}[/bold] [dim]{description}[/dim]")
    console.print()
    # IN 块
    console.print(f"  [dim]IN[/dim]   [cyan]{input_text}[/cyan]")
    console.print()
    # OUT 块  
    for line in output_text.split('\n'):
        console.print(f"  [dim]OUT[/dim]  {line}")

def thinking(expanded: bool = False):
    """思考指示器"""
    arrow = "∨" if expanded else "›"
    console.print()
    console.print(f"{dot('running')} [italic dim]Thinking[/italic dim] [dim]{arrow}[/dim]")

# ═══════════════════════════════════════════════════════════════
# 表格 - 标准样式 (无圆角)
# ═══════════════════════════════════════════════════════════════

def standard_table(title: str, headers: list, rows: list, status_col: int = None):
    """标准表格 - 类似 Claude Code 原版"""
    table = Table(
        title=f"[bold]{title}[/bold]" if title else None,
        box=box.SIMPLE_HEAD,  # 只有表头下划线
        show_header=True,
        header_style="dim",
        padding=(0, 2),
        collapse_padding=True,
    )
    
    for header in headers:
        table.add_column(header)
    
    for row in rows:
        formatted_row = []
        for i, cell in enumerate(row):
            if status_col is not None and i == status_col:
                # 状态列特殊处理
                if "一致" in str(cell) or "✓" in str(cell):
                    formatted_row.append(f"[green]✓[/green] 一致")
                elif "不一致" in str(cell) or "✗" in str(cell):
                    formatted_row.append(f"[red]✗[/red] 不一致")
                else:
                    formatted_row.append(str(cell))
            else:
                formatted_row.append(str(cell))
        table.add_row(*formatted_row)
    
    return table

# ═══════════════════════════════════════════════════════════════
# Todo 列表 - 绿色连线
# ═══════════════════════════════════════════════════════════════

def todo_list(items: list):
    """Todo 列表 - 带连线效果"""
    console.print()
    for i, (status, text) in enumerate(items):
        is_last = i == len(items) - 1
        
        if status == "completed":
            icon = "[green]✓[/green]"
            line_color = "green"
            text_style = "strike dim"
        elif status == "in_progress":
            icon = "[blue]●[/blue]"
            line_color = "blue"
            text_style = "bold"
        else:
            icon = "[dim]○[/dim]"
            line_color = "dim"
            text_style = "dim"
        
        console.print(f"  {icon} [{text_style}]{text}[/{text_style}]")
        if not is_last:
            console.print(f"  [{line_color}]│[/{line_color}]")

# ═══════════════════════════════════════════════════════════════
# 流式输出
# ═══════════════════════════════════════════════════════════════

def stream_text(text: str, delay: float = 0.015):
    """流式打字效果"""
    for char in text:
        console.print(char, end="")
        time.sleep(delay)
    console.print()

# ═══════════════════════════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════════════════════════

def main():
    console.clear()
    
    # 思考中
    thinking()
    time.sleep(0.3)
    
    # Glob 工具调用
    console.print()
    console.print(f"{dot('success')} [bold]Glob[/bold] [dim]pattern: \"**/*\"[/dim]")
    console.print(f"  [dim]Found 101 files[/dim]")
    
    # 普通文本
    console.print()
    console.print(f"{dot('running')} 让我查找全局 Claude 配置文件和 MCP memory 相关内容:")
    
    # MCP 工具调用 (错误)
    console.print()
    console.print(f"{dot('error')} [bold]mcp__filesystem__list_directory[/bold]")
    console.print()
    console.print('  [dim]IN[/dim]   [cyan]{"path": "/Users/domiyoung___/.claude"}[/cyan]')
    console.print()
    console.print('  [dim]OUT[/dim]  [red]Access denied - path outside allowed directories[/red]')
    
    # 思考中
    thinking()
    time.sleep(0.3)
    
    # Bash 工具调用
    tool_call(
        "Bash", 
        "List Claude config directory",
        "ls -la ~/.claude/ 2>/dev/null | head -30",
        "total 9840\ndrwxr-xr-x@  33 domiyoung___  staff  1056 Jan 11 16:41 .\ndrwxr-x---+  75 domiyoung___  staff  2400 Jan 11 16:40 .."
    )
    
    # Bash 读取设置
    tool_call(
        "Bash",
        "Read Claude settings", 
        "cat ~/.claude/settings.json 2>/dev/null",
        '{\n    "permissions": {\n        "allow": ['
    )
    
    # 思考中
    thinking()
    
    # 标题
    console.print()
    console.print()
    console.print("[bold]█ CLAUDE.md 完整审核报告[/bold]")
    console.print()
    
    # 版本验证结果
    console.print("[green]✓[/green] [bold]版本验证结果[/bold]")
    console.print()
    
    version_table = standard_table(
        None,
        ["依赖", "CLAUDE.md 版本", "package.json 实际版本", "状态"],
        [
            ("Redux Toolkit", "2.0.0", "2.0.0", "✓"),
            ("MUI", "5.18.0", "^5.18.0", "✓"),
            ("Yjs", "14.0.0-1", "14.0.0-1", "✓"),
            ("Slate", "0.101.4", "^0.101.4", "✓"),
            ("Axios", "1.9.0", "^1.9.0", "✓"),
        ],
        status_col=3
    )
    console.print(version_table)
    console.print()
    console.print("[dim]所有依赖版本都是准确的。[/dim]")
    
    # 改进建议
    console.print()
    console.print("[yellow]⚠[/yellow] [bold]改进建议[/bold]")
    console.print()
    console.print("[bold]1. 缺少的专家角色[/bold]")
    console.print()
    console.print("[dim]当前项目使用但未列入专家库的依赖:[/dim]")
    console.print()
    
    expert_table = standard_table(
        None,
        ["依赖", "版本", "建议添加的专家"],
        [
            ("SignalR", "^10.0.0", "实时通信专家 (WebSocket, 重连策略)"),
            ("FullCalendar", "^6.1.19", "日历/时间专家 (事件渲染, 性能)"),
            ("Radix UI", "多个组件", "无障碍专家 (a11y, 键盘导航)"),
            ("Floating UI", "^0.26.27", "定位专家 (Popover, Tooltip)"),
        ],
        status_col=None
    )
    console.print(expert_table)
    
    # Hard Constraints
    console.print()
    console.print("[bold]2. Hard Constraints 可补充[/bold]")
    console.print()
    
    constraints_table = standard_table(
        None,
        ["建议添加", "说明"],
        [
            ("避免 [red]!important[/red]", "CSS 优先级问题"),
            ("禁止直接操作 DOM", "使用 React ref"),
            ("必须处理 loading/error 状态", "UX 完整性"),
        ],
        status_col=None
    )
    console.print(constraints_table)
    
    # 流程优化建议
    console.print()
    console.print("[bold]3. 流程优化建议[/bold]")
    console.print()
    console.print("  [dim]Step 6.5:[/dim] [cyan]同步到 Obsidian[/cyan] [yellow][强制][/yellow]")
    console.print("[green]+ Step 6.6:[/green] [cyan]知识沉淀检查[/cyan] [dim][自动][/dim] - 建议添加")
    console.print("[green]+   - 检查是否有踩坑需要记录[/green]")
    console.print("[green]+   - 更新 pitfalls.md (如适用)[/green]")
    
    # 总结
    console.print()
    console.print("[bold]📊 总结[/bold]")
    console.print()
    
    summary_table = standard_table(
        None,
        ["评估项", "得分", "说明"],
        [
            ("结构完整性", "9/10", "流程清晰，专家定义明确"),
            ("版本准确性", "10/10", "所有版本与实际一致"),
            ("可执行性", "8/10", "同步脚本存在且可用"),
            ("覆盖完整性", "7/10", "缺少部分重要依赖的专家角色"),
        ],
        status_col=None
    )
    console.print(summary_table)
    
    console.print()
    console.print("[dim]总评: 8.5/10 - 这是一份高质量的 AI 工作流配置文件。建议补充 SignalR、Radix UI 等专家角色。[/dim]")
    console.print()

if __name__ == "__main__":
    main()
