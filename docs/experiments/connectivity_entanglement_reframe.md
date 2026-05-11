# Reframe: Connectivity-Entangled Dynamics in GCMS-D0

**Status:** hypothesis reframe / post-ablation interpretation checkpoint  
**Date:** 2026-05-11  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Triggering result:** `docs/results/v010_lcf_constrained_ablation_variant2.md`  
**Triggering review:** `docs/reviews/v010_lcf_constrained_ablation_variant2_qwen_review.md`  
**Related prior result:** `docs/results/v010_density_matched_ablation_variant2.md`  
**Related random-removal result:** `docs/results/v010_density_matched_ablation_variant2_random_preliminary.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Why this reframe exists

The original working hypothesis after `confirm_connectivity_variant2` was:

```text
Variant 2 compensation may produce a locally distinguishable structure that survives density and connectivity controls.
```

The evidence chain changed this interpretation.

### confirm_connectivity_variant2

Positive signal:

```text
compensated beta=0.003 structure_success = 0.72
uncompensated beta=0.003 structure_success = 0.52
```

But unresolved blocker:

```text
compensated graphs had higher edge count / density.
```

### random_edge_removal_preliminary

Result:

```text
edge count can be matched exactly,
but random removal destroys connectivity.
```

Primary target:

```text
target_edge_count = 25
structure_success = 0.345
largest_component_fraction = 0.307
```

Interpretation:

```text
naive edge-count matching is too destructive and creates a fragmentation confound.
```

### lcf_constrained_ablation_variant2

Result:

```text
LCF can be preserved,
but low edge-count targets are often unreachable.
```

Key values:

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

Reference:

```text
uncompensated beta=0.003 structure_success = 0.52
```

Qwen review classified this as:

```text
Confound-control experiment / null-result under strict topology preservation.
```

Therefore the project should not continue as if the original density-independent mechanism claim survived.

---

## 2. Old claim versus new frame

### Old candidate claim

```text
Variant 2 compensation creates local structure independently of density / edge count.
```

Status:

```text
blocked / not supported after LCF-constrained ablation.
```

### New frame

```text
Variant 2 compensation may generate structure through endogenous connectivity production.
```

More precisely:

```text
The compensation-aware relation appears to increase or preserve graph connectivity, and that higher connectivity may be a necessary condition for sector formation and structure_success.
```

This is not a rescue of the old claim.

It is a new, weaker, and more honest hypothesis:

```text
compensation and connectivity are entangled in the dynamics.
```

---

## 3. Updated status of beta=0.003

Previous status after `confirm_connectivity_variant2`:

```text
leading clean positive candidate
```

Status after random-removal ablation:

```text
unresolved but not weakened, because random removal caused severe fragmentation
```

Status after LCF-constrained ablation and Qwen review:

```text
connectivity-threshold-dependent candidate
```

Definition:

```text
A parameter regime where compensated dynamics appears structurally favorable only when it is allowed to maintain higher baseline connectivity.
```

Not allowed:

```text
clean density-independent candidate
```

Allowed:

```text
candidate regime for studying compensation-connectivity entanglement
```

---

## 4. What has been resolved

The following has been resolved:

```text
1. The original positive signal is not sufficient to claim a density-independent mechanism.
2. Simple edge-count matching is not enough because it can destroy topology.
3. LCF-preserving edge removal shows that strict low-edge matching is often structurally infeasible.
4. Valid LCF-matched rows do not exceed the uncompensated beta=0.003 reference.
5. The main object of study should shift from effect rescue to connectivity generation.
```

---

## 5. What remains open

The following remains scientifically open:

```text
1. Why does compensated Variant 2 generate higher edge count / connectivity?
2. Is increased connectivity a direct consequence of the compensation-aware relation?
3. Is there a minimum cycle / non-bridge structure required for sector formation?
4. Does structure_success track edge count, cycle rank, bridge fraction, spectral gap, or another connectivity descriptor?
5. Can compensated and uncompensated regimes be separated by endogenous topology statistics rather than by structure_success alone?
6. Is the observed effect a robust connectivity-threshold phenomenon across N, d, threshold, and beta?
```

---

## 6. New primary research question

Old question:

```text
Does compensation create local structure independently of density?
```

New question:

```text
Does compensation alter the endogenous connectivity regime in a way that enables or stabilizes local structure?
```

Alternative wording:

```text
Is the apparent Variant 2 signal mediated by a compensation-induced connectivity threshold?
```

---

## 7. New objects of analysis

The next stage should focus on graph-topological descriptors of the original, unpruned compensated and uncompensated graphs.

Recommended primary descriptors:

```text
edge_count
density
n_components
largest_component_fraction
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank / cyclomatic_number
degree_variance
mean_degree
largest_component_edge_count
largest_component_cycle_rank
spectral gap, if feasible
algebraic connectivity, if feasible
```

The immediate priority is not another edge-removal ablation.

The immediate priority is to analyze:

```text
what topology the dynamics produces before pruning.
```

---

## 8. Minimal next diagnostic experiment

Suggested next experiment name:

```text
connectivity_entanglement_audit_variant2
```

Purpose:

```text
Compare original compensated and uncompensated graphs at beta=0.003 using topology descriptors that explain why LCF-constrained pruning fails.
```

Inputs:

```text
raw confirm_connectivity_variant2 outputs if available;
or rerun a small audit using the same seeds and parameters.
```

Recommended outputs:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
```

