# Extension Plan: lcf_constrained_ablation_variant2

**Status:** extension plan / full LCF mode not yet implemented / full LCF run not authorized  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `lcf_constrained_ablation_variant2`  
**Design checkpoint:** `docs/experiments/lcf_constrained_ablation_variant2_design.md`  
**Smoke validation:** `docs/results/smoke_lcf_ablation_variant2_validation.md`  
**Related Qwen review:** `docs/reviews/v010_density_matched_ablation_variant2_qwen_review.md`  
**Tool:** `tools/ablate_density_variant2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This document defines how to extend the validated `lcf_smoke` mode into a full LCF-constrained ablation.

The previous random-removal ablation matched edge counts exactly but caused severe fragmentation. Qwen classified it as a useful non-final stress test and required topology-preserving ablation before stronger interpretation.

The `lcf_smoke` mode has now validated the required control logic:

```text
target_reached
target_connectivity_preserved
valid_lcf_matched = target_reached AND target_connectivity_preserved
```

This extension plan prevents accidental transition from smoke success to an under-specified full run.

---

## 2. Current validated state

Current implemented mode:

```text
--mode lcf_smoke
```

Committed tool state:

```text
32f145e Add LCF constrained ablation smoke mode
```

Smoke-validation note:

```text
docs/results/smoke_lcf_ablation_variant2_validation.md
```

Smoke result:

```text
target_edge_count = 25: valid_lcf_matched_rate = 0.5
target_edge_count = 30: valid_lcf_matched_rate = 0.5
```

Observed smoke behavior:

```text
seed 0: target 25/30 reached with LCF preserved;
seed 3: LCF preserved but target 25/30 not reached, reason = failed_no_non_bridge_edges.
```

Important implication:

```text
Full LCF ablation must report infeasibility explicitly.
Failure to reach target edge count while preserving LCF is a meaningful outcome, not a hidden error.
```

---

## 3. Full LCF experiment goal

Primary goal:

```text
Test whether the beta=0.003 Variant 2 compensation signal persists when compensated graphs are matched to low edge-count targets while preserving largest-component connectivity.
```

Primary comparison reference from `confirm_connectivity_variant2`:

```text
uncompensated beta=0.003 structure_success = 0.52
uncompensated beta=0.003 LCF ≈ 0.949
uncompensated beta=0.003 edge_count ≈ 25
```

Primary endpoint:

```text
structure_success_rate_valid(target_edge_count = 25)
```

where:

```text
valid = target_reached == True AND target_connectivity_preserved == True
```

---

## 4. Proposed full LCF settings

New mode to implement:

```text
--mode lcf_full
```

Proposed CLI, not yet authorized for execution:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf_full --out-prefix v010_lcf_constrained_ablation_variant2
```

Full settings:

```text
relation_variant = 2
model_mode = compensated
beta = 0.003
target_edge_counts = [25, 30, 35]
seeds = 100
repetitions_per_target = 5
baseline_count = 100
N = 150
d = 4
steps = 200
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
epsilon_norm = 0.0
lambda_val = 0.0
LCF_min_threshold = 0.85
max_attempts_per_seed = 100
subsampling_method = greedy_non_bridge_removal_with_LCF_constraint
max_seed_scan = 10000
```

Expected maximum raw rows:

```text
100 seeds × 3 target_edge_counts × 5 repetitions = 1500 rows
```

Important:

```text
The run may produce 1500 attempted rows, but fewer valid rows.
The valid row count is part of the result.
```

---

## 5. Required outputs

Full LCF mode should produce:

```text
outputs/raw_v010_lcf_constrained_ablation_variant2.csv
outputs/summary_v010_lcf_constrained_ablation_variant2.csv
outputs/per_seed_v010_lcf_constrained_ablation_variant2.csv
```

Optional additional output:

```text
outputs/reason_counts_v010_lcf_constrained_ablation_variant2.csv
```

The optional reason-count output is recommended because infeasibility is expected to be important.

---

## 6. Required raw fields

Raw output must include all current LCF smoke fields:

