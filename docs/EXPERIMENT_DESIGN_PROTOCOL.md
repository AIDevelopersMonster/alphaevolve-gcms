# GCMS-D0 Experiment Design Protocol

**Status:** working protocol  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Purpose:** prevent ad hoc modeling by requiring every proposed experiment to define verification, data, metrics, and interpretation criteria before execution.

---

## 1. Core rule

No serious experiment should be launched only because an idea is interesting.

Before modeling, the project must know:

```text
1. What hypothesis is being tested?
2. What data will be produced?
3. Which metrics will be evaluated?
4. What result would count as good?
5. What result would count as bad, null, or confounded?
6. What document or protocol defines these criteria?
```

Short form:

```text
hypothesis -> data -> metrics -> thresholds -> confounds -> interpretation
```

---

## 2. Proposal status levels

Not every idea should immediately become code.

Use these levels:

### Level 0: Reflection

A conceptual idea or intuition.

Allowed output:

```text
notes, diagrams, questions, possible directions
```

Not allowed:

```text
code changes, experiment launch, strong claims
```

### Level 1: Research proposal

A structured proposal with hypothesis, expected data, metrics, and risks.

Allowed output:

```text
proposal document, review prompt, planned metrics
```

Not allowed:

```text
running large experiments before criteria are fixed
```

### Level 2: Experiment design

A concrete preset/grid with fixed endpoints and output schema.

Allowed output:

```text
PRESET proposal, run-count estimate, command plan
```

Required before execution:

```text
review by Delta-D0 and explicit Aleksey resolution
```

### Level 3: Execution

The experiment is run.

Allowed output:

```text
raw/summary/comparison/residual CSV files, logs
```

Rules:

```text
Do not change criteria during or after execution.
Do not interpret before outputs are validated.
```

### Level 4: Audit

Results are analyzed using deterministic tools.

Allowed output:

```text
audit tables, CI, McNemar tests, density checks, plots
```

### Level 5: Interpretation

Only after audit.

Allowed output:

```text
conservative result note in docs/results
Qwen review prompt
next experiment recommendation
```

---

## 3. Required experiment proposal template

Every non-trivial experiment proposal should use this template:

```text
Title:
Status: reflection / proposal / design / execution / audit / interpretation

Hypothesis:
What would support it:
What would weaken or falsify it:

Model change:
Control condition:
Primary endpoint:
Secondary metrics:
Expected output files:

Run grid:
Estimated total runs:
Estimated runtime:

Confounds:
Failure modes:
Collapse criteria:

Good result:
Bad/null result:
Ambiguous result:

Analysis method:
Reviewer task:
Document basis:
Next action:
```

---

## 4. Required data definition

Before running, define expected outputs.

For GCMS v0.10+ experiments, default outputs are:

```text
outputs/raw_<prefix>.csv
outputs/summary_<prefix>.csv
outputs/comparison_<prefix>.csv
outputs/residual_<prefix>.csv
```

Minimum raw columns expected:

```text
model_mode
relation_variant
beta
lambda_val
epsilon_norm
seed
structure_success
strict_success
compensation_valid
analyzed
edge_count
density
sector_size
lifetime
dp_valid
p_gnp_empirical
p_dp_empirical
```

If future experiments require new metrics, define them before running.

Examples:

```text
mean_degree
degree_variance
failure_reason
component_count
largest_component_size
```

---

## 5. Required metrics

Default metrics for compensation-sensitive GCMS experiments:

```text
structure_success_rate_attempted
structure_success_rate_analyzed
strict_success_rate_attempted
strict_success_rate_analyzed
compensation_effect_attempted
compensation_effect_analyzed
Wilson CI for individual rates
paired exact McNemar test when seeds are paired
density
edge_count
mean_degree
sector_size
lifetime
dp_valid
analyzed_runs
failure-mode counts
```

Do not interpret effect size without density and analyzed-denominator checks.

---

## 6. What counts as good, bad, or ambiguous

### Good result

