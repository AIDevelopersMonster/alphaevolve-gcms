# Design Checkpoint: connectivity_entanglement_audit_variant2

**Status:** design checkpoint / not yet implemented / not yet executed  
**Date:** 2026-05-11  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `connectivity_entanglement_audit_variant2`  
**Triggering reframe:** `docs/experiments/connectivity_entanglement_reframe.md`  
**Triggering review:** `docs/reviews/connectivity_entanglement_reframe_qwen_review.md`  
**LCF result:** `docs/results/v010_lcf_constrained_ablation_variant2.md`  
**LCF review:** `docs/reviews/v010_lcf_constrained_ablation_variant2_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This checkpoint defines the next experiment after the connectivity-entanglement reframe.

The goal is no longer to rescue the original density-independent mechanism claim by trying additional edge-removal ablations.

The goal is now:

```text
Measure the native topology produced by compensated and uncompensated Variant 2 dynamics, and determine whether structure_success is mediated by endogenous connectivity descriptors.
```

In short:

```text
Do not remove edges.
Measure the topology the dynamics actually creates.
```

---

## 2. Background

The prior LCF-constrained ablation showed:

```text
LCF can be preserved,
but low edge-count targets are often unreachable under non-bridge removal.
```

Key values from `v010_lcf_constrained_ablation_variant2`:

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

Qwen classified the LCF result as:

```text
confound-control experiment / null-result under strict topology preservation
```

Qwen approved the reframe:

```text
from: density-independent mechanism claim
into: compensation-connectivity entanglement / connectivity-threshold-dependent candidate
```

Therefore this experiment studies native topology rather than artificial pruning.

---

## 3. Research question

Primary question:

```text
Does compensated Variant 2 at beta=0.003 endogenously produce a different connectivity regime than the uncompensated mode, and does that regime explain structure_success?
```

Secondary questions:

```text
1. Do compensated graphs have lower bridge_fraction or higher non_bridge_edge_count than uncompensated graphs?
2. Do compensated graphs have higher cycle_rank / cyclomatic_number?
3. Does structure_success correlate more strongly with cycle capacity than with compensation mode itself?
4. Is there a minimum non_bridge_edge_count or cycle_rank threshold associated with structure_success > 0.5?
5. Does beta=0.003 remain useful as a connectivity-threshold-dependent study regime?
```

---

## 4. Scope

Experiment name:

```text
connectivity_entanglement_audit_variant2
```

Modes:

```text
model_modes = [compensated, uncompensated]
```

Core settings:

```text
relation_variant = 2
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

Expected rows:

```text
2 model_modes × 100 seeds = 200 rows
```

Important:

```text
No pruning.
No edge removal.
No density matching by graph modification.
No LCF-constrained removal.
```

---

## 5. Required topology descriptors

For each generated graph, compute:

```text
edge_count
density
n_components
largest_component_fraction
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_edge_count
largest_component_node_count
largest_component_cycle_rank
mean_degree
degree_variance
max_degree
clustering
spectral_gap_optional
algebraic_connectivity_optional
```

Definitions:

```text
bridge_count = number of bridges in the graph
bridge_fraction = bridge_count / edge_count if edge_count > 0 else 0
non_bridge_edge_count = edge_count - bridge_count
cycle_rank = edge_count - node_count + n_components
largest_component_cycle_rank = E_LCC - V_LCC + 1 for largest connected component
mean_degree = 2 * edge_count / node_count
degree_variance = variance of node degrees
```

Optional spectral descriptors should be computed only if numerically stable and not too slow.

If spectral descriptors fail, report:

```text
spectral_gap_available = false
algebraic_connectivity_available = false
```

Do not fail the experiment solely because optional spectral descriptors cannot be computed.

---

## 6. Required outcome descriptors

Retain all existing structure outcome fields:

```text
sector_size
lifetime
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

The audit must allow comparison of topology descriptors against:

```text
structure_success
failed_p_gnp
failed_p_dp
sector_size
```

---

## 7. Required raw output

Raw output path:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
```

Required raw columns:

