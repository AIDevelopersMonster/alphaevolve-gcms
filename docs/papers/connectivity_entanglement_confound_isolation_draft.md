# Connectivity Entanglement in a Graph-Constrained Compensation Toy Model: A Confound-Isolation Study

**Status:** first technical draft / not final manuscript  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Primary experiment:** `v010_connectivity_entanglement_audit_variant2`  
**Statistical strengthening:** `v010_connectivity_entanglement_audit_variant2_ci_pairing`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## Abstract

We study GCMS-D0, a graph-constrained computational toy model in which global compensation constraints interact with local graph formation through a compensation-aware relation function. An initial Variant 2 experiment showed a higher `structure_success` rate in the compensated mode at `beta=0.003` than in the corresponding uncompensated reference. However, the positive signal was confounded by native graph topology: compensated graphs also occupied a different edge-count and connectivity regime.

We report a sequence of confound-isolation tests. First, random edge removal matched edge counts but severely fragmented the compensated graphs, making it unsuitable as a final density control. Second, LCF-constrained non-bridge removal preserved connectivity but revealed that strict low-edge matching was often infeasible: attempts frequently failed because no removable non-bridge edges remained. This blocked the original density-independent mechanism claim and motivated a reframe from density independence to compensation-connectivity entanglement.

We then audited the native topology of compensated and uncompensated Variant 2 graphs without pruning or edge removal. The audit showed that compensated graphs at `beta=0.003` have higher `non_bridge_edge_count`, `cycle_rank`, largest-component cycle rank, and sector size. These topology descriptors are strongly associated with `structure_success`. A post-hoc split at `non_bridge_edge_count >= 19` separates high- and low-success regimes, with Wilson and bootstrap uncertainty estimates. Paired seed analysis shows systematic positive deltas in non-bridge edge count and cycle rank for compensated runs.

We conclude that the original density-independent mechanism claim is not supported. Instead, the results support a conservative compensation-connectivity entanglement interpretation in this toy model: compensated dynamics appears empirically coupled to the production of native topological capacity associated with local structural success. No causal, universal, or physical claim is made.

---

## 1. Introduction

Positive results in computational toy models are often difficult to interpret because an apparent mechanism may be entangled with uncontrolled structural confounders. In graph-based simulations, this problem is especially acute: a local success criterion may appear to improve under one model mode while the graph itself has also changed in edge count, connectedness, cyclic redundancy, or bridge structure.

GCMS-D0 was developed as a graph-constrained toy model for studying whether global compensation constraints can produce locally distinguishable graph structures under compensation-aware relation functions. The model is not presented here as a physical theory. It is used as a controlled computational setting for studying how global constraints, graph topology, and local success criteria interact.

The starting point for this report was an initially positive result in Variant 2 at `beta=0.003`. In that experiment, the compensated mode had a higher `structure_success` rate than the uncompensated reference. However, compensated graphs also differed in native topology. This made a density-independent interpretation unsafe.

The central contribution of this note is not confirmation of the original mechanism hypothesis. Instead, the contribution is a documented confound-isolation sequence showing why the original density-independent claim had to be weakened and what scientifically useful structure remained. The result is a reframe: compensated Variant 2 at `beta=0.003` is best treated as a connectivity-threshold-dependent study regime in which success is empirically coupled to native topological capacity.

This note makes four contributions. First, it documents why the initial compensated advantage cannot be interpreted as density-independent. Second, it shows that random edge removal and LCF-constrained pruning fail for different methodological reasons: fragmentation and structural infeasibility. Third, it reframes the result as compensation-connectivity entanglement and audits native topology without graph modification. Fourth, it reports paired-seed and uncertainty analyses showing that `non_bridge_edge_count` and `cycle_rank` provide a topology-threshold description of the observed success pattern.

---

## 2. Model and outcome overview

GCMS-D0 represents a graph-constrained setting in which candidate node sets or sectors are evaluated under local structural criteria. The relevant mode comparison in this report is between:

```text
model_modes = [compensated, uncompensated]
relation_variant = 2
beta = 0.003
```

The compensated mode enforces a global compensation condition, while the uncompensated mode provides a reference without that constraint. Variant 2 uses a compensation-aware relation function to define graph structure. The relevant outcome is `structure_success`, which depends on a fixed set of criteria already used in the project, including empirical probability checks, DP validity, lifetime, and sector-size bounds.

The audit and post-processing described here do not change these criteria. They also do not modify the generated graphs. In particular, the native-topology audit follows the invariant:

```text
Measure native topology first. Do not prune. Do not rescue.
```

### 2.1 Topology definitions

The main topology descriptors used in this report are:

```text
edge_count
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
largest_component_fraction
sector_size
```

