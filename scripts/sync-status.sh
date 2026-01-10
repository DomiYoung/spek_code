#!/bin/bash
# ============================================
# 检查 Claude 配置同步状态
# ============================================

DOTFILES_CLAUDE="$HOME/dotfiles/claude"
CLAUDE_HOME="$HOME/.claude"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo "========================================"
echo "  Claude Code 配置同步状态"
echo "========================================"
echo ""

# 检查软链接状态
echo "📁 软链接状态:"
for item in CLAUDE.md AGENTS.md core skills commands configs hooks rules templates; do
    if [ -L "$CLAUDE_HOME/$item" ]; then
        target=$(readlink "$CLAUDE_HOME/$item")
        echo -e "  ${GREEN}✓${NC} $item -> $target"
    elif [ -e "$CLAUDE_HOME/$item" ]; then
        echo -e "  ${YELLOW}⚠${NC} $item (非软链接)"
    else
        echo -e "  ${RED}✗${NC} $item (不存在)"
    fi
done

echo ""

# Git 状态
echo "📊 Git 状态:"
cd "$DOTFILES_CLAUDE"
if [ -d .git ]; then
    CHANGES=$(git status --porcelain | wc -l | tr -d ' ')
    BRANCH=$(git branch --show-current)

    echo "  分支: $BRANCH"
    echo "  未提交变更: $CHANGES 个文件"

    if [ "$CHANGES" -gt 0 ]; then
        echo ""
        echo "  变更文件:"
        git status --porcelain | head -10 | sed 's/^/    /'
        if [ "$CHANGES" -gt 10 ]; then
            echo "    ... 还有 $((CHANGES - 10)) 个文件"
        fi
    fi

    # 检查是否需要 push
    AHEAD=$(git rev-list --count @{upstream}..HEAD 2>/dev/null || echo "0")
    if [ "$AHEAD" -gt 0 ]; then
        echo ""
        echo -e "  ${YELLOW}⚠${NC} 有 $AHEAD 个提交未推送到远程"
    fi
else
    echo -e "  ${RED}✗${NC} 不是 Git 仓库"
fi

echo ""
