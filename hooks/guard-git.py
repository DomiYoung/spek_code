#!/usr/bin/env python3
"""Git 约束门禁 Hook（全局）

目标：让 Claude Code 在所有项目里执行 git commit / git push 时，必须遵循统一约束。

策略：
1) 在 PreToolUse 阶段拦截 Bash 命令
2) 若命令包含 git commit / git push，则进行校验
3) 不通过则阻断，并给出可执行的修复指令

注意：该 Hook 只影响 Claude Code 的工具调用，不修改 git 全局配置。
"""

import json
import os
import re
import subprocess
import sys


FIXED_AUTHOR = "YOUR_USERNAME <YOUR_USERNAME@gmail.com>"

SKIP_KEYWORDS = [
    "/skip-git-guard",
    "skip-git-guard",
    "跳过git门禁",
    "跳过 git 门禁",
]


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        out = subprocess.check_output(cmd, stderr=subprocess.STDOUT, text=True)
        return 0, out.strip()
    except subprocess.CalledProcessError as e:
        return e.returncode, (e.output or "").strip()


def _in_git_repo() -> bool:
    code, _ = _run(["git", "rev-parse", "--is-inside-work-tree"])
    return code == 0


def _has_skip_keyword(data: dict) -> bool:
    tool_input = data.get("tool_input", {})
    if isinstance(tool_input, dict):
        for _, v in tool_input.items():
            if isinstance(v, str):
                lowered = v.lower()
                for kw in SKIP_KEYWORDS:
                    if kw.lower() in lowered:
                        return True

    session_id = str(data.get("session_id", ""))
    for kw in SKIP_KEYWORDS:
        if kw.lower() in session_id.lower():
            return True

    return False


def _block(payload: dict):
    print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
    sys.exit(2)


def _validate_conventional_subject(subject: str) -> tuple[bool, str]:
    m = re.match(r"^(feat|fix|refactor|perf|style|docs|chore|test)(\([^\)]+\))?:\s+(.+)$", subject)
    if not m:
        return False, "标题必须符合 <type>(<scope>): <中文用户价值描述>"

    desc = m.group(3) or ""
    if not re.search(r"[\u4e00-\u9fff]", desc):
        return False, "标题描述必须包含中文（type/scope 除外）"

    return True, ""


def _validate_message(message: str) -> list[str]:
    errors: list[str] = []
    msg = message.strip("\n")

    if not msg.strip():
        return ["commit message 不能为空"]

    lines = msg.splitlines()
    subject = ""
    for line in lines:
        if line.strip():
            subject = line.strip()
            break

    ok, reason = _validate_conventional_subject(subject)
    if not ok:
        errors.append(reason)

    required = ["核心改动", "影响范围", "技术背景", "相关文件"]
    for section in required:
        if not re.search(rf"(^|\n)\s*-?\s*{re.escape(section)}[:：]", msg):
            errors.append(f"正文必须包含「{section}：」字段")

    banned = [
        r"\bai\b",
        r"\bagent\b",
        r"\bclaude\b",
        r"\bbot\b",
        r"\banthropic\b",
        r"\bsonnet\b",
        r"\bopus\b",
        r"\bhaiku\b",
        r"\bgpt\b",
        r"\bchatgpt\b",
        r"\bcopilot\b",
        r"\bgenerated\b",
        r"\bco-authored-by\b",
    ]
    for pat in banned:
        if re.search(pat, msg, re.IGNORECASE):
            errors.append(f"包含禁止词：{pat}")
    if "🤖" in msg:
        errors.append("包含禁止标记：🤖")

    return errors


def _check_last_commit() -> list[str]:
    # author
    _, author = _run(["git", "log", "-1", "--pretty=format:%an <%ae>"])
    if FIXED_AUTHOR not in author:
        return [f"最近一次提交 Author 必须是 {FIXED_AUTHOR}，当前为：{author}"]

    # message
    _, message = _run(["git", "log", "-1", "--pretty=format:%B"])
    return _validate_message(message)


def main():
    raw = sys.stdin.read()
    if not raw.strip():
        sys.exit(0)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        sys.exit(0)

    if _has_skip_keyword(data):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    if tool_name != "Bash":
        sys.exit(0)

    tool_input = data.get("tool_input", {})
    command = ""
    if isinstance(tool_input, dict):
        command = str(tool_input.get("command", "") or tool_input.get("cmd", ""))

    if not command:
        sys.exit(0)

    # 只处理 git commit / push
    lowered = command.lower()
    is_commit = re.search(r"(^|\s|&&|;)git\s+commit\b", lowered) is not None
    is_push = re.search(r"(^|\s|&&|;)git\s+push\b", lowered) is not None

    if not (is_commit or is_push):
        sys.exit(0)

    if not _in_git_repo():
        sys.exit(0)

    if re.search(r"(^|\s)(-f|--force)\b", lowered):
        _block({
            "error": "🛑 禁止 force push（默认）",
            "reason": "force push 可能破坏远端历史",
            "resolution": [
                "如确需 force push，请在命令中添加 /skip-git-guard 并确保你理解风险。"
            ],
        })

    if is_push:
        # 工作区必须干净
        _, status = _run(["git", "status", "--porcelain"])
        if status.strip():
            _block({
                "error": "🛑 推送前工作区必须干净",
                "reason": "存在未提交变更，容易造成版本不可追溯",
                "resolution": [
                    "先提交或暂存变更后再 push",
                    "或将 push 拆分为更小的可回滚提交",
                ],
                "details": status.splitlines()[:50],
            })

        errors = _check_last_commit()
        if errors:
            _block({
                "error": "🛑 最近一次提交不符合全局提交规范",
                "reason": "为保证跨项目一致性，push 前必须满足统一 commit 规范",
                "violations": errors,
                "resolution": [
                    f"修复 Author：git commit --amend --author=\"{FIXED_AUTHOR}\"",
                    "修复 message：git commit --amend",
                    "修复后再执行：git push",
                ],
            })

        sys.exit(0)

    # git commit：只强制 author（message 在 push 时强校验，避免解析 shell quoting）
    if is_commit:
        if FIXED_AUTHOR not in command:
            _block({
                "error": "🛑 git commit 必须使用固定 Author",
                "reason": f"跨项目血缘追踪依赖 Author 一致性：{FIXED_AUTHOR}",
                "resolution": [
                    f"请使用：git commit ... --author=\"{FIXED_AUTHOR}\"",
                    "或在提交后修复：git commit --amend --author=\"YOUR_USERNAME <YOUR_USERNAME@gmail.com>\"",
                ],
            })

        sys.exit(0)


if __name__ == "__main__":
    main()