Definitions:

```text
bridge_count = number of graph bridges
bridge_fraction = bridge_count / edge_count, when edge_count > 0
non_bridge_edge_count = edge_count - bridge_count
cycle_rank = E - V + C, where E is edge count, V is node count, and C is number of connected components
largest_component_cycle_rank = E_LCC - V_LCC + 1 for the largest connected component
```

The primary descriptor for reporting is `non_bridge_edge_count`, because it directly connects the native-topology audit to the failure mode observed in the LCF-constrained ablation: `failed_no_non_bridge_edges`. `cycle_rank` and `largest_component_cycle_rank` are used as confirmatory descriptors of cyclic redundancy.

`sector_size` is reported because it is strongly associated with success, but it is outcome-adjacent rather than a clean explanatory topology variable: sector-size bounds are part of the broader success criteria. Therefore, `sector_size` is treated as descriptive/supporting context, not as the primary topology descriptor.

---

## 3. Initial positive signal and topology confound

The initial Variant 2 result at `beta=0.003` showed:

```text
compensated structure_success = 0.72
uncompensated structure_success = 0.52
```

This was an encouraging signal but not a clean mechanism result. The compensated graphs had a different native topology regime, especially in edge count and connectivity-related descriptors. Therefore, the initial result could not support the claim that Variant 2 compensation creates local structure independently of density or connectivity.

The appropriate next step was confound isolation: test whether the positive signal survived attempts to control edge count and connectivity.

---

## 4. Density and connectivity controls

### 4.1 Random edge removal

The first density-matching attempt used random edge removal to match edge counts. This matched the requested edge counts exactly, but it also severely fragmented the compensated graphs.

For the low-edge target:

```text
target_edge_count = 25
structure_success = 0.345
largest_component_fraction = 0.307
```

This result was informative but not final. It showed that naive density matching can create a new fragmentation confound. A graph that has been randomly fragmented is not a fair topology-preserving comparison to the original compensated graph.

Therefore, random edge removal was classified as a useful stress test but not a valid final control.

### 4.2 LCF-constrained non-bridge removal

The next control used non-bridge removal with a largest-component constraint. The goal was to reduce edge count while preserving the largest component:

```text
LCF threshold = 0.85
target_edge_counts = [25, 30, 35]
```

The result changed the interpretation. LCF preservation was mostly possible, but low-edge targets were often unreachable under the non-bridge constraint.

Key results:

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

The valid rows did not exceed the uncompensated reference success rate. The dominant failure mode, `failed_no_non_bridge_edges`, indicated that aggressive low-edge matching was structurally incompatible with preserving the graph's largest component for many compensated graphs.

### 4.3 Interpretation of ablation controls

The control sequence blocked the original density-independent mechanism claim.

Random removal showed:

```text
edge count can be matched, but topology collapses.
```

LCF-constrained removal showed:

```text
topology can be preserved, but low-edge matching is often infeasible.
```

Together, these results suggest that edge count, largest-component preservation, and cyclic/non-bridge capacity cannot be cleanly separated by simple pruning controls. This led to the reframe: rather than asking whether compensation creates structure independently of topology, the next question became whether compensation is empirically coupled to the production of the topology that supports success.

---

## 5. Reframe: compensation-connectivity entanglement

The rejected frame was:

```text
Variant 2 compensation creates local structure independently of density or edge count.
```

The conservative replacement frame is:

```text
Variant 2 compensation is empirically coupled to native graph connectivity capacity, and that capacity is associated with structure_success.
```

This report uses the phrase `compensation-connectivity entanglement` in a limited, toy-model sense. It does not imply a causal proof. It means that, within this computational setup, compensated dynamics and topology descriptors such as non-bridge edge count and cycle rank vary together in a way that is associated with local structural success.

This reframe is not a rescue of the original claim. It is a weakening of the claim to match the evidence.

The reframe and audit interpretation were subjected to independent methodological review within the project workflow. That review recommended treating `non_bridge_edge_count` as the primary descriptor, reporting the `>=19` threshold as post-hoc exploratory, and adding paired-seed and uncertainty analyses before drafting. This review is part of the project's internal methodological pressure system; it is not presented as journal peer review.

---

## 6. Native-topology audit

After the reframe, the next experiment did not prune or modify graphs. Instead, it measured the native topology produced by compensated and uncompensated Variant 2 dynamics at `beta=0.003`.

Settings:

```text
relation_variant = 2
model_modes = [compensated, uncompensated]
beta = 0.003
seeds = 100
N = 150
d = 4
steps = 200
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
epsilon_norm = 0.0
lambda_val = 0.0
baseline_count = 100
```

Run integrity:

