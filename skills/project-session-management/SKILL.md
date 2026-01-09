---
name: project-session-management
description: "Cross-session state tracking with SESSION.md and git checkpoints. Converts IMPLEMENTATION_PHASES.md into trackable session state with phase status, progress markers, and recovery points. Auto-triggers on: 'start project tracking', 'resume work', 'show progress', 'continue project', '项目进度', '恢复工作'."
---

# Project Session Management Skill

**Purpose**: Track progress across work sessions using SESSION.md with git checkpoints and concrete next actions. Converts IMPLEMENTATION_PHASES.md into trackable session state with phase status, progress markers, and recovery points.

**Use when**: Starting projects after planning phase, resuming work after context clears, managing multi-phase implementations, or troubleshooting lost progress tracking.

---

## Core Concepts

**Phases** (IMPLEMENTATION_PHASES.md): Units of work with verification criteria, may span multiple sessions

**Sessions** (SESSION.md): Units of context that complete before clearing/compacting

**Stages**: Implementation → Verification → Debugging cycle within each phase

---

## Workflow

### Starting New Project
1. After planning creates IMPLEMENTATION_PHASES.md, offer SESSION.md creation
2. Generate SESSION.md with Phase 1 as 🔄, others as ⏸️
3. Set concrete "Next Action" with file, line, and specific task

### Ending Session
- Automated: `/wrap-session` - updates docs, creates checkpoint, outputs summary
- Manual: Update SESSION.md → git checkpoint → set next action

### Resuming
- Automated: `/continue-session` - loads context, shows summary, continues from next action
- Manual: Read SESSION.md → check next action → continue

---

## SESSION.md Structure

Target: <200 lines in project root

```markdown
# Session State

**Current Phase**: Phase 3
**Current Stage**: Implementation
**Last Checkpoint**: abc1234 (2025-10-23)
**Planning Docs**: `docs/IMPLEMENTATION_PHASES.md`

## Phase 1: Setup ✅
**Completed**: 2025-10-15 | **Checkpoint**: abc1234

## Phase 3: Tasks API 🔄
**Progress**:
- [x] GET endpoint
- [ ] PATCH endpoint ← **CURRENT**

**Next Action**: Implement PATCH /api/tasks/:id in src/routes/tasks.ts:47

**Key Files**: src/routes/tasks.ts
```

---

## Status Icons

- ⏸️ Not started
- 🔄 In progress
- ✅ Complete
- 🚫 Blocked

---

## Git Checkpoint Format

```
checkpoint: Phase [N] [Status] - [Brief Description]

Phase: [N] - [Name]
Status: [Complete/In Progress/Paused]
Session: [What was accomplished]

Files Changed:
- path/to/file.ts (what changed)

Next: [Concrete next action]
```

---

## Expected Uncommitted Files

**Normal (no warning)**:
- SESSION.md - Updated post-commit with checkpoint hash
- CLAUDE.md - Development notes
- .roomodes - Editor state

**Warning triggers**: Source files, configs, planning docs, new untracked files

---

## Guidelines

✅ DO: Collapse completed phases, concrete next actions, reference planning docs, checkpoint at phase boundaries

❌ DON'T: Copy code, duplicate IMPLEMENTATION_PHASES.md, vague actions, exceed 200 lines
