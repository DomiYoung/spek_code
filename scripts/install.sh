#!/bin/bash
# ============================================
# Claude Code 配置安装脚本
# 用于多设备同步配置
# ============================================

set -e

DOTFILES_CLAUDE="$HOME/dotfiles/claude"
CLAUDE_HOME="$HOME/.claude"

# 颜色
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 需要软链接的文件/目录
SYMLINK_ITEMS=(
    "CLAUDE.md"
    "AGENTS.md"
    "README.md"
    ".gitignore"
    "core"
    "skills"
    "commands"
    "configs"
    "hooks"
    "rules"
    "templates"
)

# 可选同步的目录
OPTIONAL_ITEMS=(
    "settings.json"
)

create_symlink() {
    local src="$1"
    local dest="$2"

    if [ -L "$dest" ]; then
        log_warn "软链接已存在: $dest"
        return 0
    fi

    if [ -e "$dest" ]; then
        log_warn "备份现有文件: $dest -> $dest.bak"
        mv "$dest" "$dest.bak"
    fi

    ln -s "$src" "$dest"
    log_info "创建软链接: $dest -> $src"
}

main() {
    echo "========================================"
    echo "  Claude Code 配置安装"
    echo "========================================"
    echo ""

    # 检查 dotfiles 仓库
    if [ ! -d "$DOTFILES_CLAUDE" ]; then
        log_error "未找到 dotfiles 仓库: $DOTFILES_CLAUDE"
        echo "请先克隆仓库:"
        echo "  git clone <your-repo> ~/dotfiles/claude"
        exit 1
    fi

    # 确保 ~/.claude 目录存在
    mkdir -p "$CLAUDE_HOME"

    # 创建核心软链接
    log_info "创建核心配置软链接..."
    for item in "${SYMLINK_ITEMS[@]}"; do
        if [ -e "$DOTFILES_CLAUDE/$item" ]; then
            create_symlink "$DOTFILES_CLAUDE/$item" "$CLAUDE_HOME/$item"
        else
            log_warn "源文件不存在: $DOTFILES_CLAUDE/$item"
        fi
    done

    # 可选项
    echo ""
    read -p "是否同步 settings.json? (y/n): " sync_settings
    if [ "$sync_settings" = "y" ]; then
        if [ -e "$DOTFILES_CLAUDE/settings.json" ]; then
            create_symlink "$DOTFILES_CLAUDE/settings.json" "$CLAUDE_HOME/settings.json"
        fi
    fi

    echo ""
    log_info "安装完成！"
    echo ""
    echo "已同步的配置:"
    ls -la "$CLAUDE_HOME" | grep "^l" | awk '{print "  " $9 " -> " $11}'
    echo ""
    echo "提示:"
    echo "  - 修改 ~/.claude/ 或 ~/dotfiles/claude/ 效果相同"
    echo "  - 记得定期 git push 同步到远程"
}

main "$@"
