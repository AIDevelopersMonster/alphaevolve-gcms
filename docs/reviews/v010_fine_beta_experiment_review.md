# Review: v0.10 fine beta experiment, result processing, and evaluation

**Status:** pre-result review / exploratory-pre-confirmatory evaluation protocol  
**Date:** 2026-05-10  
**Experiment:** `fine_beta_v010`  
**Related protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Related skill plan:** `skills/proposals/gcms-result-auditor/LITE_TEST_PLAN.md`  
**External pre-result reviewer:** Qwen  

---

## 1. Review purpose

This document reviews the current fine beta experiment before interpreting its results.

Purpose:

```text
Prevent post-result criteria drift.
Separate experiment design, result processing, and scientific evaluation.
Define what counts as good, bad, ambiguous, or confounded before looking at the final output.
Record external pre-result review before interpretation.
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
7. Current raw schema likely does not include connectivity fragmentation metrics.
```

### 3.3 Design discipline

The experiment must not be reinterpreted after seeing results by changing:

```text
- primary endpoint;
- success definition;
- preferred denominator;
- beta range;
- collapse criteria;
- control interpretation;
- claim strength.
```

---

## 4. External pre-result review by Qwen

Qwen reviewed the design, processing plan, and evaluation criteria before final results were interpreted.

### 4.1 Major concerns from Qwen

Qwen identified four major concerns:

```text
1. No quantitative thresholds were pre-specified for a clean result.
2. Current graph metrics may miss subtle fragmentation or connectivity collapse.
3. Testing only Variant 2 limits mechanistic inference.
4. Multiple testing across six beta values was not explicitly handled.
```

### 4.2 Minor concerns from Qwen

Qwen also noted:

```text
1. Residual mode is excluded from the fine grid.
2. The audit script version should be recorded.
3. No power analysis justifies seeds=100.
4. Failure-mode decomposition should be reported.
```

### 4.3 What Qwen considered well-designed

Qwen agreed that the design is strong in several ways:

```text
- focused beta grid centered on the prior candidate;
- paired-seed design;
- attempted-denominator primary endpoint;
- comprehensive raw column plan;
- conservative framing that the largest effect is not automatically best;
- deterministic lite audit step.
```

### 4.4 Qwen decision-rule recommendation

Qwen recommended a stricter clean-positive rule:

```text
A clean positive result at beta = X requires all of:
1. compensation_effect_attempted > 0 with CI lower bound > 0;
2. exact McNemar p-value < 0.05;
3. uncompensated analyzed_runs >= 80/100;
4. uncompensated mean_density >= 0.10 and largest_component_fraction >= 0.50;
5. compensated compensation_valid rate >= 95/100.

If multiple beta values satisfy these criteria, select the smallest beta.
If no beta satisfies all criteria, report the grid transparently and classify the result as inconclusive.
```

### 4.5 Immediate implication for the current run

Because the current raw schema likely does not include `largest_component_fraction`, `n_components`, `degree_variance`, or failure-mode decomposition, the current `fine_beta_v010` run should be classified as:

```text
exploratory refinement / pre-confirmatory run
```

It can strengthen or weaken the beta ~= 0.005 candidate, but it should not be treated as a final confirmatory experiment.

---

## 5. Primary endpoint

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

## 6. Required result processing

### 6.1 File existence checks

Check that all expected files exist:

```text
raw
summary
comparison
residual
```

### 6.2 Schema checks

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

### 6.3 Deterministic lite audit

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

Record the git commit hash of `tools/audit_gcms_lite.py` used for the audit.

### 6.4 Full statistical audit

The full review should compute:

```text
Wilson CI for individual structure_success rates
paired exact McNemar test by seed
paired table: both_success, comp_only, uncomp_only, both_fail
effect size with uncertainty
```

For this run, treat beta=0.005 as the prior primary candidate from the previous beta-grid.

Other beta values are neighborhood/stability checks unless a later confirmatory design explicitly applies a multiple-testing correction across the whole grid.

### 6.5 Density and collapse audit

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

### 6.6 Missing connectivity audit

The following metrics are recommended by Qwen but may not be available in the current raw output:

```text
largest_component_fraction
n_components
algebraic_connectivity
degree_variance
degree_gini
failure_reason / failure-mode counts
```

If absent, report them as missing limitations, not as passed checks.

---

## 7. Evaluation criteria

### 7.1 Clean exploratory positive

For the current run, a clean exploratory positive would show:

```text
1. Positive compensation_effect_attempted at beta=0.005 or at a smaller neighboring beta.
2. Paired evidence supports compensated > uncompensated.
3. McNemar p-value is < 0.05 for the relevant beta.
4. uncompensated analyzed_runs >= 80/100.
5. uncompensated mean_density >= 0.10.
6. edge_count and sector_size do not collapse to near zero.
7. lifetime remains substantial.
8. effect is not isolated to a single unstable beta.
9. density/mean-degree audit does not explain the result as pure sparsification.
```

