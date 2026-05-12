# Paper Outline: Connectivity Entanglement as a Confound-Isolation Result in GCMS-D0

**Status:** technical-note outline / not a manuscript draft  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Primary experiment:** `v010_connectivity_entanglement_audit_variant2`  
**Statistical strengthening:** `v010_connectivity_entanglement_audit_variant2_ci_pairing`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Working title options

Preferred conservative title:

```text
Connectivity Entanglement in a Graph-Constrained Compensation Toy Model: A Confound-Isolation Study
```

Alternative titles:

```text
A Confound-Isolation Study of Compensation-Connectivity Coupling in a Graph-Constrained Toy Model
```

```text
Topology Thresholds in a Compensation-Aware Graph Toy Model
```

```text
When Density Controls Fail: Connectivity Entanglement in GCMS-D0 Variant 2
```

Avoid titles implying:

```text
mechanism proof
physical theory
spacetime / constants / gravity
universal threshold
causal proof
```

---

## 2. One-sentence claim

Allowed one-sentence claim:

```text
In a graph-constrained compensation toy model, the apparent compensated advantage in Variant 2 is not density-independent; it is empirically coupled to native topological capacity, especially non-bridge edge count and cycle rank.
```

Forbidden one-sentence claim:

```text
The model proves that compensation creates structure independently of density.
```

---

## 3. Abstract skeleton

```text
We study a graph-constrained computational toy model, GCMS-D0, in which global compensation constraints influence local graph structure through a compensation-aware relation function. An initial Variant 2 experiment showed higher structure_success in the compensated mode at beta=0.003 than in an uncompensated reference. However, this positive signal was confounded by graph topology: compensated graphs had higher native edge count and cyclic redundancy.

We perform a sequence of confound-isolation tests. Random edge removal matched edge counts but fragmented graphs. LCF-constrained non-bridge removal preserved connectivity but revealed that low-edge matching is often infeasible, with failed_no_non_bridge_edges dominating. We therefore reframe the result as a native-topology question and audit compensated versus uncompensated graphs without pruning.

The native-topology audit shows that compensated graphs have higher non_bridge_edge_count, cycle_rank, largest-component cycle rank, and sector size. Structure_success is strongly associated with these topology descriptors. A post-hoc threshold at non_bridge_edge_count >= 19 separates high and low success regimes, with Wilson and bootstrap uncertainty estimates. Paired seed analysis shows systematic positive deltas for non_bridge_edge_count and cycle_rank in compensated runs.

We conclude that the original density-independent mechanism claim is not supported. Instead, the result supports a conservative compensation-connectivity entanglement interpretation in this toy model: compensated dynamics appears empirically coupled to the production of topological capacity that is associated with local structural success. No causal, universal, or physical claim is made.
```

---

## 4. Paper type and target frame

This is not framed as:

```text
mechanism proof
physical theory paper
emergent spacetime claim
density-independent compensation proof
```

It is framed as:

```text
computational toy-model report
confound-isolation study
negative-control / reframe paper
topology-threshold diagnostic
reproducibility-oriented methodology note
```

---

## 5. Core narrative arc

### Stage 1: Initial positive signal

```text
confirm_connectivity_variant2:
    compensated beta=0.003 structure_success = 0.72
    uncompensated beta=0.003 structure_success = 0.52
```

Blocker:

```text
compensated graphs had different native topology / edge counts.
```

### Stage 2: Naive density control fails by fragmentation

```text
target_edge_count = 25:
    structure_success = 0.345
    largest_component_fraction = 0.307
```

Interpretation:

```text
naive edge-count matching creates a fragmentation confound.
```