A good result supports the hypothesis while avoiding obvious confounds.

For the current Variant 2 beta refinement, a good result would be:

```text
positive compensation_effect_attempted;
paired evidence supports compensated > uncompensated;
uncompensated mode remains analyzable;
edge_count and sector_size do not collapse to near zero;
lifetime remains substantial;
density/degree audit does not explain the effect as pure sparsification;
result is stable around neighboring beta values.
```

### Bad or null result

A bad/null result includes:

```text
no reliable compensation effect;
confidence intervals include zero widely;
paired discordance is balanced;
Variant 0 behaves similarly to Variant 2;
results depend entirely on one seed cluster;
```

### Confounded result

A confounded result may show a large effect but is not clean.

Examples:

```text
uncompensated graph collapses to near-zero edges;
analyzed_runs are too low;
sector_size is near zero;
mean lifetime is too short;
metrics were changed after seeing results;
output columns are missing or inconsistent.
```

### Ambiguous result

A result is ambiguous if:

```text
effect is positive but weak;
density/degree changes may explain the effect;
neighboring beta values are unstable;
CI is wide;
more seeds are needed;
reviewer objections remain unresolved.
```

---

## 7. Controls

Controls must be defined before interpretation.

For GCMS-D0 current work:

```text
Variant 0 = distance-only control.
```

Expected behavior:

```text
Variant 0 should show little or no compensation effect because distance-only relations are translation-invariant under mean subtraction.
```

If a new relation variant is introduced, include a control unless the proposal explicitly justifies why not.

---

## 8. Confound checklist

Before accepting a result, check:

```text
1. Is the effect driven by graph collapse?
2. Are analyzed denominators high enough?
3. Are paired seeds used correctly?
4. Are generated CSVs uncommitted unless intentionally archived?
5. Are output columns present and consistent?
6. Did criteria change after results?
7. Does the result survive a nearby parameter sweep?
8. Does Qwen or another reviewer see an unresolved objection?
```

---

## 9. Agent use in experiment design

Agent roles:

```text
Delta-D0: proposal framing, methodology, interpretation.
Codex: execution, syntax, schema validation, local checks.
Qwen: skeptical review, confounds, conservative wording.
Gemini: variant generation only, not criteria authority.
Skills: repeatable procedures after they are validated.
```

No agent should change primary endpoints after seeing results.

---

## 10. Current application: fine beta-grid

Current experiment:

```text
fine_beta_v010
```

Hypothesis:

```text
Variant 2 has a non-collapse compensation-sensitive transition near beta ~= 0.005.
```

Run grid:

```text
relation_variant = 2
model_modes = compensated, uncompensated
beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008
seeds = 100
baseline_count = 100
```

Primary endpoint:

```text
compensation_effect_attempted = structure_success_rate_attempted(compensated) - structure_success_rate_attempted(uncompensated)
```

Required audit:

```text
paired seed table
exact McNemar test
Wilson CI
edge_count
density
mean_degree
sector_size
lifetime
dp_valid
analyzed_runs
collapse warnings
```

Good outcome:

```text
Find the weakest beta where compensation_effect is reliably positive while uncompensated worlds remain analyzable and non-collapsed.
```

Bad outcome:

```text
No beta in the 0.003-0.008 range shows a reliable positive effect without collapse/confound.
```

Ambiguous outcome:

```text
Positive effect exists but is sensitive to beta, unstable across seeds, or explainable by sector-size/density changes.
```

---

## 11. Proposal discipline

Delta-D0 may propose future ideas, but proposals must be labeled.

Required label examples:

```text
Reflection only.
Candidate proposal.
Ready for design.
Ready for Codex validation.
Ready for execution.
Ready for Qwen review.
```

If the label is missing, the idea is not ready for action.

---

## 12. Core principle

A model is not an experiment until verification is defined.

A result is not a claim until confounds are audited.

A tool is not a method until its role is documented.

Short form:

```text
Before we model, define how we will know whether the model taught us anything.
```