```text
model_mode
relation_variant
beta
seed
subsample_rep
target_edge_count
actual_edge_count
original_edge_count
edge_removal_count
edge_removal_fraction
subsampling_method
target_reachable
target_reached
reachability_reason
target_connectivity_preserved
connectivity_preservation_reason
lcf_min_threshold
actual_largest_component_fraction
removal_attempts
removal_failures
valid_lcf_matched
N
d
steps
baseline_count
mutation_rate
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
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Required invariant:

```text
actual_largest_component_fraction should equal or explain any difference from largest_component_fraction.
```

If they are both retained, document that:

```text
actual_largest_component_fraction = LCF measured immediately after removal;
largest_component_fraction = LCF from final graph analysis.
```

They should normally match.

---

## 7. Required summary fields

Summary must include:

```text
subsampling_method
target_edge_count
attempted_runs_all
target_reached_count
target_reached_rate
target_connectivity_preserved_count
target_connectivity_preserved_rate
valid_lcf_matched_count
valid_lcf_matched_rate
structure_success_rate_valid
mean_actual_edge_count_valid
mean_largest_component_fraction_valid
mean_n_components_valid
mean_degree_variance_valid
mean_sector_size_valid
failed_p_gnp_rate_valid
failed_p_dp_rate_valid
failed_dp_valid_rate_valid
mean_dp_valid_valid
mean_dp_swap_success_rate_valid
mean_removal_attempts
mean_removal_failures
failed_no_non_bridge_edges_count
failed_no_non_bridge_edges_rate
failed_max_attempts_count
failed_max_attempts_rate
failed_lcf_constraint_count
failed_lcf_constraint_rate
```

The existing LCF smoke summary already includes most required fields. Full mode should add reason counts or produce a separate reason-count output.

---

## 8. Required per-seed fields

Per-seed output must include:

```text
target_edge_count
seed
connectivity_preservation_fraction_per_seed_target
valid_repetitions
success_count_valid
success_fraction_per_seed_target_valid
majority_success_per_seed_target_valid
mean_largest_component_fraction_per_seed_target_valid
mean_failed_p_gnp_per_seed_target_valid
mean_sector_size_per_seed_target_valid
reason_failed_no_non_bridge_edges_count
reason_failed_max_attempts_count
reason_failed_lcf_constraint_count
```

Do not treat the 1500 attempted rows as independent seeds.

Primary inference should use per-seed derived values.

---

## 9. Valid row logic

Definitions:

```text
target_reachable = original_edge_count >= target_edge_count
target_reached = actual_edge_count == target_edge_count
target_connectivity_preserved = largest_component_fraction >= LCF_min_threshold
valid_lcf_matched = target_reached AND target_connectivity_preserved
```

Primary analysis rows:

```text
valid_lcf_matched == True
```

Rows with:

```text
target_connectivity_preserved == True
but target_reached == False
```

must not be used as successful matched rows. They should be counted as informative infeasibility cases.

Rows with:

```text
target_reached == True
but target_connectivity_preserved == False
```

must not be used for topology-preserving inference.

---

## 10. Handling infeasible rows

If edge count cannot be reduced to target while preserving LCF, record the reason.

Allowed reasons:

```text
preserved
failed_lcf_constraint
failed_no_non_bridge_edges
failed_max_attempts
not_reached
unreachable_original_edge_count
```

Interpretation rules:

```text
failed_no_non_bridge_edges:
    topology-preserving removal exhausted removable edges before reaching target;
    this suggests the target may be structurally incompatible with the LCF constraint for that seed.

failed_max_attempts:
    algorithmic search may be insufficient;
    consider increasing attempts or improving heuristic before interpreting as structural infeasibility.

failed_lcf_constraint:
    target reached or attempted removal would violate LCF threshold;
    compare actual LCF and removal trace.

unreachable_original_edge_count:
    original graph has fewer edges than target;
    this should be rare because seed selection requires reachability.