This is still exploratory because connectivity metrics are missing unless added in the current raw schema.

### 7.2 Strong but not clean

A result is strong but not clean if:

```text
effect is large,
but density, sector_size, lifetime, or analyzed_runs raise substantial confound concerns.
```

### 7.3 Bad or null result

A bad/null result would show:

```text
1. No reliable positive compensation effect.
2. Confidence intervals remain wide and include zero substantially.
3. Paired discordance is balanced between comp_only and uncomp_only.
4. Neighboring beta values are inconsistent.
5. Variant 2 in this range behaves like distance-only control.
```

### 7.4 Confounded result

A result is confounded if:

```text
1. The largest effects occur only when uncompensated graph collapses.
2. analyzed_count becomes too low.
3. sector_size or edge_count approaches zero.
4. lifetime collapses.
5. The success difference is mostly explained by denominator loss.
6. Metrics required for audit are missing.
7. Connectivity fragmentation cannot be ruled out and is plausible from available metrics.
```

### 7.5 Ambiguous result

A result is ambiguous if:

```text
1. Effect is positive but weak.
2. Effect exists only at one beta.
3. Density or sector-size changes could explain the effect.
4. More seeds are needed.
5. Qwen or another reviewer finds a strong unresolved objection.
```

---

## 8. What not to conclude

Do not conclude:

```text
Variant 2 proves a physical theory.
GCMS-D0 proves global compensation causes local structure in reality.
Largest beta effect is automatically best.
A pretty effect-vs-beta chart is sufficient evidence.
The current run is final confirmation if connectivity/failure-mode metrics are missing.
```

Allowed conservative conclusion if supported:

```text
The fine beta-grid supports a preliminary toy-model compensation-sensitive transition in Variant 2, with an exploratory candidate non-collapse regime around the beta value where positive effect and analyzability coexist.
```

---

## 9. Processing order after completion

After the run completes:

```text
1. Verify expected files exist.
2. Check git status.
3. Record current git commit hash.
4. Run lite auditor.
5. Inspect effect table.
6. Run or compute full paired statistical audit.
7. Check density/degree/sector-size/lifetime.
8. Explicitly list missing connectivity/failure-mode metrics.
9. Draft result note in docs/results.
10. Send Qwen result-review prompt.
11. Update PROJECT_INVENTORY.
12. Only then update technical note or article draft.
```

---

## 10. Codex task template for result processing

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
3. Current git commit hash and audit tool version/commit.
4. Generated lite-audit files.
5. Effect table by beta.
6. Any collapse warnings.
7. Missing connectivity/failure-mode metrics.
8. git status --short after processing.
```

---

## 11. Qwen review prompt after processing

```text
You are an independent methodological reviewer for GCMS-D0.

Review the fine beta-grid result for Variant 2.
Do not strengthen claims.

Context:
- Earlier beta-grid suggested beta ~= 0.005 as a non-collapse candidate.
- This experiment tests beta = 0.003, 0.004, 0.005, 0.006, 0.007, 0.008 with 100 seeds.
- Pre-result review classified this run as exploratory/pre-confirmatory unless connectivity and failure-mode metrics are available.

Please review:
1. Is there a reliable positive compensation effect?
2. Is the best beta non-collapsed or graph-collapse dominated?
3. Are analyzed denominators acceptable?
4. Do density, edge_count, mean_degree, sector_size, and lifetime support the interpretation?
5. What cannot be concluded without largest_component_fraction, n_components, degree_variance, and failure-mode counts?
6. Are CI/McNemar results sufficient for an exploratory technical note?
7. What is the strongest skeptical objection?
8. What exact wording is conservative enough?

Return:
- Major concerns
- Minor concerns
- What is stronger now
- What remains unresolved
- Suggested conservative claim
- Recommended confirmatory experiment
```

---

## 12. Next confirmatory experiment requirements

If this run yields a promising exploratory result, the next confirmatory run should add:

```text
largest_component_fraction
n_components
degree_variance or degree_gini
failure_reason
per-criterion failure counts
pre-specified primary beta or formal multiple-testing correction
recorded audit-tool commit/version
```

Possible confirmatory plan if beta=X is promising:

```text
relation_variant = 2
beta = X
model_modes = compensated, uncompensated
seeds = 200
baseline_count = 100
all connectivity and failure-mode metrics enabled
```

---

## 13. Final reviewer stance

Current status before seeing result:

```text
Experiment design is appropriate and focused as an exploratory/pre-confirmatory refinement.
Processing must be deterministic.
Evaluation must prioritize non-collapse evidence over maximum effect size.
Claims must remain toy-model and preliminary.
A final confirmatory claim requires connectivity/failure-mode metrics and stricter decision thresholds.
```

Most important sentence:

```text
The clean result is not merely the largest effect, and not even merely the earliest positive effect; it must pass denominator, density, connectivity, and multiple-testing discipline.
```
