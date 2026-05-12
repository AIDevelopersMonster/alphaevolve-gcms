# Review Pass: connectivity_entanglement_confound_isolation_draft

**Status:** internal review pass / no new experiments  
**Date:** 2026-05-12  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Reviewed draft:** `docs/papers/connectivity_entanglement_confound_isolation_draft.md`  
**Outline:** `docs/papers/connectivity_entanglement_confound_isolation_outline.md`  
**Frame:** confound-isolation / topology-threshold diagnostic in a computational toy model  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Review scope

This review pass evaluates the first connected technical draft.

It is not an authorization for new experiments.
It is not a request for additional simulation runs.
It is not a return to edge-removal rescue.

The purpose is:

```text
Improve the draft's structure, claim discipline, clarity, and publication-readiness while preserving the conservative frame.
```

Core invariant:

```text
Review the text. Do not run experiments.
```

---

## 2. Overall assessment

The draft is methodologically aligned with the approved project direction.

It correctly presents the project as:

```text
confound-isolation / topology-threshold diagnostic in a computational toy model
```

It does not claim:

```text
mechanism proof;
physical relevance;
universal threshold;
density-independent compensation mechanism;
causal proof.
```

The draft's central narrative is valid:

```text
initial positive signal -> topology confound -> failed pruning controls -> reframe -> native topology audit -> CI/pairing support -> conservative conclusion
```

This is the correct narrative for the first technical note.

---

## 3. Claim discipline check

### Safe claims present in the draft

The draft safely states:

```text
1. The original density-independent mechanism claim is not supported.
2. Random edge removal introduced fragmentation.
3. LCF-constrained edge removal exposed structural infeasibility.
4. Native topology audit supports compensation-connectivity entanglement as an empirical coupling.
5. non_bridge_edge_count and cycle_rank are associated with structure_success.
6. non_bridge_edge_count >= 19 is post-hoc exploratory.
7. No causal, universal, or physical claim is made.
```

These claims are consistent with Qwen review and result notes.

### Claims that remain blocked

The draft correctly avoids the blocked claims:

```text
1. compensation causes structure;
2. density-independent mechanism confirmed;
3. non_bridge_edge_count >= 19 is universal;
4. threshold is mechanistic;
5. result has physical implications;
6. real-world constants, spacetime, gravity, photons;
7. edge-removal rescue should continue.
```

No correction needed on this front.

---

## 4. Strong parts of the draft

### 4.1 Narrative discipline

The draft does not try to rescue the original claim. It presents the negative/blocked density-independent claim as a scientific result.

This is important because the paper's value comes from:

```text
honest confound isolation;
explicit weakening of the claim;
identification of a topology-threshold pattern;
reproducible decision trail.
```

### 4.2 Correct use of primary descriptor

The draft correctly identifies:

```text
non_bridge_edge_count
```

as the primary reporting descriptor, with:

```text
cycle_rank
largest_component_cycle_rank
sector_size
```

as supporting descriptors.

This matches Qwen's recommendation.

### 4.3 Good integration of CI/pairing

The draft includes the required statistical strengthening:

```text
Wilson CI for model-mode rates;
Wilson CI for threshold groups;
bootstrap CI for threshold contrast;
paired seed deltas.
```

This satisfies the minimal pre-draft requirements from Qwen.

### 4.4 Correct caveat on threshold

The draft clearly marks:

```text
non_bridge_edge_count >= 19
```

as:

```text
post-hoc exploratory
```

and not universal or mechanistic.

This must remain unchanged.

---

## 5. Issues to improve before next draft

### Issue 1: Add a compact contributions paragraph

The Introduction should explicitly list the paper's contributions.

Suggested paragraph:

```text
This note makes four contributions. First, it documents why the initial compensated advantage cannot be interpreted as density-independent. Second, it shows that random edge removal and LCF-constrained pruning fail for different methodological reasons: fragmentation and structural infeasibility. Third, it reframes the result as compensation-connectivity entanglement and audits native topology without graph modification. Fourth, it reports paired-seed and uncertainty analyses showing that non_bridge_edge_count and cycle_rank provide a topology-threshold description of the observed success pattern.
```

