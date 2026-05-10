# Result Note: v010_confirm_connectivity_variant2

**Status:** pre-review result note  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `confirm_connectivity_variant2`  
**Design checkpoint:** `docs/experiments/confirm_connectivity_variant2_design.md`  
**Expectations checkpoint:** `docs/experiments/confirm_connectivity_variant2_expectations.md`  
**Experiment script:** `experiments/ae_v010_2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Execution summary

Command executed locally:

```powershell
.\.venv\Scripts\python.exe experiments\ae_v010_2.py --mode confirm_connectivity_variant2 --out-prefix v010_confirm_connectivity_variant2
```

Generated outputs:

```text
outputs/raw_v010_confirm_connectivity_variant2.csv
outputs/summary_v010_confirm_connectivity_variant2.csv
outputs/comparison_v010_confirm_connectivity_variant2.csv
outputs/residual_v010_confirm_connectivity_variant2.csv
```

Runtime:

```text
15629.69 sec ≈ 4.34 hours
```

Working tree status after run:

```text
git status --short: clean
```

Generated outputs are local artifacts and are not committed.

---

## 2. Schema validation

Raw output schema includes required diagnostics:

```text
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
n_components
largest_component_fraction
degree_variance
```

Summary output schema includes required aggregate diagnostics:

```text
mean_n_components
mean_largest_component_fraction
mean_degree_variance
failed_p_gnp_rate
failed_p_dp_rate
failed_dp_valid_rate
failed_lifetime_rate
failed_sector_size_rate
```

Schema validation passed.

---

## 3. Primary comparison result

From `outputs/comparison_v010_confirm_connectivity_variant2.csv`:

| beta | compensated structure_success attempted | uncompensated structure_success attempted | compensation_effect_attempted | compensated analyzed | uncompensated analyzed |
|---:|---:|---:|---:|---:|---:|
| 0.003 | 0.72 | 0.52 | 0.20 | 90 | 96 |
| 0.005 | 0.72 | 0.35 | 0.37 | 90 | 89 |
| 0.007 | 0.72 | 0.18 | 0.54 | 90 | 85 |

Observed pattern:

```text
compensated success remains stable at 0.72 across beta values;
uncompensated success decreases as beta increases;
attempted-denominator compensation effect increases from +0.20 to +0.54.
```

This reproduces the relevant fine_beta_v010 pattern at the three selected beta points.

---

## 4. Wilson CI and paired McNemar audit

From `outputs/v010_confirm_connectivity_variant2_mcnemar_wilson.csv`:

| beta | n | comp_success | uncomp_success | effect | comp Wilson 95% CI | uncomp Wilson 95% CI | comp_only | uncomp_only | McNemar p |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.003 | 100 | 72 | 52 | 0.20 | [0.625, 0.799] | [0.423, 0.615] | 32 | 12 | 3.657767e-03 |
| 0.005 | 100 | 72 | 35 | 0.37 | [0.625, 0.799] | [0.264, 0.447] | 45 | 8 | 2.368351e-07 |
| 0.007 | 100 | 72 | 18 | 0.54 | [0.625, 0.799] | [0.117, 0.267] | 58 | 4 | 2.591759e-13 |

Interpretation:

```text
All three beta points show paired support for compensated > uncompensated.
The statistical signal strengthens as beta increases.
However, increasing effect size must be interpreted together with connectivity and failure-mode diagnostics.
```

---

## 5. Connectivity and failure-mode diagnostics

From `outputs/summary_v010_confirm_connectivity_variant2.csv`:

### Compensated mode

Compensated values are stable across beta points:

| beta | analyzed_runs | structure_success_attempted | mean_sector_size | mean_n_components | mean_largest_component_fraction | mean_degree_variance | failed_p_gnp_rate | failed_p_dp_rate | failed_dp_valid_rate | failed_sector_size_rate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.003 | 90 | 0.72 | 29.86 | 0.91 | 0.895 | 2.117 | 0.28 | 0.15 | 0.11 | 0.10 |
| 0.005 | 90 | 0.72 | 29.86 | 0.91 | 0.895 | 2.117 | 0.28 | 0.15 | 0.11 | 0.10 |
| 0.007 | 90 | 0.72 | 29.86 | 0.91 | 0.895 | 2.117 | 0.28 | 0.15 | 0.11 | 0.10 |

### Uncompensated mode

| beta | analyzed_runs | structure_success_attempted | mean_sector_size | mean_n_components | mean_largest_component_fraction | mean_degree_variance | failed_p_gnp_rate | failed_p_dp_rate | failed_dp_valid_rate | failed_sector_size_rate |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.003 | 96 | 0.52 | 18.17 | 1.01 | 0.949 | 1.697 | 0.47 | 0.33 | 0.06 | 0.04 |
| 0.005 | 89 | 0.35 | 12.97 | 0.95 | 0.872 | 1.420 | 0.64 | 0.42 | 0.18 | 0.11 |
| 0.007 | 85 | 0.18 | 9.72 | 0.92 | 0.823 | 1.099 | 0.81 | 0.49 | 0.26 | 0.15 |

Key observations:

```text
1. largest_component_fraction remains > 0.5 for all selected beta points.
2. beta=0.003 has the cleanest uncompensated connectivity profile.
3. beta=0.005 shows stronger effect but more diagnostic degradation.
4. beta=0.007 has maximum effect but also the strongest failure-rate increase and sector-size reduction.
5. The effect increase is primarily driven by decreasing uncompensated success, not increasing compensated success.
```

---

## 6. Beta classification after confirmatory diagnostics

### beta=0.003

Classification:

```text
leading clean positive candidate
```

Reason:

```text
positive effect (+0.20);
paired McNemar support;
largest_component_fraction high (0.949 in uncompensated);
mean_n_components approximately 1;
failed_sector_size_rate low (0.04);
uncompensated analyzed_runs high (96/100).
```

Conservative interpretation:

```text
beta=0.003 remains the cleanest candidate for a compensation-sensitive difference in the current Variant 2 toy model.
```

### beta=0.005

Classification:

```text
practical transition region
```

Reason:

```text
stronger effect (+0.37) and strong paired support;
connectivity still acceptable but visibly degraded;
sector size decreases from 18.17 to 12.97 in uncompensated mode;
failure rates increase.
```

Conservative interpretation:

```text
beta=0.005 remains a practical transition point, but interpretation should explicitly mention increasing graph-degradation confounds.
```

### beta=0.007

Classification:

```text
peak effect / high-confound reference point
```

Reason:

```text
largest effect (+0.54) and strongest paired support;
but uncompensated mean_sector_size falls to 9.72;
failed_p_gnp_rate rises to 0.81;
failed_p_dp_rate rises to 0.49;
failed_dp_valid_rate rises to 0.26;
failed_sector_size_rate rises to 0.15.
```

Conservative interpretation:

```text
beta=0.007 should not be treated as the best clean point merely because it has the maximum effect.
It is better treated as a peak-effect/high-confound diagnostic point.
```

---

## 7. Relation to expectations checkpoint

Expected before run:

```text
Not maximum effect, but interpretable effect.
Not pretty transition, but auditable mechanism.
Not claim first, but blocker removal first.
```

Observed:

```text
The result supports this framing.
beta=0.003 is strengthened as the clean candidate.
beta=0.007 is strengthened as peak/high-confound rather than clean-best.
beta=0.005 remains a practical transition point.
```

---

## 8. What this result resolves

This run addresses several Qwen blockers from the fine beta-grid review:

```text
connectivity metrics are now present;
largest_component_fraction is reported;
n_components is reported;
degree_variance is reported;
failure-mode flags are reported;
summary aggregates failure rates.
```

The result reduces the concern that beta=0.003 is merely a fragmentation artifact, because the uncompensated graph remains highly connected by largest_component_fraction.

---

## 9. What remains unresolved

The result does not fully solve density/edge-matched confounding.

Still needed before stronger claim:

```text
density/edge-matched compensated ablation;
possibly degree-preserving edge removal from compensated graphs;
sector_size distribution inspection;
lifetime distribution inspection;
multiple-testing wording discipline;
external review of this confirmatory result.
```

Therefore the result should not be framed as proof of physical theory or as final mechanism confirmation.

---

## 10. Conservative conclusion before Qwen review

Pre-review conclusion:

```text
confirm_connectivity_variant2 reproduces the fine_beta_v010 Variant 2 pattern at beta=0.003, 0.005, and 0.007 while adding connectivity and failure-mode diagnostics.
The result strengthens beta=0.003 as the leading clean candidate, keeps beta=0.005 as a practical transition point, and confirms beta=0.007 as a peak-effect/high-confound point rather than the clean best point.
The result remains a computational toy-model finding and still requires density/edge-matched ablation before stronger mechanistic or preprint-level claims.
```

---

## 11. Next required step

Submit this result to Qwen as an external methodological review.

Qwen should focus on:

```text
clean candidate status of beta=0.003;
transition status of beta=0.005;
high-confound status of beta=0.007;
whether largest_component_fraction sufficiently reduces fragmentation concern;
whether failure taxonomy resolves or shifts the previous blockers;
whether density-matched ablation remains mandatory;
what exact conservative wording is justified.
```

No stronger project claim should be made before Qwen review.
