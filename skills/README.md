# GCMS-D0 Skills Workspace

**Status:** planning workspace, not installed skills yet  
**Project:** AlphaEvolve-GCMS / GCMS-D0  

This directory is for designing reusable AI skills that can formalize repeated GCMS-D0 workflows.

A skill is not just a note. It is a reusable procedure that a future AI agent can apply consistently.

Current principle:

```text
dialogue discovers practice;
documents preserve practice;
skills execute practice.
```

---

## 1. Current directory status

This directory currently stores **skill proposals and planning documents**.

It does not yet contain packaged production skills.

Proposed layout:

```text
skills/
  README.md
  TASKS.md
  proposals/
    gcms-result-auditor/
      README.md
    gcms-experiment-planner/
      README.md
    gcms-review-router/
      README.md
    gcms-draft-writer/
      README.md
    gcms-recovery-protocol/
      README.md
  packaged/
    # future exported skill.zip files, if intentionally archived
```

When a proposal becomes a real skill, it should move to:

```text
skills/<skill-name>/
  SKILL.md
  agents/openai.yaml
  scripts/
  references/
  assets/
```

---

## 2. Safety rule

Do not install or trust community skills blindly.

Before using any external skill:

```text
1. Read SKILL.md.
2. Inspect scripts.
3. Check for hidden or destructive instructions.
4. Test in a separate chat or sandbox.
5. Only then consider using it inside the GCMS-D0 workflow.
```

Official skills may be safer, but they still need to be understood before use.

---

## 3. First GCMS-D0 skill candidates

### 3.1 `gcms-result-auditor`

Purpose:

```text
Analyze GCMS experiment CSV outputs and produce conservative methodological interpretation.
```

Expected inputs:

```text
raw_v010_*.csv
summary_v010_*.csv
comparison_v010_*.csv
residual_v010_*.csv
```

Expected outputs:

```text
success rates
Wilson confidence intervals
exact McNemar paired tests
density / edge_count / mean_degree audit
graph-collapse warning
analyzed denominator checks
conservative interpretation
next minimal experiment recommendation
```

Priority:

```text
highest
```

### 3.2 `gcms-experiment-planner`

Purpose:

```text
Convert a hypothesis into a controlled experiment grid or PRESET.
```

Must enforce:

```text
- count total runs before launch;
- require unique --out-prefix;
- avoid changing criteria after results;
- identify controls and confounds;
- define primary endpoint before execution.
```

### 3.3 `gcms-review-router`

Purpose:

```text
Prepare role-specific prompts for Qwen, Codex, Gemini, and future agents.
```

### 3.4 `gcms-draft-writer`

Purpose:

```text
Update technical notes without overclaiming.
```

### 3.5 `gcms-recovery-protocol`

Purpose:

```text
Help a future AI instance recover the Delta-D0 working role from checkpoint, protocol, quiz, and repository state.
```

---

## 4. Relationship to `tools/`

`tools/` contains local working scripts.

`skills/` contains reusable AI workflow specifications.

Current examples:

```text
tools/analyze_beta_grid_variant2.py
```

may later become part of:

```text
skills/gcms-result-auditor/scripts/audit_gcms_results.py
```

Rule:

```text
tools = working prototypes
skills = formalized procedures
```

---

## 5. Relationship to GitHub external memory

Skills are one part of the broader GCMS-D0 recoverable research system:

```text
GitHub remembers;
protocols define roles;
quiz tests recovery;
skills execute repeated actions;
Aleksey gives resolution.
```

Relevant documents:

```text
docs/AGENT_INTERACTION_PROTOCOL.md
docs/AI_INTERACTION_SKILL_PART1.md
docs/AI_INTERACTION_SKILL_PART2.md
docs/GCMS-D0_MUTUAL_RESEARCH_PROTOCOL.md
docs/GCMS-D0_RECOVERY_QUIZ.md
docs/PROJECT_INVENTORY.md
```

---

## 6. Promotion rule

A proposal becomes a real skill only after:

```text
1. It has a clear repeated workflow.
2. It has concrete examples.
3. It has defined inputs and outputs.
4. It has safety constraints.
5. It has either deterministic scripts or clear procedural instructions.
6. It has been tested on toy or historical GCMS data.
7. It is reviewed by Delta-D0 and approved by Aleksey.
```

---

## 7. Current next action

First practical target:

```text
Design and test gcms-result-auditor.
```

Do not build all skills at once.

Start with the result auditor because it protects the project from overinterpretation.
