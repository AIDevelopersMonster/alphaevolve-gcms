# Release Summary: Connectivity Entanglement Confound-Isolation v0.1

**Status:** release-summary / README-style navigation note  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Manuscript:** `docs/papers/connectivity_entanglement_confound_isolation_v0_1.md`  
**Final wording check:** `docs/reviews/connectivity_entanglement_confound_isolation_v0_1_final_wording_check.md`  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. What this release is

This v0.1 package records a completed experimental branch of GCMS-D0 Variant 2 at `beta=0.003`.

It is a conservative technical note about a computational toy model.

It documents a confound-isolation sequence that moved the project from an initially positive but topology-confounded result to a weaker, reproducible, and methodologically safer interpretation:

```text
compensation-connectivity empirical coupling
```

This release is not a physical theory paper and does not claim a causal mechanism.

---

## 2. One-paragraph summary

An initial Variant 2 experiment showed higher `structure_success` for compensated graphs than for an uncompensated reference at `beta=0.003`. Follow-up controls showed that this positive signal was not density-independent. Random edge removal matched edge counts but fragmented the graphs; LCF-constrained non-bridge removal preserved largest-component structure but made strict low-edge matching often infeasible. The project therefore reframed the result as a native-topology question. A topology audit showed that compensated graphs co-occur with higher `non_bridge_edge_count`, `cycle_rank`, and largest-component cycle rank, and these descriptors are associated with `structure_success`. The final interpretation is a conservative confound-isolation result: compensated Variant 2 at `beta=0.003` is a connectivity-threshold-dependent study regime, not a density-independent mechanism proof.

---

## 3. Core claim boundary

Allowed core claim:

```text
In this toy model, compensated Variant 2 at beta=0.003 is best interpreted as a connectivity-threshold-dependent study regime. The apparent compensated advantage is empirically coupled to native topological capacity, especially non_bridge_edge_count and cycle_rank. This supports a confound-isolation / topology-threshold framing, not a density-independent proof.
```

Forbidden claims:

```text
compensation causes structure;
density-independent mechanism confirmed;
non_bridge_edge_count >= 19 is universal;
threshold >=19 is mechanistic;
physical relevance;
claims about real constants, spacetime, gravity, photons, or cosmology.
```

---

## 4. Main evidence chain

### 4.1 Initial signal

```text
compensated beta=0.003 structure_success = 0.72
uncompensated beta=0.003 structure_success = 0.52
```

Interpretation:

```text
positive signal, but topology-confounded.
```

### 4.2 Random edge-removal stress test

```text
target_edge_count = 25
structure_success = 0.345
largest_component_fraction = 0.307
```

Interpretation:

```text
exact edge-count matching introduced fragmentation, so it was not a valid final control.
```

### 4.3 LCF-constrained ablation

```text
target 25:
    valid_lcf_matched_rate = 0.06
    structure_success_valid = 0.000
    failed_no_non_bridge_edges_rate = 0.93

target 30:
    valid_lcf_matched_rate = 0.21
    structure_success_valid = 0.238
    failed_no_non_bridge_edges_rate = 0.78

target 35:
    valid_lcf_matched_rate = 0.37
    structure_success_valid = 0.411
    failed_no_non_bridge_edges_rate = 0.62
```

Interpretation:

```text
strict low-edge matching while preserving largest-component structure is often structurally infeasible.
```

### 4.4 Native topology audit

| mode | structure_success | edge_count | non_bridge_edge_count | cycle_rank | largest_component_cycle_rank | bridge_fraction | sector_size |
|---|---:|---:|---:|---:|---:|---:|---:|
| compensated | 0.72 | 44.96 | 33.52 | 16.09 | 15.93 | 0.269 | 29.86 |
| uncompensated | 0.53 | 25.35 | 17.82 | 8.16 | 8.15 | 0.335 | 18.17 |

Interpretation:

```text
compensated graphs occupy a higher native topological-capacity regime.
```

### 4.5 CI/pairing post-processing

Post-hoc threshold:

