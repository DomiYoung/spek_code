# MCP Server Selection Guide

Quick reference for choosing the right MCP server. **Use the best tool for each task.**

---

## Server Quick Matrix

| Server | Purpose | Use For | NOT For |
|--------|---------|---------|---------|
| **Context7** | Library docs | Framework patterns, official APIs | Generic explanations |
| **Magic** | UI generation | Components, design systems | Backend logic |
| **Morphllm** | Pattern edits | Bulk transforms, style enforcement | Symbol operations |
| **Playwright** | Browser automation | E2E tests, visual validation | Static analysis |
| **Sequential** | Multi-step reasoning | Complex debugging, architecture | Simple tasks |
| **Serena** | Semantic code | Symbol ops, project memory | Text replacements |
| **Tavily** | Web search | Current info, research | Training knowledge |

---

## Context7

**Trigger Keywords**: `import`, `require`, React, Vue, Angular, Next.js

**Choose When**:
- Need official documentation patterns (not generic solutions)
- Version-specific implementation required
- Framework compliance mandatory

**Pairs With**: Sequential (analysis) → Context7 (patterns)

---

## Magic

**Trigger Keywords**: button, form, modal, card, `/ui`, `/21`, responsive, accessible

**Choose When**:
- UI component creation (production-ready, accessible)
- Design system consistency needed
- Modern framework best practices

**Pairs With**: Sequential (requirements) → Magic (implementation)

---

## Morphllm

**Trigger Keywords**: bulk edit, style enforcement, pattern replace, framework update

**Choose When**:
- Multi-file pattern transformations
- Style guide enforcement across codebase
- Token efficiency matters (30-50% savings)
- <10 files, straightforward transforms

**NOT For**: Symbol renames (use Serena), semantic operations

---

## Playwright

**Trigger Keywords**: E2E, browser test, screenshot, form validation, WCAG, accessibility

**Choose When**:
- Real browser interaction needed
- Visual testing, responsive validation
- User journey verification
- Accessibility compliance testing

**NOT For**: Static code review, logic validation

---

## Sequential

**Trigger Flags**: `--think`, `--think-hard`, `--ultrathink`

**Choose When**:
- 3+ interconnected components
- Root cause analysis, architecture review
- Cross-domain issues (frontend + backend + DB)
- Hypothesis testing required

**NOT For**: Simple explanations, single-file changes

**Execution Flow (MUST FOLLOW)**:
```
1. Problem Decomposition → Break into sub-problems
2. Hypothesis Formation → Generate 2-3 competing theories
3. Evidence Gathering → Collect supporting/contradicting data
4. Analysis → Evaluate each hypothesis against evidence
5. Synthesis → Integrate findings into coherent conclusion
6. Validation → Test conclusion against original problem
```

**Depth Levels**:
- `--think`: ~4K tokens, standard analysis
- `--think-hard`: ~10K tokens, deep with Context7
- `--ultrathink`: ~32K tokens, comprehensive with all MCP

---

## Serena

**Trigger Keywords**: rename symbol, find references, `list_memories`, `read_memory`, project memory

**Choose When**:
- Symbol operations with dependency tracking
- Session persistence needed
- Large codebase (>50 files)
- Multi-language LSP integration

**NOT For**: Pattern-based bulk edits (use Morphllm)

---

## Tavily

**Trigger Keywords**: research, current info, news, `--research`

**Choose When**:
- Information beyond knowledge cutoff
- Multi-source research investigation
- Fact-checking, verification needs

**Multi-Hop Research Flow (MUST FOLLOW)**:
```
Hop 1: Broad Search → Identify key entities
Hop 2: Entity Expansion → Explore discovered entities
Hop 3: Deep Dive → Targeted follow-up on gaps
Hop 4: Synthesis → Combine all sources, resolve contradictions
Hop 5: Validation → Cross-reference critical claims
```

**Source Credibility Tiers**:
- Tier 1 (0.9+): Academic, Government, Official docs
- Tier 2 (0.7-0.9): Established media, Industry reports
- Tier 3 (0.5-0.7): Community resources, Wikipedia
- Tier 4 (0.3-0.5): Forums, Social media

**Integration Pipeline**:
```
Tavily (search) → Sequential (analyze gaps) → Tavily (refine) → Sequential (synthesize) → Serena (store)
```

---

## Common Combinations

| Scenario | Pipeline |
|----------|----------|
| Debug complex issue | Sequential → Serena → Context7 |
| Build UI feature | Magic → Playwright (test) → Context7 (docs) |
| Refactor codebase | Serena (analyze) → Morphllm (transform) |
| Research topic | Tavily → Sequential → Serena (memory) |
| Implement with docs | Context7 → Sequential → Magic/Morphllm |
