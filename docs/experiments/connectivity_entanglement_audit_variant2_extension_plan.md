# Extension Plan: connectivity_entanglement_audit_variant2

**Status:** extension plan / full audit not yet implemented / full audit not yet executed  
**Date:** 2026-05-11  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Design checkpoint:** `docs/experiments/connectivity_entanglement_audit_variant2_design.md`  
**Smoke validation:** `docs/results/smoke_connectivity_entanglement_audit_variant2_validation.md`  
**Reframe:** `docs/experiments/connectivity_entanglement_reframe.md`  
**Qwen reframe review:** `docs/reviews/connectivity_entanglement_reframe_qwen_review.md`  
**Tool:** `tools/audit_connectivity_entanglement_variant2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This extension plan defines the transition from validated smoke mode to full execution for `connectivity_entanglement_audit_variant2`.

The purpose of the full audit is:

```text
Measure native topology in compensated and uncompensated Variant 2 graphs at beta=0.003 and determine whether topology descriptors explain structure_success.
```

This is not an edge-removal experiment.

Core invariant:

```text
Measure native topology first. Do not prune. Do not rescue.
```

---

## 2. Current validated state

Smoke tool implemented:

```text
tools/audit_connectivity_entanglement_variant2.py
```

Smoke validation document:

```text
docs/results/smoke_connectivity_entanglement_audit_variant2_validation.md
```

Smoke commands passed:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\audit_connectivity_entanglement_variant2.py
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2
```

Smoke outputs produced:

```text
outputs/raw_smoke_connectivity_entanglement_audit_variant2.csv
outputs/summary_smoke_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_smoke_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_smoke_connectivity_entanglement_audit_variant2.csv
```

Safety status:

```text
full mode is currently a NotImplementedError placeholder;
full audit has not been run;
no pruning logic is present;
no full output files exist.
```

---

## 3. Full audit settings

New full mode to implement:

```text
--mode full
```

Full CLI to implement but not run until authorization:

```powershell
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode full --out-prefix v010_connectivity_entanglement_audit_variant2
```

Full configuration:

```text
relation_variant = 2
model_modes = [compensated, uncompensated]
beta = 0.003
seeds = 100
N = 150
d = 4
steps = 200
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
epsilon_norm = 0.0
lambda_val = 0.0
baseline_count = 100
```

Expected rows:

```text
2 modes × 100 seeds = 200 raw rows
100 paired per-seed rows
```

---

## 4. Required full outputs

Full outputs:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
```

Optional if implemented without new dependencies:

```text
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
outputs/regression_v010_connectivity_entanglement_audit_variant2.csv
```

Do not add new dependencies for regression.

If logistic regression is not already available with existing dependencies, use descriptive correlations and threshold tables only.

---

## 5. Required raw schema

Raw columns must include:

```text
model_mode
relation_variant
beta
seed
N
d
steps
baseline_count
mutation_rate
sector_size
lifetime
edge_count
density
n_components
largest_component_fraction
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_edge_count
largest_component_node_count
largest_component_cycle_rank
mean_degree
degree_variance
max_degree
clustering
spectral_gap_optional
spectral_gap_available
algebraic_connectivity_optional
algebraic_connectivity_available
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Do not remove smoke columns.

Do not rename existing output columns after smoke validation unless necessary and documented.

---

## 6. Required summary schema

Summary grouped by:

```text
model_mode
relation_variant
beta
```

Required summary columns:

```text
runs
structure_success_rate
mean_edge_count
mean_density
mean_n_components
mean_largest_component_fraction
mean_bridge_count
mean_bridge_fraction
mean_non_bridge_edge_count
mean_cycle_rank
mean_largest_component_cycle_rank
mean_mean_degree
mean_degree_variance
mean_max_degree
mean_sector_size
mean_failed_p_gnp
mean_failed_p_dp
mean_dp_valid
mean_dp_swap_success_rate
q25_non_bridge_edge_count
q50_non_bridge_edge_count
q75_non_bridge_edge_count
q25_cycle_rank
q50_cycle_rank
q75_cycle_rank
q25_bridge_fraction
q50_bridge_fraction
q75_bridge_fraction
```

If the existing smoke summary uses `structure_success` instead of `structure_success_rate`, preserve compatibility if needed but prefer adding the clearer alias in full output.

---

## 7. Required per-seed paired output

Per-seed output must compare compensated and uncompensated rows with the same seed.

Required columns:

```text
seed
edge_count_compensated
edge_count_uncompensated
delta_edge_count
bridge_fraction_compensated
bridge_fraction_uncompensated
delta_bridge_fraction
non_bridge_edge_count_compensated
non_bridge_edge_count_uncompensated
delta_non_bridge_edge_count
cycle_rank_compensated
cycle_rank_uncompensated
delta_cycle_rank
largest_component_fraction_compensated
largest_component_fraction_uncompensated
delta_largest_component_fraction
structure_success_compensated
structure_success_uncompensated
delta_structure_success
failed_p_gnp_compensated
failed_p_gnp_uncompensated
delta_failed_p_gnp
failed_p_dp_compensated
failed_p_dp_uncompensated
delta_failed_p_dp
```

Recommended additional paired columns:

