#!/bin/bash
# setup-plan.sh - 初始化 plan.md 的脚本
# 用于 /speckit.plan 命令

set -e

JSON_OUTPUT=false
[[ "$1" == "--json" ]] && JSON_OUTPUT=true

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || pwd)
SPECIFY_DIR="$REPO_ROOT/.specify"
SPECS_DIR="$SPECIFY_DIR/specs"

# 查找当前功能目录
FEATURE_DIR=$(find "$SPECS_DIR" -mindepth 1 -maxdepth 1 -type d -exec stat -f '%m %N' {} \; 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2-)

if [[ -z "$FEATURE_DIR" ]]; then
    echo '{"error": "No feature directory found"}'
    exit 1
fi

FEATURE_SPEC="$FEATURE_DIR/spec.md"
IMPL_PLAN="$FEATURE_DIR/plan.md"
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")

# 如果 plan.md 不存在，从模板创建
if [[ ! -f "$IMPL_PLAN" ]]; then
    cat > "$IMPL_PLAN" << 'TEMPLATE'
# Implementation Plan

## Technical Context

| Aspect | Decision |
|--------|----------|
| Framework | NEEDS CLARIFICATION |
| Database | NEEDS CLARIFICATION |
| Auth | NEEDS CLARIFICATION |

## Constitution Check

- [ ] Principle 1: ...
- [ ] Principle 2: ...

## Phase 0: Research

See: research.md

## Phase 1: Design

### Data Model
See: data-model.md

### API Contracts
See: contracts/

## Quality Gates

- [ ] All NEEDS CLARIFICATION resolved
- [ ] Constitution principles satisfied
- [ ] Data model reviewed
- [ ] API contracts defined
TEMPLATE
fi

if [[ "$JSON_OUTPUT" == "true" ]]; then
    cat <<EOF
{
    "FEATURE_SPEC": "$FEATURE_SPEC",
    "IMPL_PLAN": "$IMPL_PLAN",
    "SPECS_DIR": "$SPECS_DIR",
    "BRANCH": "$BRANCH"
}
EOF
else
    echo "Feature spec: $FEATURE_SPEC"
    echo "Implementation plan: $IMPL_PLAN"
    echo "Branch: $BRANCH"
fi
