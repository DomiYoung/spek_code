#!/bin/bash
# Skill Compliance Test Suite v1.1
# 测试 Skills 是否符合官方模板规范

SKILLS_DIR="${HOME}/.claude/skills"
PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║         Skill Compliance Test Suite v1.1                     ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

test_skill_compliance() {
    local file="$1"
    local skill_name=$(basename "$(dirname "$file")")
    local score=0
    local max_score=100
    local issues=()

    echo -e "${BLUE}Testing: ${NC}$skill_name"

    # Test 1: YAML Frontmatter (10 points)
    if grep -q "^---" "$file" && grep -q "^name:" "$file"; then
        ((score+=10))
    else
        issues+=("缺少 YAML frontmatter")
    fi

    # Test 2: Section 1 - Hard Constraints (25 points)
    if grep -qE "^## 1\. 硬性约束|^### 1\. 硬性约束|Hard Constraints" "$file"; then
        ((score+=15))
        if grep -qE "^\|.*\|.*审计" "$file" || grep -qE "^\|.*\|.*Audit" "$file"; then
            ((score+=10))
        else
            issues+=("硬性约束缺少审计规则表格")
        fi
    else
        issues+=("缺少 Section 1: 硬性约束")
    fi

    # Test 3: Section 2 - Anti-Patterns (25 points)
    if grep -qE "^## 2\. 反模式|^### 2\. 反模式|Anti-Patterns" "$file"; then
        ((score+=15))
        if grep -qE "\*\*检测\*\*:|\*\*Detection\*\*:|检测.*:" "$file"; then
            ((score+=10))
        else
            issues+=("反模式缺少检测逻辑")
        fi
    else
        issues+=("缺少 Section 2: 反模式")
    fi

    # Test 4: Section 3 - Golden Paths (25 points)
    if grep -qE "^## 3\. 最佳实践|^### 3\. 最佳实践|Golden Paths" "$file"; then
        ((score+=15))
        if grep -q '```' "$file"; then
            ((score+=10))
        else
            issues+=("最佳实践缺少代码示例")
        fi
    else
        issues+=("缺少 Section 3: 最佳实践")
    fi

    # Test 5: Section 4 - Self-Verification (15 points)
    if grep -qE "^## 4\. 自我验证|^### 4\. 自我验证|Self-Verification" "$file"; then
        ((score+=15))
    else
        issues+=("缺少 Section 4: 自我验证")
    fi

    # Test 6: QA Audit Checklist (10 points)  
    if grep -qE "QA Audit Checklist" "$file"; then
        ((score+=10))
    else
        issues+=("缺少 QA Audit Checklist")
    fi

    # 输出结果
    if [ $score -ge 70 ]; then
        echo -e "  ${GREEN}✅ PASS${NC} - Score: ${score}/${max_score}"
        ((PASS_COUNT++))
    elif [ $score -ge 50 ]; then
        echo -e "  ${YELLOW}⚠️ WARN${NC} - Score: ${score}/${max_score}"
        ((WARN_COUNT++))
    else
        echo -e "  ${RED}❌ FAIL${NC} - Score: ${score}/${max_score}"
        ((FAIL_COUNT++))
    fi

    if [ ${#issues[@]} -gt 0 ]; then
        for issue in "${issues[@]}"; do
            echo -e "     ${YELLOW}→ ${issue}${NC}"
        done
    fi
    echo ""
}

echo -e "${BLUE}Phase 1: Testing Updated Skills${NC}"
echo "─────────────────────────────────────────────────────────────"

UPDATED_SKILLS=(
    "${SKILLS_DIR}/zustand-patterns/SKILL.md"
    "${SKILLS_DIR}/react-query-patterns/SKILL.md"
    "${SKILLS_DIR}/code-quality-gates/SKILL.md"
    "${SKILLS_DIR}/review-quality-gates/SKILL.md"
    "${SKILLS_DIR}/experts/frontend/SKILL.md"
    "${SKILLS_DIR}/experts/backend/SKILL.md"
    "${SKILLS_DIR}/experts/product/SKILL.md"
    "${SKILLS_DIR}/experts/database/SKILL.md"
    "${SKILLS_DIR}/experts/quality/SKILL.md"
    "${SKILLS_DIR}/experts/performance/SKILL.md"
)

for skill in "${UPDATED_SKILLS[@]}"; do
    if [ -f "$skill" ]; then
        test_skill_compliance "$skill"
    else
        echo -e "${YELLOW}⚠️ File not found: $skill${NC}"
        echo ""
    fi
done

echo "═══════════════════════════════════════════════════════════════"
echo -e "${BLUE}Test Summary${NC}"
echo "─────────────────────────────────────────────────────────────"
echo -e "  ${GREEN}Passed: ${PASS_COUNT}${NC}"
echo -e "  ${YELLOW}Warnings: ${WARN_COUNT}${NC}"
echo -e "  ${RED}Failed: ${FAIL_COUNT}${NC}"
echo ""

TOTAL=$((PASS_COUNT + WARN_COUNT + FAIL_COUNT))
if [ $TOTAL -gt 0 ]; then
    PASS_RATE=$((PASS_COUNT * 100 / TOTAL))
    echo -e "Pass Rate: ${PASS_RATE}%"
fi

echo ""
if [ $FAIL_COUNT -eq 0 ]; then
    echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║              ✅ ALL TESTS PASSED                             ║${NC}"
    echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 0
else
    echo -e "${RED}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${RED}║              ❌ SOME TESTS FAILED                            ║${NC}"
    echo -e "${RED}╚══════════════════════════════════════════════════════════════╝${NC}"
    exit 1
fi
