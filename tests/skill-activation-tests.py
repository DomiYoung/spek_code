#!/usr/bin/env python3
"""
Skill 激活机制测试套件
测试 description 语义匹配 + Hook 提醒机制
"""

import json
import subprocess
import sys
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent.parent
HOOKS_DIR = PROJECT_ROOT / "hooks"
SKILLS_DIR = PROJECT_ROOT / "skills"


class TestResult:
    def __init__(self, name: str, passed: bool, message: str = ""):
        self.name = name
        self.passed = passed
        self.message = message

    def __str__(self):
        status = "✅ PASS" if self.passed else "❌ FAIL"
        msg = f" - {self.message}" if self.message else ""
        return f"{status}: {self.name}{msg}"


def run_hook(hook_name: str, input_data: dict) -> tuple[int, str, str]:
    """运行 Hook 脚本并返回 (exit_code, stdout, stderr)"""
    hook_path = HOOKS_DIR / hook_name
    if not hook_path.exists():
        return -1, "", f"Hook not found: {hook_path}"
    
    try:
        result = subprocess.run(
            ["python3", str(hook_path)],
            input=json.dumps(input_data),
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", "Timeout"
    except Exception as e:
        return -1, "", str(e)


def test_skill_hint_hook():
    """测试 skill-hint.py Hook"""
    results = []
    
    # Test 1: 任务请求应该触发提醒
    code, stdout, stderr = run_hook("skill-hint.py", {
        "prompt": "帮我实现一个用户登录功能",
        "session_id": "test-123"
    })
    output = json.loads(stdout) if stdout else {}
    passed = (
        code == 0 and 
        "hookSpecificOutput" in output and
        "INSTRUCTION" in output.get("hookSpecificOutput", {}).get("additionalContext", "")
    )
    results.append(TestResult(
        "skill-hint: 任务请求触发提醒",
        passed,
        f"stdout: {stdout[:100]}..." if not passed else ""
    ))
    
    # Test 2: 简单确认不应触发
    code, stdout, stderr = run_hook("skill-hint.py", {
        "prompt": "好的",
        "session_id": "test-123"
    })
    output = json.loads(stdout) if stdout else {}
    passed = code == 0 and output == {}
    results.append(TestResult(
        "skill-hint: 简单确认不触发",
        passed,
        f"stdout: {stdout}" if not passed else ""
    ))
    
    # Test 3: 短输入不应触发
    code, stdout, stderr = run_hook("skill-hint.py", {
        "prompt": "继续",
        "session_id": "test-123"
    })
    output = json.loads(stdout) if stdout else {}
    passed = code == 0 and output == {}
    results.append(TestResult(
        "skill-hint: 短输入不触发",
        passed,
        f"stdout: {stdout}" if not passed else ""
    ))
    
    return results


def test_skill_evolution_hook():
    """测试 skill-evolution.py Hook"""
    results = []
    
    # Test 1: Stop 事件应该输出进化提醒
    code, stdout, stderr = run_hook("skill-evolution.py", {
        "hook_event_name": "Stop",
        "session_id": "test-123",
        "transcript_path": "/tmp/test.jsonl"
    })
    output = json.loads(stdout) if stdout else {}
    passed = (
        code == 0 and
        "hookSpecificOutput" in output and
        "Evolution" in output.get("hookSpecificOutput", {}).get("additionalContext", "")
    )
    results.append(TestResult(
        "skill-evolution: Stop 事件触发进化提醒",
        passed,
        f"stdout: {stdout[:100]}..." if not passed else ""
    ))
    
    return results


def test_skill_description_format():
    """测试 Skills 的 description 格式是否符合最佳实践"""
    results = []
    
    # 需要检查的核心 Skills
    core_skills = [
        "reactflow-patterns",
        "zustand-patterns", 
        "brainstorm",
        "workflow-orchestrator",
        "planning-with-files",
        "speckit.specify",
        "mermaid-expert",
        "experts/performance",
        "experts/architect",
        "signalr-patterns"
    ]
    
    for skill_name in core_skills:
        skill_path = SKILLS_DIR / skill_name / "SKILL.md"
        if not skill_path.exists():
            results.append(TestResult(
                f"description: {skill_name}",
                False,
                "SKILL.md not found"
            ))
            continue
        
        content = skill_path.read_text()
        
        # 检查是否有 description
        has_description = "description:" in content
        
        # 检查 description 是否包含 "Use when" 或触发词
        has_use_when = "Use when" in content or "触发" in content or "关键词" in content
        
        # 检查是否使用第三人称（不应该有 "I can" 或 "我可以"）
        uses_third_person = "I can" not in content and "我可以" not in content
        
        passed = has_description and has_use_when and uses_third_person
        message = []
        if not has_description:
            message.append("缺少 description")
        if not has_use_when:
            message.append("缺少 Use when/触发词")
        if not uses_third_person:
            message.append("应使用第三人称")
        
        results.append(TestResult(
            f"description: {skill_name}",
            passed,
            ", ".join(message) if message else ""
        ))
    
    return results


def test_skill_description_length():
    """测试 description 长度是否符合 ≤1024 字符限制"""
    results = []
    
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        skill_path = skill_dir / "SKILL.md"
        if not skill_path.exists():
            continue
        
        content = skill_path.read_text()
        
        # 提取 description（简化解析）
        import re
        match = re.search(r'description:\s*\|?\s*\n?((?:  .+\n?)+|.+)', content)
        if match:
            description = match.group(1).strip()
            length = len(description)
            passed = length <= 1024
            results.append(TestResult(
                f"length: {skill_dir.name}",
                passed,
                f"{length} chars" if not passed else ""
            ))
    
    return results


def test_hook_json_output_format():
    """测试 Hook 输出格式是否符合官方规范"""
    results = []
    
    # 测试 skill-hint.py 输出格式
    code, stdout, stderr = run_hook("skill-hint.py", {
        "prompt": "帮我创建一个 React 组件",
        "session_id": "test-123"
    })
    
    if stdout:
        try:
            output = json.loads(stdout)
            # 检查必需字段
            has_hook_output = "hookSpecificOutput" in output
            has_event_name = output.get("hookSpecificOutput", {}).get("hookEventName") == "UserPromptSubmit"
            has_context = "additionalContext" in output.get("hookSpecificOutput", {})
            
            passed = has_hook_output and has_event_name and has_context
            results.append(TestResult(
                "hook-format: skill-hint.py",
                passed,
                "Missing required fields" if not passed else ""
            ))
        except json.JSONDecodeError:
            results.append(TestResult(
                "hook-format: skill-hint.py",
                False,
                "Invalid JSON output"
            ))
    
    return results


def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 Skill 激活机制测试套件")
    print("=" * 60)
    print()
    
    all_results = []
    
    # 运行各测试组
    test_groups = [
        ("1. skill-hint.py Hook 测试", test_skill_hint_hook),
        ("2. skill-evolution.py Hook 测试", test_skill_evolution_hook),
        ("3. Skill description 格式测试", test_skill_description_format),
        ("4. Hook JSON 输出格式测试", test_hook_json_output_format),
    ]
    
    for group_name, test_func in test_groups:
        print(f"\n### {group_name}")
        print("-" * 40)
        try:
            results = test_func()
            all_results.extend(results)
            for r in results:
                print(r)
        except Exception as e:
            print(f"❌ 测试组执行失败: {e}")
    
    # 统计结果
    print()
    print("=" * 60)
    passed = sum(1 for r in all_results if r.passed)
    total = len(all_results)
    print(f"📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("✅ 所有测试通过！")
        return 0
    else:
        print("❌ 部分测试失败")
        return 1


if __name__ == "__main__":
    sys.exit(main())