```text
density_compensated
density_uncompensated
delta_density
bridge_count_compensated
bridge_count_uncompensated
delta_bridge_count
largest_component_cycle_rank_compensated
largest_component_cycle_rank_uncompensated
delta_largest_component_cycle_rank
sector_size_compensated
sector_size_uncompensated
delta_sector_size
```

Do not treat mode rows as independent when paired seed comparisons are possible.

---

## 8. Threshold analysis

Threshold output path:

```text
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
```

Threshold types:

```text
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
bridge_fraction_le
edge_count
```

For each threshold:

```text
threshold_type
threshold_value
rows_above_threshold
structure_success_rate_above_threshold
rows_below_threshold
structure_success_rate_below_threshold
```

For `bridge_fraction_le`, interpret above-threshold column as rows satisfying:

```text
bridge_fraction <= threshold_value
```

Purpose:

```text
Estimate topology thresholds where structure_success becomes more likely.
```

---

## 9. Recommended descriptive correlation output

Optional output:

```text
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
```

Fields:

```text
feature
method
correlation_with_structure_success
correlation_with_failed_p_gnp
correlation_with_failed_p_dp
n_rows
```

Candidate features:

```text
edge_count
density
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
mean_degree
degree_variance
max_degree
sector_size
```

Allowed methods:

```text
pearson
spearman_if_available
```

If `scipy` is unavailable, do not install it. Use pandas/numpy correlation only.

---

## 10. Optional regression output

Optional output:

```text
outputs/regression_v010_connectivity_entanglement_audit_variant2.csv
```

Only implement if possible with existing dependencies.

Candidate simple models:

```text
structure_success ~ model_mode
structure_success ~ edge_count
structure_success ~ non_bridge_edge_count
structure_success ~ cycle_rank
structure_success ~ bridge_fraction
structure_success ~ model_mode + edge_count + bridge_fraction + non_bridge_edge_count
```

If logistic regression is not available, do not install packages.

Instead report:

```text
regression_skipped_reason = dependency_unavailable_or_not_implemented
```

Regression is not required for the full audit to be valid.

---

## 11. Interpretation plan

The full audit should answer:

```text
1. Does compensated beta=0.003 produce a different native topology than uncompensated beta=0.003?
2. Which topology descriptors differ most strongly by model_mode?
3. Do successful rows have higher non_bridge_edge_count or cycle_rank?
4. Does bridge_fraction explain failures through p_gnp / p_dp?
5. Is beta=0.003 a useful connectivity-threshold-dependent regime?
```

Expected possible outcomes:

### Outcome A: Strong topology mediation

```text
compensated graphs show higher non_bridge_edge_count / cycle_rank;
structure_success increases above a topology threshold;
mode effect appears mediated by connectivity descriptors.
```

Interpretation:

```text
supports compensation-connectivity entanglement.
```

### Outcome B: Weak topology mediation

```text
topology descriptors differ but do not clearly explain structure_success.
```

Interpretation:

```text
reframe remains plausible but needs broader parameter sweep.
```

### Outcome C: No topology difference

```text
compensated and uncompensated native topology descriptors are similar.
```

Interpretation:

```text
connectivity-entanglement frame weakens; investigate measurement or relation dynamics.
```

---

## 12. Required validation before full run

Before full run:

```powershell
git status --short
.\.venv\Scripts\python.exe -m py_compile tools\audit_connectivity_entanglement_variant2.py
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2
Get-Content outputs\summary_smoke_connectivity_entanglement_audit_variant2.csv
Get-Content outputs\per_seed_smoke_connectivity_entanglement_audit_variant2.csv
Get-ChildItem outputs\*v010_connectivity_entanglement_audit_variant2*
```

Expected:

```text
working tree clean;
py_compile passes;
smoke still passes;
full output files do not yet exist;
full run explicitly authorized.
```

---

## 13. Implementation task boundary

Codex implementation task should be narrow:

```text
Implement --mode full in tools/audit_connectivity_entanglement_variant2.py using the same native-topology logic as smoke mode.
Do not run full.
Run only py_compile and smoke validation.
Do not install dependencies.
Do not use global Python.
Do not modify experiments/ae_v010_2.py.
Do not add pruning or edge removal.
Do not commit.
```

Required Python invocation:

```powershell
.\.venv\Scripts\python.exe
```

Forbidden:

```text
python
py
C:\Python314\python.exe
pip install
any dependency modification
```

---

## 14. What must not change

Do not change:

```text
Variant 2 relation logic;
structure_success criteria;
p_gnp threshold;
p_dp threshold;
dp_valid requirement;
lifetime threshold;
sector_size bounds;
existing ablation result interpretation;
existing reframe status.
```

Do not add:

```text
pruning;
edge removal;
rescue ablation;
density matching by modification;
```

---

## 15. Review step after full audit

After full execution, create result note:

```text
docs/results/v010_connectivity_entanglement_audit_variant2.md
```

Then prepare Qwen review packet asking:

```text
1. Does the audit support compensation-connectivity entanglement?
2. Which topology descriptor best explains structure_success?
3. Is beta=0.003 still useful as a study regime?
4. Is publication as confound-isolation study justified?
5. What additional controls remain before technical write-up?
```

---

## 16. Current status

```text
Smoke tool validated.
Extension plan created.
Full mode not yet implemented.
Full audit not yet executed.
```

Short invariant:

```text
Full audit is a native topology measurement, not a new attempt to save the old claim.
```
