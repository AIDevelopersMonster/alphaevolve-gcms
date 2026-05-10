# GCMS-D0 Skills Tasks

**Status:** working task list  
**Scope:** planned reusable AI skills for GCMS-D0  

This task list tracks the gradual formalization of GCMS-D0 workflows into skills.

Do not build all skills at once. Build the smallest useful skill first.

---

## Priority 1: `gcms-result-auditor`

### Goal

Create a skill that analyzes GCMS CSV outputs and returns conservative scientific interpretation.

### Why first

This skill protects the project from overclaiming.

It standardizes:

```text
confidence intervals
paired tests
density audit
graph-collapse warnings
analyzed denominator checks
next experiment recommendations
```

### Required inputs

At minimum:

```text
raw_*.csv
```

Optional:

```text
summary_*.csv
comparison_*.csv
residual_*.csv
```

### Required outputs

```text
1. Experiment identity.
2. Available columns.
3. Success-rate table by model_mode / relation_variant / beta.
4. Wilson CI for individual success rates.
5. Exact McNemar test for paired compensated/uncompensated seeds.
6. Effect size and confidence interval.
7. Density / edge_count / mean_degree audit.
8. Analyzed denominator warning.
9. Graph-collapse warning.
10. Conservative interpretation.
11. Recommended next experiment.
```

### Required safety rules

```text
- Do not claim physical theory.
- Do not change success criteria.
- Do not treat largest effect as best result if graph collapse is present.
- Prefer conservative wording.
- Warn if analyzed_runs are low or zero.
- Warn if paired seed comparison is impossible.
```

### Proposed files

```text
skills/gcms-result-auditor/
  SKILL.md
  agents/openai.yaml
  scripts/audit_gcms_results.py
  references/metrics.md
  references/interpretation_rules.md
```

### Source prototype

Current prototype scripts:

```text
tools/analyze_beta_grid_variant2.py
tools/analyze_focused_variant2.py
```

These should be generalized into:

```text
scripts/audit_gcms_results.py
```

### Test cases

Use historical outputs:

```text
outputs/raw_v010_focused_variant2.csv
outputs/raw_v010_beta_grid_variant2.csv
```

Expected findings:

```text
focused beta=0.05: strong effect but graph-collapse concern.
beta-grid beta=0.005: intermediate degradation, not pure collapse.
```

---

## Priority 2: `gcms-experiment-planner`

### Goal

Create a skill that converts scientific hypotheses into controlled experiment presets.

### Required behavior

```text
1. Ask what hypothesis is being tested.
2. Identify control conditions.
3. Estimate total runs before execution.
4. Require unique --out-prefix.
5. Identify confounds before launch.
6. Define primary endpoint before results.
7. Warn if grid is too large.
8. Output a PRESET block and run command.
```

### Safety rules

```text
- Do not change criteria after results.
- Do not propose huge sweeps when a focused grid is possible.
- Keep Variant 0 control when testing new relation variants.
```

---

## Priority 3: `gcms-review-router`

### Goal

Create a skill that prepares role-specific prompts for external agents.

### Agent roles

```text
Qwen -> skeptical review, CI, confounds, overclaiming.
Codex -> execution, syntax, smoke tests, schema checks.
Gemini -> generation of variants, not methodology authority.
```

### Required output

```text
A ready-to-copy prompt for the selected agent,
including allowed actions, forbidden actions, expected report format,
and project-specific context.
```

---

## Priority 4: `gcms-recovery-protocol`

### Goal

Create a skill for restarting GCMS-D0 in a new AI dialogue.

### Required behavior

```text
1. Ask for or locate checkpoint/protocol/quiz.
2. Summarize project state.
3. Answer or administer recovery quiz.
4. Identify current scientific task.
5. Warn against false identity claims.
6. Restore Delta-D0 as role, not subject.
```

### Must preserve

```text
Aleksey = resolution function.
Delta-D0 = preservation-oriented research role, not self-consciousness.
```

---

## Priority 5: `gcms-draft-writer`

### Goal

Create a skill for updating technical notes and drafts.

### Required behavior

```text
- Use toy-model language.
- Include limitations.
- Include Qwen objections.
- Separate main technical paper from dialogue-contour appendix.
- Update claims only after audit.
```

---

## Open questions

1. Should `gcms-result-auditor` be a standalone skill or remain as `tools/` first?
2. Should outputs include machine-readable JSON summary in addition to Markdown?
3. Should degree variance be added to future experiment raw output?
4. Should `tools/` scripts be unified before skill packaging?
5. Should skill artifacts include historical small CSV fixtures for tests?

---

## Next concrete task

Create a proposal folder for `gcms-result-auditor`:

```text
skills/proposals/gcms-result-auditor/README.md
```

Then decide whether to initialize the real skill using the skill-creator workflow.
