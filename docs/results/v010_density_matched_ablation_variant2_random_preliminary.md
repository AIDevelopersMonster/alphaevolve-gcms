# Result Note: v010_density_matched_ablation_variant2_random_preliminary

**Status:** preliminary result note / not final density-matched proof  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `density_matched_ablation_variant2`  
**Subsampling method:** `random_edge_removal_preliminary`  
**Design checkpoint:** `docs/experiments/density_matched_ablation_variant2_design.md`  
**Extension plan:** `docs/experiments/density_matched_ablation_variant2_extension_plan.md`  
**Related Qwen review:** `docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md`  
**Tool:** `tools/ablate_density_variant2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Execution summary

Command executed locally:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode full --out-prefix v010_density_matched_ablation_variant2
```

Generated outputs:

```text
outputs/raw_v010_density_matched_ablation_variant2.csv
outputs/summary_v010_density_matched_ablation_variant2.csv
outputs/per_seed_v010_density_matched_ablation_variant2.csv
```

Working tree after run:

```text
git status --short: clean
```

Generated outputs are local artifacts and are not committed.

---

## 2. Purpose of this ablation

The experiment tests the core remaining blocker identified after `confirm_connectivity_variant2`:

```text
Density/edge-count confound.
```

Reference values from `confirm_connectivity_variant2`:

```text
compensated beta=0.003 structure_success attempted = 0.72
uncompensated beta=0.003 structure_success attempted = 0.52
uncompensated beta=0.003 mean edge count approx 25
uncompensated beta=0.003 largest_component_fraction approx 0.949
```

This ablation reduces compensated graphs to target edge counts:

```text
25, 30, 35, 40
```

and recomputes structure and connectivity diagnostics.

---

## 3. Technical integrity checks

The run produced:

```text
4000 raw rows
100 seeds x 4 target_edge_counts x 10 repetitions = 4000
```

Reachability check:

| target_edge_count | rows | target_reached_count | target_reached_rate | actual_edge_count min | mean | max |
|---:|---:|---:|---:|---:|---:|---:|
| 25 | 1000 | 1000 | 1.0 | 25 | 25.0 | 25 |
| 30 | 1000 | 1000 | 1.0 | 30 | 30.0 | 30 |
| 35 | 1000 | 1000 | 1.0 | 35 | 35.0 | 35 |
| 40 | 1000 | 1000 | 1.0 | 40 | 40.0 | 40 |

Per-seed aggregation check:

| target_edge_count | per-seed rows | unique seeds |
|---:|---:|---:|
| 25 | 100 | 100 |
| 30 | 100 | 100 |
| 35 | 100 | 100 |
| 40 | 100 | 100 |

Conclusion:

```text
The tool successfully performs exact target edge-count matching for all requested targets.
```

---

## 4. Main summary result

From `outputs/summary_v010_density_matched_ablation_variant2.csv`:

| target_edge_count | structure_success_rate_reached | mean_actual_edge_count | mean_original_edge_count | mean_sector_size | mean_largest_component_fraction | mean_n_components | failed_p_gnp_rate | failed_p_dp_rate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 25 | 0.345 | 25.0 | 65.29 | 42.56 | 0.307 | 19.621 | 0.610 | 0.602 |
| 30 | 0.496 | 30.0 | 65.29 | 42.56 | 0.391 | 16.135 | 0.453 | 0.432 |
| 35 | 0.688 | 35.0 | 65.29 | 42.56 | 0.478 | 13.107 | 0.292 | 0.258 |
| 40 | 0.814 | 40.0 | 65.29 | 42.56 | 0.573 | 10.384 | 0.169 | 0.135 |

Observed trend:

```text
As target_edge_count increases, structure_success increases monotonically:
25 -> 30 -> 35 -> 40
0.345 -> 0.496 -> 0.688 -> 0.814
```

---

## 5. Per-seed majority result

From `outputs/per_seed_v010_density_matched_ablation_variant2.csv`:

| target_edge_count | majority_success seeds | majority_success_rate | mean success_fraction_per_seed | min | max |
|---:|---:|---:|---:|---:|---:|
| 25 | 14/100 | 0.14 | 0.345 | 0.0 | 1.0 |
| 30 | 38/100 | 0.38 | 0.496 | 0.1 | 1.0 |
| 35 | 77/100 | 0.77 | 0.688 | 0.2 | 1.0 |
| 40 | 91/100 | 0.91 | 0.814 | 0.3 | 1.0 |

Important note:

```text
Per-seed majority_success is stricter than raw repetition-level success.
It confirms that target 25 is weak under random removal, while targets 35 and 40 are strong.
```

---

## 6. Connectivity problem introduced by random removal

The key issue is that random edge removal strongly fragments the compensated graphs.

Mean largest component fraction by target:

