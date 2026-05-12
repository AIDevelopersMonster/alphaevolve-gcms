# Editorial Patch Plan: connectivity_entanglement_confound_isolation_v0_1

**Status:** editorial patch plan / science frozen  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Target manuscript:** `docs/papers/connectivity_entanglement_confound_isolation_v0_1.md`  
**Checklist:** `docs/reviews/connectivity_entanglement_confound_isolation_v0_1_checklist.md`  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This document defines a presentation-only patch for `connectivity_entanglement_confound_isolation_v0_1.md`.

The science for v0.1 is frozen.

Allowed work:

```text
experiment-chain table;
optional figure placeholders;
section tightening;
public-facing abstract;
final wording scan;
formatting polish.
```

Forbidden work:

```text
new experiments;
new simulations;
new statistics;
new controls;
new thresholds;
new causal claims;
new physical claims;
new universal claims;
claim expansion.
```

Short invariant:

```text
Change presentation only. Do not change the scientific content.
```

---

## 2. Current v0.1 status

The v0.1 checklist concluded:

```text
v0.1 checklist complete;
v0.1 passes claim discipline and caveat requirements;
no new experiments required;
no new statistics required;
remaining work is editorial presentation only.
```

The scientific status is:

```text
frozen for v0.1
```

Therefore, the next patch should improve readability and navigation without modifying the evidence base.

---

## 3. Patch target

Patch only:

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1.md
```

Do not patch:

```text
tools/*
outputs/*
results notes
review files
experiment design files
```

Do not commit generated output files.

---

## 4. Required editorial additions

### 4.1 Experiment-chain table

Add a table near the end of the Introduction or at the start of Section 3.

Purpose:

```text
Make the confound-isolation narrative readable at a glance.
```

Suggested table title:

```text
Table 1. Confound-isolation sequence
```

Suggested columns:

```text
stage
experiment / artifact
purpose
main result
claim impact
```

Suggested rows:

```text
Initial signal | confirm_connectivity_variant2 | compare compensated vs uncompensated Variant 2 | 0.72 vs 0.52 success | positive signal but topology-confounded
Random density control | random_edge_removal_preliminary | exact edge-count matching | target 25 success 0.345, LCF 0.307 | invalid final control due to fragmentation
LCF-constrained control | lcf_constrained_ablation_variant2 | preserve largest component while reducing edges | failed_no_non_bridge_edges dominates | density-independent claim blocked
Reframe | connectivity_entanglement_reframe | replace density-independent claim | compensation-connectivity empirical coupling | claim weakened and made conservative
Native topology audit | connectivity_entanglement_audit_variant2 | measure native topology without pruning | compensated has higher non_bridge/cycle capacity | reframe supported descriptively
CI/pairing | connectivity_entanglement_audit_variant2_ci_pairing | uncertainty and paired checks | threshold contrast and paired deltas | reportability strengthened
```

Important:

```text
Do not add new numbers beyond already reported values.
Do not imply causal progression.
```

---

### 4.2 Optional figure placeholders

Add a short subsection after tables or before Reproducibility:

```text
Optional figures for future formatting
```

This should be placeholders only, not generated figures.

Suggested placeholders:

```text
Figure 1. Confound-isolation workflow diagram
Figure 2. Distribution of non_bridge_edge_count by mode
Figure 3. structure_success versus non_bridge_edge_count with post-hoc threshold marker
Figure 4. Paired seed deltas for non_bridge_edge_count and cycle_rank
```

Required caption caveats:

```text
Descriptive only; no causal interpretation.
Threshold marker is post-hoc exploratory and selected on the same dataset.
```

---

### 4.3 Public-facing abstract

Add after the technical abstract or before the Introduction:

```text
Plain-language summary
```

Purpose:

```text
Make the paper understandable without weakening claim discipline.
```

Suggested summary:

```text
This note reports a negative but useful result from a graph-based toy model. An initial compensated mode appeared to perform better than an uncompensated reference, but further checks showed that the effect was not independent of graph topology. Attempts to match edge counts either fragmented the graph or became structurally infeasible. A later audit showed that compensated graphs naturally had more non-bridge edges and higher cycle rank, and those topology features were associated with success. The result therefore shifts the interpretation from a clean compensation mechanism to an empirical coupling between compensation-aware dynamics and native connectivity capacity. The study makes no physical or causal claim.
```

Allowed wording:

```text
negative but useful result;
associated with;
empirical coupling;
toy model;
no physical or causal claim.
```

Forbidden wording:

```text
proves;
causes;
mechanism;
physics;
universal threshold.
```

---

### 4.4 Section tightening

Make small readability edits only.

Allowed:

```text
split long paragraphs;
remove repetition;
standardize heading names;
ensure table numbering is consistent;
make captions explicit;
move repeated caveats into footnotes where appropriate.
```

Forbidden:

```text
change claims;
change numbers;
change interpretation;
remove key caveats;
move threshold caveat out of visible text;
remove toy-model disclaimer.
```

---

### 4.5 Final wording scan

Scan for forbidden terms and replace if needed.

Forbidden or high-risk terms:

```text
proves
causes
enables stability
defines successful regime
universal
physical
spacetime
constants
gravity
photons
real-world mechanism
density-independent mechanism confirmed
```

Preferred replacements:

```text
is associated with
co-occurs with
empirically coupled
post-hoc exploratory
observed in this dataset
supports a conservative reframe
```

---

## 5. Required caveats to preserve

The editorial patch must preserve these caveats visibly in the main text:

```text
1. GCMS-D0 is a computational toy model.
2. No physical claim is made.
3. No causal claim is made.
4. The audit is observational.
5. The threshold non_bridge_edge_count >= 19 is post-hoc exploratory.
6. The threshold was selected on the full dataset.
7. The threshold is prone to selection bias.
8. Validation on held-out seeds or independent beta/N/threshold settings is required before generalization.
9. sector_size is outcome-adjacent.
10. density is a misleading standalone predictor in this regime.
11. topology descriptors are collinear.
12. no intervention was performed.
```

Do not hide these only in appendices.

---

## 6. Verification checklist after patch

After applying the editorial patch, verify:

```text
Only docs/papers/connectivity_entanglement_confound_isolation_v0_1.md changed.
No outputs committed.
No tools changed.
No new numbers introduced.
No new claims introduced.
All Qwen caveats remain present.
Table numbering is consistent.
Plain-language summary remains conservative.
Figure placeholders are clearly marked optional/descriptive.
```

Suggested local commands:

```powershell
git status --short
git diff --stat
git diff -- docs\papers\connectivity_entanglement_confound_isolation_v0_1.md
```

Commit command after review:

```powershell
git add docs\papers\connectivity_entanglement_confound_isolation_v0_1.md
git commit -m "Apply editorial patch to connectivity entanglement v0.1"
```

Do not use:

```powershell
git add .
```

---

## 7. Expected result after patch

After this patch, the manuscript should be ready for:

```text
final wording-only review;
optional Qwen final wording check;
public-facing abstract extraction;
possible conversion to PDF / preprint-style format later.
```

It should not be treated as:

```text
submission-ready final paper;
causal proof;
physical-theory result;
completed generalization study.
```

---

## 8. Current status

```text
editorial patch plan created;
science frozen;
no v0.1 editorial patch applied yet;
next step: patch docs/papers/connectivity_entanglement_confound_isolation_v0_1.md only.
```

Short invariant:

```text
Improve readability. Preserve humility.
```
