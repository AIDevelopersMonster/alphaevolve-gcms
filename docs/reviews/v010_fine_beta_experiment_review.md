# Review: v0.10 fine beta experiment, result processing, and evaluation

**Status:** pre-result review / evaluation protocol  
**Date:** 2026-05-10  
**Experiment:** `fine_beta_v010`  
**Related protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Related skill plan:** `skills/proposals/gcms-result-auditor/LITE_TEST_PLAN.md`  

---

## 1. Review purpose

This document reviews the current fine beta experiment before interpreting its results.

Purpose:

```text
Prevent post-result criteria drift.
Separate experiment design, result processing, and scientific evaluation.
Define what counts as good, bad, ambiguous, or confounded before looking at the final output.
```

This is not a claim document. It is a review frame.

---

## 2. Experiment under review

Experiment mode:

```text
fine_beta_v010
```

Scientific target:

```text
Refine Variant 2 around the current candidate beta ~= 0.005.
```

Hypothesis:

```text
Variant 2 has a non-collapse compensation-sensitive transition near beta ~= 0.005.
```

Run grid:

```text
relation_variant = 2
model_modes = compensated, uncompensated
beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008
seeds = 100
baseline_count = 100
```

Expected run count:

```text
2 model modes * 1 relation variant * 6 beta values * 100 seeds = 1200 runs
```

Expected output files:

```text
outputs/raw_v010_fine_beta_variant2.csv
outputs/summary_v010_fine_beta_variant2.csv
outputs/comparison_v010_fine_beta_variant2.csv
outputs/residual_v010_fine_beta_variant2.csv
```

---

## 3. Design review

### 3.1 Strengths

The experiment is well-targeted because it:

```text
- focuses on the currently most interesting Variant 2 regime;
- tests a narrow beta range around 0.005;
- increases seeds from 50 to 100;
- keeps compensated and uncompensated modes paired by seed;
- avoids adding new mechanisms before auditing the current one;
- directly addresses the earlier graph-collapse concern at larger beta.
```

### 3.2 Design risk

Main risks:

```text
1. The effect may still be driven by sector-size or density differences.
2. A positive effect may be unstable across neighboring beta values.
3. The best-looking beta may be selected post hoc.
4. Analyzed denominators may differ between modes.
5. Degree distribution is not fully captured if only mean degree is computed after the fact.
6. The raw output may not include failure_reason or degree_variance.
```

### 3.3 Design discipline

The experiment must not be reinterpreted after seeing results by changing:

```text
- primary endpoint;
- success definition;
- preferred denominator;
- beta range;
- collapse criteria;
- control interpretation.
```

---

## 4. Primary endpoint

Primary endpoint:

```text
compensation_effect_attempted =
structure_success_rate_attempted(compensated) - structure_success_rate_attempted(uncompensated)
```

Reason:

```text
Attempted denominator preserves failed and unanalyzable runs as part of the experimental outcome.
```

Secondary endpoint:

```text
compensation_effect_analyzed
```

Caution:

```text
Analyzed-only effects must not be used alone, because low analyzed denominators can hide collapse.
```

---

## 5. Required result processing

### 5.1 File existence checks

Check that all expected files exist:

```text
raw
summary
comparison
residual
```

### 5.2 Schema checks

Required raw columns:

```text
model_mode
relation_variant
beta
seed
structure_success
strict_success
compensation_valid
analyzed
edge_count
density
sector_size
lifetime
dp_valid
p_gnp_empirical
p_dp_empirical
```

If any required column is missing, record it before interpreting.

### 5.3 Deterministic lite audit

Run:

```powershell
python tools\audit_gcms_lite.py --raw outputs\raw_v010_fine_beta_variant2.csv --out-prefix v010_fine_beta_variant2_lite
```

Expected generated local outputs:

```text
outputs/v010_fine_beta_variant2_lite_summary.csv
outputs/v010_fine_beta_variant2_lite_effect.csv
outputs/v010_fine_beta_variant2_lite_effect.png
outputs/v010_fine_beta_variant2_lite_report.md
```

These generated outputs are local analysis artifacts and should not be committed unless explicitly archived.

### 5.4 Full statistical audit

The full review should compute:

```text
Wilson CI for individual structure_success rates
paired exact McNemar test by seed
paired table: both_success, comp_only, uncomp_only, both_fail
effect size with uncertainty
```

### 5.5 Density and collapse audit

For each beta and mode, report:

```text
attempted
analyzed_count
structure_success_count
structure_success_rate
edge_count
density
mean_degree
sector_size
lifetime
dp_valid
p_gnp_empirical
p_dp_empirical
```

