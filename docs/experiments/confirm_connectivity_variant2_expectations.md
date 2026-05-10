# Expectations Checkpoint: confirm_connectivity_variant2

**Status:** pre-run expectations checkpoint  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `confirm_connectivity_variant2`  
**Related design checkpoint:** `docs/experiments/confirm_connectivity_variant2_design.md`  
**Related result note:** `docs/results/v010_fine_beta_variant2.md`  
**Related Qwen review:** `docs/reviews/v010_fine_beta_qwen_result_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  
**External reviewer role:** Qwen, independent methodological reviewer  

---

## 1. Why this document exists

This document records what Delta-D0 and Qwen expect to see before the `confirm_connectivity_variant2` result is interpreted.

It is not a result document.

It prevents post-result drift by separating:

```text
expectation -> observation -> audit -> interpretation -> claim
```

This checkpoint covers not only calculations, but the overall research-management question:

```text
What do we expect from the experiment as a project decision point?
What would make us continue, narrow, redesign, or stop?
```

---

## 2. Current state before the run

Previous experiment:

```text
fine_beta_v010
```

Main result:

```text
Strong exploratory support for a compensation-sensitive transition in Variant 2.
```

Current classification:

```text
beta=0.003: leading clean positive candidate
beta=0.004-0.005: practical transition region
beta=0.007: peak effect, high confound
beta=0.006-0.008: high-effect / high-sparsification region
```

Main blocker from Qwen:

```text
The previous result cannot yet distinguish mechanism from topological artifact because connectivity metrics, failure-mode taxonomy, and density-matched ablation were absent.
```

---

## 3. What Delta-D0 expects to see

Delta-D0 expects the confirmatory run to clarify whether the earlier effect is robust or mainly a graph-degradation artifact.

### 3.1 Expected if the mechanism is real within the toy model

```text
1. compensated structure_success remains stable or mostly stable across beta=0.003, 0.005, 0.007;
2. uncompensated structure_success remains lower than compensated;
3. beta=0.003 remains positive and statistically supported;
4. beta=0.003 has acceptable connectivity metrics;
5. beta=0.007 shows stronger effect but worse connectivity/failure profile;
6. failure reasons are distributed across criteria rather than dominated by a single trivial failure;
7. largest_component_fraction remains reasonably high at beta=0.003;
8. n_components and degree_variance do not reveal severe fragmentation at beta=0.003.
```

### 3.2 Expected if the effect is mostly sparsification/confound

```text
1. compensation_effect grows mainly where uncompensated edge_count and sector_size collapse;
2. largest_component_fraction drops sharply in uncompensated mode;
3. n_components rises or fragmentation becomes obvious;
4. failed_sector_size dominates failure taxonomy;
5. failed_dp_valid or p_dp failures dominate due to graph degeneracy;
6. beta=0.007 looks strong only because uncompensated graphs become structurally poor;
7. beta=0.003 weakens or becomes ambiguous under connectivity metrics.
```

### 3.3 Expected if the result is ambiguous

```text
1. effect remains positive, but connectivity metrics are mixed;
2. beta=0.003 is significant but has borderline component structure;
3. beta=0.005 becomes the practical compromise;
4. failure taxonomy shows multiple plausible causes;
5. density-matched ablation becomes mandatory before any stronger statement.
```

---

## 4. What Qwen is expected to check

Qwen is expected to review the post-run result as a skeptical methodological reviewer.

Primary Qwen questions:

```text
1. Does beta=0.003 remain a clean positive candidate?
2. Does beta=0.005 remain a practical transition point?
3. Is beta=0.007 confirmed as high-effect/high-confound or rehabilitated by connectivity metrics?
4. Does largest_component_fraction rule out severe fragmentation?
5. Which failure criterion dominates uncompensated failures?
6. Does degree_variance suggest a degree-distribution confound?
7. Is density-matched ablation still required before a preprint?
8. What exact conservative wording is now justified?
```

Qwen should not strengthen claims.

Qwen should classify each beta point as one of:

```text
clean candidate
practical transition candidate
high-effect/high-confound
fragmentation-dominated
ambiguous
blocked
```

---

## 5. Expected observations by beta

### beta=0.003

Delta-D0 expectation:

```text
This is the leading clean candidate.
It should preserve the best signal-to-confound ratio.
```

What we hope to see:

```text
positive compensation_effect_attempted;
McNemar support;
uncompensated analyzed_runs high;
largest_component_fraction > 0.5;
n_components not excessive;
failure taxonomy not dominated by sector_size collapse.
```

What would weaken it:

```text
fragmentation appears despite acceptable edge_count;
largest_component_fraction <= 0.5;
failed_sector_size or failed_dp_valid dominates;
effect becomes weak or unstable.
```

### beta=0.005

Delta-D0 expectation:

```text
This is the practical transition point and prior candidate.
```

What we hope to see:

```text
stronger effect than beta=0.003;
connectivity degradation present but not fatal;
component structure still interpretable;
failure taxonomy not trivially dominated by one mode.
```

What would weaken it:

```text
component fragmentation explains most failures;
connectivity metrics move close to beta=0.007 behavior;
sector_size or dp_valid failure dominates.
```

### beta=0.007

Delta-D0 expectation:

```text
This is peak effect but high-confound.
```

What we expect to test:

```text
whether the peak is a genuine optimum or a sparsification-dominated point.
```

What would rehabilitate beta=0.007:

```text
largest_component_fraction remains high;
n_components remains low;
degree_variance does not show severe distortion;
failure taxonomy is not dominated by trivial graph degradation;
compensation_effect remains strong for non-degenerate reasons.
```

What would confirm high-confound status:

```text
low largest_component_fraction;
high n_components;
large degree_variance shift;
failed_sector_size / failed_dp_valid dominates;
edge_count and sector_size degradation explain most of the effect.
```

---

## 6. What would count as success for this experiment

This experiment succeeds methodologically if it produces interpretable diagnostic evidence, even if the original hypothesis weakens.

### Strong success

```text
beta=0.003 remains positive, statistically supported, and connectivity-clean;
beta=0.005 remains interpretable as transition;
beta=0.007 is clearly classified as either rehabilitated or high-confound;
failure taxonomy identifies no single trivial failure mode dominating beta=0.003;
Qwen agrees that the result supports a stronger technical-note claim.
```

### Useful success

```text
connectivity metrics explain why beta=0.007 is confounded;
beta=0.003 or beta=0.005 remains viable;
next density-matched ablation can be designed precisely.
```

### Negative but valuable result

```text
connectivity metrics show that the apparent compensation effect is mostly fragmentation or sector collapse.
```

This would weaken the claim but improve the project scientifically.

---

## 7. What would block interpretation

Interpretation should be blocked if:

```text
1. output files are missing;
2. raw schema lacks required connectivity/failure columns;
3. summary lacks aggregate connectivity/failure metrics;
4. paired seed audit cannot be computed;
5. largest_component_fraction or n_components behaves inconsistently with edge_count/sector_size;
6. failure taxonomy is broken or not interpretable;
7. code changed during/after the run;
8. generated outputs were accidentally committed without decision.
```

---

## 8. Expected project-level decision after the result

After this experiment, the project should choose one of five directions:

```text
A. Proceed to density-matched ablation at beta=0.003.
B. Treat beta=0.005 as the best practical transition candidate.
C. Use beta=0.007 only as a high-confound demonstration, not a clean claim.
D. Redesign Variant 2 or add a new relation variant if connectivity metrics undermine the effect.
E. Prepare a conservative technical note if Qwen accepts the diagnostic evidence as sufficient for exploratory/preprint-level reporting.
```

---

## 9. Delta-D0 expected language after run

If result is supportive:

```text
The confirm_connectivity_variant2 run strengthens the exploratory evidence that Variant 2 produces a compensation-sensitive transition in the GCMS-D0 toy model, while identifying beta=0.003 as the cleanest candidate and beta=0.007 as the peak-effect/high-confound reference point.
```

If result is mixed:

```text
The confirm_connectivity_variant2 run preserves evidence for a compensation-sensitive difference, but connectivity and failure-mode diagnostics show that stronger effects are partly entangled with graph degradation. Further density-matched ablation is required.
```

If result is negative:

```text
The confirm_connectivity_variant2 run indicates that the apparent compensation effect is not cleanly separable from graph fragmentation or failure-mode concentration under the current Variant 2 relation. The result remains useful as a constraint on future relation design.
```

---

## 10. Core expectation

The goal is not to prove the largest effect.

The goal is to decide whether the effect survives a stricter diagnostic frame.

Short form:

```text
Not maximum effect, but interpretable effect.
Not pretty transition, but auditable mechanism.
Not claim first, but blocker removal first.
```
