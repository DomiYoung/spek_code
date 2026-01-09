# Skill Definition Template (Strict Mode)

> **Instructions**: All new skills MUST follow this template. If sections are missing or generic, the skill will be rejected by the QA system.

## Skill Meta
- **Name**: [skill-name]
- **Type**: [Strict/Expert/Routing]
- **Version**: 1.0.0

---

### 1. 硬性约束 (Hard Constraints)
> ❌ **Blocker**: violates these rules -> Code Rejected.

| 维度 | 要求 | 自动审计规则 (Audit Regex/Script) |
|------|------|-----------------------------------|
| [Example: Type Safety] | [Must not use 'any'] | `grep -r ": any" src/` |
| [Dimension] | [Requirement] | [Validation Logic] |

### 2. 反模式 (Anti-Patterns)
> ⚠️ **Warning**: detects bad practices.

#### ❌ [Bad Pattern Name]
**Description**: [Why is this bad?]
**Detection**: [How do we see it?]
**Correction**: [What is the right way?]

### 3. 最佳实践 (Golden Paths)
> ✅ **Recommended**: The standard way to solve problems.

```[language]
// Standard implementation code
// Must be copy-pasteable
```

### 4. 自我验证 (Self-Verification)
> 🛡️ **Self-Audit**: The agent runs this BEFORE submitting code.

1.  [Check 1]
2.  [Check 2]
3.  [Check 3]

---

**QA Audit Checklist** (Do not remove):
- [ ] "Hard Constraints" contains specific rejection criteria?
- [ ] "Anti-Patterns" contains detection logic?
- [ ] No generic advice ("be careful", "make it fast")?