```text
raw rows = 200
compensated rows = 100
uncompensated rows = 100
```

Native topology summary:

| mode | structure_success | edge_count | non_bridge_edge_count | cycle_rank | largest_component_cycle_rank | bridge_fraction | sector_size |
|---|---:|---:|---:|---:|---:|---:|---:|
| compensated | 0.72 | 44.96 | 33.52 | 16.09 | 15.93 | 0.269 | 29.86 |
| uncompensated | 0.53 | 25.35 | 17.82 | 8.16 | 8.15 | 0.335 | 18.17 |

The compensated mode has higher success and a higher native topology-capacity regime. In particular, it has more non-bridge edges and higher cycle rank. This is exactly the capacity that LCF-constrained pruning depleted or failed to remove without destroying connectivity.

---

## 7. Correlations, threshold pattern, and paired-seed analysis

### 7.1 Descriptive correlations

The parent audit found the following Pearson correlations with `structure_success`:

| feature | correlation with structure_success |
|---|---:|
| edge_count | 0.704 |
| sector_size | 0.700 |
| non_bridge_edge_count | 0.690 |
| max_degree | 0.647 |
| cycle_rank | 0.642 |
| largest_component_cycle_rank | 0.638 |
| mean_degree | 0.572 |
| degree_variance | 0.509 |
| density | -0.458 |
| bridge_fraction | -0.242 |

These correlations are descriptive. They do not imply causality. They also involve collinear graph descriptors: edge count, cycle rank, non-bridge edge count, and sector size are not independent explanatory variables.

However, the pattern is consistent with the reframe: success is associated with structural redundancy and cycle capacity rather than scalar density alone. The negative correlation with density warns that density alone is not a reliable proxy for the relevant topological capacity.

The negative density correlation should not be read as evidence that sparse graphs are generally better. Density is normalized by sector size / node count and is therefore entangled with the size of the selected graph. In this audit, `edge_count` and especially `non_bridge_edge_count` are more interpretable descriptors of absolute topological capacity than scalar density alone.

### 7.2 Post-hoc non-bridge threshold

The audit identified a strong post-hoc split at:

```text
non_bridge_edge_count >= 19
```

Rows above the threshold had substantially higher success than rows below it:

```text
non_bridge_edge_count >= 19:
    103/105 success = 0.981
    Wilson CI = [0.933, 0.995]

non_bridge_edge_count < 19:
    22/95 success = 0.232
    Wilson CI = [0.158, 0.326]
```

The rate difference was:

```text
difference = 0.749
bootstrap 95% CI = [0.656, 0.834]
```

This is a large descriptive contrast. However, the threshold was selected on the same data and must therefore be reported as post-hoc exploratory. It is not validated as a universal or mechanistic cutoff.

### 7.3 Wilson confidence intervals for model-mode rates

The model-mode success rates with Wilson confidence intervals are:

| group | success_count | n | rate | Wilson CI |
|---|---:|---:|---:|---:|
| compensated | 72 | 100 | 0.720 | [0.625, 0.799] |
| uncompensated | 53 | 100 | 0.530 | [0.433, 0.625] |

Failure-rate intervals also favored the compensated mode:

| failure | compensated | uncompensated |
|---|---:|---:|
| failed_p_gnp | 0.170 [0.109, 0.255] | 0.430 [0.337, 0.528] |
| failed_p_dp | 0.160 [0.101, 0.244] | 0.320 [0.237, 0.417] |

These intervals strengthen the descriptive reportability of the result but do not convert the observational audit into a causal mechanism proof.

### 7.4 Paired seed analysis

Because compensated and uncompensated rows were generated for the same seeds, paired analysis is more informative than treating all rows as independent.

Paired deltas showed systematic topology differences:

| metric | mean_delta | median_delta | positive | negative | zero | positive_fraction |
|---|---:|---:|---:|---:|---:|---:|
| delta_edge_count | 19.61 | 22.5 | 82 | 17 | 1 | 0.82 |
| delta_non_bridge_edge_count | 15.70 | 16.0 | 80 | 18 | 2 | 0.80 |
| delta_cycle_rank | 7.93 | 8.0 | 80 | 18 | 2 | 0.80 |
| delta_largest_component_cycle_rank | 7.78 | 8.0 | 79 | 19 | 2 | 0.79 |
| delta_sector_size | 11.69 | 11.0 | 83 | 16 | 1 | 0.83 |

Paired success counts were:

```text
compensated_only_success_count = 32
uncompensated_only_success_count = 13
both_success_count = 40
both_failure_count = 15
paired_success_delta_mean = 0.19
```

The topology deltas are more systematic than the binary success delta, which is expected because `structure_success` is a downstream binary criterion. The paired evidence supports the claim that compensated runs usually occupy a higher topological-capacity regime for the same seed.

