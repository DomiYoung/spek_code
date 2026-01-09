#!/usr/bin/env python3
"""
全局工作流强制约束 Hook

功能：
1. 代码编写前检查 spec.md 是否存在
2. 检测模糊需求，建议先 brainstorm
3. 验证文件路径规范
4. [NEW] 检查工作流阶段是否完成（权重评估、Task Master、Phase 标记）

触发时机：PreToolUse (Edit/Write/MultiEdit)

工作流状态文件：.workflow-state.json
{
  "weight": 5,                    # 任务权重
  "weight_assessed": true,        # 权重评估已完成
  "task_created": true,           # Task Master 已创建
  "phase1_completed": true,       # Phase 1 分析已完成
  "phase2_completed": false       # Phase 2 设计已完成
}
"""
import sys
import json
import os
import re

# ==================== 配置 ====================

# 代码文件扩展名
CODE_EXTENSIONS = [".ts", ".tsx", ".js", ".jsx", ".py", ".go", ".rs", ".java", ".kt"]

# 豁免路径模式（这些路径不需要 spec）
EXEMPT_PATHS = [
    r"\.specify/",           # Spec-Kit 目录本身
    r"\.claude/",            # Claude 配置
    r"docs/",                # 文档目录
    r"\.md$",                # Markdown 文件
    r"\.json$",              # JSON 配置
    r"\.yaml$",              # YAML 配置
    r"\.yml$",               # YAML 配置
    r"test.*\.py$",          # 测试文件
    r".*\.test\.(ts|tsx|js|jsx)$",  # 测试文件
    r".*\.spec\.(ts|tsx|js|jsx)$",  # 测试文件
    r"__tests__/",           # 测试目录
    r"scripts/",             # 脚本目录
    r"hooks/",               # Hooks 目录
]

# 豁免关键词（用户输入包含这些词时跳过检查）
EXEMPT_KEYWORDS = [
    "跳过检查", "skip-check", "skip check",
    "紧急修复", "hotfix", "quick fix",
    "调试", "debug", "测试", "test",
]

# 工作流状态文件名
WORKFLOW_STATE_FILE = ".workflow-state.json"

# 权重阈值配置
WEIGHT_THRESHOLDS = {
    "task_required": 3,      # 权重 >= 3 需要 Task Master
    "phase1_required": 5,    # 权重 >= 5 需要 Phase 1
    "phase2_required": 7,    # 权重 >= 7 需要 Phase 2
}

# ==================== 核心逻辑 ====================

def is_code_file(file_path: str) -> bool:
    """判断是否为代码文件"""
    return any(file_path.endswith(ext) for ext in CODE_EXTENSIONS)

def is_exempt_path(file_path: str) -> bool:
    """判断是否为豁免路径"""
    for pattern in EXEMPT_PATHS:
        if re.search(pattern, file_path):
            return True
    return False

def has_exempt_keyword(context: str) -> bool:
    """检查是否包含豁免关键词"""
    context_lower = context.lower()
    return any(kw.lower() in context_lower for kw in EXEMPT_KEYWORDS)

def find_project_root(start_path: str) -> str:
    """向上查找项目根目录（包含 .git 或 package.json 的目录）"""
    current = os.path.dirname(os.path.abspath(start_path))
    while current != "/":
        if os.path.exists(os.path.join(current, ".git")) or \
           os.path.exists(os.path.join(current, "package.json")) or \
           os.path.exists(os.path.join(current, "pyproject.toml")):
            return current
        current = os.path.dirname(current)
    return os.getcwd()

def check_spec_exists(project_root: str) -> tuple[bool, str]:
    """检查项目是否有 spec.md 文件"""
    spec_dir = os.path.join(project_root, ".specify", "specs")

    # 如果 .specify 目录不存在
    if not os.path.exists(spec_dir):
        return False, "未找到 .specify/specs/ 目录"

    # 检查是否有任何 spec.md 文件
    for root, dirs, files in os.walk(spec_dir):
        for f in files:
            if f == "spec.md":
                return True, os.path.join(root, f)

    return False, "未找到任何 spec.md 文件"


# ==================== 工作流阶段检查 (NEW) ====================

def load_workflow_state(project_root: str) -> dict:
    """
    加载工作流状态文件

    Returns:
        状态字典，如果文件不存在返回空字典（视为权重 0）
    """
    state_file = os.path.join(project_root, WORKFLOW_STATE_FILE)

    if not os.path.exists(state_file):
        return {}

    try:
        with open(state_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}


