# v0.1 Checklist: connectivity_entanglement_confound_isolation

**Status:** review checklist / no new experiments  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Reviewed manuscript:** `docs/papers/connectivity_entanglement_confound_isolation_v0_1.md`  
**v0.1 plan:** `docs/papers/connectivity_entanglement_confound_isolation_v0_1_plan.md`  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This checklist verifies that `connectivity_entanglement_confound_isolation_v0_1.md` remains within the approved conservative frame.

It is a review checklist only.

It does not authorize:

```text
new experiments;
new simulations;
new statistics;
new pruning ablations;
new figures with new data;
claim expansion;
physical interpretation;
causal interpretation;
universal threshold interpretation.
```

Short invariant:

```text
v0.1 is a presentation upgrade, not a scientific-claim upgrade.
```

---

## 2. Required status checks

| Check | Required status | v0.1 status |
|---|---|---|
| Technical note / toy model frame | Must be explicit | Present |
| Non-causal boundary | Must be explicit | Present |
| Non-physical boundary | Must be explicit | Present |
| Density-independent claim blocked | Must be explicit | Present |
| Threshold marked post-hoc | Must be explicit | Present |
| No new experiments | Must be explicit | Present |
| No new statistics | Must be explicit | Present |
| Reproducibility table | Required | Present |
| Claim discipline checklist | Required | Present |

---

## 3. Claim discipline checklist

Allowed wording in v0.1:

```text
supports the reframe;
is associated with;
empirical coupling;
empirical co-variation;
post-hoc exploratory threshold;
topology-threshold diagnostic;
toy model;
confound-isolation.
```

Forbidden wording in v0.1:

```text
proves;
causes;
enables stability;
defines successful regime;
universal;
physical;
spacetime;
constants;
gravity;
photons;
real-world mechanism;
density-independent mechanism confirmed.
```

Checklist:

| Item | Status |
|---|---|
| `entanglement` defined as empirical co-variation without causality | Pass |
| `mechanism proof` avoided | Pass |
| `causal` language avoided | Pass |
| `universal threshold` language avoided | Pass |
| physical/cosmological language avoided | Pass |
| density-independent proof language avoided | Pass |
| threshold `>=19` marked post-hoc exploratory | Pass |

---

## 4. Numerical consistency checklist

The v0.1 manuscript should not introduce any new numerical results beyond existing documented outputs.

Required values:

### Initial positive signal

```text
compensated structure_success = 0.72
uncompensated structure_success = 0.52 or 0.53 depending reference context
```

v0.1 uses:

```text
0.72 / 0.52 in initial signal context;
0.72 / 0.53 in native audit context.
```

Status:

```text
Pass, but keep context clear.
```

### Random edge-removal stress test

```text
target_edge_count = 25
structure_success = 0.345
largest_component_fraction = 0.307
```

Status:

```text
Pass
```

### LCF-constrained ablation

Required values:

```text
target 25:
    valid_lcf_matched_rate = 0.06
    structure_success_valid = 0.000
    failed_no_non_bridge_edges_rate = 0.93

target 30:
    valid_lcf_matched_rate = 0.21
    structure_success_valid = 0.238
    failed_no_non_bridge_edges_rate = 0.78

target 35:
    valid_lcf_matched_rate = 0.37
    structure_success_valid = 0.411
    failed_no_non_bridge_edges_rate = 0.62
```

Status:

```text
Pass
```

### Native topology audit

Required values:

| mode | structure_success | edge_count | non_bridge_edge_count | cycle_rank | LCC cycle rank | bridge_fraction | sector_size |
|---|---:|---:|---:|---:|---:|---:|---:|
| compensated | 0.72 | 44.96 | 33.52 | 16.09 | 15.93 | 0.269 | 29.86 |
| uncompensated | 0.53 | 25.35 | 17.82 | 8.16 | 8.15 | 0.335 | 18.17 |

Status:

```text
Pass
```

### Threshold and CI values

Required values:

