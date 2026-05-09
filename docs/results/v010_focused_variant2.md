# v0.10 focused Variant 2 results

**Date:** 2026-05-09  
**Experiment:** `focused_v010` / Variant 2 compensation-aware relation  
**Source files:**

- `outputs/raw_v010_focused_variant2.csv`
- `outputs/summary_v010_focused_variant2.csv`
- `outputs/comparison_v010_focused_variant2.csv`
- `outputs/residual_v010_focused_variant2.csv`

## Purpose

This experiment tests whether a compensation-aware relation can create a real structural difference between globally compensated and uncompensated worlds.

The previous v0.9.1 distance-only relation was translation-invariant:

```text
R_ij = exp(-alpha * ||I_i - I_j||^2)
```

Because subtracting the global mean does not change pairwise distances, v0.9.1 could show non-random sectors but could not prove that global compensation caused them.

The v0.10.2 focused run therefore compares:

- Variant 0: distance-only control.
- Variant 2: compensation-aware candidate.

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
relation_variants = 0, 2
betas = 0.0, 0.05, 0.5
epsilon_norms = 0.0
lambda_values = 0.0
```

Total attempted runs:

```text
400
```

## Success metrics

```text
compensation_valid = global_error < 1e-12

structure_success =
    p_gnp_empirical < 0.05
    and p_dp_empirical < 0.05
    and dp_valid
    and lifetime > 20
    and 5 <= sector_size <= 60

strict_success = compensation_valid and structure_success
```

The main comparison uses `structure_success`, because uncompensated worlds are expected to fail `compensation_valid` by construction.

## Variant 0 control

Variant 0 uses the old distance-only relation:

```text
R_ij = exp(-alpha * ||I_i - I_j||^2)
```

Results:

```text
compensated:   37 / 50 structure_success = 74%
uncompensated: 35 / 50 structure_success = 70%
compensation_effect_attempted = +4%
```

Analyzed-rate comparison:

```text
compensated:   37 / 46 = 80.43%
uncompensated: 35 / 45 = 77.78%
compensation_effect_analyzed ~= +2.66%
```

Interpretation:

Variant 0 behaves as expected. The compensation effect is near zero. This confirms that distance-only graph structure is approximately insensitive to global compensation.

The small nonzero difference may come from sector selection through `chi`, which is not fully translation-invariant.

## Variant 2 candidate

Variant 2 uses the compensation-alignment relation:

```text
K_B = sum_B I_i
R_ij = exp(-alpha * ||I_i - I_j||^2 - beta * |(I_i + I_j) dot K_B|)
```

This relation is pair-specific and sensitive to the global residual `K_B`.

### beta = 0.05

Results:

```text
compensated:   37 / 50 structure_success = 74%
uncompensated:  1 / 50 structure_success = 2%
compensation_effect_attempted = +72%
```

Analyzed-rate comparison:

```text
compensated:   37 / 46 = 80.43%
uncompensated:  1 / 7  = 14.29%
compensation_effect_analyzed ~= +66.15%
```

Paired seed comparison:

```text
both successful:        1
compensated only:      36
uncompensated only:     0
both unsuccessful:     13
```

Interpretation:

At beta 0.05, Variant 2 shows a strong and directional compensation effect. Most successful sectors occur only in the compensated mode.

### beta = 0.5

Results:

```text
compensated:   37 / 50 structure_success = 74%
uncompensated:  0 / 50 structure_success = 0%
compensation_effect_attempted = +74%
```

Analyzed-rate comparison:

```text
compensated:   37 / 46 = 80.43%
uncompensated:  0 analyzed
compensation_effect_analyzed ~= +80.43%
```

Paired seed comparison:

```text
compensated only:      37
both unsuccessful:     13
uncompensated only:     0
both successful:        0
```

Interpretation:

At beta 0.5, uncompensated worlds fail to produce analyzable successful sectors under this relation, while compensated worlds preserve the same success rate as Variant 0.

This is a strong signal, but beta 0.5 may be a harsh gate. The beta 0.05 result is more interpretable as a candidate mechanism.

## Scientific interpretation

The focused Variant 2 run supports the following toy-model result:

```text
When local relations are sensitive to the global residual K_B,
globally compensated worlds preserve long-lived non-random local sectors,
while uncompensated worlds largely lose them.
```

This is stronger than v0.9.1 because Variant 0 now acts as a control confirming that the old distance-only graph is insensitive to compensation, while Variant 2 introduces a relation where compensation becomes functionally meaningful.

## Limitations

This result does not prove a physical theory.

It shows a toy-model mechanism:

```text
global compensation + compensation-aware relation
    -> stable non-random local graph sectors
```

Further checks are needed:

1. Repeat around smaller beta grid values, for example `0.01, 0.02, 0.05, 0.1`.
2. Test more seeds for the best beta.
3. Add confidence intervals for `compensation_effect`.
4. Confirm that the effect is not purely due to graph-density collapse in uncompensated mode.
5. Inspect density and analyzed-runs behavior for beta 0.05.

## Current status

Variant 2 is the leading v0.10 candidate.

Recommended next focused run:

```text
relation_variant = 2
beta = 0.01, 0.02, 0.05, 0.1
model_modes = compensated, uncompensated
seeds = 100
baseline_count = 100
```

Primary target:

```text
Find the weakest beta that produces a stable positive compensation_effect
without simply destroying the uncompensated graph.
```
