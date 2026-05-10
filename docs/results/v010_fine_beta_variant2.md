# v0.10 Fine Beta Grid Result: Variant 2

**Status:** exploratory / pre-confirmatory result note  
**Date:** 2026-05-10  
**Experiment mode:** `fine_beta_v010`  
**Output prefix:** `v010_fine_beta_variant2`  
**Related review:** `docs/reviews/v010_fine_beta_experiment_review.md`  
**Related protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Processing tool:** `tools/audit_gcms_lite.py`  

---

## 1. Purpose

This run refines the Variant 2 compensation-alignment relation around the previous candidate region near `beta ~= 0.005`.

The purpose is not to make a final physical claim.

The purpose is to check whether the compensation-sensitive effect appears in a low-beta, non-collapse regime.

---

## 2. Experiment design

```text
relation_variant = 2
model_modes = compensated, uncompensated
beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008
seeds = 100
baseline_count = 100
```

Expected run count:

```text
2 model modes * 6 beta values * 100 seeds = 1200 runs
```

Runtime:

```text
26447.59 sec ~= 7 h 20 min 48 sec
```

Produced files:

```text
outputs/raw_v010_fine_beta_variant2.csv
outputs/summary_v010_fine_beta_variant2.csv
outputs/comparison_v010_fine_beta_variant2.csv
outputs/residual_v010_fine_beta_variant2.csv
```

Generated local lite-audit files:

```text
outputs/v010_fine_beta_variant2_lite_summary.csv
outputs/v010_fine_beta_variant2_lite_effect.csv
outputs/v010_fine_beta_variant2_lite_effect.png
outputs/v010_fine_beta_variant2_lite_report.md
outputs/v010_fine_beta_variant2_mcnemar_wilson.csv
```

Generated outputs are local artifacts and should not be committed unless explicitly archived.

---

## 3. Primary endpoint

Primary endpoint:

```text
compensation_effect_attempted =
structure_success_rate_attempted(compensated) - structure_success_rate_attempted(uncompensated)
```

Reason:

```text
Attempted denominator preserves failed and unanalyzable runs as part of the experimental outcome.
```

---

## 4. Lite audit effect table

The lite auditor recomputed effect values directly from `outputs/raw_v010_fine_beta_variant2.csv`.

| beta | compensated_rate | uncompensated_rate | effect | comp_analyzed | uncomp_analyzed | comp_edges | uncomp_edges | comp_density | uncomp_density | comp_mean_degree | uncomp_mean_degree | comp_sector | uncomp_sector | comp_lifetime | uncomp_lifetime |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.003 | 0.72 | 0.52 | 0.20 | 90 | 96 | 45.08 | 25.30 | 0.118717 | 0.195286 | 2.619071 | 2.552747 | 29.86 | 18.17 | 143.43 | 158.57 |
| 0.004 | 0.72 | 0.38 | 0.34 | 90 | 93 | 45.08 | 19.85 | 0.118717 | 0.216974 | 2.619071 | 2.385972 | 29.86 | 14.54 | 143.43 | 146.92 |
| 0.005 | 0.72 | 0.35 | 0.37 | 90 | 89 | 45.08 | 17.46 | 0.118717 | 0.230230 | 2.619071 | 2.276014 | 29.86 | 12.97 | 143.43 | 135.67 |
| 0.006 | 0.72 | 0.24 | 0.48 | 90 | 86 | 45.08 | 13.91 | 0.118717 | 0.251008 | 2.619071 | 2.128619 | 29.86 | 10.73 | 143.43 | 132.48 |
| 0.007 | 0.72 | 0.18 | 0.54 | 90 | 85 | 45.08 | 12.17 | 0.118717 | 0.262096 | 2.619071 | 2.028813 | 29.86 | 9.72 | 143.43 | 129.84 |
| 0.008 | 0.72 | 0.19 | 0.53 | 90 | 84 | 45.08 | 10.87 | 0.118717 | 0.265139 | 2.619071 | 1.974042 | 29.86 | 8.87 | 143.43 | 132.58 |

---

## 5. Paired McNemar / Wilson audit

| beta | n | comp_success | uncomp_success | effect | comp_CI_95 | uncomp_CI_95 | both_success | comp_only | uncomp_only | both_fail | McNemar p |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.003 | 100 | 72 | 52 | 0.20 | [0.625, 0.799] | [0.423, 0.615] | 40 | 32 | 12 | 16 | 3.66e-03 |
| 0.004 | 100 | 72 | 38 | 0.34 | [0.625, 0.799] | [0.291, 0.478] | 27 | 45 | 11 | 17 | 5.38e-06 |
| 0.005 | 100 | 72 | 35 | 0.37 | [0.625, 0.799] | [0.264, 0.447] | 27 | 45 | 8 | 20 | 2.37e-07 |
| 0.006 | 100 | 72 | 24 | 0.48 | [0.625, 0.799] | [0.167, 0.332] | 19 | 53 | 5 | 23 | 3.50e-11 |
| 0.007 | 100 | 72 | 18 | 0.54 | [0.625, 0.799] | [0.117, 0.267] | 14 | 58 | 4 | 24 | 2.59e-13 |
| 0.008 | 100 | 72 | 19 | 0.53 | [0.625, 0.799] | [0.125, 0.278] | 17 | 55 | 2 | 26 | 2.30e-14 |