```

Do not collapse these into a generic failure.

---

## 11. Success criteria

### Strong success

At target_edge_count = 25:

```text
valid_lcf_matched_rate >= 0.80
mean_largest_component_fraction_valid >= 0.85
structure_success_rate_valid > 0.52
per-seed majority_success_valid > uncompensated reference majority if paired reference is available
failed_p_gnp_rate_valid does not exceed uncompensated reference by more than approximately 0.10
```

If this holds, beta=0.003 becomes substantially stronger as a clean toy-model candidate.

### Partial success

```text
target 25 has low valid_lcf_matched_rate but target 30 or 35 is feasible and positive;
or target 25 effect is near reference but target 30 is clearly positive.
```

Interpretation:

```text
The Variant 2 signal may require a minimum topology-preserving edge density.
```

### Negative result

```text
target 25 is feasible with LCF preserved but structure_success_rate_valid remains below reference;
target 30 and 35 also fail to recover.
```

Interpretation:

```text
The beta=0.003 compensation signal is likely not robust under topology-preserving density matching.
```

### Infeasible result

```text
target 25 is rarely feasible with LCF >= 0.85, especially due to failed_no_non_bridge_edges.
```

Interpretation:

```text
Strict low-edge matching may be topologically incompatible with preserving the compensated graph's largest component.
This would not prove or disprove the mechanism directly, but would establish a minimum-connectivity constraint.
```

---

## 12. Statistical reporting

For each target edge count, report:

```text
valid_lcf_matched_rate
structure_success_rate_valid
per-seed success_fraction_valid
per-seed majority_success_valid
Wilson CI for valid aggregate success rate
reason distribution
LCF distribution on valid rows
```

If comparing against uncompensated beta=0.003 reference, state whether the comparison is:

```text
paired by seed;
unpaired because reachable seed selection differs;
descriptive only.
```

Do not run McNemar unless a clear binary paired outcome per seed exists for both modes.

Potential paired rule:

```text
For each seed, define majority_success_valid over valid repetitions.
Compare to uncompensated beta=0.003 structure_success for the same seed, if that reference is available and seed sets overlap.
```

If many seeds have zero valid repetitions, report them separately instead of forcing them into success/failure.

---

## 13. Required validation before full LCF run

Before running `lcf_full`, perform:

```powershell
git status --short
.\.venv\Scripts\python.exe -m py_compile tools\ablate_density_variant2.py
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode smoke --out-prefix smoke_density_ablation_variant2
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf_smoke --out-prefix smoke_lcf_ablation_variant2
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --help
Get-Content outputs\summary_smoke_lcf_ablation_variant2.csv
```

Validation checklist:

```text
[ ] working tree clean before new code changes or only expected tool changes;
[ ] old smoke still works;
[ ] lcf_smoke still works;
[ ] help shows smoke, full, lcf_smoke, and only after implementation lcf_full;
[ ] raw includes target_connectivity_preserved and valid_lcf_matched;
[ ] summary includes valid_lcf_matched_count and valid_lcf_matched_rate;
[ ] per_seed output exists;
[ ] no generated outputs are committed;
[ ] full LCF run explicitly authorized by Aleksey.
```

---

## 14. Implementation task for Codex

When ready, give Codex a narrow task:

```text
Extend tools/ablate_density_variant2.py from lcf_smoke to support --mode lcf_full.
Preserve smoke, full, and lcf_smoke behavior.
Do not modify experiments/ae_v010_2.py.
Do not change structure_success criteria.
Add LCF_FULL_CONFIG with target_edge_counts=[25,30,35], seeds=100, repetitions_per_target=5, baseline_count=100, lcf_min_threshold=0.85, max_attempts_per_seed=100, max_seed_scan=10000.
Add full summary reason counts for connectivity_preservation_reason.
Add per-seed reason counts.
Run only py_compile, smoke, and lcf_smoke validation.
Do not run lcf_full.
Do not commit.
Report changed files and validation results.
```

---

## 15. What must not be claimed before LCF full result

Do not claim:

```text
density confound resolved;
beta=0.003 proven clean;
mechanism confirmed;
preprint ready;
physical theory relevance.
```

Allowed language:

```text
The LCF smoke validation confirms that the tool can distinguish exact target matching from topology preservation and can explicitly report infeasible low-edge targets under LCF constraints.
```

---

## 16. Current status

```text
LCF smoke implemented and validated.
Full LCF mode not yet implemented.
Full LCF run not authorized.
Next action: implement lcf_full mode under strict validation, but run only smoke/lcf_smoke checks before approval.
```

Short invariant:

```text
The full LCF experiment is not just an edge-count run.
Its result is the joint distribution of edge matching, connectivity preservation, and structure_success.
```
