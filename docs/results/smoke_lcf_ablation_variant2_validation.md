# Smoke Validation: lcf_constrained_ablation_variant2

**Status:** smoke validation / not full experiment  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Mode:** `lcf_smoke`  
**Tool:** `tools/ablate_density_variant2.py`  
**Related design checkpoint:** `docs/experiments/lcf_constrained_ablation_variant2_design.md`  
**Related Qwen review:** `docs/reviews/v010_density_matched_ablation_variant2_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This note validates the new `lcf_smoke` mode before any full-scale LCF-constrained ablation.

The purpose is not to interpret scientific effect size, but to verify that the tool can explicitly distinguish:

```text
target_reached
target_connectivity_preserved
valid_lcf_matched = target_reached AND target_connectivity_preserved
```

This follows the conclusion from the previous random-removal ablation:

```text
Edge count alone was not enough.
The next test must match edge count without destroying the largest component.
```

---

## 2. Code state

The LCF smoke mode was implemented and committed:

```text
32f145e Add LCF constrained ablation smoke mode
```

Recent commit context:

```text
32f145e Add LCF constrained ablation smoke mode
5e4c521 Add LCF constrained ablation design checkpoint
9859339 Add Qwen review for preliminary density matched ablation
2106c66 Add Qwen prompt for density matched ablation review
7883623 Add preliminary density matched ablation result note
```

---

## 3. Smoke command

Command executed locally:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf_smoke --out-prefix smoke_lcf_ablation_variant2
```

Generated outputs:

```text
outputs/raw_smoke_lcf_ablation_variant2.csv
outputs/summary_smoke_lcf_ablation_variant2.csv
outputs/per_seed_smoke_lcf_ablation_variant2.csv
```

---

## 4. Summary output

From `outputs/summary_smoke_lcf_ablation_variant2.csv`:

| target_edge_count | attempted_runs_all | target_reached_count | target_reached_rate | target_connectivity_preserved_count | target_connectivity_preserved_rate | valid_lcf_matched_count | valid_lcf_matched_rate | mean_actual_edge_count_valid | mean_LCF_valid | structure_success_rate_valid |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 4 | 2 | 0.5 | 4 | 1.0 | 2 | 0.5 | 25.0 | 1.0 | 0.0 |
| 30 | 4 | 2 | 0.5 | 4 | 1.0 | 2 | 0.5 | 30.0 | 1.0 | 0.0 |

Interpretation:

```text
The smoke mode successfully reports separate reachability and connectivity-preservation outcomes.
It produces valid LCF-matched rows where both edge-count and LCF constraints hold.
It also explicitly records cases where LCF is preserved but target edge count cannot be reached.
```

---

## 5. Raw row inspection

Observed rows:

```text
seed=0, target=25: actual_edge_count=25, original_edge_count=34, target_reached=True, target_connectivity_preserved=True, valid_lcf_matched=True, reason=preserved, LCF=1.0
seed=0, target=30: actual_edge_count=30, original_edge_count=34, target_reached=True, target_connectivity_preserved=True, valid_lcf_matched=True, reason=preserved, LCF=1.0
seed=3, target=25: actual_edge_count=39, original_edge_count=58, target_reached=False, target_connectivity_preserved=True, valid_lcf_matched=False, reason=failed_no_non_bridge_edges, LCF=1.0
seed=3, target=30: actual_edge_count=39, original_edge_count=58, target_reached=False, target_connectivity_preserved=True, valid_lcf_matched=False, reason=failed_no_non_bridge_edges, LCF=1.0
```

This is methodologically useful:

```text
For seed 0, the tool can satisfy both constraints.
For seed 3, the tool preserves connectivity but cannot reach the target edge count under the current non-bridge / LCF-constrained method.
```

The second case is not a failure to be hidden. It is a valid smoke result showing that strict edge-count matching under connectivity preservation can be infeasible for some graph topologies.

---

## 6. Per-seed output

From `outputs/per_seed_smoke_lcf_ablation_variant2.csv`:

| target_edge_count | seed | connectivity_preservation_fraction | valid_repetitions | success_count_valid | success_fraction_valid | mean_LCF_valid | mean_sector_size_valid |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 0 | 1.0 | 2 | 0 | 0.0 | 1.0 | 24.0 |
| 25 | 3 | 1.0 | 0 | 0 | 0.0 | 0.0 | 0.0 |
| 30 | 0 | 1.0 | 2 | 0 | 0.0 | 1.0 | 24.0 |
| 30 | 3 | 1.0 | 0 | 0 | 0.0 | 0.0 | 0.0 |

Important interpretation:

```text
Per-seed aggregation is present and does not treat repetitions as independent seeds.
Seeds with zero valid repetitions are explicitly represented.
```

---

## 7. Validation result

The smoke validation passes for implementation safety:

```text
lcf_smoke mode exists;
raw, summary, and per_seed outputs are produced;
target_connectivity_preserved is reported;
connectivity_preservation_reason is reported;
valid_lcf_matched is reported;
valid rows require both target_reached and target_connectivity_preserved;
old smoke mode still works;
no full LCF run was executed.
```

Scientific interpretation remains blocked because this is only a smoke run.

---

## 8. Important observation for full design

The smoke result already suggests a key risk for full LCF-constrained ablation:

```text
Some graphs may preserve LCF but fail to reach low target_edge_count because no removable non-bridge edges remain.
```

This is not an error.

It implies that full LCF ablation must report:

```text
valid_lcf_matched_rate;
target_reached_rate;
target_connectivity_preserved_rate;
connectivity_preservation_reason distribution;
failed_no_non_bridge_edges rate;
```

If target 25 is often infeasible, that becomes a meaningful result about minimum connectivity / density requirements.

---

## 9. Next required step

Before full LCF ablation, create an extension plan that specifies:

```text
1. full LCF settings;
2. allowed failure reasons;
3. how infeasible target rows are handled;
4. how valid rows are compared against the uncompensated beta=0.003 reference;
5. how per-seed aggregation is performed;
6. explicit prohibition on treating repetitions as independent seeds.
```

Suggested next document:

```text
docs/experiments/lcf_constrained_ablation_variant2_extension_plan.md
```

No full LCF run should be launched before that extension plan.

---

## 10. Short conclusion

```text
LCF smoke mode is technically valid.
It demonstrates that edge-count matching under LCF preservation is feasible for some seeds and infeasible for others.
This is exactly the distinction required before a full topology-preserving ablation.
```