Observation:

```text
All tested beta values show a positive paired compensation effect.
The effect is already statistically supported at beta=0.003.
```

---

## 6. Collapse / sparsification audit

The effect increases as beta increases, but uncompensated graph-sector quantities decline.

Key uncompensated trend:

```text
beta=0.003: edge_count=25.30, sector_size=18.17, analyzed=96/100
beta=0.004: edge_count=19.85, sector_size=14.54, analyzed=93/100
beta=0.005: edge_count=17.46, sector_size=12.97, analyzed=89/100
beta=0.006: edge_count=13.91, sector_size=10.73, analyzed=86/100
beta=0.007: edge_count=12.17, sector_size=9.72, analyzed=85/100
beta=0.008: edge_count=10.87, sector_size=8.87, analyzed=84/100
```

Interpretation:

```text
The transition is not an immediate full graph collapse in this range,
because analyzed_counts remain high.

However, increasing beta progressively degrades uncompensated edge_count,
sector_size, and mean_degree, so larger effects at beta >= 0.006 carry
stronger sparsification/confound risk.
```

---

## 7. Candidate classification

### Earliest clean exploratory candidate

```text
beta = 0.003
```

Reason:

```text
- effect = +20 percentage points;
- McNemar p = 3.66e-03;
- uncompensated analyzed_count = 96/100;
- uncompensated edge_count = 25.30;
- uncompensated sector_size = 18.17;
- uncompensated lifetime = 158.57;
- lowest beta tested, therefore least likely to be dominated by sparsification.
```

### Stronger exploratory candidates

```text
beta = 0.004 and beta = 0.005
```

Reason:

```text
- beta=0.004 effect = +34 pp, McNemar p = 5.38e-06;
- beta=0.005 effect = +37 pp, McNemar p = 2.37e-07;
- both remain substantially analyzable, but show more graph-sector degradation than beta=0.003.
```

### High-effect but higher-confound region

```text
beta = 0.006, 0.007, 0.008
```

Reason:

```text
- effects are larger, from +48 to +54 pp;
- uncompensated edge_count, sector_size, and mean_degree continue to decline;
- these values require stronger connectivity/failure-mode audit before being called clean.
```

---

## 8. Conservative result statement

Conservative statement:

```text
The fine beta-grid supports an exploratory toy-model compensation-sensitive
transition in Variant 2. The earliest statistically supported non-collapse
candidate is beta=0.003, while beta=0.004-0.005 provide stronger effects with
increasing sparsification risk. Larger beta values show stronger effects but
are less clean because uncompensated graph-sector quantities decline.
```

What this does not show:

```text
This does not prove a physical theory.
This does not establish final confirmation of the mechanism.
This does not rule out connectivity fragmentation or unreported failure-mode confounds.
```

---

## 9. Limitations

Known limitations of the current run:

```text
1. No largest_component_fraction.
2. No n_components.
3. No degree_variance or degree_gini.
4. No failure_reason / per-criterion failure counts.
5. No explicit density-matched ablation.
6. Multiple beta values were tested; beta=0.005 was prior candidate, but beta=0.003 emerges as earliest positive point.
```

Therefore:

```text
This run should be treated as exploratory / pre-confirmatory.
A confirmatory run should add connectivity and failure-mode metrics.
```

---

## 10. Recommended next experiment

If the project chooses the earliest clean candidate:

```text
confirmatory_variant2_beta003
relation_variant = 2
beta = 0.003
model_modes = compensated, uncompensated
seeds = 200
baseline_count = 100
```

Required additions:

```text
largest_component_fraction
n_components
degree_variance or degree_gini
failure_reason
per-criterion failure counts
recorded audit-tool commit/version
```

Alternative if treating beta=0.004-0.005 as stronger transition region:

```text
confirmatory_variant2_beta003_005
beta = 0.003, 0.004, 0.005
seeds = 200 each
apply primary-beta or multiple-testing plan before run
```

---

## 11. Result status

```text
Result status: strong exploratory support.
Leading clean candidate: beta=0.003.
Strong transition region: beta=0.004-0.005.
High-effect/high-confound region: beta=0.006-0.008.
Next step: Qwen result review, then confirmatory design with connectivity/failure metrics.
```
