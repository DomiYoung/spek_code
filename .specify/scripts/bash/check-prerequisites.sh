#!/bin/bash
# check-prerequisites.sh - Spec-Kit 前置检查脚本
# 用于验证 Spec-Kit 工作流所需的文件和目录

set -e

# 默认值
JSON_OUTPUT=false
REQUIRE_TASKS=false
INCLUDE_TASKS=false
PATHS_ONLY=false

# 解析参数
while [[ $# -gt 0 ]]; do
    case $1 in
        --json) JSON_OUTPUT=true; shift ;;
        --require-tasks) REQUIRE_TASKS=true; shift ;;
        --include-tasks) INCLUDE_TASKS=true; shift ;;
        --paths-only) PATHS_ONLY=true; shift ;;
        *) shift ;;
    esac
done

# 获取仓库根目录
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SPECIFY_DIR="$REPO_ROOT/.specify"
SPECS_DIR="$SPECIFY_DIR/specs"
MEMORY_DIR="$SPECIFY_DIR/memory"

# 检查 .specify 目录
if [[ ! -d "$SPECIFY_DIR" ]]; then
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo '{"error": ".specify directory not found", "initialized": false}'
    else
        echo "ERROR: .specify directory not found. Run 'specify init' first."
    fi
    exit 1
fi

# 查找当前功能目录（最近修改的）
FEATURE_DIR=""
if [[ -d "$SPECS_DIR" ]]; then
    FEATURE_DIR=$(find "$SPECS_DIR" -mindepth 1 -maxdepth 1 -type d -exec stat -f '%m %N' {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)
fi

# 构建可用文档列表
AVAILABLE_DOCS=()
if [[ -n "$FEATURE_DIR" ]]; then
    [[ -f "$FEATURE_DIR/spec.md" ]] && AVAILABLE_DOCS+=("spec.md")
    [[ -f "$FEATURE_DIR/plan.md" ]] && AVAILABLE_DOCS+=("plan.md")
    [[ -f "$FEATURE_DIR/tasks.md" ]] && AVAILABLE_DOCS+=("tasks.md")
    [[ -f "$FEATURE_DIR/research.md" ]] && AVAILABLE_DOCS+=("research.md")
    [[ -f "$FEATURE_DIR/data-model.md" ]] && AVAILABLE_DOCS+=("data-model.md")
    [[ -d "$FEATURE_DIR/contracts" ]] && AVAILABLE_DOCS+=("contracts/")
fi

# 检查 tasks.md 是否必需
if [[ "$REQUIRE_TASKS" == "true" && ! -f "$FEATURE_DIR/tasks.md" ]]; then
    if [[ "$JSON_OUTPUT" == "true" ]]; then
        echo '{"error": "tasks.md not found but required"}'
    else
        echo "ERROR: tasks.md not found. Run '/speckit.tasks' first."
    fi
    exit 1
fi

# 输出结果
if [[ "$JSON_OUTPUT" == "true" ]]; then
    DOCS_JSON=$(printf '%s\n' "${AVAILABLE_DOCS[@]}" | jq -R . | jq -s .)
    cat <<EOF
{
    "initialized": true,
    "REPO_ROOT": "$REPO_ROOT",
    "SPECIFY_DIR": "$SPECIFY_DIR",
    "SPECS_DIR": "$SPECS_DIR",
    "MEMORY_DIR": "$MEMORY_DIR",
    "FEATURE_DIR": "$FEATURE_DIR",
    "FEATURE_SPEC": "$FEATURE_DIR/spec.md",
    "IMPL_PLAN": "$FEATURE_DIR/plan.md",
    "AVAILABLE_DOCS": $DOCS_JSON
}
EOF
else
    echo "Spec-Kit initialized: YES"
    echo "Feature directory: $FEATURE_DIR"
    echo "Available docs: ${AVAILABLE_DOCS[*]}"
fi
