---
name: speckit.clarify
description: |
  需求澄清工具 - Spec-Kit 质量保障。
  Use when:
  - spec.md 有模糊/遗漏的地方
  - 需要向用户提问澄清需求
  触发词：clarify、澄清、不清楚、确认需求
  Related Skills: speckit.specify, speckit.analyze, brainstorm
globs:
  - ".specify/**/*"
  - "**/spec.md"
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Outline

Goal: Detect and reduce ambiguity or missing decision points in the active feature specification and record the clarifications directly in the spec file.

Note: This clarification workflow is expected to run (and be completed) BEFORE invoking `/speckit.plan`. If the user explicitly states they are skipping clarification (e.g., exploratory spike), you may proceed, but must warn that downstream rework risk increases.

Execution steps:

1. Run `.specify/scripts/bash/check-prerequisites.sh --json --paths-only` from repo root **once**. Parse minimal JSON payload fields:
   - `FEATURE_DIR`
   - `FEATURE_SPEC`

2. Load the current spec file. Perform a structured ambiguity & coverage scan using this taxonomy. For each category, mark status: Clear / Partial / Missing.

   **Taxonomy Categories:**
   - Functional Scope & Behavior
   - Domain & Data Model
   - Interaction & UX Flow
   - Non-Functional Quality Attributes
   - Integration & External Dependencies
   - Edge Cases & Failure Handling
   - Constraints & Tradeoffs
   - Terminology & Consistency
   - Completion Signals

3. Generate (internally) a prioritized queue of candidate clarification questions (maximum 5). Apply these constraints:
   - Maximum of 10 total questions across the whole session.
   - Each question must be answerable with EITHER:
     - A short multiple-choice selection (2–5 distinct, mutually exclusive options), OR
     - A one-word / short-phrase answer (explicitly constrain: "Answer in <=5 words").
   - Only include questions whose answers materially impact architecture, data modeling, task decomposition, test design, UX behavior, operational readiness, or compliance validation.

4. Sequential questioning loop (interactive):
   - Present EXACTLY ONE question at a time.
   - For multiple-choice questions:
     - **Analyze all options** and determine the **most suitable option**
     - Present your **recommended option prominently** at the top
     - Format as: `**Recommended:** Option [X] - <reasoning>`
     - Then render all options as a Markdown table
   - After the user answers:
     - Validate the answer maps to one option or fits the <=5 word constraint
     - Record it in working memory and move to the next queued question
   - Stop asking further questions when:
     - All critical ambiguities resolved early, OR
     - User signals completion ("done", "good", "no more"), OR
     - You reach 5 asked questions

5. Integration after EACH accepted answer (incremental update approach):
   - Ensure a `## Clarifications` section exists
   - Under it, create `### Session YYYY-MM-DD` subheading for today
   - Append a bullet line: `- Q: <question> → A: <final answer>`
   - Apply the clarification to the most appropriate section(s)
   - Save the spec file AFTER each integration

6. Validation (performed after EACH write plus final pass):
   - Clarifications session contains exactly one bullet per accepted answer
   - Total asked questions ≤ 5
   - Updated sections contain no lingering vague placeholders
   - Markdown structure valid

7. Write the updated spec back to `FEATURE_SPEC`.

8. Report completion:
   - Number of questions asked & answered
   - Path to updated spec
   - Sections touched
   - Coverage summary table
   - Suggested next command

Behavior rules:
- If no meaningful ambiguities found, respond: "No critical ambiguities detected worth formal clarification."
- If spec file missing, instruct user to run `/speckit.specify` first
- Never exceed 5 total asked questions
- Respect user early termination signals ("stop", "done", "proceed")
