#!/bin/bash
# ============================================
# Spek Code 部署脚本
# 将仓库配置通过符号链接部署到 ~/.claude/
# ============================================

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 获取脚本所在目录（仓库根目录）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$(dirname "$SCRIPT_DIR")"
TARGET_DIR="$HOME/.claude"

# 需要链接的配置目录/文件
CONFIG_ITEMS=(
    "CLAUDE.md"
    "AGENTS.md"
    "README.md"
    "core"
    "skills"
    "commands"
    "configs"
    "hooks"
    "rules"
    "templates"
    ".gitignore"
)

# 打印带颜色的消息
info() { echo -e "${BLUE}[INFO]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 显示帮助
show_help() {
    echo "Spek Code 部署脚本"
    echo ""
    echo "用法: $0 [选项]"
    echo ""
    echo "选项:"
    echo "  --install    安装/更新符号链接"
    echo "  --uninstall  移除符号链接"
    echo "  --status     检查当前状态"
    echo "  --backup     备份现有配置"
    echo "  --help       显示此帮助"
    echo ""
    echo "仓库位置: $REPO_DIR"
    echo "目标位置: $TARGET_DIR"
}

# 检查状态
check_status() {
    info "检查部署状态..."
    echo ""

    for item in "${CONFIG_ITEMS[@]}"; do
        target_path="$TARGET_DIR/$item"
        source_path="$REPO_DIR/$item"

        if [ -L "$target_path" ]; then
            link_target=$(readlink "$target_path")
            if [ "$link_target" = "$source_path" ]; then
                echo -e "  ${GREEN}✓${NC} $item → 已链接"
            else
                echo -e "  ${YELLOW}⚠${NC} $item → 链接到其他位置: $link_target"
            fi
        elif [ -e "$target_path" ]; then
            echo -e "  ${YELLOW}⚠${NC} $item → 存在（非链接）"
        else
            echo -e "  ${RED}✗${NC} $item → 不存在"
        fi
    done

    echo ""
    info "第三方扩展状态:"
    for ext in "anthropic-skills" "happy-claude-skills" "plugins"; do
        if [ -d "$TARGET_DIR/$ext" ]; then
            echo -e "  ${BLUE}◆${NC} $ext → 存在"
        fi
    done
}

# 备份现有配置
backup_existing() {
    local backup_dir="$TARGET_DIR/backups/pre-deploy-$(date +%Y%m%d-%H%M%S)"
    info "备份现有配置到: $backup_dir"

    mkdir -p "$backup_dir"

    for item in "${CONFIG_ITEMS[@]}"; do
        target_path="$TARGET_DIR/$item"
        if [ -e "$target_path" ] && [ ! -L "$target_path" ]; then
            cp -r "$target_path" "$backup_dir/"
            success "  已备份: $item"
        fi
    done

    success "备份完成"
}

# 安装符号链接
install_links() {
    info "开始部署 (符号链接模式)..."
    echo ""
    info "仓库: $REPO_DIR"
    info "目标: $TARGET_DIR"
    echo ""

    # 确保目标目录存在
    mkdir -p "$TARGET_DIR"

    for item in "${CONFIG_ITEMS[@]}"; do
        source_path="$REPO_DIR/$item"
        target_path="$TARGET_DIR/$item"

        # 检查源文件是否存在
        if [ ! -e "$source_path" ]; then
            warn "跳过不存在的文件: $item"
            continue
        fi

        # 如果目标已存在
        if [ -e "$target_path" ] || [ -L "$target_path" ]; then
            if [ -L "$target_path" ]; then
                # 已经是符号链接，先删除
                rm "$target_path"
            else
                # 是真实文件/目录，备份后删除
                warn "$item 已存在，移动到备份..."
                mkdir -p "$TARGET_DIR/backups/replaced"
                mv "$target_path" "$TARGET_DIR/backups/replaced/$item.$(date +%s)"
            fi
        fi

        # 创建符号链接
        ln -s "$source_path" "$target_path"
        success "已链接: $item"
    done

    echo ""
    success "部署完成！"
    echo ""
    info "提示: 修改仓库文件将立即生效"
    info "仓库位置: $REPO_DIR"
}

# 卸载符号链接
uninstall_links() {
    info "移除符号链接..."
    echo ""

    for item in "${CONFIG_ITEMS[@]}"; do
        target_path="$TARGET_DIR/$item"

        if [ -L "$target_path" ]; then
            rm "$target_path"
            success "已移除: $item"
        elif [ -e "$target_path" ]; then
            warn "跳过非链接: $item"
        fi
    done

    echo ""
    success "卸载完成"
    warn "注意: ~/.claude 现在没有配置文件，Claude Code 可能无法正常工作"
}

# 主逻辑
case "${1:-}" in
    --install)
        install_links
        ;;
    --uninstall)
        uninstall_links
        ;;
    --status)
        check_status
        ;;
    --backup)
        backup_existing
        ;;
    --help|"")
        show_help
        ;;
    *)
        error "未知选项: $1"
        show_help
        exit 1
        ;;
esac