```text
non_bridge_edge_count >= 19:
    103/105 success = 0.981
    Wilson score interval = [0.933, 0.995]

non_bridge_edge_count < 19:
    22/95 success = 0.232
    Wilson score interval = [0.158, 0.326]

difference = 0.749
bootstrap 95% CI = [0.656, 0.834]
```

Status:

```text
Pass
```

### Paired seed deltas

Required values:

```text
delta_edge_count:
    mean = 19.61
    median = 22.5
    positive = 82
    negative = 17
    zero = 1

delta_non_bridge_edge_count:
    mean = 15.70
    median = 16.0
    positive = 80
    negative = 18
    zero = 2

delta_cycle_rank:
    mean = 7.93
    median = 8.0
    positive = 80
    negative = 18
    zero = 2

delta_largest_component_cycle_rank:
    mean = 7.78
    median = 8.0
    positive = 79
    negative = 19
    zero = 2

delta_sector_size:
    mean = 11.69
    median = 11.0
    positive = 83
    negative = 16
    zero = 1
```

Status:

```text
Pass
```

---

## 5. Caveat checklist

Required caveats and their status:

| Caveat | Required | v0.1 status |
|---|---|---|
| `entanglement` is empirical co-variation only | Yes | Present |
| no directed causality | Yes | Present |
| no necessity / universality | Yes | Present |
| threshold selected on full dataset | Yes | Present |
| threshold prone to selection bias | Yes | Present |
| held-out or independent parameter validation required | Yes | Present |
| sector_size outcome-adjacent | Yes | Present |
| density can be misleading | Yes | Present |
| descriptors collinear | Yes | Present |
| no intervention performed | Yes | Present |
| single beta limitation | Yes | Present |
| fixed N/threshold/mutation limitation | Yes | Present |
| passive residual diagnostics not causal | Yes | Present |

Status:

```text
Pass
```

---

## 6. Table and structure checklist

Required v0.1 sections:

| Section | Status |
|---|---|
| Status and claim boundary | Present |
| Abstract | Present |
| Introduction | Present |
| Model and outcome overview | Present |
| Topology definitions | Present |
| Initial positive signal and topology confound | Present |
| Density and connectivity controls | Present |
| Reframe and methodological transparency | Present |
| Native-topology audit | Present |
| Correlations / threshold / paired analysis | Present |
| Reproducibility and artifact trail | Present |
| Limitations | Present |
| Conclusion | Present |
| Artifact chain appendix | Present |
| Claim discipline checklist appendix | Present |

Required tables:

| Table | Status |
|---|---|
| Native topology summary | Present |
| Descriptive correlations | Present |
| Post-hoc threshold rates | Present |
| Model-mode success rates | Present |
| Failure rates by mode | Present |
| Paired seed deltas | Present |
| Reproducibility artifacts | Present |

Status:

```text
Pass
```

---

## 7. Remaining editorial issues

No scientific blockers remain for v0.1.

Remaining editorial-only tasks:

```text
1. Decide whether to add an experiment-chain summary table.
2. Decide whether to add figure placeholders.
3. Decide whether to create a shorter public-facing abstract.
4. Decide whether to split long sections for readability.
5. Run final wording scan for forbidden terms before public release.
```

These tasks do not require new data or new analysis.

---

## 8. Recommended next step

Recommended next document:

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1_editorial_patch.md
```

Purpose:

```text
Plan the final editorial pass: experiment-chain table, optional figure placeholders, section tightening, and public-facing abstract.
```

Alternative next step:

```text
Send v0.1 to Qwen for final wording-only check.
```

Preferred path:

```text
editorial patch plan -> apply editorial patch -> optional Qwen final wording check
```

---

## 9. Final status

```text
v0.1 checklist complete.
v0.1 passes claim discipline and caveat requirements.
No new experiments required.
No new statistics required.
Remaining work is editorial presentation only.
```

Short invariant:

```text
The science is frozen for v0.1. Only presentation can change.
```