Required columns:

```text
model_mode
relation_variant
beta
seed
edge_count
density
n_components
largest_component_fraction
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
mean_degree
degree_variance
sector_size
structure_success
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Primary comparison:

```text
compensated beta=0.003 vs uncompensated beta=0.003
```

Primary question:

```text
Does compensated beta=0.003 produce more non-bridge/cycle capacity than uncompensated beta=0.003, and is structure_success conditioned on that capacity?
```

---

## 9. Interpretation rules going forward

### Do not say

```text
Variant 2 proves a density-independent compensation mechanism.
```

### Do not say

```text
The project failed because LCF ablation was negative.
```

### Do say

```text
Variant 2 produced an initial positive signal, but strict density/LCF controls show that the signal is connectivity-dependent.
```

### Do say

```text
The result suggests compensation-connectivity entanglement: the compensatory relation may generate structural effects by shifting the graph into a higher-connectivity regime.
```

### Do say

```text
The next scientific object is endogenous topology generation, not rescue of the original density-independent claim.
```

---

## 10. Publication framing

The project is no longer framed as:

```text
mechanism proof
```

The viable publication frame is:

```text
confound-isolation study in a computational toy model
```

Possible title direction:

```text
A Toy-Model Study of Compensation-Connectivity Entanglement in Graph-Constrained Sector Formation
```

Acceptable claims:

```text
1. A compensation-aware relation produced an initial structure_success advantage.
2. That advantage was not robust to strict density/LCF controls.
3. The controls revealed a strong coupling between compensation and graph connectivity.
4. Topology-preserving pruning exposed structural infeasibility at low edge count.
5. The result motivates analysis of endogenous connectivity generation rather than density-independent mechanism claims.
```

Unacceptable claims:

```text
1. density-independent mechanism confirmed;
2. physical theory relevance;
3. direct connection to real-world constants;
4. proof of emergent causal structure;
5. preprint-level mechanism result without reframing.
```

---

## 11. Next review step

This reframe should be submitted for external review.

Review questions:

```text
1. Is the connectivity-entanglement reframe a correct response to the LCF-null result?
2. Should further edge-removal ablations stop as the main path?
3. Is connectivity_entanglement_audit_variant2 the right next diagnostic?
4. Which topology descriptors are mandatory?
5. What conservative wording is publication-safe?
6. Does beta=0.003 remain useful as a study regime despite losing clean-candidate status?
```

---

## 12. Current status

```text
Original density-independent claim: blocked.
Beta=0.003 clean-candidate status: downgraded.
New frame: connectivity-entangled dynamics.
Next action: external review of this reframe, then design checkpoint for connectivity_entanglement_audit_variant2 if approved.
```

Short invariant:

```text
We are no longer trying to remove connectivity from the effect.
We are trying to understand why compensation creates or requires connectivity.
```
