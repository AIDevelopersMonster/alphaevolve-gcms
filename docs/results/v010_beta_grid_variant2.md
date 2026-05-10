# v0.10 Variant 2 beta-grid results

**Date:** 2026-05-09  
**Experiment:** Variant 2 beta-grid  
**Source files:**

- `outputs/raw_v010_beta_grid_variant2.csv`
- `outputs/summary_v010_beta_grid_variant2.csv`
- `outputs/comparison_v010_beta_grid_variant2.csv`
- `outputs/residual_v010_beta_grid_variant2.csv`

## Purpose

The previous focused Variant 2 run showed a very large difference between compensated and uncompensated worlds at `beta=0.05` and `beta=0.5`.

However, a density audit showed that at those beta values the uncompensated graph was strongly sparsified or collapsed. Therefore, the key question became:

```text
Is there a smaller beta where the compensation effect appears
while the uncompensated graph still remains alive?
```

This beta-grid run tests that question.

---

## Relation tested

Variant 2 uses the compensation-alignment relation:

```text
K_B = sum_B I_i
R_ij = exp(-alpha * ||I_i - I_j||^2 - beta * |(I_i + I_j) dot K_B|)
```

This relation is pair-specific and sensitive to the global residual `K_B`.

---

## Configuration

```text
N = 150
d = 4
steps = 200
seeds = 50
baseline_count = 100
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
model_modes = compensated, uncompensated
relation_variant = 2
betas = 0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05
epsilon_norms = 0.0
lambda_values = 0.0
```

---

## Statistical audit method

The post-run audit used:

```text
Wilson score interval for individual structure_success rates.
Approximate normal confidence interval for the difference of two proportions.
Exact McNemar test, implemented as a two-sided exact binomial test on discordant paired seeds.
```

The McNemar test is appropriate here because compensated and uncompensated runs are paired by seed.

---

## Main observed transition

The compensated mode stayed essentially stable across beta values:

```text
compensated structure_success = 37 / 50 = 74%
```

The uncompensated mode degraded as beta increased:

```text
beta=0.000 -> 35 / 50 = 70%
beta=0.001 -> 37 / 50 = 74%
beta=0.002 -> 33 / 50 = 66%
beta=0.005 -> 22 / 50 = 44%
beta=0.010 ->  7 / 50 = 14%
beta=0.020 ->  1 / 50 = 2%
beta=0.050 ->  1 / 50 = 2%
```

This suggests a compensation-sensitive transition rather than a single binary effect.

---

## Regime interpretation

### 1. Distance-like regime

```text
beta = 0.000, 0.001, 0.002
```

The effect is small or statistically weak. The system behaves close to the distance-only control.

### 2. Intermediate non-collapse compensation regime

```text
beta = 0.005
```

This is the current most interesting regime.

Observed structure_success result:

```text
compensated:   37 / 50 = 74%
uncompensated: 22 / 50 = 44%
compensation_effect_attempted = +30 percentage points
approx 95% CI for effect = [11.6%, 48.4%]
exact McNemar p ~= 0.0041
```

Paired seed table:

```text
both_success:   17
comp_only:      20
uncomp_only:     5
both_fail:       8
```

Direct density/sector audit at `beta=0.005`:

```text
                 compensated     uncompensated
analyzed         46 / 50         46 / 50
structure_success 37 / 50        22 / 50
edge_count       43.36           19.18
density           0.119888        0.223705
mean_degree       2.657782        2.373795
sector_size      28.74           14.16
lifetime        152.52          134.82
dp_valid          0.90            0.84
```

Interpretation:

At `beta=0.005`, the uncompensated mode is degraded but not collapsed. It has the same analyzed-run fraction as the compensated mode (`46/50`), nonzero edge count, long lifetime, and comparable mean degree inside detected sectors.

However, it forms smaller sectors with fewer edges and lower success rate. This supports an intermediate **compensation-sensitive degradation** regime, not a pure graph-collapse explanation.

This makes `beta=0.005` a better scientific candidate than `beta=0.05`, because the effect is not simply caused by total graph collapse.

### 3. Collapse / sparsification regime

```text
beta = 0.01, 0.02, 0.05
```

The observed compensation effect becomes larger, but the uncompensated graph increasingly loses analyzable sectors.

At `beta=0.01`:

```text
uncompensated structure_success = 7 / 50 = 14%
uncompensated analyzed_runs = 38 / 50
uncompensated mean edge_count ~= 8.76
uncompensated mean sector_size ~= 7.46
uncompensated mean lifetime ~= 108.32
```

At `beta=0.05`:

```text
uncompensated structure_success = 1 / 50 = 2%
uncompensated analyzed_runs = 7 / 50
uncompensated mean edge_count ~= 0.56
uncompensated mean density ~= 0.0384
uncompensated mean sector_size ~= 0.82
uncompensated mean lifetime ~= 14.08
```

Thus `beta=0.05` should no longer be treated as the cleanest result. It remains evidence of compensation sensitivity, but likely includes graph-density collapse.

---

## Updated main interpretation

The current best statement is:

```text
Variant 2 shows a compensation-sensitive transition.
For very small beta, it behaves close to the distance-only control.
Around beta=0.005, compensated worlds retain structure while uncompensated worlds degrade without full collapse.
For larger beta, uncompensated worlds undergo strong graph sparsification or collapse.
```

This is stronger and more precise than the earlier statement that Variant 2 simply has a large compensation effect.

---

## Scientific significance

This beta-grid supports the idea that global compensation can become functionally meaningful when local relations are sensitive to the global residual.

The most important point is not the largest effect size. The most important point is the appearance of an intermediate regime:

```text
not distance-only
not collapsed
but compensation-sensitive
```

This aligns with the broader GCMS intuition:

```text
exact zero -> stability
small compensation-aware perturbation -> structured differentiation
large residual penalty -> collapse
```

The result also supports the next conceptual hypothesis:

```text
development may occur near zero, not merely at zero or far from zero.
```

---

## Limitations

1. This is still a toy-model result.
2. It does not prove a physical theory.
3. The current confidence interval for the effect is an approximate two-proportion interval, not a paired bootstrap interval.
4. Degree variance and full degree distributions were not recorded in the raw output.
5. `beta=0.005` needs confirmation with more seeds.
6. The transition curve should be refined around `0.003-0.008`.
7. The analyzed-run failures should be characterized directly in future scripts.

---

## Recommended next experiment

Refine around the current candidate:

```text
relation_variant = 2
model_modes = compensated, uncompensated
beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008
N = 150
steps = 200
seeds = 100
baseline_count = 100
```

Required outputs and analysis:

```text
structure_success_rate_attempted
structure_success_rate_analyzed
compensation_effect_attempted
confidence intervals
McNemar p-value
mean_density
mean_edge_count
mean_degree
degree variance / degree distribution
analyzed_runs
mean_sector_size
mean_lifetime
failure-mode counts
```

Primary target:

```text
Find the weakest beta where compensation_effect is reliably positive
while the uncompensated graph remains analyzable and non-collapsed.
```

---

## Updated publication posture

The beta-grid result strengthens the draft technical note by showing a transition law rather than only a large separation at harsh beta.

Recommended wording:

```text
In Variant 2, increasing beta produces a compensation-sensitive transition. The intermediate regime around beta=0.005 shows a positive compensation effect without full uncompensated graph collapse, making it the current leading candidate for a nontrivial GCMS mechanism.
```

Avoid stronger wording such as:

```text
Variant 2 proves global compensation causes local structure.
```

The correct status remains:

```text
preliminary toy-model mechanism, now supported by a focused transition experiment and a direct density audit.
```
