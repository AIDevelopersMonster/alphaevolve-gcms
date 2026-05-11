# Result Note: v010_lcf_constrained_ablation_variant2

**Status:** result note / requires external review  
**Date:** 2026-05-11  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `lcf_constrained_ablation_variant2`  
**Subsampling method:** `greedy_non_bridge_removal_with_LCF_constraint`  
**Design checkpoint:** `docs/experiments/lcf_constrained_ablation_variant2_design.md`  
**Extension plan:** `docs/experiments/lcf_constrained_ablation_variant2_extension_plan.md`  
**Smoke validation:** `docs/results/smoke_lcf_ablation_variant2_validation.md`  
**Related Qwen review:** `docs/reviews/v010_density_matched_ablation_variant2_qwen_review.md`  
**Tool:** `tools/ablate_density_variant2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Execution summary

Command executed locally:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf_full --out-prefix v010_lcf_constrained_ablation_variant2
```

Generated outputs:

```text
outputs/raw_v010_lcf_constrained_ablation_variant2.csv
outputs/summary_v010_lcf_constrained_ablation_variant2.csv
outputs/per_seed_v010_lcf_constrained_ablation_variant2.csv
outputs/reason_counts_v010_lcf_constrained_ablation_variant2.csv
```

Working tree after run:

```text
git status --short: clean
```

Generated outputs are local artifacts and are not committed.

---

## 2. Purpose

This experiment was designed after the preliminary random-removal density ablation.

The random-removal ablation matched edge counts exactly but severely fragmented compensated graphs:

```text
random-removal target_edge_count=25:
    structure_success = 0.345
    largest_component_fraction = 0.307

uncompensated beta=0.003 reference:
    structure_success = 0.52
    largest_component_fraction approx 0.949
```

Qwen classified random removal as a useful non-final stress test and required a topology-preserving / LCF-constrained ablation.

This experiment tests whether compensated Variant 2 graphs can be matched to low edge counts while preserving largest-component connectivity.

Primary valid-row definition:

```text
valid_lcf_matched = target_reached AND target_connectivity_preserved
```

where:

```text
target_reached = actual_edge_count == target_edge_count
target_connectivity_preserved = largest_component_fraction >= 0.85
```

---

