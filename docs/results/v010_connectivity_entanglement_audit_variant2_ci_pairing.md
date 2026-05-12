# Result Note: v010_connectivity_entanglement_audit_variant2_ci_pairing

**Status:** post-processing result note / pre-draft statistical strengthening  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Parent experiment:** `v010_connectivity_entanglement_audit_variant2`  
**Parent result note:** `docs/results/v010_connectivity_entanglement_audit_variant2.md`  
**Parent Qwen review:** `docs/reviews/v010_connectivity_entanglement_audit_variant2_qwen_review.md`  
**Extension plan:** `docs/experiments/connectivity_entanglement_audit_variant2_ci_pairing_extension.md`  
**Post-processing tool:** `tools/postprocess_connectivity_audit_ci_pairing.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This note records the minimal statistical strengthening requested by Qwen after review of `v010_connectivity_entanglement_audit_variant2`.

Qwen accepted the full audit as a valid confound-isolation / topology-threshold diagnostic, but required the following additions before technical draft:

```text
1. paired seed analysis;
2. bootstrap confidence interval for the post-hoc threshold contrast;
3. Wilson confidence intervals for rates.
```

This is post-processing only.

No simulations were rerun.
No pruning was performed.
No edge-removal rescue logic was introduced.
No success criteria were changed.

---

## 2. Inputs

Post-processing used existing parent audit outputs:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
```

Primary descriptor:

```text
non_bridge_edge_count
```

Primary exploratory threshold:

```text
non_bridge_edge_count >= 19
```

This threshold is post-hoc and was identified on the same parent-audit data. It is not treated as mechanistic or universal.

---

## 3. Generated outputs

Post-processing outputs:

```text
outputs/paired_seed_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/wilson_cis_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/bootstrap_ci_non_bridge_ge19_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

Generated outputs remain local artifacts and are not committed by default.

---

## 4. Paired seed analysis

The paired analysis compares compensated and uncompensated runs for the same seed.

Key paired deltas from `outputs/paired_seed_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv`:

| metric | mean_delta | median_delta | positive | negative | zero | positive_fraction |
|---|---:|---:|---:|---:|---:|---:|
| delta_edge_count | 19.61 | 22.5 | 82 | 17 | 1 | 0.82 |
| delta_non_bridge_edge_count | 15.70 | 16.0 | 80 | 18 | 2 | 0.80 |
| delta_cycle_rank | 7.93 | 8.0 | 80 | 18 | 2 | 0.80 |
| delta_largest_component_cycle_rank | 7.78 | 8.0 | 79 | 19 | 2 | 0.79 |
| delta_sector_size | 11.69 | 11.0 | 83 | 16 | 1 | 0.83 |
| delta_structure_success | 0.19 | 0.0 | 32 | 13 | 55 | 0.32 |

Paired success counts:

```text
compensated_only_success_count = 32
uncompensated_only_success_count = 13
both_success_count = 40
both_failure_count = 15
paired_success_delta_mean = 0.19
```

Interpretation:

```text
The compensated mode has systematically higher native topology capacity across paired seeds: non_bridge_edge_count, cycle_rank, LCC cycle rank, and sector_size are positive in approximately 79-83% of paired comparisons.
```

The binary success comparison is weaker than topology deltas but still directionally favorable:

```text
32 compensated-only successes vs 13 uncompensated-only successes.
```

---

## 5. Wilson confidence intervals

Wilson score intervals were computed at 95% CI.

From `outputs/wilson_cis_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv`:

| group | subgroup | success_count | n | rate | ci_low | ci_high |
|---|---|---:|---:|---:|---:|---:|
| model_mode | compensated | 72 | 100 | 0.720 | 0.625 | 0.799 |
| model_mode | uncompensated | 53 | 100 | 0.530 | 0.433 | 0.625 |
| non_bridge_edge_count_threshold | >=19 | 103 | 105 | 0.981 | 0.933 | 0.995 |
| non_bridge_edge_count_threshold | <19 | 22 | 95 | 0.232 | 0.158 | 0.326 |
| failed_p_gnp | compensated | 17 | 100 | 0.170 | 0.109 | 0.255 |
| failed_p_gnp | uncompensated | 43 | 100 | 0.430 | 0.337 | 0.528 |
| failed_p_dp | compensated | 16 | 100 | 0.160 | 0.101 | 0.244 |
| failed_p_dp | uncompensated | 32 | 100 | 0.320 | 0.237 | 0.417 |

Interpretation:

```text
The model-mode structure_success intervals overlap only near the boundary, while the threshold groups show a large separation: >=19 non-bridge edges has Wilson CI [0.933, 0.995], while <19 has Wilson CI [0.158, 0.326].
```

This supports reporting the threshold contrast descriptively, with the required post-hoc warning.

---

## 6. Bootstrap confidence interval for threshold difference

Bootstrap settings:

```text
threshold_type = non_bridge_edge_count_threshold
threshold_value = 19
iterations = 1000
random_seed = 20260512
ci_level = 0.95
resampling_unit = row
note = post_hoc_threshold_same_data_exploratory
```

From `outputs/bootstrap_ci_non_bridge_ge19_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv`:

```text
above_n = 105
above_success_count = 103
above_rate = 0.9809523809523809

