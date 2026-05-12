# Result Note: v010_connectivity_entanglement_audit_variant2

**Status:** result note / requires external review  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `connectivity_entanglement_audit_variant2`  
**Tool:** `tools/audit_connectivity_entanglement_variant2.py`  
**Design checkpoint:** `docs/experiments/connectivity_entanglement_audit_variant2_design.md`  
**Extension plan:** `docs/experiments/connectivity_entanglement_audit_variant2_extension_plan.md`  
**Smoke validation:** `docs/results/smoke_connectivity_entanglement_audit_variant2_validation.md`  
**Reframe:** `docs/experiments/connectivity_entanglement_reframe.md`  
**Qwen reframe review:** `docs/reviews/connectivity_entanglement_reframe_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Execution summary

Command executed locally:

```powershell
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode full --out-prefix v010_connectivity_entanglement_audit_variant2
```

Generated outputs:

```text
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
```

Run integrity:

```text
raw rows = 200
compensated rows = 100
uncompensated rows = 100
git status after run = clean
```

Generated outputs are local artifacts and are not committed.

---

## 2. Purpose

This audit follows the post-LCF reframe.

It is not a pruning experiment.
It is not an edge-removal ablation.
It is not a rescue attempt for the original density-independent claim.

The purpose is:

```text
Measure native topology produced by compensated and uncompensated Variant 2 dynamics at beta=0.003.
```

Core invariant:

```text
Measure native topology first. Do not prune. Do not rescue.
```

The audit tests whether the observed compensated advantage is associated with native connectivity descriptors such as:

```text
edge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_cycle_rank
sector_size
```

---

## 3. Experimental settings

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

Expected rows:

```text
2 modes x 100 seeds = 200 rows
```

Observed rows:

```text
200 rows
```

---

## 4. Summary result

From `outputs/summary_v010_connectivity_entanglement_audit_variant2.csv`:

| model_mode | runs | structure_success_rate | mean_edge_count | mean_density | mean_LCF | mean_bridge_count | mean_bridge_fraction | mean_non_bridge_edge_count | mean_cycle_rank | mean_LCC_cycle_rank | mean_sector_size | mean_global_error | mean_sector_chi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| compensated | 100 | 0.72 | 44.96 | 0.1184 | 0.8908 | 11.44 | 0.2691 | 33.52 | 16.09 | 15.93 | 29.86 | 1.12e-14 | 16.35 |
| uncompensated | 100 | 0.53 | 25.35 | 0.2003 | 0.9559 | 7.53 | 0.3353 | 17.82 | 8.16 | 8.15 | 18.17 | 23.62 | 11.14 |

Primary observation:

```text
Compensated beta=0.003 produces higher structure_success and substantially higher native connectivity capacity: more edges, more non-bridge edges, higher cycle rank, higher LCC cycle rank, and larger sectors.
```

Important caveat:

```text
This supports connectivity-entanglement, not density-independent mechanism proof.
```

---

## 5. Paired per-seed evidence

The per-seed output compares compensated and uncompensated graphs at the same seed.

Example rows from `outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv` show large seed-dependent differences:

```text
seed 0:
    delta_edge_count = +15
    delta_non_bridge_edge_count = +12
    delta_cycle_rank = +6
    delta_structure_success = 0

seed 3:
    delta_edge_count = +50
    delta_non_bridge_edge_count = +41
    delta_cycle_rank = +17
    delta_structure_success = +1

seed 4:
    delta_edge_count = +22
    delta_non_bridge_edge_count = +24
    delta_cycle_rank = +11
    delta_structure_success = +1

seed 10:
    delta_edge_count = +36
    delta_non_bridge_edge_count = +31
    delta_cycle_rank = +13
    delta_structure_success = +1
```

The paired table is important because it avoids treating mode rows as fully independent when seed-matched comparison is possible.

---

## 6. Threshold analysis

From `outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv`:

### non_bridge_edge_count thresholds

| threshold | rows above | success above | rows below | success below |
|---:|---:|---:|---:|---:|
| >= 19 | 105 | 0.981 | 95 | 0.232 |
| >= 38 | 57 | 1.000 | 143 | 0.476 |
| >= 57 | 18 | 1.000 | 182 | 0.588 |

### cycle_rank thresholds

| threshold | rows above | success above | rows below | success below |
|---:|---:|---:|---:|---:|
| >= 10 | 98 | 0.969 | 102 | 0.294 |
| >= 21 | 46 | 1.000 | 154 | 0.513 |
| >= 31 | 15 | 1.000 | 185 | 0.595 |

### edge_count thresholds

| threshold | rows above | success above | rows below | success below |
|---:|---:|---:|---:|---:|
| >= 22 | 130 | 0.885 | 70 | 0.143 |
| >= 41 | 71 | 1.000 | 129 | 0.419 |
| >= 66 | 33 | 1.000 | 167 | 0.551 |

Primary threshold observation:

```text
Structure_success is strongly associated with non_bridge_edge_count, cycle_rank, largest_component_cycle_rank, and edge_count thresholds.
```

Most striking threshold:

```text
non_bridge_edge_count >= 19:
    structure_success_rate = 0.981
non_bridge_edge_count < 19:
    structure_success_rate = 0.232
