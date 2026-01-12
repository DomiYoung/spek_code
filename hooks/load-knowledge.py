#!/usr/bin/env python3
"""
SessionStart Hook: 自动加载 Skills 知识库

功能：
1. 加载项目特定 Skills（按技术栈）
2. 输出相关踩坑提醒

兼容：Claude / Gemini / 其他模型
"""
import os
import sys
import json
from pathlib import Path

# ==================== 配置 ====================

SKILLS_BASE = Path.home() / ".claude" / "skills"

# 最大读取行数（避免过长）
MAX_LINES_PER_FILE = 50

# ==================== 核心逻辑 ====================

def get_current_project() -> str:
    """获取当前项目名称"""
    cwd = os.getcwd()
    git_dir = Path(cwd)
    while git_dir != git_dir.parent:
        if (git_dir / ".git").exists():
            return git_dir.name
        git_dir = git_dir.parent
    return Path(cwd).name

def detect_tech_stack(cwd: str) -> list[str]:
    """根据项目文件检测适用的技术栈"""
    techs = []
    cwd_path = Path(cwd)

    # 前端检测
    if (cwd_path / "package.json").exists():
        try:
            with open(cwd_path / "package.json") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "react" in deps:
                    techs.append("react")
                if "vue" in deps:
                    techs.append("vue")
                if "zustand" in deps:
                    techs.append("zustand")
                if "reactflow" in deps or "@xyflow/react" in deps:
                    techs.append("reactflow")
                if "@tanstack/react-query" in deps:
                    techs.append("react-query")
                if "@microsoft/signalr" in deps:
                    techs.append("signalr")
        except:
            pass

    # 后端检测
    if (cwd_path / "requirements.txt").exists() or (cwd_path / "pyproject.toml").exists():
        techs.append("python")

    return techs

def read_skill_pitfalls(skill_path: Path, max_lines: int = MAX_LINES_PER_FILE) -> str:
    """读取 SKILL.md 中的踩坑部分"""
    if not skill_path.exists():
        return ""

    try:
        with open(skill_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 提取反模式/踩坑部分
        lines = content.split("\n")
        pitfalls = []
        in_pitfall_section = False
        
        for line in lines:
            if "反模式" in line or "Anti-Pattern" in line or "踩坑" in line or "Pitfall" in line:
                in_pitfall_section = True
                pitfalls.append(line)
            elif in_pitfall_section:
                if line.startswith("## ") or line.startswith("# "):
                    break
                if line.strip():
                    pitfalls.append(line)
                if len(pitfalls) > max_lines:
                    break

        return "\n".join(pitfalls[:max_lines]) if pitfalls else ""
    except:
        return ""

def main():
    cwd = os.getcwd()
    project_name = get_current_project()
    techs = detect_tech_stack(cwd)

    output_parts = []

    # 加载对应技术的 Skills
    for tech in techs:
        skill_path = SKILLS_BASE / f"{tech}-patterns" / "SKILL.md"
        if skill_path.exists():
            summary = read_skill_pitfalls(skill_path)
            if summary:
                output_parts.append(f"🏷️ **{tech} 踩坑记录**:\n{summary[:500]}...")

    # 输出结果
    if output_parts:
        print(f"""
🧠 **Skills 知识库已加载**

当前项目: {project_name}
检测技术栈: {', '.join(techs) if techs else '无'}

{chr(10).join(output_parts)}

💡 提示: 开发时注意以上历史踩坑！
""")
    else:
        print(f"""
🧠 **Skills 知识库**

当前项目: {project_name}
检测技术栈: {', '.join(techs) if techs else '无'}

📭 暂无相关踩坑记录

💡 提示: 遇到问题后通过知识四问评估，写入对应 SKILL.md + Evolution Marker
""")

if __name__ == "__main__":
    main()
