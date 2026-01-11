---
name: speckit.taskstoissues
description: |
  任务转 Issue 工具 - Spec-Kit GitHub 集成。
  Use when:
  - 将 tasks.md 转为 GitHub Issues
  - 创建 Issue 并设置依赖
  触发词：issues、GitHub Issue、创建 issue
  Related Skills: speckit.tasks, smart-commit
globs:
  - ".specify/**/*"
  - "**/tasks.md"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --require-tasks --include-tasks` from repo root and parse FEATURE_DIR and AVAILABLE_DOCS list. All paths must be absolute.

2. From the executed script, extract the path to **tasks**.

3. Get the Git remote by running:

```bash
git config --get remote.origin.url
```

> [!CAUTION]
> ONLY PROCEED TO NEXT STEPS IF THE REMOTE IS A GITHUB URL

4. For each task in the list, use the GitHub MCP server to create a new issue in the repository that is representative of the Git remote.

> [!CAUTION]
> UNDER NO CIRCUMSTANCES EVER CREATE ISSUES IN REPOSITORIES THAT DO NOT MATCH THE REMOTE URL