## 3. Experimental settings

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
```

Expected maximum raw rows:

```text
100 seeds x 3 target_edge_counts x 5 repetitions = 1500 rows
```

Observed:

```text
raw rows = 1500
valid_lcf_matched rows = 320
```

---

## 4. Summary result

From `outputs/summary_v010_lcf_constrained_ablation_variant2.csv`:

| target_edge_count | attempted_runs | target_reached_rate | connectivity_preserved_rate | valid_lcf_matched_rate | valid rows | structure_success_valid | mean_actual_edge_count_valid | mean_LCF_valid | mean_n_components_valid | failed_p_gnp_rate_valid | failed_p_dp_rate_valid |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 500 | 0.06 | 0.99 | 0.06 | 30 | 0.000 | 25.0 | 1.0 | 1.0 | 1.000 | 0.900 |
| 30 | 500 | 0.21 | 0.99 | 0.21 | 105 | 0.238 | 30.0 | 1.0 | 1.0 | 0.752 | 0.695 |
| 35 | 500 | 0.37 | 0.99 | 0.37 | 185 | 0.411 | 35.0 | 1.0 | 1.0 | 0.584 | 0.503 |

Reference from `confirm_connectivity_variant2`:

```text
uncompensated beta=0.003 structure_success = 0.52
uncompensated beta=0.003 LCF approx 0.949
uncompensated beta=0.003 edge_count approx 25
```

Primary observation:

```text
LCF is preserved in almost all attempts, but low edge-count targets are often not reachable under the non-bridge / LCF-constrained removal rule.
```

---

## 5. Reason counts

From `outputs/reason_counts_v010_lcf_constrained_ablation_variant2.csv`:

| target_edge_count | failed_no_non_bridge_edges | failed_max_attempts | preserved |
|---:|---:|---:|---:|
| 25 | 465 | 5 | 30 |
| 30 | 390 | 5 | 105 |
| 35 | 310 | 5 | 185 |

Dominant reason:

```text
failed_no_non_bridge_edges
```

Rates:

```text
target 25: 465/500 = 0.93
target 30: 390/500 = 0.78
target 35: 310/500 = 0.62
```

Interpretation:

```text
The graph often cannot be reduced to the requested low edge count using non-bridge removal while keeping the largest component preserved.
```

This is not a hidden implementation failure. It is a structural outcome of the constrained ablation.

---

## 6. Target-level interpretation

### target_edge_count = 25

Result:

```text
valid_lcf_matched_rate = 0.06
structure_success_valid = 0.000
mean_LCF_valid = 1.0
failed_no_non_bridge_edges_rate = 0.93
```

Interpretation:

```text
Strict matching to edge_count=25 while preserving LCF is rarely feasible under the current non-bridge rule. Among feasible valid rows, structure_success does not recover and remains below the uncompensated reference.
```

Classification:

```text
infeasible / negative under current LCF-constrained method
```

### target_edge_count = 30

Result:

```text
valid_lcf_matched_rate = 0.21
structure_success_valid = 0.238
mean_LCF_valid = 1.0
failed_no_non_bridge_edges_rate = 0.78
```

Interpretation:

```text
Target 30 is more feasible than target 25 but still strongly constrained. The valid-row success rate remains below the uncompensated reference.
```

Classification:

```text
low-feasibility negative / weak
```

### target_edge_count = 35

Result:

```text
valid_lcf_matched_rate = 0.37
structure_success_valid = 0.411
mean_LCF_valid = 1.0
failed_no_non_bridge_edges_rate = 0.62
```

Interpretation:

```text
Target 35 has partial feasibility and partial recovery, but still does not exceed the uncompensated beta=0.003 reference of 0.52.
```

Classification:

```text
partial feasibility but below reference
```

---

## 7. Main interpretation

The LCF-constrained ablation shifts the blocker from fragmentation to structural feasibility.

Previous random-removal result:

```text
edge count can be matched exactly, but LCF collapses.
```

Current LCF-constrained result:

```text
LCF can be preserved, but low edge-count targets are often unreachable.
```

Therefore:

```text
low edge-count matching and largest-component preservation are jointly difficult for compensated Variant 2 graphs.
```

This suggests a minimum-connectivity / non-bridge-edge constraint rather than a clean density-independent compensation mechanism.

---

## 8. Claim impact

### What this result supports

```text
1. Naive density matching is insufficient.
2. Topology-preserving density matching reveals strong structural constraints.
3. The Variant 2 signal is strongly connectivity-dependent.
4. Strict edge_count approx 25 matching with LCF preservation is rarely feasible under greedy non-bridge removal.
5. Valid LCF-matched rows do not show success above the uncompensated beta=0.003 reference.
```

### What this result does not support

```text
1. It does not support a stronger mechanism claim.
2. It does not confirm beta=0.003 as clean after density/LCF control.
3. It does not support preprint-level claims that density confounding is resolved in favor of compensation.
4. It does not prove that the original effect is purely an artifact, because only one topology-preserving removal heuristic was tested.
```

---

## 9. Status of beta=0.003

Previous status after `confirm_connectivity_variant2`:

```text
leading clean positive candidate, pending density/edge-count ablation
```

After random-removal density ablation:

```text
unresolved but not weakened, because random removal introduced severe fragmentation
```

After LCF-constrained ablation:

```text
weakened / unresolved; no longer eligible for clean-candidate wording without qualification
```

Proposed updated status:

```text
connectivity-threshold-dependent candidate
```

Rationale:

```text
The signal appears to require sufficient connectivity. When low-edge matching is attempted while preserving LCF, valid rows are scarce and structure_success remains below the reference.
```

---

## 10. Conservative conclusion

Pre-review conclusion:

```text
The LCF-constrained ablation preserves largest-component connectivity but shows that strict low-edge matching is often infeasible under greedy non-bridge removal. At target_edge_count=25, only 6% of attempts produce valid LCF-matched rows, and these rows have structure_success=0.0. At target_edge_count=30 and 35, feasibility improves but valid-row structure_success remains below the uncompensated beta=0.003 reference. The result does not confirm beta=0.003 as a clean density-independent compensation signal. It suggests that the Variant 2 effect is strongly connectivity-threshold dependent. However, because only one LCF-constrained heuristic was tested, the mechanism should not be declared refuted without external review and possible degree-aware follow-up.
```

---

## 11. Next review step

Submit this result to Qwen for methodological review.

Questions for Qwen:

```text
1. Does this LCF-constrained result downgrade beta=0.003 from leading clean candidate to connectivity-threshold-dependent candidate?
2. Should the low valid_lcf_matched_rate be interpreted as structural infeasibility or as a limitation of the greedy non-bridge heuristic?
3. Does the lack of success above the 0.52 reference among valid rows block preprint-level mechanism claims?
4. Is another degree-aware / distribution-matched method justified, or should the result be reframed as connectivity-dependent rather than density-independent?
5. What conservative wording is now justified?
```

No stronger claim should be made before Qwen review.
