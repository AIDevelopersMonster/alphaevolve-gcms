# Qwen Review: v010_density_matched_ablation_variant2_random_preliminary

**Status:** external methodological review  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment:** `density_matched_ablation_variant2`  
**Subsampling method:** `random_edge_removal_preliminary`  
**Reviewed result note:** `docs/results/v010_density_matched_ablation_variant2_random_preliminary.md`  
**Reviewer role:** Independent methodological reviewer, computational statistics / complex systems  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Overall classification

Qwen classified the result as:

```text
Useful non-final random-removal stress test
```

It should not be treated as a failed technical ablation, because edge-count targets were reached exactly.

It should also not be treated as final density-confound isolation, because random removal introduced a stronger fragmentation confound.

---

## 2. Answers to core review questions

### 2.1 Failed ablation or useful stress test?

Qwen answer:

```text
Useful non-final random-removal stress test.
```

Reason:

```text
The technical implementation succeeded: target_reached_rate = 1.0 and exact edge-count matching was achieved.
However, random_edge_removal introduced severe graph fragmentation, especially at target_edge_count = 25.
```

Qwen interprets this as failure of the naive assumption that edge-count matching alone is sufficient.

---

### 2.2 Does target 25 weaken beta=0.003?

Qwen answer:

```text
No, not directly; the comparison is invalid because topology is not matched.
```

Reference:

```text
uncompensated beta=0.003:
    structure_success = 0.52
    LCF approx 0.949
    n_components approx 1.01

random-removal compensated target 25:
    structure_success = 0.345
    LCF = 0.307
    n_components approx 19.6
```

Qwen states that the fall to 0.345 cannot be interpreted as refuting the original beta=0.003 signal because the comparison is between a connected graph and a heavily fragmented graph.

---

### 2.3 Is LCF=0.307 a new confound?

Qwen answer:

```text
Yes. It is a more serious confound than the original edge-count gap.
```

Reason:

```text
The original problem was density difference: compensated graphs had more edges.
The new problem is that edge count is matched but largest component fraction collapses to 0.307 versus 0.949 in the reference.
```

Therefore, the comparison `0.345 vs 0.52` is not statistically valid without controlling LCF and component structure.

---

### 2.4 Is topology-preserving ablation now mandatory?

Qwen answer:

```text
Yes. Connectivity-preserving / degree-aware / LCF-constrained removal is now mandatory before mechanistic claims.
```

Recommended constraints:

```yaml
next_ablation_method: connectivity_preserving_edge_removal_preliminary
required_constraints:
  - target_edge_count_reached: true
  - largest_component_fraction_min: 0.85
  - avoid_disconnecting_largest_component: true
  - degree_distribution_KS_distance_max: 0.15
  - report_target_connectivity_preserved: true
```

Recommended method priority:

```text
1. LCF-constrained edge removal
2. Degree-aware removal
3. Connectivity-preserving non-bridge removal
4. Degree-distribution matching
```

---

### 2.5 Conservative wording

Qwen recommends wording equivalent to:

```text
A preliminary random-removal ablation exactly matched edge counts but caused substantial fragmentation in compensated graphs. This makes direct comparison of structure_success statistically invalid. The result shows that the Variant 2 signal is strongly sensitive to connectivity, and that naive edge removal is too destructive for valid density-confound isolation. beta=0.003 remains the leading clean candidate, but final resolution requires topology-preserving ablation such as LCF-constrained or degree-aware edge removal.
```

---

## 3. Status table

| Aspect | Qwen status | Comment |
|---|---|---|
| Technical ablation implementation | Successful | Exact target edge-count matching and reproducibility |
| Density-confound isolation | Failed / unresolved | A stronger fragmentation confound was introduced |
| Interpretation of 0.345 vs 0.52 | Not valid | LCF difference dominates comparison |
| beta=0.003 clean-candidate status | Unresolved but not weakened | Requires topology-preserving ablation |
| Preprint readiness | Blocked | Connectivity-preserving ablation required |

---

## 4. Recommended next experiment

Qwen recommends:

```yaml
experiment: lcf_constrained_ablation_variant2_beta0.003
goal: isolate edge-count effect while preserving graph connectivity
design:
  relation_variant: 2
  model_mode: compensated
  beta: 0.003
  seeds: 100
  target_edge_counts: [25, 30, 35]
  removal_method: greedy_non_bridge_removal_with_LCF_constraint
  LCF_min_threshold: 0.85
  max_attempts_per_seed: 100
  repetitions: 5
required_outputs:
  - structure_success_rate_LCF_constrained
  - actual_LCF_distribution
  - actual_degree_variance_vs_reference
  - connectivity_preservation_rate
  - comparison_to_uncompensated_reference:
      effect_size
      McNemar_p
      LCF_difference
```

Primary analysis:

```text
Check whether positive compensation effect persists at matched edge count and LCF >= 0.85.
```

Preprint-level success criteria proposed by Qwen:

```text
1. compensation_effect_attempted remains positive and statistically significant at edge_count approx 25 and LCF >= 0.85;
2. LCF differs from reference by no more than 0.10;
3. no more than 20% of removal attempts fail due to inability to preserve connectivity.
```

---

## 5. Final Qwen assessment

Qwen's final assessment:

```text
The preliminary random-removal ablation is a valuable stress test that clarified the limits of naive density matching. It does not refute the beta=0.003 signal, but it requires one final topology-preserving ablation before mechanistic claims or preprint submission.
```

---

## 6. Delta-D0 action interpretation

Accepted from Qwen:

```text
1. The random-removal ablation was technically successful.
2. It did not isolate the density confound because it introduced severe fragmentation.
3. beta=0.003 remains unresolved but not downgraded.
4. Preprint-level claims remain blocked.
5. The next required experiment is topology-preserving ablation.
```

Next required document:

```text
docs/experiments/lcf_constrained_ablation_variant2_design.md
```

No stronger scientific claim should be made before that ablation.