```text
model_mode
relation_variant
beta
seed
N
d
steps
baseline_count
mutation_rate
sector_size
lifetime
edge_count
density
n_components
largest_component_fraction
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_edge_count
largest_component_node_count
largest_component_cycle_rank
mean_degree
degree_variance
max_degree
clustering
spectral_gap_optional
spectral_gap_available
algebraic_connectivity_optional
algebraic_connectivity_available
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

---

## 8. Required summary output

Summary output path:

```text
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
```

Group by:

```text
model_mode
relation_variant
beta
```

Required summary columns:

```text
runs
structure_success_rate
mean_edge_count
mean_density
mean_n_components
mean_largest_component_fraction
mean_bridge_count
mean_bridge_fraction
mean_non_bridge_edge_count
mean_cycle_rank
mean_largest_component_cycle_rank
mean_mean_degree
mean_degree_variance
mean_max_degree
mean_sector_size
mean_failed_p_gnp
mean_failed_p_dp
mean_dp_valid
mean_dp_swap_success_rate
```

Also include distribution quantiles where feasible:

```text
q25_non_bridge_edge_count
q50_non_bridge_edge_count
q75_non_bridge_edge_count
q25_cycle_rank
q50_cycle_rank
q75_cycle_rank
q25_bridge_fraction
q50_bridge_fraction
q75_bridge_fraction
```

---

## 9. Required per-seed paired output

Per-seed output path:

```text
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
```

Purpose:

```text
Compare compensated and uncompensated outcomes for the same seed.
```

Required columns:

```text
seed
edge_count_compensated
edge_count_uncompensated
delta_edge_count
bridge_fraction_compensated
bridge_fraction_uncompensated
delta_bridge_fraction
non_bridge_edge_count_compensated
non_bridge_edge_count_uncompensated
delta_non_bridge_edge_count
cycle_rank_compensated
cycle_rank_uncompensated
delta_cycle_rank
largest_component_fraction_compensated
largest_component_fraction_uncompensated
delta_largest_component_fraction
structure_success_compensated
structure_success_uncompensated
delta_structure_success
failed_p_gnp_compensated
failed_p_gnp_uncompensated
failed_p_dp_compensated
failed_p_dp_uncompensated
```

Do not treat mode rows as independent if paired seed comparison is possible.

---

## 10. Required statistical analysis output

Optional but recommended output:

```text
outputs/regression_v010_connectivity_entanglement_audit_variant2.csv
```

Analysis plan:

```text
1. Compare topology descriptors between compensated and uncompensated modes.
2. Estimate whether structure_success is better explained by topology descriptors than by model_mode alone.
3. Estimate a minimal non_bridge_edge_count / cycle_rank threshold associated with structure_success > 0.5.
```

Suggested simple models:

```text
structure_success ~ model_mode
structure_success ~ edge_count
structure_success ~ non_bridge_edge_count
structure_success ~ cycle_rank
structure_success ~ bridge_fraction
structure_success ~ model_mode + edge_count + bridge_fraction + non_bridge_edge_count
```

If logistic regression dependencies or numerical stability are problematic, do not add new dependencies. Instead output descriptive correlations and threshold tables.

Strict dependency rule:

```text
Do not install new packages.
Use only existing project dependencies.
```

---

## 11. Threshold analysis

Required threshold table path:

```text
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
```

Suggested thresholds:

```text
non_bridge_edge_count >= k
cycle_rank >= k
bridge_fraction <= x
```

For each threshold, report:

```text
threshold_type
threshold_value
rows_above_threshold
structure_success_rate_above_threshold
rows_below_threshold
structure_success_rate_below_threshold
```

Purpose:

```text
Estimate whether there is a topology threshold below which structure_success collapses.
```

---

## 12. Interpretation rules

Allowed interpretations:

```text
1. compensation-connectivity coupling in this toy model;
2. connectivity-threshold-dependent candidate;
3. topology descriptors mediate or explain observed structure_success;
4. density-independent mechanism claim remains blocked;
5. edge-removal rescue is no longer the main path.
```

Forbidden interpretations:

```text
1. Variant 2 proves density-independent compensation mechanism;
2. compensation causally creates structure independent of graph topology;
3. physical theory relevance;
4. direct claims about real constants, causality, or spacetime;
5. success if only edge_count differs but topology descriptors do not explain outcomes.
```

---

## 13. Implementation strategy

Preferred script:

```text
tools/audit_connectivity_entanglement_variant2.py
```

Reason:

```text
This is no longer an ablation by removal; it is a topology audit.
It should not be added to the pruning/ablation tool unless reuse is unavoidable.
```

Required CLI:

```powershell
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2

.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode full --out-prefix v010_connectivity_entanglement_audit_variant2
```

Smoke settings:

```text
model_modes = [compensated, uncompensated]
seeds = 2
baseline_count = 10
target beta = 0.003
```

Full settings:

```text
model_modes = [compensated, uncompensated]
seeds = 100
baseline_count = 100
target beta = 0.003
```

---

## 14. Required smoke validation

Before full run:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\audit_connectivity_entanglement_variant2.py
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2
Get-Content outputs\raw_smoke_connectivity_entanglement_audit_variant2.csv -TotalCount 1
Get-Content outputs\summary_smoke_connectivity_entanglement_audit_variant2.csv
Get-Content outputs\per_seed_smoke_connectivity_entanglement_audit_variant2.csv
```

Expected smoke outputs:

```text
outputs/raw_smoke_connectivity_entanglement_audit_variant2.csv
outputs/summary_smoke_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_smoke_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_smoke_connectivity_entanglement_audit_variant2.csv
```

Full mode must not be run until smoke validation is reviewed.

---

## 15. What must not change

Do not change:

```text
Variant 2 relation logic;
structure_success criteria;
p_gnp threshold;
p_dp threshold;
dp_valid requirement;
lifetime threshold;
sector_size bounds;
existing confirm_connectivity interpretation;
existing ablation results;
existing tool outputs.
```

Do not add dependencies.

Do not use global Python.

Use only:

```powershell
.\.venv\Scripts\python.exe
```

---

## 16. Review step after execution

After full audit execution, prepare a Qwen review packet asking:

```text
1. Did the audit confirm compensation-connectivity coupling?
2. Which topology descriptor best explains structure_success?
3. Is beta=0.003 still a useful study regime?
4. Is publication as confound-isolation study justified?
5. What controls remain before technical write-up?
```

---

## 17. Current status

```text
Design checkpoint created.
No code implemented.
No smoke run executed.
No full run authorized.
```

Short invariant:

```text
Measure native topology first. Do not prune. Do not rescue.
```
