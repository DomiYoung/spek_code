#!/usr/bin/env python3
"""
Claude Code UI 工具库
模拟 Claude Code 原版界面风格，可在任意 Python 脚本中复用

使用方法:
    from claude_ui import ui
    
    ui.thinking()
    ui.tool_call("Bash", "执行命令", "ls -la", "文件列表...")
    ui.table(["列1", "列2"], [("值1", "值2")])
    ui.todo([("completed", "任务1"), ("in_progress", "任务2")])
    ui.success("操作成功")
    ui.error("操作失败")
    ui.stream("流式输出文本...")
"""

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box
import time

class ClaudeUI:
    """Claude Code 风格 UI 组件"""
    
    def __init__(self):
        self.console = Console()
    
    # ═══════════════════════════════════════════════════════════════
    # 状态圆点
    # ═══════════════════════════════════════════════════════════════
    
    def dot(self, status: str) -> str:
        """状态圆点"""
        colors = {
            "success": "[green]●[/green]",
            "error": "[red]●[/red]",
            "warning": "[yellow]●[/yellow]",
            "pending": "[dim]○[/dim]",
            "running": "[#888888]●[/#888888]",
            "info": "[blue]●[/blue]",
        }
        return colors.get(status, "[dim]○[/dim]")
    
    # ═══════════════════════════════════════════════════════════════
    # 思考指示器
    # ═══════════════════════════════════════════════════════════════
    
    def thinking(self, expanded: bool = False):
        """思考中指示器"""
        arrow = "∨" if expanded else "›"
        self.console.print()
        self.console.print(f"{self.dot('running')} [italic dim]Thinking[/italic dim] [dim]{arrow}[/dim]")
    
    # ═══════════════════════════════════════════════════════════════
    # 工具调用
    # ═══════════════════════════════════════════════════════════════
    
    def tool_call(self, tool_name: str, description: str, input_text: str, output_text: str, status: str = "success"):
        """工具调用卡片"""
        self.console.print()
        self.console.print(f"{self.dot(status)} [bold]{tool_name}[/bold] [dim]{description}[/dim]")
        self.console.print()
        self.console.print(f"  [dim]IN[/dim]   [cyan]{input_text}[/cyan]")
        self.console.print()
        for line in output_text.split('\n'):
            self.console.print(f"  [dim]OUT[/dim]  {line}")
    
    def tool_simple(self, tool_name: str, description: str, result: str = None, status: str = "success"):
        """简单工具调用（无 IN/OUT）"""
        self.console.print()
        self.console.print(f"{self.dot(status)} [bold]{tool_name}[/bold] [dim]{description}[/dim]")
        if result:
            self.console.print(f"  [dim]{result}[/dim]")
    
    # ═══════════════════════════════════════════════════════════════
    # 表格
    # ═══════════════════════════════════════════════════════════════
    
    def table(self, headers: list, rows: list, title: str = None, status_col: int = None):
        """标准表格"""
        table = Table(
            title=f"[bold]{title}[/bold]" if title else None,
            box=box.SIMPLE_HEAD,
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
                    if "一致" in str(cell) or "✓" in str(cell) or cell == True:
                        formatted_row.append("[green]✓[/green] 一致")
                    elif "不一致" in str(cell) or "✗" in str(cell) or cell == False:
                        formatted_row.append("[red]✗[/red] 不一致")
                    else:
                        formatted_row.append(str(cell))
                else:
                    formatted_row.append(str(cell))
            table.add_row(*formatted_row)
        
        self.console.print()
        self.console.print(table)
    
    # ═══════════════════════════════════════════════════════════════
    # Todo 列表
    # ═══════════════════════════════════════════════════════════════
    
    def todo(self, items: list):
        """Todo 列表 - 带连线"""
        self.console.print()
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
            
            self.console.print(f"  {icon} [{text_style}]{text}[/{text_style}]")
            if not is_last:
                self.console.print(f"  [{line_color}]│[/{line_color}]")
    
    # ═══════════════════════════════════════════════════════════════
    # 消息输出
    # ═══════════════════════════════════════════════════════════════
    
    def success(self, text: str):
        """成功消息"""
        self.console.print(f"[green]✓[/green] [bold]{text}[/bold]")
    
    def error(self, text: str):
        """错误消息"""
        self.console.print(f"[red]✗[/red] [bold]{text}[/bold]")
    
    def warning(self, text: str):
        """警告消息"""
        self.console.print(f"[yellow]⚠[/yellow] [bold]{text}[/bold]")
    
    def info(self, text: str):
        """信息消息"""
        self.console.print(f"[blue]●[/blue] {text}")
    
    def title(self, text: str):
        """标题"""
        self.console.print()
        self.console.print(f"[bold]█ {text}[/bold]")
        self.console.print()
    
    def section(self, text: str, icon: str = ""):
        """章节标题"""
        self.console.print()
        self.console.print(f"[bold]{icon} {text}[/bold]" if icon else f"[bold]{text}[/bold]")
        self.console.print()
    
    def text(self, text: str, style: str = None):
        """普通文本"""
        if style:
            self.console.print(f"[{style}]{text}[/{style}]")
        else:
            self.console.print(text)
    
    def dim(self, text: str):
        """灰色文本"""
        self.console.print(f"[dim]{text}[/dim]")
    
    # ═══════════════════════════════════════════════════════════════
    # Diff 风格
    # ═══════════════════════════════════════════════════════════════
    
    def diff_add(self, text: str):
        """Diff 添加行"""
        self.console.print(f"[green]+ {text}[/green]")
    
    def diff_remove(self, text: str):
        """Diff 删除行"""
        self.console.print(f"[red]- {text}[/red]")
    
    def diff_context(self, text: str):
        """Diff 上下文行"""
        self.console.print(f"  [dim]{text}[/dim]")
    
    # ═══════════════════════════════════════════════════════════════
    # 流式输出
    # ═══════════════════════════════════════════════════════════════
    
    def stream(self, text: str, delay: float = 0.015):
        """流式打字效果"""
        for char in text:
            self.console.print(char, end="")
            time.sleep(delay)
        self.console.print()
    
    # ═══════════════════════════════════════════════════════════════
    # 工具方法
    # ═══════════════════════════════════════════════════════════════
    
    def clear(self):
        """清屏"""
        self.console.clear()
    
    def line(self):
        """空行"""
        self.console.print()
    
    def divider(self):
        """分隔线"""
        self.console.print("[dim]─" * 60 + "[/dim]")


# 全局实例
ui = ClaudeUI()


# ═══════════════════════════════════════════════════════════════
# 演示
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    ui.clear()
    
    # 思考中
    ui.thinking()
    
    # 工具调用
    ui.tool_simple("Glob", 'pattern: "**/*"', "Found 101 files")
    
    ui.tool_call(
        "Bash",
        "List directory",
        "ls -la ~/.claude/",
        "total 9840\ndrwxr-xr-x@  33 user  staff  1056 Jan 11 16:41 .\ndrwxr-x---+  75 user  staff  2400 Jan 11 16:40 .."
    )
    
    ui.tool_call(
        "mcp__filesystem__read",
        "读取配置文件",
        '{"path": "/Users/xxx/.claude"}',
        "Access denied - path outside allowed directories",
        status="error"
    )
    
    # 标题
    ui.title("CLAUDE.md 完整审核报告")
    
    # 成功消息
    ui.success("版本验证结果")
    
    # 表格
    ui.table(
        ["依赖", "CLAUDE.md 版本", "package.json 版本", "状态"],
        [
            ("Redux Toolkit", "2.0.0", "2.0.0", True),
            ("MUI", "5.18.0", "^5.18.0", True),
            ("Axios", "1.9.0", "^1.9.0", True),
        ],
        status_col=3
    )
    
    ui.line()
    ui.dim("所有依赖版本都是准确的。")
    
    # 警告
    ui.line()
    ui.warning("改进建议")
    
    ui.table(
        ["依赖", "版本", "建议添加的专家"],
        [
            ("SignalR", "^10.0.0", "实时通信专家"),
            ("Radix UI", "多个组件", "无障碍专家"),
        ]
    )
    
    # Diff 风格
    ui.section("流程优化建议", "3.")
    ui.diff_context("Step 6.5: 同步到 Obsidian [强制]")
    ui.diff_add("Step 6.6: 知识沉淀检查 [自动]")
    ui.diff_add("  - 检查是否有踩坑需要记录")
    
    # Todo 列表
    ui.section("任务进度", "📋")
    ui.todo([
        ("completed", "检查 package.json 依赖版本"),
        ("completed", "验证 CLAUDE.md 版本声明"),
        ("in_progress", "分析缺失的专家角色"),
        ("pending", "生成改进建议"),
    ])
    
    # 总结表格
    ui.section("总结", "📊")
    ui.table(
        ["评估项", "得分", "说明"],
        [
            ("结构完整性", "9/10", "流程清晰"),
            ("版本准确性", "10/10", "所有版本一致"),
            ("可执行性", "8/10", "脚本可用"),
        ]
    )
    
    ui.line()
    ui.dim("总评: 8.5/10 - 高质量配置文件")
    ui.line()
