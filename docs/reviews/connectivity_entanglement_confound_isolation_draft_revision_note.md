# Revision Note: connectivity_entanglement_confound_isolation_draft

**Status:** revision note / Qwen critique addressed  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Reviewed draft:** `docs/papers/connectivity_entanglement_confound_isolation_draft.md`  
**Qwen review:** `docs/reviews/connectivity_entanglement_confound_isolation_draft_qwen_review.md`  
**Revision commit:** `019e35e Apply Qwen text-only caveat revisions`  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This note records that Qwen's manuscript-review critique of the first technical draft was addressed by text-only revisions.

No new experiments were run.
No new simulations were run.
No new statistical analysis was added.
No claims were strengthened.
No physical interpretation was added.

The revision only improves:

```text
claim discipline;
caveats;
definitions;
limitations;
reader clarity;
methodological transparency.
```

---

## 2. Qwen classification

Qwen classified the draft as:

```text
A. Acceptable for technical-note revision after text-only edits.
```

Qwen explicitly stated:

```text
Do not add experiments.
Do not strengthen claims.
Apply lexical and caveat edits precisely.
```

This revision follows that instruction.

---

## 3. Required Qwen edits and resolution status

| Qwen requirement | Status | Resolution |
|---|---|---|
| Define `entanglement` as empirical co-variation without causality | Closed | Draft now defines compensation-connectivity entanglement as observed co-variation / empirical coupling without directed causality, necessity, or universality. |
| Strengthen `sector_size` caveat | Closed | Draft now states that `sector_size` is outcome-adjacent and partially coupled to the success definition, not a clean independent topology predictor. |
| Clarify negative density correlation | Closed | Draft now explains that density is a normalized ratio and may be misleading relative to absolute edge/cycle capacity. |
| Strengthen post-hoc threshold warning | Closed | Draft now states that `non_bridge_edge_count >= 19` was selected on the full dataset, is prone to selection bias, and requires held-out or independent-parameter validation. |
| Add collinearity acknowledgment | Closed | Draft now states that edge count, non-bridge edge count, cycle rank, LCC cycle rank, and sector size co-vary and that multivariate attribution is deferred. |
| Standardize CI language | Closed | Draft now uses `Wilson score interval` and `bootstrap 95% CI with row-level resampling` language. |
| Remove or soften residual mechanism / causes / independent / universal wording | Closed | Draft now uses empirical coupling / associated / co-vary wording and avoids causal or universal threshold claims. |
| Expand limitations | Closed | Draft now includes single beta, fixed N/threshold/mutation settings, no intervention, collinearity, and post-hoc threshold bias. |

---

## 4. Important wording changes

### 4.1 Entanglement definition

The draft now defines the term as:

```text
an observed co-variation where compensation-aware dynamics consistently co-occur with higher native topological capacity, without implying directed causality, necessity, or universality
```

This prevents `entanglement` from being read as causal.

### 4.2 Sector-size caveat

The draft now treats `sector_size` as:

```text
outcome-adjacent rather than a clean explanatory topology variable
```

and notes that its correlation with `structure_success` partially reflects success-definition coupling.

### 4.3 Density clarification

The draft now clarifies that:

```text
density is a normalized ratio and may be affected by component-size or sector-size normalization;
structural success is better described by absolute edge/cycle capacity, especially non_bridge_edge_count, than by relative sparsity;
density is a misleading standalone predictor in this regime.
```

### 4.4 Threshold warning

The threshold `non_bridge_edge_count >= 19` is now described as:

```text
selected on the full dataset;
prone to selection bias;
post-hoc exploratory;
not mechanistic;
not universal;
not validated;
requiring held-out seeds or independent beta/N/threshold settings before generalization.
```

### 4.5 CI wording

The draft now distinguishes:

```text
95% Wilson score intervals for rate estimates;
bootstrap 95% CI with row-level resampling for threshold-difference estimate.
```

---

## 5. What was not changed

The revision did not change:

```text
reported numerical results;
model settings;
experiment descriptions;
success criteria;
primary descriptor selection;
post-hoc threshold value;
paired seed results;
Wilson CI values;
bootstrap CI values;
artifact trail;
research framing.
```

The revision did not add:

```text
new simulations;
new controls;
logistic regression;
new bootstrap runs;
new figures;
physical claims;
causal claims;
universal threshold claims.
```

---

## 6. Current draft status

After this revision, the draft status is:

```text
Qwen manuscript-review critique addressed by text-only caveat revision.
Technical/confound-isolation note remains within conservative toy-model scope.
No new experiments are required before next editorial pass.
```

The draft is now suitable for:

```text
second internal editorial pass;
formatting / figure-table planning;
optional Qwen check on final wording;
preparing a clean v0.1 manuscript version.
```

It is not yet marked as:

```text
final manuscript;
submission-ready paper;
physical theory claim;
causal mechanism proof.
```

---

## 7. Next recommended step

Recommended next document:

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1_plan.md
```

Purpose:

```text
Convert the revised draft into a clean v0.1 manuscript plan with tables, figures, formatting tasks, and final editorial checklist.
```

Short invariant:

```text
From here forward, improve presentation. Do not expand the claim.
```