### Stage 3: LCF-preserving control reveals structural infeasibility

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
low-edge matching and largest-component preservation are jointly difficult;
valid rows do not recover the uncompensated reference.
```

### Stage 4: Reframe

Old frame:

```text
density-independent mechanism
```

New frame:

```text
compensation-connectivity entanglement
```

### Stage 5: Native-topology audit supports reframe

| mode | success | edge_count | non_bridge | cycle_rank | LCC cycle rank | sector_size |
|---|---:|---:|---:|---:|---:|---:|
| compensated | 0.72 | 44.96 | 33.52 | 16.09 | 15.93 | 29.86 |
| uncompensated | 0.53 | 25.35 | 17.82 | 8.16 | 8.15 | 18.17 |

### Stage 6: CI/pairing strengthens reportability

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

Threshold contrast:

```text
non_bridge_edge_count >= 19:
    103/105 success = 0.981
    Wilson CI = [0.933, 0.995]

non_bridge_edge_count < 19:
    22/95 success = 0.232
    Wilson CI = [0.158, 0.326]

difference = 0.749
bootstrap 95% CI = [0.656, 0.834]
```

Caveat:

```text
threshold is post-hoc exploratory, not validated as universal or mechanistic.
```

---

## 6. Proposed section structure

### 1. Introduction

Goals:

```text
Introduce GCMS-D0 as a toy model.
State the risk of confounded positive simulation results.
Present the paper as a confound-isolation report.
```

### 2. Model overview

Include only enough model detail to make experiments interpretable:

```text
World vectors
compensation vs uncompensated modes
Variant 2 relation
structure_success criteria
p_gnp / p_dp / dp_valid / lifetime / sector_size
```

### 3. Initial signal and confound

Report:

```text
compensated 0.72 vs uncompensated 0.52
edge/density topology difference
why this blocks clean claim
```

### 4. Ablation controls and why they fail

Subsections:

```text
4.1 Random edge removal: exact edge matching but fragmentation
4.2 LCF-constrained removal: preserves LCF but low-edge matching infeasible
4.3 Interpretation: edge count and connectivity cannot be cleanly separated by pruning
```

### 5. Reframe: compensation-connectivity entanglement

Define:

```text
compensation-connectivity entanglement = empirical coupling between compensated dynamics and native topological capacity associated with success.
```

Explicitly say:

```text
This is a reframe, not a rescue of the original density-independent claim.
```

### 6. Native-topology audit

Report:

```text
settings
100 seeds x 2 modes
no pruning
native graph descriptors
```

### 7. Threshold and paired-seed analysis

Subsections:

```text
7.1 Correlations with structure_success
7.2 Post-hoc non_bridge_edge_count threshold
7.3 Wilson CIs
7.4 Bootstrap CI for threshold contrast
7.5 Paired seed deltas
```

### 8. Discussion

Interpretation:

```text
The data support topology-threshold framing.
non_bridge_edge_count is primary.
cycle_rank is confirmatory.
edge_count alone is insufficient because it cannot distinguish bridges from redundant capacity.
density alone is misleading.
```

### 9. Limitations

Mandatory limitations:

```text
toy model only;
no physical claims;
post-hoc threshold;
observational audit, not intervention;
causal interpretation blocked;
N/beta/threshold generality not established;
logistic/collinearity-aware analysis optional future work;
passive residual diagnostics exploratory only.
```

### 10. Conclusion

Conservative conclusion:

```text
The original density-independent claim is not supported. The confound-isolation sequence identifies native connectivity capacity as a major explanatory object. In this toy model, compensated Variant 2 at beta=0.003 is best interpreted as a connectivity-threshold-dependent study regime.
```

---

## 7. Figures and tables plan

### Table 1: Experiment chain

Columns:

```text
stage
experiment
purpose
main result
interpretation
claim impact
```

Rows:

```text
confirm_connectivity_variant2
random_edge_removal_preliminary
lcf_constrained_ablation_variant2
connectivity_entanglement_audit_variant2
ci_pairing postprocess
```

### Table 2: Native topology summary

Columns:

```text
model_mode
structure_success_rate
edge_count
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
bridge_fraction
sector_size
```

### Table 3: Paired seed deltas

Columns:

```text
metric
mean_delta
median_delta
positive_fraction
negative_fraction
zero_fraction
```

### Table 4: Threshold rates with Wilson CI

Rows:

```text
model_mode compensated
model_mode uncompensated
non_bridge >=19
non_bridge <19
```

### Table 5: Bootstrap threshold contrast

Columns:

```text
threshold
above_rate
below_rate
difference
bootstrap_ci_low
bootstrap_ci_high
note
```

### Figure 1: Experiment flow diagram

Flow:

```text
initial positive signal -> random removal -> LCF constrained removal -> reframe -> native topology audit -> CI/pairing
```

### Figure 2: Distribution of non_bridge_edge_count by mode

Expected message:

```text
compensated shifted right relative to uncompensated
```

### Figure 3: structure_success versus non_bridge_edge_count

Include threshold line:

```text
non_bridge_edge_count = 19
```

Label as:

```text
post-hoc exploratory threshold
```

### Figure 4: Paired seed deltas

Could be histogram or ordered plot:

```text
delta_non_bridge_edge_count
delta_cycle_rank
delta_structure_success
```

---

## 8. Core claims table

| Claim | Status | Evidence | Wording |
|---|---|---|---|
| Initial compensated advantage exists at beta=0.003 | Supported descriptively | 0.72 vs 0.52 | descriptive only |
| Density-independent mechanism | Blocked | ablations and audit | do not claim |
| Random removal is final control | Blocked | fragmentation | do not claim |
| LCF-constrained low-edge matching often infeasible | Supported | failed_no_non_bridge_edges | allowed |
| compensation-connectivity entanglement | Supported as empirical coupling | audit + review | allowed with toy-model qualifier |
| non_bridge_edge_count is primary descriptor | Supported by Qwen | Qwen review | allowed |
| threshold >=19 is meaningful | Exploratory only | Wilson/bootstrap | post-hoc only |
| causal mechanism | Blocked | observational audit | do not claim |
| physical relevance | Blocked | toy model | do not claim |

---

## 9. Required citations to internal artifacts

The technical note should reference:

```text
docs/results/v010_confirm_connectivity_variant2.md
docs/results/v010_density_matched_ablation_variant2_random_preliminary.md
docs/results/v010_lcf_constrained_ablation_variant2.md
docs/reviews/v010_lcf_constrained_ablation_variant2_qwen_review.md
docs/experiments/connectivity_entanglement_reframe.md
docs/reviews/connectivity_entanglement_reframe_qwen_review.md
docs/results/v010_connectivity_entanglement_audit_variant2.md
docs/reviews/v010_connectivity_entanglement_audit_variant2_qwen_review.md
docs/results/v010_connectivity_entanglement_audit_variant2_ci_pairing.md
```

---

## 10. Writing rules

Use:

```text
suggests
is associated with
supports the reframe
empirical coupling
post-hoc exploratory threshold
toy model
confound-isolation
```

Avoid:

```text
proves
causes
universal
physical
spacetime
constants
gravity
photons
real-world mechanism
```

Replace:

```text
mechanism confirmed
```

with:

```text
topology-threshold pattern observed
```

Replace:

```text
compensation creates structure
```

with:

```text
compensated runs occupy a higher topological-capacity regime associated with structure_success
```

---

## 11. Remaining optional work before manuscript draft

Not required for technical-note outline, but possible before a fuller manuscript:

```text
1. logistic regression or collinearity-aware model;
2. threshold variation 0.70-0.80;
3. beta 0.004 / 0.005 stability check;
4. N=100 / N=200 cross-check;
5. intervention experiment on topology capacity, if a causal claim is later desired.
```

Do not run these before writing the first technical note unless explicitly approved.

---

## 12. Current status

```text
technical/confound-isolation draft is methodologically permitted;
outline created;
no manuscript draft yet;
no additional simulations authorized.
```

Short invariant:

```text
This paper is valuable because it does not rescue the original claim. It documents why the original claim had to be weakened and what scientifically useful structure remained.
```
