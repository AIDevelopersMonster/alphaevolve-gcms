# Extension Plan: density_matched_ablation_variant2

**Status:** extension plan / full mode not yet implemented / full run not authorized  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `density_matched_ablation_variant2`  
**Design checkpoint:** `docs/experiments/density_matched_ablation_variant2_design.md`  
**Smoke tool:** `tools/ablate_density_variant2.py`  
**Related Qwen review:** `docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This document defines how to extend the accepted smoke-mode density ablation tool into a full `density_matched_ablation_variant2` run.

The smoke tool has been implemented and committed:

```text
8f108e7 Add density matched ablation smoke tool
```

Smoke validation confirmed:

```text
raw schema exists;
summary schema exists;
target_reachable / target_reached / reachability_reason are reported;
target_reached_rate = 1.0 for smoke targets 25 and 35;
actual_edge_count reaches target_edge_count in smoke output;
full mode is not implemented;
only --mode smoke is currently supported.
```

This plan prevents accidental transition from smoke success to a flawed full run.

---

## 2. Current state

Current tool:

```text
tools/ablate_density_variant2.py
```

Current supported CLI:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode smoke --out-prefix smoke_density_ablation_variant2
```

Current mode:

```text
smoke only
```

Current subsampling method:

```text
random_edge_removal_preliminary
```

Current smoke settings:

```text
beta = 0.003
target_edge_counts = [25, 35]
seeds = 2
repetitions_per_target = 2
baseline_count = 10
```

Current full-run status:

```text
not implemented
not authorized
not executed
```

---

## 3. Why extension must be careful

Qwen identified the remaining core blocker as:

```text
density/edge-count confound
```

The full ablation is intended to test whether the compensated advantage persists when compensated graphs are reduced to the uncompensated edge-count regime.

This only works if the ablation actually reaches the requested edge counts.

Important invariant:

```text
unreachable target != failed structure_success
unreachable target = invalid matching row
```

A full run must not silently include unreachable rows in primary effect estimates.

---

## 4. Required full-mode design

Add a full mode only after preserving smoke mode.

Proposed CLI:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode full --out-prefix v010_density_matched_ablation_variant2
```

Full settings:

```text
beta = 0.003
target_edge_counts = [25, 30, 35, 40]
seeds = 100
repetitions_per_target = 10
baseline_count = 100
subsampling_method = random_edge_removal_preliminary
```

Full outputs:

```text
outputs/raw_v010_density_matched_ablation_variant2.csv
outputs/summary_v010_density_matched_ablation_variant2.csv
```

Optional later output:

```text
outputs/comparison_v010_density_matched_ablation_variant2.csv
```

---

## 5. Mandatory reachability rules

The raw output must keep:

```text
target_reachable
target_reached
reachability_reason
```

Rules:

```text
target_reachable = original_edge_count >= target_edge_count
target_reached = target_reachable and actual_edge_count == target_edge_count
```

Reachability reasons:

```text
reached
failed_to_reach
unreachable_original_edge_count
```

Primary analysis must use:

```text
target_reached == True
```

Unreachable rows may be reported for diagnostics but must not be interpreted as density-matched ablation evidence.

---

## 6. Summary requirements

Full summary must clearly separate all rows from reached rows.

Required summary columns:

```text
subsampling_method
target_edge_count
attempted_runs_all
attempted_runs_reached
target_reachable_count
target_reached_count
target_reached_rate
structure_success_rate_attempted_all
structure_success_rate_attempted_reached
structure_success_rate_analyzed_reached
mean_actual_edge_count_all
mean_actual_edge_count_reached
mean_original_edge_count_all
mean_edge_removal_fraction_reached
mean_sector_size_reached
mean_density_reached
mean_n_components_reached
mean_largest_component_fraction_reached
mean_degree_variance_reached
failed_p_gnp_rate_reached
failed_p_dp_rate_reached
failed_dp_valid_rate_reached
failed_lifetime_rate_reached
failed_sector_size_rate_reached
mean_dp_valid_reached
mean_dp_swap_success_rate_reached
```

Legacy smoke summary names may remain, but full-mode summary must not leave ambiguity about whether statistics are all-row or reached-only.

---

## 7. Independence rule

Full ablation will have:

```text
100 seeds * 4 target_edge_counts * 10 repetitions = 4000 subsampled graph evaluations
```

But these 4000 evaluations are not independent seeds.

They are nested:

```text
seed -> target_edge_count -> subsampling repetition
```

Forbidden interpretation:

```text
Treating all 4000 rows as independent experimental seeds.
```

Required interpretation:

```text
Use repetitions to estimate subsampling variability within each seed and target.
Primary inference should aggregate per seed.
```

Recommended per-seed derived metrics:

```text
success_fraction_per_seed_target
majority_success_per_seed_target
mean_largest_component_fraction_per_seed_target
mean_failed_p_gnp_per_seed_target
mean_sector_size_per_seed_target
```

---

## 8. Recommended comparison to uncompensated reference

Reference from `confirm_connectivity_variant2` at `beta=0.003`:

```text
uncompensated structure_success attempted = 0.52
uncompensated edge_count ≈ 25
uncompensated largest_component_fraction = 0.949
uncompensated failed_p_gnp_rate = 0.47
uncompensated failed_p_dp_rate = 0.33
```

Comparison should be done at each target:

```text
target_edge_count = 25, 30, 35, 40
```

Primary comparison at:

```text
target_edge_count = 25
```

because it best matches the uncompensated beta=0.003 edge-count regime.

Recommended comparison output:

```text
target_edge_count
subsampled_comp_success_rate_reached
uncomp_reference_success_rate
matched_compensation_effect
subsampled_lcf
uncomp_reference_lcf
subsampled_failed_p_gnp_rate
uncomp_reference_failed_p_gnp_rate
subsampled_sector_size
uncomp_reference_sector_size
target_reached_rate
interpretation_note
```

---

## 9. Statistical reporting rule

Wilson confidence intervals may be reported for reached aggregate success rates, but must be labeled as descriptive if repetitions are included.

Preferred primary test options:

### Option A — majority per seed

For each seed and target:

```text
majority_success = majority(structure_success across 10 repetitions)
```

Then compare:

```text
majority_success_subsampled_compensated(seed)
vs
uncompensated_success_reference(seed)
```

using paired McNemar.

### Option B — per-seed success fraction

For each seed and target:

```text
success_fraction = successes / reached_repetitions
```

Then report paired mean difference or paired bootstrap.

Initial full run may report both, but must clearly state that repetitions are nested under seed.

---

## 10. Required validation before full run

Before running full mode, execute:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\ablate_density_variant2.py
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode smoke --out-prefix smoke_density_ablation_variant2
Get-Content outputs\raw_smoke_density_ablation_variant2.csv -TotalCount 1
Get-Content outputs\summary_smoke_density_ablation_variant2.csv
```

