# Extension Plan: connectivity_entanglement_audit_variant2_ci_pairing

**Status:** extension plan / post-processing only / not yet implemented  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Parent experiment:** `connectivity_entanglement_audit_variant2`  
**Parent result note:** `docs/results/v010_connectivity_entanglement_audit_variant2.md`  
**Parent Qwen review:** `docs/reviews/v010_connectivity_entanglement_audit_variant2_qwen_review.md`  
**Tool to extend or add:** `tools/audit_connectivity_entanglement_variant2.py` or a new post-processing tool  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

Qwen reviewed `v010_connectivity_entanglement_audit_variant2` and classified it as:

```text
Confound-isolation / topology-threshold diagnostic in a toy model
```

Qwen accepted the reframe:

```text
compensation-connectivity entanglement
```

and recommended `non_bridge_edge_count` as the primary reporting descriptor.

Before a technical/confound-isolation draft, Qwen requires a minimal post-processing extension:

```text
1. paired seed analysis;
2. bootstrap confidence intervals for threshold proportions;
3. Wilson or exact confidence intervals for rates.
```

This document defines that extension.

---

## 2. Strict scope

This is post-processing only.

Allowed input files:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
```

Forbidden actions:

```text
Do not rerun the full audit.
Do not rerun simulations.
Do not prune.
Do not remove edges.
Do not add edge-removal rescue logic.
Do not change structure_success criteria.
Do not change Variant 2 relation logic.
Do not change existing result notes.
Do not reinterpret passive residual diagnostics causally.
Do not add dependencies.
```

Allowed actions:

```text
Read existing output CSV files.
Compute paired seed deltas and sign-style summaries.
Compute Wilson confidence intervals for proportions.
Compute bootstrap confidence intervals for threshold differences.
Write post-processing CSV outputs.
Write a compact result note after validation.
```

---

## 3. Motivation from Qwen review

Qwen stated that the current evidence is sufficient for a first technical draft only after mandatory additions:

```text
1. Paired seed analysis.
2. Bootstrap confidence interval for threshold proportions.
3. Wilson or exact confidence intervals for rates.
```

Qwen also stated:

```text
non_bridge_edge_count should be the primary reporting descriptor.
cycle_rank should be secondary / confirmatory.
threshold non_bridge_edge_count >= 19 is reportable only as post-hoc exploratory.
```

Therefore this extension must preserve the exploratory status of the threshold.

---

## 4. Primary descriptor and threshold

Primary descriptor:

```text
non_bridge_edge_count
```

Primary post-hoc exploratory threshold:

```text
non_bridge_edge_count >= 19
```

Required threshold comparison:

```text
above threshold: non_bridge_edge_count >= 19
below threshold: non_bridge_edge_count < 19
```

Known parent-audit values:

```text
above threshold:
    rows = 105
    structure_success_rate = 0.981
below threshold:
    rows = 95
    structure_success_rate = 0.232
```

Important:

```text
The threshold was identified on the same data.
It must be reported as post-hoc exploratory, not mechanistic or universal.
```

---

## 5. Required new outputs

Suggested output prefix:

```text
v010_connectivity_entanglement_audit_variant2_ci_pairing
```

Required outputs:

```text
outputs/paired_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/rate_ci_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/threshold_bootstrap_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

Optional output:

```text
outputs/paired_deltas_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

The optional paired-deltas file may duplicate or subset the existing `per_seed` file with normalized columns for reporting.

---

## 6. Paired seed analysis

Input:

```text
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
```

Primary paired metrics:

```text
delta_non_bridge_edge_count
delta_cycle_rank
delta_edge_count
delta_structure_success
delta_bridge_fraction
delta_largest_component_cycle_rank
delta_sector_size
```

Required paired summary columns:

```text
metric
n_pairs
mean_delta
median_delta
q25_delta
q75_delta
min_delta
max_delta
positive_delta_count
negative_delta_count
zero_delta_count
positive_delta_fraction
negative_delta_fraction
zero_delta_fraction
sign_test_positive_rate
```

For binary deltas such as `delta_structure_success`, report:

```text
compensated_only_success_count
uncompensated_only_success_count
both_success_count
both_failure_count
paired_success_delta_mean
```

Definitions:

```text
compensated_only_success = structure_success_compensated == 1 and structure_success_uncompensated == 0
uncompensated_only_success = structure_success_compensated == 0 and structure_success_uncompensated == 1
both_success = both == 1
both_failure = both == 0
```

No McNemar test is required unless implemented with existing standard-library math only.

A sign-style summary is sufficient for the first technical draft.

---

## 7. Wilson confidence intervals

Input:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
```

Required rates:

```text
structure_success_rate by model_mode
structure_success_rate for non_bridge_edge_count >= 19
structure_success_rate for non_bridge_edge_count < 19
failed_p_gnp_rate by model_mode
failed_p_dp_rate by model_mode
```

Required output columns:

```text
group
subgroup
success_count
n
rate
ci_method
ci_level
ci_low
ci_high
```

Recommended method:

```text
Wilson score interval, 95% CI
```

Use standard-library math only.

No external dependency required.

Wilson formula:

```text
z = 1.959963984540054
phat = k / n
denominator = 1 + z^2 / n
center = (phat + z^2 / (2n)) / denominator
half_width = z * sqrt((phat * (1 - phat) / n) + (z^2 / (4n^2))) / denominator
ci_low = max(0, center - half_width)
ci_high = min(1, center + half_width)
```

If n = 0, write empty CI fields and mark rate unavailable.

---

## 8. Bootstrap confidence intervals for threshold difference

Primary threshold:

```text
non_bridge_edge_count >= 19
```

Statistic:

```text
diff = structure_success_rate_above_threshold - structure_success_rate_below_threshold
```

Bootstrap settings:

```text
iterations = 1000
random_seed = 20260512
ci_level = 0.95
resampling_unit = row
```

Required output columns:

```text
threshold_type
threshold_value
iterations
random_seed
above_n
above_success_count
above_rate
below_n
below_success_count
below_rate
rate_difference
bootstrap_ci_low
bootstrap_ci_high
ci_level
note
```

Note must include:

```text
post_hoc_threshold_same_data_exploratory
```

Implementation detail:

```text
Resample above-threshold rows with replacement to compute above_rate_boot.
Resample below-threshold rows with replacement to compute below_rate_boot.
Store diff_boot = above_rate_boot - below_rate_boot.
Use 2.5 and 97.5 percentiles as CI.
```

If either group has n = 0, skip bootstrap and record unavailable.

---

## 9. Optional secondary bootstrap thresholds

Optional confirmatory thresholds:

```text
cycle_rank >= 10
edge_count >= 22
```

These may be included if implementation is simple.

But reporting should emphasize:

```text
primary descriptor = non_bridge_edge_count
primary threshold = >= 19
cycle_rank and edge_count thresholds are secondary / confirmatory
```

---

## 10. Passive residual diagnostics rule

Passive diagnostics are not part of this CI/pairing extension except as existing context.

Do not model:

```text
global_error
sector_chi
```

Do not report threshold CIs for passive residual diagnostics.

Allowed statement:

```text
Passive diagnostics were recorded in the parent audit and remain exploratory/control-only.
```

Forbidden statement:

```text
Residual diagnostics explain or cause structure_success.
```

---

## 11. Suggested implementation options

Preferred new tool:

```text
tools/postprocess_connectivity_audit_ci_pairing.py
```

Reason:

```text
This is post-processing, not simulation. Keeping it separate prevents accidental full reruns.
```

Required CLI:

```powershell
.\.venv\Scripts\python.exe tools\postprocess_connectivity_audit_ci_pairing.py --input-prefix v010_connectivity_entanglement_audit_variant2 --out-prefix v010_connectivity_entanglement_audit_variant2_ci_pairing
```

Alternative:

```text
Add a --mode postprocess_ci_pairing to tools/audit_connectivity_entanglement_variant2.py
```

But this is less preferred because the audit tool already runs simulations.

---

## 12. Verification commands

Before running post-processing:

```powershell
git status --short
Get-ChildItem outputs\*v010_connectivity_entanglement_audit_variant2*
```

Expected required parent files:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
```

After implementation, run only post-processing:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\postprocess_connectivity_audit_ci_pairing.py
.\.venv\Scripts\python.exe tools\postprocess_connectivity_audit_ci_pairing.py --input-prefix v010_connectivity_entanglement_audit_variant2 --out-prefix v010_connectivity_entanglement_audit_variant2_ci_pairing
```

Inspect outputs:

```powershell
Get-Content outputs\paired_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
Get-Content outputs\rate_ci_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
Get-Content outputs\threshold_bootstrap_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

Git checks:

```powershell
git status --short
git diff --stat
```

Expected code changes:

```text
new tool only:
    tools/postprocess_connectivity_audit_ci_pairing.py
```

Expected generated output files:

```text
outputs/paired_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/rate_ci_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/threshold_bootstrap_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

Do not commit generated outputs unless separately authorized.

---

## 13. Result note after post-processing

After successful post-processing, create:

```text
docs/results/v010_connectivity_entanglement_audit_variant2_ci_pairing.md
```

This note should report:

```text
1. paired deltas for non_bridge_edge_count and cycle_rank;
2. paired structure_success counts;
3. Wilson CIs for model-mode success rates;
4. Wilson CIs for above/below non_bridge threshold success rates;
5. bootstrap CI for threshold difference;
6. explicit post-hoc warning for threshold >=19.
```

---

## 14. Current status

```text
Qwen review saved.
CI/pairing extension planned.
No code implemented.
No post-processing run executed.
No technical draft started.
```

Short invariant:

```text
This extension strengthens reporting uncertainty. It does not change the experiment.
```