def check_workflow_phase(project_root: str) -> tuple[bool, list[str]]:
    """
    检查工作流阶段是否完成

    根据权重判断需要完成哪些阶段：
    - 权重 >= 3: 需要 Task Master 创建
    - 权重 >= 5: 需要 Phase 1 分析完成
    - 权重 >= 7: 需要 Phase 1 + Phase 2 完成

    Returns:
        (passed, missing_steps): 是否通过，缺失的步骤列表
    """
    state = load_workflow_state(project_root)

    # 如果没有状态文件，视为权重 0（简单问答），直接通过
    if not state:
        return True, []

    weight = state.get("weight", 0)
    missing = []

    # 检查权重评估
    if not state.get("weight_assessed", False):
        missing.append("权重评估 (weight_assessed)")

    # 检查 Task Master（权重 >= 3）
    if weight >= WEIGHT_THRESHOLDS["task_required"]:
        if not state.get("task_created", False):
            missing.append(f"Task Master 创建 (权重 {weight} >= {WEIGHT_THRESHOLDS['task_required']})")

    # 检查 Phase 1（权重 >= 5）
    if weight >= WEIGHT_THRESHOLDS["phase1_required"]:
        if not state.get("phase1_completed", False):
            missing.append(f"Phase 1 分析 (权重 {weight} >= {WEIGHT_THRESHOLDS['phase1_required']})")

    # 检查 Phase 2（权重 >= 7）
    if weight >= WEIGHT_THRESHOLDS["phase2_required"]:
        if not state.get("phase2_completed", False):
            missing.append(f"Phase 2 设计 (权重 {weight} >= {WEIGHT_THRESHOLDS['phase2_required']})")

    return len(missing) == 0, missing


def create_workflow_state(project_root: str, weight: int) -> None:
    """
    创建初始工作流状态文件（供 Claude 调用）

    Usage in Claude response:
        创建状态: echo '{"weight": 5, "weight_assessed": true}' > .workflow-state.json
    """
    state_file = os.path.join(project_root, WORKFLOW_STATE_FILE)
    initial_state = {
        "weight": weight,
        "weight_assessed": True,
        "task_created": False,
        "phase1_completed": False,
        "phase2_completed": False,
    }
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(initial_state, f, indent=2, ensure_ascii=False)

def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)
        input_data = json.loads(raw)
    except Exception:
        # 无法解析输入，放行
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    # 只检查文件操作工具
    if tool_name not in ["Write", "Edit", "MultiEdit"]:
        sys.exit(0)

    # 获取文件路径（支持 MultiEdit 多文件遍历）
    file_paths = []
    if tool_name == "MultiEdit":
        edits = tool_input.get("edits", [])
        for edit in edits:
            fp = edit.get("file_path", "")
            if fp:
                file_paths.append(fp)
    else:
        fp = tool_input.get("file_path", "")
        if fp:
            file_paths.append(fp)

    if not file_paths:
        sys.exit(0)

    # 检查所有代码文件是否需要 spec
    for file_path in file_paths:
        # 检查是否为代码文件
        if not is_code_file(file_path):
            continue

        # 检查是否为豁免路径
        if is_exempt_path(file_path):
            continue

        # 查找项目根目录
        project_root = find_project_root(file_path)

        # 检查 1: spec 是否存在
        spec_exists, spec_info = check_spec_exists(project_root)

        if not spec_exists:
            error_msg = {
                "error": "🚫 Spec-Kit 约束触发：代码编写前必须存在 spec.md",
                "reason": spec_info,
                "resolution": [
                    "1. 运行 /speckit.specify 创建需求规范",
                    "2. 或在项目根目录创建 .specify/specs/{feature}/spec.md",
                    "3. 紧急场景可在请求中包含 skip-check / hotfix / 跳过检查",
                ],
                "target": file_path,
                "projectRoot": project_root,
            }
            print(json.dumps(error_msg, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)

        # 检查 2: 工作流阶段是否完成 (NEW)
        phase_passed, missing_steps = check_workflow_phase(project_root)

        if not phase_passed:
            error_msg = {
                "error": "🚫 工作流阶段检查未通过",
                "missing_steps": missing_steps,
                "resolution": [
                    "1. 完成权重评估并输出: ⚖️ 权重: X | ...",
                    "2. 创建 .workflow-state.json 文件记录状态",
                    "3. 按权重完成对应阶段（Task Master / Phase 1 / Phase 2）",
                    "4. 或使用 '跳过检查' 临时豁免",
                ],
                "how_to_update": "echo '{\"weight\": 5, \"weight_assessed\": true, \"task_created\": true, \"phase1_completed\": true}' > .workflow-state.json",
                "target": file_path,
                "projectRoot": project_root,
            }
            print(json.dumps(error_msg, ensure_ascii=False, indent=2), file=sys.stderr)
            sys.exit(2)

    # 所有检查通过
    sys.exit(0)

if __name__ == "__main__":
    main()