Then verify:

```text
1. target_reached_rate > 0 for every smoke target;
2. mean_actual_edge_count_reached equals target edge count;
3. no existing success criteria changed;
4. no changes to experiments/ae_v010_2.py unless explicitly justified;
5. git status shows only expected tool changes;
6. full mode is not run until explicitly authorized.
```

---

## 11. Full run authorization checklist

Before full run, Aleksey must explicitly approve.

Checklist:

```text
[ ] full mode implemented;
[ ] smoke mode still passes;
[ ] summary separates reached-only metrics;
[ ] per-seed aggregation is implemented or planned as post-processing;
[ ] repetitions are not treated as independent seeds;
[ ] structure_success criteria unchanged;
[ ] expected runtime is estimated;
[ ] output names are fixed;
[ ] Git working tree is clean or expected changes are committed.
```

Only after all items are satisfied, run:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode full --out-prefix v010_density_matched_ablation_variant2
```

---

## 12. Expected result interpretation

### If effect persists at target_edge_count = 25

Interpretation:

```text
The beta=0.003 compensation signal survives the primary density/edge-count control.
```

Possible next step:

```text
Qwen review, then technical note/preprint planning.
```

### If effect disappears at target_edge_count = 25

Interpretation:

```text
The previous beta=0.003 effect was likely primarily connectivity-driven.
```

Possible next step:

```text
Reframe result as a connectivity-sensitive artifact or redesign relation variant.
```

### If effect persists only at 30/35/40

Interpretation:

```text
The mechanism may depend on a connectivity threshold rather than being edge-count independent.
```

Possible next step:

```text
Map effect vs edge count and consider a refined model.
```

### If subsampling causes fragmentation

Interpretation:

```text
random_edge_removal_preliminary is too destructive.
```

Possible next step:

```text
Implement degree-aware or fragmentation-constrained removal.
```

---

## 13. What must not be claimed after full run without review

Even if full ablation is positive, do not immediately claim:

```text
physical theory;
causal law;
proof of compensation mechanism;
real-world constants;
quantum or gravity explanation;
preprint-ready conclusion without review.
```

Allowed provisional language after positive full ablation:

```text
The density-matched ablation provides additional toy-model evidence that the beta=0.003 Variant 2 compensation signal is not solely explained by edge-count differences.
```

Final wording must wait for Qwen review.

---

## 14. Codex instruction for next implementation step

When ready, give Codex a narrow task:

```text
Extend tools/ablate_density_variant2.py from smoke-only to support --mode full.
Preserve smoke mode.
Do not modify experiments/ae_v010_2.py unless absolutely necessary.
Do not change structure_success criteria.
Add full settings: beta=0.003, target_edge_counts=[25,30,35,40], seeds=100, repetitions_per_target=10, baseline_count=100.
Update summary to separate all-row and reached-only metrics.
Add per-seed aggregation output or prepare it as a post-processing step.
Run only py_compile and smoke validation.
Do not run full mode.
Do not commit.
Report changed files and smoke validation results.
```

---

## 15. Current status

```text
Smoke tool committed.
Full mode not implemented.
Full run not authorized.
Next action: implement full-mode extension under strict validation, but run smoke only.
```

Short invariant:

```text
Smoke success proves the tool can reach targets.
Full success must prove the effect survives target matching.
```