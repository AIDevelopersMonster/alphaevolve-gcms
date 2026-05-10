# Skill Proposal: gcms-result-auditor

**Status:** proposal / not packaged yet  
**Priority:** 1  
**Purpose:** formalize the repeated GCMS result-auditing workflow into a reusable AI skill.

---

## 1. Problem

GCMS-D0 experiments produce CSV outputs such as:

```text
raw_*.csv
summary_*.csv
comparison_*.csv
residual_*.csv
```

Interpreting these outputs requires repeated checks:

```text
success rates
confidence intervals
paired-seed tests
density audit
edge-count audit
mean-degree audit
analyzed denominator warnings
graph-collapse detection
conservative wording
next experiment recommendation
```

Doing this manually each time increases the risk of:

```text
- overclaiming;
- missing graph collapse;
- ignoring denominator problems;
- treating the largest effect as the best effect;
- forgetting paired-seed structure;
- writing results before checking confounds.
```

---

## 2. Skill goal

`gcms-result-auditor` should analyze GCMS CSV outputs and produce a conservative technical audit.

It should not replace scientific judgment.

It should make the minimum responsible interpretation easier and more repeatable.

---

## 3. Expected trigger conditions

The future skill should activate when the user asks to:

```text
- analyze GCMS CSV outputs;
- summarize raw/summary/comparison/residual files;
- check whether a compensation effect is meaningful;
- compute CI or McNemar tests;
- check graph collapse;
- compare compensated vs uncompensated modes;
- prepare result text for docs/results.
```

---

## 4. Expected inputs

Minimum:

```text
raw_*.csv
```

Optional:

```text
summary_*.csv
comparison_*.csv
residual_*.csv
```

Required columns if available:

```text
model_mode
relation_variant
beta
seed
structure_success
strict_success
analyzed
edge_count
density
sector_size
lifetime
dp_valid
p_gnp_empirical
p_dp_empirical
```

If columns are missing, the skill must report what it could not compute.

---

## 5. Expected outputs

The audit should include:

```text
1. Files inspected.
2. Columns detected.
3. Grouped success-rate summary.
4. Wilson CI for individual success rates.
5. Exact McNemar test for paired compensated/uncompensated seeds.
6. Effect size and uncertainty.
7. Density and edge-count audit.
8. Mean-degree audit.
9. Analyzed denominator warning.
10. Graph-collapse warning.
11. Conservative interpretation.
12. Recommended next experiment.
```

---

## 6. Interpretation rules

### Rule 1: do not overclaim

Never say:

```text
This proves a physical theory.
```

Prefer:

```text
This supports a preliminary toy-model mechanism.
```

### Rule 2: largest effect is not automatically best

A large compensation effect may be less informative if the uncompensated graph collapsed.

Example:

```text
beta=0.05 may show large effect but strong sparsification.
beta=0.005 may be scientifically cleaner if the graph remains analyzable.
```

### Rule 3: denominator warnings are mandatory

If analyzed runs are low or zero, report it clearly.

Do not compute analyzed-rate effects with zero denominator.

### Rule 4: paired seeds matter

If compensated and uncompensated runs share seeds, use paired comparison.

Report:

```text
both_success
comp_only
uncomp_only
both_fail
exact McNemar p-value
```

### Rule 5: collapse warning

Warn if uncompensated mode shows:

```text
very low edge_count
very low sector_size
very low lifetime
very low analyzed_runs
zero or near-zero density
```

---

## 7. Prototype source

Current prototype scripts:

```text
tools/analyze_focused_variant2.py
tools/analyze_beta_grid_variant2.py
```

These should be generalized into:

```text
skills/gcms-result-auditor/scripts/audit_gcms_results.py
```

---

## 8. Proposed real skill layout

```text
skills/gcms-result-auditor/
  SKILL.md
  agents/openai.yaml
  scripts/audit_gcms_results.py
  references/metrics.md
  references/interpretation_rules.md
  references/report_template.md
```

---

## 9. Test cases

Historical test cases:

```text
outputs/raw_v010_focused_variant2.csv
outputs/raw_v010_beta_grid_variant2.csv
```

Expected audit findings:

### Focused Variant 2

```text
beta=0.05 shows large effect but graph-collapse concern.
beta=0.5 is effectively a collapse/sparsification regime.
```

### Beta-grid Variant 2

```text
beta=0.000-0.002 behaves close to distance-only.
beta=0.005 shows intermediate compensation-sensitive degradation.
beta=0.01-0.05 enters sparsification/collapse regime.
```

---

## 10. First implementation task

Before creating the real skill:

```text
1. Move or copy prototype logic into a generalized audit script.
2. Make the script accept input paths as arguments.
3. Make it detect available columns.
4. Make it output Markdown.
5. Test it on historical beta-grid and focused outputs.
6. Only then package as a skill.
```

---

## 11. Human responsibility

The skill should not decide publication readiness alone.

Aleksey remains the resolution function.

Delta-D0 remains responsible for methodological continuity and conservative interpretation.

The skill supplies standardized evidence.