below_n = 95
below_success_count = 22
below_rate = 0.23157894736842105

rate_difference = 0.7493734335839599
bootstrap_ci_low = 0.6556390977443609
bootstrap_ci_high = 0.8335839598997493
```

Interpretation:

```text
The observed post-hoc threshold contrast is large: rows with non_bridge_edge_count >= 19 have an approximately 0.75 higher structure_success rate than rows below the threshold, with bootstrap 95% CI approximately [0.656, 0.834].
```

Caveat:

```text
The threshold was selected on the same data, so this interval quantifies uncertainty of the observed contrast but does not validate the threshold as universal or mechanistic.
```

---

## 7. Relation to Qwen requirements

Qwen requested:

```text
1. paired seed analysis;
2. bootstrap CI for threshold proportions;
3. Wilson or exact CI for rates.
```

This extension satisfies the minimal pre-draft requirements:

```text
paired seed analysis: complete
Wilson CIs: complete
bootstrap CI for threshold contrast: complete
```

Qwen also required:

```text
non_bridge_edge_count as primary descriptor;
cycle_rank as secondary / confirmatory;
threshold >=19 only as post-hoc exploratory;
passive diagnostics as exploratory/control-only.
```

This note follows those constraints.

---

## 8. Conservative interpretation

Allowed conclusion:

```text
The CI/pairing extension strengthens the descriptive evidence for compensation-connectivity entanglement. Across paired seeds, compensated runs more often produce higher non_bridge_edge_count, cycle_rank, LCC cycle rank, and sector_size. The post-hoc non_bridge_edge_count >= 19 split shows a large success-rate contrast with Wilson and bootstrap uncertainty estimates. This supports the topology-threshold framing for the toy model.
```

Forbidden conclusion:

```text
The non_bridge_edge_count >= 19 threshold is universal.
The threshold is causal.
The compensation mechanism is proven.
The density-independent claim is restored.
This has direct physical relevance.
```

---

## 9. Current status

After this extension:

```text
Full audit result: externally reviewed.
Qwen-required minimal post-processing: completed.
Primary descriptor: non_bridge_edge_count.
Primary threshold: non_bridge_edge_count >= 19, post-hoc exploratory only.
Technical/confound-isolation draft: now methodologically permitted as a conservative toy-model report.
```

Remaining optional additions before a fuller paper:

```text
1. logistic / collinearity-aware analysis;
2. threshold variation 0.70-0.80;
3. beta 0.004 / 0.005 stability check;
4. N=100/200 cross-check.
```

These are not required for the first technical/confound-isolation draft according to the Qwen review.

---

## 10. Next step

Prepare technical-note outline:

```text
docs/papers/connectivity_entanglement_confound_isolation_outline.md
```

Framing:

```text
confound-isolation / topology-threshold diagnostic in a computational toy model
```

Not framing:

```text
mechanism proof
physical theory claim
density-independent compensation proof
```
