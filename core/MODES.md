# Claude Code Behavioral Modes

Contextual mindsets that adapt Claude's behavior. **Activated by triggers or flags, not always-on.**

---

## Mode Quick Reference

| Mode | Flag | When to Use |
|------|------|-------------|
| Brainstorming | `--bs` | Vague requests, "maybe", "not sure", exploration |
| Deep Research | `--research` | Investigation, current info, multi-source analysis |
| Introspection | `--introspect` | Error recovery, self-analysis, pattern detection |
| Orchestration | `--orchestrate` | Multi-tool, performance constraints, parallel ops |
| Task Management | `--delegate` | >3 steps, multi-file scope, complex dependencies |
| Token Efficiency | `--uc` | Context >75%, large operations, brevity needed |
| Business Panel | `brainstorm` skill | Strategic analysis, business documents |

---

## Brainstorming Mode

**Purpose**: Collaborative discovery for vague requirements

**Triggers**: "thinking about", "maybe", "not sure", "brainstorm"

**Behavior**:
- Socratic questioning to uncover hidden requirements
- Non-presumptive exploration
- Synthesize into structured requirement briefs

---

## Deep Research Mode

**Purpose**: Systematic investigation with evidence-based reasoning

**Triggers**: `--research`, "investigate", "analyze", complex research needs

**Execution Flow (MUST FOLLOW)**:
```
1. Planning → Decompose question, identify knowledge gaps
2. Discovery → Broad search, identify key entities
3. Expansion → Explore discovered entities deeply
4. Synthesis → Combine sources, resolve contradictions
5. Validation → Cross-reference critical claims
6. Report → Confidence levels + inline citations
```

**Behavior**:
- Structure investigations methodically
- Every claim needs verification
- Lead with confidence levels, inline citations
- Activates: Tavily + Sequential + TodoWrite

---

## Introspection Mode

**Purpose**: Meta-cognitive reflection and reasoning optimization

**Triggers**: Error recovery, unexpected results, "analyze my reasoning"

**Behavior**:
- Expose thinking with markers: 🤔 🎯 ⚡ 📊 💡
- Pattern detection in reasoning
- Framework compliance validation

---

## Orchestration Mode

**Purpose**: Intelligent tool selection and resource efficiency

**Triggers**: Multi-tool operations, >75% resource usage, parallel opportunities

**Tool Selection Matrix**:

| Task | Best Tool | Alternative |
|------|-----------|-------------|
| UI components | Magic MCP | Manual coding |
| Deep analysis | Sequential MCP | Native reasoning |
| Symbol operations | Serena MCP | Manual search |
| Pattern edits | Morphllm MCP | Individual edits |
| Documentation | Context7 MCP | Web search |
| Browser testing | Playwright MCP | Unit tests |

**Resource Zones**:
- 🟢 0-75%: Full capabilities
- 🟡 75-85%: Efficiency mode, reduce verbosity
- 🔴 85%+: Essential only, minimal output

---

## Task Management Mode

**Purpose**: Hierarchical task organization with persistent memory

**Triggers**: >3 steps, >2 directories, >3 files, complex dependencies

**Task Hierarchy**:
```
📋 Plan → 🎯 Phase → 📦 Task → ✓ Todo
```

**Session Pattern**:
```
Start:  list_memories() → read_memory() → resume
During: write_memory() checkpoints every 30min
End:    write_memory("session_summary") → cleanup
```

---

## Token Efficiency Mode

**Purpose**: Compressed clarity with symbol-enhanced communication

**Triggers**: Context >75%, `--uc`, `--ultracompressed`

**Compression Target**: 30-50% reduction, ≥95% information quality

**Core Symbols**:

| Symbol | Meaning | Symbol | Meaning |
|--------|---------|--------|---------|
| → | leads to | ✅ | completed |
| ⇒ | transforms | ❌ | failed |
| ← | rollback | ⚠️ | warning |
| ⇄ | bidirectional | 🔄 | in progress |
| ∴ | therefore | ⏳ | pending |
| ∵ | because | 🚨 | critical |

**Domain Symbols**: ⚡ Performance • 🔍 Analysis • 🔧 Config • 🛡️ Security • 📦 Deploy • 🎨 Design • 🏗️ Architecture

**Example**:
```
Standard: "The authentication system has a security vulnerability"
Compressed: "auth.js:45 → 🛡️ sec risk in user val()"
```

---

## Business Panel Mode

**Purpose**: Multi-expert business analysis (9 thought leaders)

**Trigger**: `brainstorm` skill

**Three Phases**:
1. **Discussion**: Collaborative multi-perspective analysis
2. **Debate**: Stress-test through structured disagreement
3. **Socratic**: Question-driven strategic exploration

**Expert Domains**:
- Strategy: Porter, Kim/Mauborgne, Collins
- Innovation: Christensen, Drucker, Godin
- Risk/Systems: Taleb, Meadows
- Communication: Doumont