```text
non_bridge_edge_count >= 19:
    103/105 success = 0.981
    Wilson score interval = [0.933, 0.995]

non_bridge_edge_count < 19:
    22/95 success = 0.232
    Wilson score interval = [0.158, 0.326]

difference = 0.749
bootstrap 95% CI = [0.656, 0.834]
```

Paired deltas:

```text
delta_non_bridge_edge_count:
    mean = +15.70
    median = +16.0
    positive = 80/100

delta_cycle_rank:
    mean = +7.93
    median = +8.0
    positive = 80/100

delta_structure_success:
    compensated-only success = 32
    uncompensated-only success = 13
    both success = 40
    both failure = 15
```

Required caveat:

```text
The threshold non_bridge_edge_count >= 19 is post-hoc exploratory, selected on the full dataset, prone to selection bias, and not universal or mechanistic.
```

---

## 5. Primary documents

### Main manuscript

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1.md
```

### Final wording check

```text
docs/reviews/connectivity_entanglement_confound_isolation_v0_1_final_wording_check.md
```

### v0.1 checklist

```text
docs/reviews/connectivity_entanglement_confound_isolation_v0_1_checklist.md
```

### Editorial patch plan

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1_editorial_patch.md
```

---

## 6. Supporting artifact chain

```text
docs/results/v010_confirm_connectivity_variant2.md
docs/results/v010_density_matched_ablation_variant2_random_preliminary.md
docs/results/v010_lcf_constrained_ablation_variant2.md
docs/reviews/v010_lcf_constrained_ablation_variant2_qwen_review.md
docs/experiments/connectivity_entanglement_reframe.md
docs/reviews/connectivity_entanglement_reframe_qwen_review.md
docs/results/v010_connectivity_entanglement_audit_variant2.md
docs/reviews/v010_connectivity_entanglement_audit_variant2_qwen_review.md
docs/experiments/connectivity_entanglement_audit_variant2_ci_pairing_extension.md
docs/results/v010_connectivity_entanglement_audit_variant2_ci_pairing.md
docs/papers/connectivity_entanglement_confound_isolation_outline.md
docs/papers/connectivity_entanglement_confound_isolation_draft.md
docs/reviews/connectivity_entanglement_confound_isolation_draft_qwen_review.md
docs/reviews/connectivity_entanglement_confound_isolation_draft_revision_note.md
docs/papers/connectivity_entanglement_confound_isolation_v0_1_plan.md
docs/papers/connectivity_entanglement_confound_isolation_v0_1.md
docs/reviews/connectivity_entanglement_confound_isolation_v0_1_final_wording_check.md
```

---

## 7. Scripts and local outputs

### Scripts

```text
tools/audit_connectivity_entanglement_variant2.py
tools/postprocess_connectivity_audit_ci_pairing.py
```

### Local outputs used by the note

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
outputs/paired_seed_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/wilson_cis_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/bootstrap_ci_non_bridge_ge19_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

Generated outputs are local artifacts and are not committed by default unless explicitly authorized.

---

## 8. Status of the experimental branch

This experimental branch is closed for v0.1.

Science status:

```text
frozen
```

No further work is currently authorized on:

```text
new simulations;
new pruning ablations;
new thresholds;
new statistics;
claim expansion;
causal interpretation;
physical interpretation.
```

Remaining work is packaging-only:

```text
local Git synchronization;
optional final Qwen wording-only check;
README placement decision;
PDF / preprint-style formatting later;
public-facing summary extraction.
```

---

## 9. Short release blurb

```text
GCMS-D0 Variant 2 at beta=0.003 produced an initially positive compensated signal, but confound-isolation controls showed that the signal is not density-independent. Random edge matching fragmented graphs, and LCF-constrained pruning exposed structural infeasibility. A native-topology audit showed that compensated graphs co-occur with higher non_bridge_edge_count and cycle_rank, both associated with structure_success. The v0.1 conclusion is conservative: this is a reproducible topology-threshold / confound-isolation result in a toy model, not a causal or physical mechanism proof.
```

---

## 10. Final invariant

```text
The experiment is closed. The remaining work is packaging.
```