```

This is consistent with the connectivity-threshold-dependent reframe.

---

## 7. Correlation analysis

From `outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv`:

| feature | target | pearson correlation |
|---|---|---:|
| edge_count | structure_success | 0.704 |
| non_bridge_edge_count | structure_success | 0.690 |
| cycle_rank | structure_success | 0.642 |
| largest_component_cycle_rank | structure_success | 0.638 |
| max_degree | structure_success | 0.647 |
| mean_degree | structure_success | 0.572 |
| degree_variance | structure_success | 0.509 |
| sector_size | structure_success | 0.700 |
| density | structure_success | -0.458 |
| bridge_fraction | structure_success | -0.242 |

Failure correlations:

```text
edge_count vs failed_p_gnp = -0.534
non_bridge_edge_count vs failed_p_gnp = -0.545
cycle_rank vs failed_p_gnp = -0.513
bridge_fraction vs failed_p_gnp = +0.478
```

Interpretation:

```text
Higher native connectivity capacity is associated with higher structure_success and lower p_gnp / p_dp failure rates.
```

Important caveat:

```text
These correlations are descriptive and do not establish causal mediation by themselves.
```

---

## 8. Passive residual diagnostics

The audit included passive diagnostics that do not affect success criteria:

```text
global_error
global_vector_norm
compensation_valid
sector_chi
```

Summary:

```text
compensated mean_global_error approx 1.12e-14
uncompensated mean_global_error approx 23.62
compensated mean_sector_chi approx 16.35
uncompensated mean_sector_chi approx 11.14
```

Interpretation:

```text
The compensated mode is globally balanced while also producing larger sector_chi and stronger native connectivity descriptors.
```

This supports a future residual/sector-stability diagnostic, but does not by itself prove a residual-stability mechanism.

Allowed conclusion:

```text
Residual and sector-level compensation diagnostics were successfully recorded for post-hoc analysis.
```

Forbidden conclusion:

```text
The residual mechanism is proven.
```

---

## 9. Relation to prior LCF ablation

Prior LCF-constrained ablation showed:

```text
strict low-edge matching while preserving LCF is often infeasible;
failed_no_non_bridge_edges dominates;
valid low-edge LCF-matched rows do not exceed the uncompensated reference.
```

This audit explains why that happened:

```text
Compensated graphs naturally occupy a higher non_bridge_edge_count / cycle_rank regime.
Pruning them down toward uncompensated edge counts removes or exhausts the cycle capacity that appears associated with structure_success.
```

Therefore, the project should not interpret the original compensated advantage as density-independent.

Instead:

```text
The compensated advantage appears entangled with native connectivity production.
```

---

## 10. Claim impact

### Supported by this audit

```text
1. Compensated Variant 2 beta=0.003 produces a different native topology regime than uncompensated beta=0.003.
2. The compensated regime has higher edge_count, non_bridge_edge_count, cycle_rank, and LCC cycle rank.
3. structure_success is strongly associated with these connectivity descriptors.
4. The connectivity-threshold-dependent candidate status is supported.
5. The reframe toward compensation-connectivity entanglement is strengthened.
```

### Not supported by this audit

```text
1. Density-independent compensation mechanism.
2. Causal proof that compensation alone creates structure.
3. Physical theory relevance.
4. Claims about real-world constants, spacetime, gravity, or photons.
5. Return to edge-removal rescue as the main path.
```

---

## 11. Current status of beta=0.003

Before LCF ablation:

```text
leading clean positive candidate
```

After LCF ablation:

```text
connectivity-threshold-dependent candidate
```

After this topology audit:

```text
connectivity-threshold-dependent candidate remains useful and is now better characterized.
```

Updated status:

```text
useful study regime for compensation-connectivity entanglement
```

---

## 12. Conservative conclusion

Pre-review conclusion:

```text
The connectivity entanglement audit supports the post-LCF reframe. In Variant 2 at beta=0.003, compensated graphs show higher structure_success and a substantially different native topology: higher edge_count, higher non_bridge_edge_count, higher cycle_rank, and higher largest-component cycle rank. Structure_success is strongly associated with these topology descriptors, especially non_bridge_edge_count and cycle_rank thresholds. This supports interpreting beta=0.003 as a connectivity-threshold-dependent study regime rather than a clean density-independent mechanism. The result strengthens the confound-isolation narrative: the original positive signal appears entangled with native connectivity generation. It does not prove a causal mechanism and does not support physical overclaims.
```

---

## 13. Next review step

Submit this result to Qwen for methodological review.

Questions for Qwen:

```text
1. Does this audit support the compensation-connectivity entanglement reframe?
2. Which topology descriptor should be treated as primary: non_bridge_edge_count, cycle_rank, edge_count, sector_size, or another descriptor?
3. Is the non_bridge_edge_count >= 19 threshold meaningful enough to report, or too post-hoc?
4. Does the audit explain the LCF ablation failure mode?
5. Is beta=0.003 now a useful study regime for a confound-isolation paper?
6. Are descriptive correlations sufficient, or is a paired/logistic analysis required before writing?
7. How should passive residual diagnostics be reported?
8. What conservative wording is publication-safe?
9. What additional controls are required before a technical write-up?
```

No stronger claim should be made before Qwen review.
