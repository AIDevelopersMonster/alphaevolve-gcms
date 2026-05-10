# Design Checkpoint: confirm_connectivity_variant2

**Status:** ready for pre-run validation / not yet executed  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `confirm_connectivity_variant2`  
**Relation variant:** Variant 2 compensation-alignment relation  
**Related result note:** `docs/results/v010_fine_beta_variant2.md`  
**Related Qwen result review:** `docs/reviews/v010_fine_beta_qwen_result_review.md`  
**Related protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Experiment script:** `experiments/ae_v010_2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This checkpoint defines the next confirmatory experiment before execution.

The previous fine beta-grid showed strong exploratory support for a compensation-sensitive transition in Variant 2.

However, Qwen review blocked stronger interpretation because the previous run lacked:

```text
largest_component_fraction
n_components
degree_variance / degree_gini
failure-mode taxonomy
density/edge-matched ablation
```

This experiment addresses the first three blockers directly and partially addresses failure-mode taxonomy through raw and summary failure flags.

---

## 2. Research question

Primary question:

```text
Does the Variant 2 compensation effect persist at selected beta values when connectivity and failure-mode diagnostics are reported?
```

Secondary questions:

```text
1. Is beta=0.003 still the leading clean positive candidate when component structure is measured?
2. Does beta=0.005 remain a practical transition point?
3. Is beta=0.007 a genuine high-effect regime or mainly a sparsification/fragmentation-dominated point?
4. Which success criterion drives uncompensated failures?
```

---

## 3. Experiment design

Preset added to `experiments/ae_v010_2.py`:

```text
confirm_connectivity_variant2
```

Grid:

```text
N = 150
d = 4
steps = 200
seeds = 100
baseline_count = 100
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
model_modes = compensated, uncompensated
relation_variants = 2
beta = 0.003, 0.005, 0.007
epsilon_norm = 0.0
lambda_val = 0.0
```

Expected run count:

```text
2 model modes * 3 beta values * 100 seeds = 600 runs
```

Expected runtime:

```text
Approximately half of fine_beta_v010, likely around 3.5-4 hours on the same local machine.
```

This runtime estimate is approximate and should be recorded after execution.

---

## 4. Why these beta values

### beta=0.003

Role:

```text
leading clean positive candidate
```

Reason:

```text
Smallest tested beta with statistically significant positive effect in fine_beta_v010.
Lowest sparsification risk among tested positive points.
```

### beta=0.005

Role:

```text
prior transition candidate / practical middle point
```

Reason:

```text
Previous beta-grid candidate and part of the stronger transition region.
Useful midpoint between clean candidate and high-effect regime.
```

### beta=0.007

Role:

```text
peak effect / high-confound test point
```

Reason:

```text
Maximum observed effect in fine_beta_v010, but high sparsification risk.
Included to test whether component metrics confirm or reject it as a clean regime.
```

---

## 5. Primary endpoint

Primary endpoint remains unchanged:

```text
compensation_effect_attempted =
structure_success_rate_attempted(compensated) - structure_success_rate_attempted(uncompensated)
```

Reason:

```text
Attempted denominator preserves failed and unanalyzable runs as part of the experimental outcome.
```

Do not change primary endpoint after seeing results.

---

## 6. Required outputs

Expected generated files:

```text
outputs/raw_v010_confirm_connectivity_variant2.csv
outputs/summary_v010_confirm_connectivity_variant2.csv
outputs/comparison_v010_confirm_connectivity_variant2.csv
outputs/residual_v010_confirm_connectivity_variant2.csv
```

Generated outputs are local artifacts and should not be committed unless explicitly archived.

Interpretation should be recorded in:

```text
docs/results/v010_confirm_connectivity_variant2.md
```

External review should be recorded in:

```text
docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md
```

---

## 7. Required raw columns

The smoke run confirmed that the updated raw schema includes:

```text
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
n_components
largest_component_fraction
degree_variance
```

These are required for this experiment.

Minimum raw schema required for interpretation:

```text
model_mode
relation_variant
alpha
threshold
beta
epsilon_norm
lambda_val
seed
N
d
steps
baseline_count
mutation_rate
global_error
compensation_valid
strict_success
analyzed
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
sector_size
edge_count
density
clustering
chi
lifetime
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
n_components
largest_component_fraction
degree_variance
```

---

## 8. Required summary metrics

The updated summary should include:

```text
attempted_runs
analyzed_runs
compensation_rate
structure_success_rate_attempted
strict_success_rate_attempted
mean_global_error
mean_lifetime
mean_sector_size
mean_n_components
mean_largest_component_fraction
mean_degree_variance
failed_p_gnp_rate
failed_p_dp_rate
failed_dp_valid_rate
failed_lifetime_rate
failed_sector_size_rate
mean_dp_valid
mean_dp_swap_success_rate
structure_success_rate_analyzed
strict_success_rate_analyzed
```

---

## 9. Evaluation criteria

### Clean positive candidate

A beta value can be called a clean exploratory/confirmatory candidate only if:

```text
1. compensation_effect_attempted remains positive;
2. paired McNemar p-value supports compensated > uncompensated;
3. uncompensated analyzed_runs remains high;
4. uncompensated largest_component_fraction > 0.5 on average;
5. n_components does not indicate severe fragmentation;
6. degree_variance does not show an extreme confound;
7. no single failure criterion explains more than 70% of uncompensated failures;
8. edge_count and sector_size do not approach near-zero collapse.
```

### High-effect but confounded

A beta value should be classified as high-effect/high-confound if:

```text
1. compensation_effect is large;
2. uncompensated edge_count or sector_size falls sharply;
3. largest_component_fraction is low;
4. n_components is high relative to sector size;
5. failures are dominated by sector_size or connectivity-related modes.
```

### Blocked interpretation

Interpretation remains blocked if:

```text
1. required connectivity columns are missing;
2. failure_reason or failure flags are absent;
3. summary does not aggregate connectivity/failure metrics;
4. density/edge-matched ablation remains required for strong claim;
5. smoke validation fails.
```

---

## 10. What this experiment still does not solve

This run adds connectivity and failure-mode diagnostics, but it does not fully solve density matching.

Still missing or partial:

```text
density/edge-matched compensated ablation
degree-preserving edge removal from compensated graphs
sector_size distribution histograms
lifetime distribution quartiles
explicit Holm/multiple-testing correction if multiple beta values are treated symmetrically
```

Therefore, even a strong result remains limited unless density-matched ablation is added or performed separately.

---

## 11. Pre-run validation already completed

Smoke validation completed locally before this design checkpoint:

```text
.\.venv\Scripts\python.exe -m py_compile experiments/ae_v010_2.py
.\.venv\Scripts\python.exe experiments/ae_v010_2.py --mode smoke_v010 --out-prefix smoke_v010_test2
Get-Content outputs\raw_smoke_v010_test2.csv -TotalCount 1
Get-Content outputs\summary_smoke_v010_test2.csv -TotalCount 1
```

Confirmed:

```text
raw schema includes connectivity metrics and failure flags;
summary schema includes aggregate connectivity and failure-rate metrics;
smoke run completes successfully;
generated outputs are ignored by git.
```

---

## 12. Execution command

Only after human approval, run:

```powershell
.\.venv\Scripts\python.exe experiments\ae_v010_2.py --mode confirm_connectivity_variant2 --out-prefix v010_confirm_connectivity_variant2
```

Do not run this command until:

```text
1. code changes are committed;
2. this design checkpoint is committed;
3. git status is clean;
4. Aleksey explicitly authorizes the full run.
```

---

## 13. Post-run processing plan

After execution, run lite audit:

```powershell
.\.venv\Scripts\python.exe tools\audit_gcms_lite.py --raw outputs\raw_v010_confirm_connectivity_variant2.csv --out-prefix v010_confirm_connectivity_variant2_lite
```

Then compute paired McNemar/Wilson audit by beta.

Required post-run documents:

```text
docs/results/v010_confirm_connectivity_variant2.md
docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md
```

---

## 14. Reviewer prompt after execution

After result processing, ask Qwen:

```text
You are an independent methodological reviewer for GCMS-D0.