| target_edge_count | mean LCF | min LCF | max LCF |
|---:|---:|---:|---:|
| 25 | 0.307 | 0.117 | 0.733 |
| 30 | 0.391 | 0.140 | 0.913 |
| 35 | 0.478 | 0.177 | 0.963 |
| 40 | 0.573 | 0.205 | 1.000 |

Reference uncompensated beta=0.003 LCF from `confirm_connectivity_variant2`:

```text
0.949
```

Therefore, although the ablation matches edge count exactly, it does not match connectivity topology.

At the primary target edge count:

```text
uncompensated beta=0.003 reference:
    edge_count approx 25
    structure_success = 0.52
    largest_component_fraction approx 0.949

random-removal compensated target 25:
    edge_count = 25
    structure_success = 0.345
    largest_component_fraction approx 0.307
```

This means the random-removal ablation introduces a new fragmentation confound.

---

## 7. Preliminary interpretation

### What the result supports

The result supports:

```text
1. Edge count / density / connectivity are major drivers of structure_success.
2. The Variant 2 compensation signal is strongly connectivity-sensitive.
3. Naive random edge matching is too destructive to serve as final density-matched proof.
4. A more topology-preserving ablation is required.
```

### What the result does not support

The result does not support:

```text
1. A stronger mechanism claim.
2. A preprint-level claim that density confounding is resolved.
3. A conclusion that beta=0.003 compensation signal is independent of edge count.
4. A conclusion that the original effect was purely an edge-count artifact.
```

Why not purely an artifact?

```text
Because the random-removal comparison matches edge count but severely mismatches largest_component_fraction and component structure.
The test is therefore not an equal-topology comparison.
```

---

## 8. Classification of target levels

### target_edge_count = 25

Classification:

```text
strict edge-match / severe random-removal fragmentation
```

Result:

```text
structure_success = 0.345 < uncompensated reference 0.52
mean LCF = 0.307 << uncompensated reference 0.949
```

Interpretation:

```text
The compensation advantage does not survive naive random removal to 25 edges, but the comparison is confounded by severe fragmentation.
```

### target_edge_count = 30

Classification:

```text
near-reference edge count / still highly fragmented
```

Result:

```text
structure_success = 0.496 approx uncompensated reference 0.52
mean LCF = 0.391
```

Interpretation:

```text
The signal is near reference but remains confounded by fragmentation.
```

### target_edge_count = 35

Classification:

```text
partial recovery / still connectivity-impaired
```

Result:

```text
structure_success = 0.688 > uncompensated reference 0.52
mean LCF = 0.478
```

Interpretation:

```text
The signal returns at 35 edges, but topology remains worse than the uncompensated reference.
```

### target_edge_count = 40

Classification:

```text
high-edge recovery / not matched to uncompensated edge count
```

Result:

```text
structure_success = 0.814 > uncompensated reference 0.52
mean LCF = 0.573
```

Interpretation:

```text
The compensated graph performs strongly at 40 edges, but this target no longer matches the primary uncompensated edge-count regime.
```

---

## 9. Methodological limitation

The method used here is:

```text
random_edge_removal_preliminary
```

This is a useful stress test but not a final density-matched ablation.

Reason:

```text
Random edge removal can destroy connectivity far more than the natural uncompensated process does.
```

Therefore, the result should be described as:

```text
preliminary random-removal density ablation
```

not as:

```text
final edge-matched ablation
```

---

## 10. Next required experiment

The next required method is:

```text
connectivity-preserving / degree-aware edge removal
```

Candidate constraints:

```text
1. target edge count must still be reached;
2. largest_component_fraction should be preserved as much as possible;
3. avoid disconnecting the largest component where possible;
4. optionally preserve or approximate degree distribution;
5. report target_reached and target_connectivity_preserved separately.
```

Possible method names:

```text
connectivity_preserving_edge_removal_preliminary
degree_aware_edge_removal_preliminary
lcf_constrained_edge_removal_preliminary
```

Recommended next design checkpoint:

```text
docs/experiments/connectivity_preserving_density_ablation_variant2_design.md
```

---

## 11. Conservative conclusion

Pre-review conclusion:

```text
The preliminary random-removal density ablation successfully matches target edge counts but also introduces severe fragmentation, especially at the primary target edge_count=25. At this strict edge match, the subsampled compensated success rate falls below the uncompensated beta=0.003 reference, suggesting that the Variant 2 signal is strongly connectivity-sensitive. However, because random removal reduces largest_component_fraction far below the uncompensated reference, the result cannot be interpreted as a final density-matched mechanism test. The appropriate conclusion is that naive edge-count matching is insufficient; a connectivity-preserving or degree-aware ablation is now required.
```

---

## 12. Next review step

Submit this result to Qwen with emphasis on:

```text
1. exact edge-count matching succeeded;
2. target 25 did not preserve the compensation advantage;
3. random removal severely fragmented graphs;
4. LCF mismatch prevents final interpretation;
5. request whether connectivity-preserving / degree-aware ablation is the correct next blocker.
```

No stronger claim should be made before external review.