### Issue 2: Clarify the difference between edge_count and density

The draft reports a negative correlation between density and structure_success, while edge_count is positively correlated. This can confuse readers.

Add an explanatory note:

```text
The negative density correlation should not be read as evidence that sparse graphs are generally better. Density is normalized by sector size / node count and is therefore entangled with the size of the selected graph. In this audit, edge_count and non_bridge_edge_count are more interpretable descriptors of absolute topological capacity than scalar density alone.
```

### Issue 3: Add a methods subsection for topology definitions

The draft names topology descriptors but does not define all of them in prose.

Add a short subsection, possibly in Section 2 or 6:

```text
bridge_count is the number of graph bridges; non_bridge_edge_count is edge_count minus bridge_count; cycle_rank is E - V + C, where E is edge count, V is node count, and C is the number of connected components; largest_component_cycle_rank is the same quantity restricted to the largest connected component.
```

### Issue 4: Distinguish outcome-adjacent sector_size from topology descriptors

`sector_size` correlates strongly with success but is not as clean as `non_bridge_edge_count` because it is closer to the success criteria.

Add caveat:

```text
sector_size is reported as an outcome-adjacent descriptor rather than a primary explanatory topology variable.
```

### Issue 5: Add a reproducibility table

Add a compact table listing scripts and outputs:

```text
tools/audit_connectivity_entanglement_variant2.py
outputs/raw_v010_connectivity_entanglement_audit_variant2.csv
outputs/summary_v010_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_v010_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_v010_connectivity_entanglement_audit_variant2.csv
outputs/correlations_v010_connectivity_entanglement_audit_variant2.csv
tools/postprocess_connectivity_audit_ci_pairing.py
outputs/paired_seed_summary_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/wilson_cis_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
outputs/bootstrap_ci_non_bridge_ge19_v010_connectivity_entanglement_audit_variant2_ci_pairing.csv
```

This strengthens the reproducibility value of the note.

### Issue 6: Add a short external-review paragraph

Because the project used independent Qwen review as methodological pressure, the draft can mention this internally or in acknowledgements/context.

Suggested cautious wording:

```text
The reframe and audit interpretation were subjected to independent methodological review within the project workflow. The review recommended treating non_bridge_edge_count as the primary descriptor, reporting the threshold as post-hoc exploratory, and adding paired-seed and uncertainty analyses before drafting.
```

Avoid implying peer review or external journal review.

### Issue 7: Add resource-constraint context only if desired

This is optional and should not be central.

Possible acknowledgement-style wording:

```text
This work was conducted under severe resource constraints using lightweight, reproducible local experiments. The design therefore emphasizes small controlled runs, explicit negative controls, conservative claims, and complete decision logging.
```

Do not add political details to the technical draft unless intentionally writing a project context note.

---

## 6. Suggested next text patch

The next patch should update the draft only.

File:

```text
docs/papers/connectivity_entanglement_confound_isolation_draft.md
```

Allowed edits:

```text
1. Add contributions paragraph.
2. Add topology definitions.
3. Add edge_count vs density clarification.
4. Add sector_size caveat.
5. Add reproducibility table.
6. Add methodological review paragraph.
7. Minor wording polish.
```

Forbidden edits:

```text
1. Do not add new results.
2. Do not add new experiments.
3. Do not change reported numbers.
4. Do not strengthen causal language.
5. Do not turn threshold >=19 into a validated cutoff.
6. Do not add physical claims.
```

---

## 7. Draft readiness after patch

After the suggested text patch, the draft should be ready for:

```text
Qwen manuscript-review pass
```

not for submission yet.

Expected next review questions:

```text
1. Is the manuscript framing conservative enough?
2. Are the limitations sufficient?
3. Is the result scientifically valuable despite blocking the original claim?
4. Are the topology descriptors explained clearly?
5. Does the draft need logistic regression before public release, or is it acceptable as a technical note?
```

---

## 8. Current status

```text
First technical draft reviewed.
No new experiments needed.
Next step: text-only patch to improve clarity and reproducibility.
```

Short invariant:

```text
Improve the manuscript. Do not expand the experiment.
```