Review confirm_connectivity_variant2.
Do not strengthen claims.
Focus on whether connectivity metrics and failure-mode taxonomy resolve the blockers from the fine beta-grid review.

Questions:
1. Does beta=0.003 remain a clean positive candidate?
2. Does beta=0.005 remain a practical transition point?
3. Is beta=0.007 confirmed as high-effect/high-confound or rehabilitated by connectivity metrics?
4. Does largest_component_fraction rule out severe fragmentation?
5. Which failure criterion dominates uncompensated failures?
6. Does degree_variance suggest a degree-distribution confound?
7. Is density-matched ablation still required before preprint?
8. What exact conservative wording is now justified?
```

---

## 15. Decision after review

Possible decisions:

```text
A. beta=0.003 confirmed as clean candidate -> plan density-matched ablation or preprint technical note.
B. beta=0.003 weakened by fragmentation/failure taxonomy -> retreat to exploratory status.
C. beta=0.005 becomes best practical candidate -> design focused confirmatory follow-up.
D. beta=0.007 remains high-effect/high-confound -> do not use as clean claim.
E. all points remain confounded -> revise relation variant or add density-matched control before more runs.
```

---

## 16. Current status

```text
Design checkpoint created.
Code instrumentation smoke-tested.
Full confirm_connectivity_variant2 run not yet authorized.
Next step: commit code instrumentation and this design checkpoint, then request explicit run approval.
```