---

## 8. Discussion

The evidence supports a topology-threshold interpretation of Variant 2 at `beta=0.003`. The compensated mode has higher `structure_success`, but it also produces a different native topology. The relevant topology is not adequately summarized by density alone. The primary descriptor is `non_bridge_edge_count`, supported by `cycle_rank` and largest-component cycle rank.

This explains the earlier LCF-constrained ablation result. When compensated graphs were forced toward low edge counts while preserving LCF, the process frequently exhausted removable non-bridge edges. This is not a minor implementation failure; it is directly related to the topology capacity that the native audit associates with success.

Therefore, the original positive signal should not be interpreted as density-independent. The more accurate statement is that compensated Variant 2 at `beta=0.003` occupies a higher topological-capacity regime, and that regime is associated with local structural success.

The result is scientifically useful precisely because it weakens the original claim. It identifies a confound, shows why naive controls fail, reframes the research question, and then measures the topology that remains explanatory under the revised frame.

---

## 9. Reproducibility and artifact trail

The result is reproducibility-oriented: the project separates design checkpoints, execution notes, result notes, external-methodology reviews, and draft writing. The main scripts and outputs used for this draft are:

| Purpose | Artifact |
|---|---|
| native topology audit tool | `tools/audit_connectivity_entanglement_variant2.py` |
| raw audit output | `outputs/raw_v010_connectivity_entanglement_audit_variant2.csv` |
| summary audit output | `outputs/summary_v010_connectivity_entanglement_audit_variant2.csv` |
| paired seed audit output | `outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv` |
| threshold output | `outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv` |
| correlation output | `outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv` |
| CI/pairing postprocess tool | `tools/postprocess_connectivity_audit_ci_pairing.py` |
| paired summary output | `outputs/paired_seed_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv` |
| Wilson CI output | `outputs/wilson_cis_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv` |
| bootstrap CI output | `outputs/bootstrap_ci_non_bridge_ge19_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv` |

Generated outputs are local artifacts and are not committed by default unless explicitly authorized.

---

## 10. Limitations

This report has several important limitations.

First, GCMS-D0 is a computational toy model. No physical claim is made.

Second, the topology audit is observational. It shows association between compensated mode, topology descriptors, and `structure_success`. It does not prove that compensation causally creates structure.

Third, the threshold `non_bridge_edge_count >= 19` is post-hoc exploratory. Although the observed contrast is large and has Wilson/bootstrap uncertainty estimates, the threshold was identified on the same data and requires validation on independent seeds or parameter settings before mechanistic interpretation.

Fourth, the graph descriptors are collinear. Edge count, non-bridge edge count, cycle rank, and sector size are related. A logistic or collinearity-aware analysis may be useful for a fuller manuscript, but it is not required for this first confound-isolation report.

Fifth, the generality of the result across `N`, `beta`, and threshold hyperparameters has not been established. Suggested future checks include threshold variation in `[0.70, 0.80]`, beta values such as `0.004` or `0.005`, and `N=100/200` cross-checks.

Finally, passive residual diagnostics such as `global_error` and `sector_chi` were recorded but are not interpreted here as causal or mechanistic predictors.

---

## 11. Conclusion

The original density-independent mechanism claim is not supported. Random edge removal introduced fragmentation, and LCF-constrained edge removal showed that strict low-edge matching is often structurally infeasible. These controls blocked the clean mechanism interpretation and motivated a reframe toward compensation-connectivity entanglement.

The native-topology audit supports this reframe. Compensated Variant 2 at `beta=0.003` produces higher non-bridge edge count, cycle rank, largest-component cycle rank, and sector size than the uncompensated reference. These descriptors are strongly associated with `structure_success`. Paired seed analysis and confidence intervals strengthen the descriptive reportability of the result.

The conservative conclusion is:

```text
In this toy model, compensated Variant 2 at beta=0.003 is best interpreted as a connectivity-threshold-dependent study regime. The apparent compensated advantage is empirically coupled to native topological capacity, especially non_bridge_edge_count and cycle_rank. This supports a confound-isolation / topology-threshold framing, not a density-independent mechanism proof.
```

No causal, universal, or physical claim is made.

---

## Appendix A. Artifact chain

This draft is based on the following internal artifacts:

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
docs/reviews/connectivity_entanglement_confound_isolation_draft_review_pass.md
```

---

## Appendix B. Claim discipline checklist

Allowed wording:

```text
supports the reframe
is associated with
empirical coupling
post-hoc exploratory threshold
topology-threshold diagnostic
toy model
confound-isolation
```

Forbidden wording:

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
density-independent mechanism confirmed
```
