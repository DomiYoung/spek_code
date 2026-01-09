#!/usr/bin/env python3
"""
SessionStart Hook: 自动加载 KI 知识库

功能：
1. 加载全局通用知识 (~/.ai-knowledge/global/)
2. 加载领域知识 (~/.ai-knowledge/domains/)
3. 加载项目特定知识 (~/.ai-knowledge/projects/{project}/)
4. 输出相关踩坑提醒

兼容：Claude / Gemini / 其他模型
"""
import os
import sys
import json
from pathlib import Path

# ==================== 配置 ====================

AI_KNOWLEDGE_BASE = Path.home() / ".ai-knowledge"
GLOBAL_DIR = AI_KNOWLEDGE_BASE / "global"
DOMAINS_DIR = AI_KNOWLEDGE_BASE / "domains"
PROJECTS_DIR = AI_KNOWLEDGE_BASE / "projects"

# 最大读取行数（避免过长）
MAX_LINES_PER_FILE = 50

# ==================== 核心逻辑 ====================

def get_current_project() -> str:
    """获取当前项目名称"""
    cwd = os.getcwd()
    # 尝试从 .git 目录获取项目名
    git_dir = Path(cwd)
    while git_dir != git_dir.parent:
        if (git_dir / ".git").exists():
            return git_dir.name
        git_dir = git_dir.parent
    # 回退到当前目录名
    return Path(cwd).name

def detect_domains(cwd: str) -> list[str]:
    """根据项目文件检测适用的领域"""
    domains = []
    cwd_path = Path(cwd)

    # 前端检测
    if (cwd_path / "package.json").exists():
        try:
            with open(cwd_path / "package.json") as f:
                pkg = json.load(f)
                deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
                if "react" in deps or "vue" in deps or "angular" in deps:
                    domains.append("frontend")
        except:
            pass

    # 后端检测
    if (cwd_path / "requirements.txt").exists() or \
       (cwd_path / "pyproject.toml").exists() or \
       (cwd_path / "go.mod").exists():
        domains.append("backend")

    # DevOps 检测
    if (cwd_path / "Dockerfile").exists() or \
       (cwd_path / "docker-compose.yml").exists() or \
       (cwd_path / ".github" / "workflows").exists():
        domains.append("devops")

    return domains

def read_pitfalls_summary(file_path: Path, max_lines: int = MAX_LINES_PER_FILE) -> str:
    """读取 pitfalls 文件的摘要"""
    if not file_path.exists():
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # 提取标题行（### 开头的行）
        summaries = []
        for line in lines:
            if line.startswith("### ["):
                summaries.append(line.strip())

        return "\n".join(summaries[:10])  # 最多返回 10 条
    except:
        return ""

def main():
    cwd = os.getcwd()
    project_name = get_current_project()
    domains = detect_domains(cwd)

    output_parts = []

    # 1. 全局知识
    global_pitfalls = GLOBAL_DIR / "pitfalls.md"
    if global_pitfalls.exists():
        summary = read_pitfalls_summary(global_pitfalls)
        if summary:
            output_parts.append(f"📚 **全局踩坑记录** ({global_pitfalls}):\n{summary}")

    # 2. 领域知识
    for domain in domains:
        domain_pitfalls = DOMAINS_DIR / domain / "pitfalls.md"
        if domain_pitfalls.exists():
            summary = read_pitfalls_summary(domain_pitfalls)
            if summary:
                output_parts.append(f"🏷️ **{domain} 领域踩坑** ({domain_pitfalls}):\n{summary}")

    # 3. 项目知识
    project_pitfalls = PROJECTS_DIR / project_name / "pitfalls.md"
    if project_pitfalls.exists():
        summary = read_pitfalls_summary(project_pitfalls)
        if summary:
            output_parts.append(f"📁 **项目踩坑记录** ({project_pitfalls}):\n{summary}")

    # 输出结果
    if output_parts:
        print(f"""
🧠 **KI 知识库已加载**

当前项目: {project_name}
检测领域: {', '.join(domains) if domains else '无'}

{chr(10).join(output_parts)}

💡 提示: 开发时注意以上历史踩坑！
""")
    else:
        print(f"""
🧠 **KI 知识库**

当前项目: {project_name}
检测领域: {', '.join(domains) if domains else '无'}

📭 暂无相关踩坑记录

💡 提示: 遇到问题后会自动沉淀到知识库
""")

if __name__ == "__main__":
    main()