Collapse warning indicators:

```text
low analyzed_count
very low edge_count
very low sector_size
very short lifetime
near-zero density
large compensated/uncompensated denominator imbalance
```

---

## 6. Evaluation criteria

### 6.1 Good result

A good result would show:

```text
1. Positive compensation_effect_attempted at one or more beta values.
2. Paired evidence supports compensated > uncompensated.
3. The effect appears in a neighborhood, not only one isolated beta.
4. Uncompensated worlds remain analyzable.
5. Edge count and sector size do not collapse to near zero.
6. Lifetime remains substantial.
7. Density/degree audit does not explain the effect as pure graph sparsification.
8. The cleanest beta is not merely the beta with the largest effect.
```

Best possible outcome:

```text
A weakest or early beta in 0.003-0.008 shows a reliable positive effect while uncompensated mode remains non-collapsed.
```

### 6.2 Bad or null result

A bad/null result would show:

```text
1. No reliable positive compensation effect.
2. Confidence intervals remain wide and include zero substantially.
3. Paired discordance is balanced between comp_only and uncomp_only.
4. Neighboring beta values are inconsistent.
5. Variant 2 in this range behaves like distance-only control.
```

### 6.3 Confounded result

A result is confounded if:

```text
1. The largest effects occur only when uncompensated graph collapses.
2. analyzed_count becomes too low.
3. sector_size or edge_count approaches zero.
4. lifetime collapses.
5. The success difference is mostly explained by denominator loss.
6. Metrics required for audit are missing.
```

### 6.4 Ambiguous result

A result is ambiguous if:

```text
1. Effect is positive but weak.
2. Effect exists only at one beta.
3. Density or sector-size changes could explain the effect.
4. More seeds are needed.
5. Qwen or another reviewer finds a strong unresolved objection.
```

---

## 7. What not to conclude

Do not conclude:

```text
Variant 2 proves a physical theory.
GCMS-D0 proves global compensation causes local structure in reality.
Largest beta effect is automatically best.
A pretty effect-vs-beta chart is sufficient evidence.
```

Allowed conservative conclusion if supported:

```text
The fine beta-grid supports a preliminary toy-model compensation-sensitive transition in Variant 2, with a candidate non-collapse regime around the beta value where positive effect and analyzability coexist.
```

---

## 8. Processing order after completion

After the run completes:

```text
1. Verify expected files exist.
2. Check git status.
3. Run lite auditor.
4. Inspect effect table.
5. Run or compute full paired statistical audit.
6. Check density/degree/sector-size/lifetime.
7. Draft result note in docs/results.
8. Send Qwen review prompt.
9. Update PROJECT_INVENTORY.
10. Only then update technical note or article draft.
```

---

## 9. Codex task template for result processing

```text
Task: Process fine_beta_v010 outputs.

Do not modify experiment code.
Do not commit generated outputs.
Do not change success criteria.

Run:
python tools/audit_gcms_lite.py --raw outputs/raw_v010_fine_beta_variant2.csv --out-prefix v010_fine_beta_variant2_lite

Then report:
1. Whether expected raw/summary/comparison/residual files exist.
2. Whether required columns are present.
3. Generated lite-audit files.
4. Effect table by beta.
5. Any collapse warnings.
6. git status --short after processing.
```

---

## 10. Qwen review prompt after processing

```text
You are an independent methodological reviewer for GCMS-D0.

Review the fine beta-grid result for Variant 2.
Do not strengthen claims.

Context:
- Earlier beta-grid suggested beta ~= 0.005 as a non-collapse candidate.
- This experiment tests beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008 with 100 seeds.

Please review:
1. Is there a reliable positive compensation effect?
2. Is the best beta non-collapsed or graph-collapse dominated?
3. Are analyzed denominators acceptable?
4. Do density, edge_count, mean_degree, sector_size, and lifetime support the interpretation?
5. Are CI/McNemar results sufficient for a technical note?
6. What is the strongest skeptical objection?
7. What exact wording is conservative enough?

Return:
- Major concerns
- Minor concerns
- What is stronger now
- What remains unresolved
- Suggested conservative claim
- Recommended next experiment
```

---

## 11. Final reviewer stance

Current status before seeing result:

```text
Experiment design is appropriate and focused.
Processing must be deterministic.
Evaluation must prioritize non-collapse evidence over maximum effect size.
Claims must remain toy-model and preliminary.
```

Most important sentence:

```text
The clean result is not the largest effect; the clean result is the earliest reliable effect that survives collapse audit.
```
