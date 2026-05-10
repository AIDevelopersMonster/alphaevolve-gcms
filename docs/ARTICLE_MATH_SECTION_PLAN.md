# Article Math Section Plan

**Status:** working article-structure note  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Related reference:** `docs/MATHEMATICAL_APPARATUS.md`  
**Purpose:** define how the mathematical apparatus should appear in the future technical note or article.

---

## 1. Core decision

The article should present the mathematical apparatus in a general, layered form.

The purpose is not to overload the paper with formalism.

The purpose is to make clear:

```text
1. what mathematical objects the toy model uses;
2. what equations define the model;
3. what statistics define the endpoints;
4. what graph diagnostics protect against overclaiming;
5. what remains exploratory rather than proven.
```

Formal lemmas, theorems, and proofs should be introduced only if they are needed for a specific claim.

---

## 2. Recommended article structure

### Main text

The main text should include a compact mathematical model section:

```text
1. vector world and global residual K;
2. compensation by mean subtraction;
3. reason distance-only relations cannot test compensation causality;
4. Variant 2 relation function;
5. graph thresholding and sector selection;
6. structure_success endpoint;
7. compensation_effect endpoint;
8. key graph diagnostics.
```

### Appendix

The appendix can contain the fuller reference layer:

```text
1. all relation variants;
2. empirical p-value definition;
3. Wilson CI;
4. exact McNemar test;
5. connectivity metrics;
6. failure-mode taxonomy;
7. multiple-testing discipline;
8. ablation logic.
```

---

## 3. What should be equations in the article

The following equations are central and should appear in the main text or methods section.

### Global residual

```math
K = \sum_{i=1}^{N} v_i
```

### Compensation by mean subtraction

```math
\bar{v} = \frac{1}{N}\sum_{i=1}^{N} v_i
```

```math
v_i' = v_i - \bar{v}
```

### Distance-only relation

```math
R_{ij}^{(0)} = \exp\left(-\alpha \|v_i - v_j\|^2\right)
```

### Distance invariance under mean subtraction

```math
(v_i - \bar{v}) - (v_j - \bar{v}) = v_i - v_j
```

This should be included because it explains why v0.9.1 was methodologically insufficient.

### Variant 2 relation

```math
R_{ij}^{(2)} = \exp\left(-\alpha \|v_i - v_j\|^2 - \beta |(v_i + v_j) \cdot K|\right)
```

### Graph thresholding

```math
A_{ij} = \mathbf{1}\{R_{ij} > \theta\}
```

### Structure success

```math
structure\_success =
(p_{GNP}<0.05) \land (p_{DP}<0.05) \land DP\_valid \land (lifetime>20) \land (5 \le n \le 60)
```

### Compensation effect

```math
\Delta_{attempted}(\beta) =
P(structure\_success \mid compensated, \beta) -
P(structure\_success \mid uncompensated, \beta)
```

---

## 4. What should remain descriptive, not theorem-like

Do not force theorem/proof language for:

```text
empirical beta transition;
clean candidate selection;
compensation-sensitive interpretation;
connectivity diagnostics;
failure-mode taxonomy;
Qwen review conclusions.
```

These are empirical toy-model findings and should be framed as computational evidence, not mathematical proof.

---

## 5. Where lemmas may be useful

A lemma is useful only when it prevents conceptual confusion.

Possible lemma:

```text
Lemma 1: Mean subtraction preserves pairwise distances.
```

Formal statement:

```math
\forall i,j: \|(v_i-\bar{v})-(v_j-\bar{v})\| = \|v_i-v_j\|
```

Purpose:

```text
Explain why a distance-only relation cannot distinguish compensated from uncompensated worlds.
```

This is the strongest candidate for a real lemma because it is simple, exact, and central to the v0.10 motivation.

---

## 6. Where theorems are probably not needed yet

The current project likely does not need theorem language for the main empirical claims.

Avoid premature theorem claims such as:

```text
Theorem: global compensation causes local structure.
Theorem: Variant 2 produces a phase transition.
Theorem: beta=0.003 is optimal.
```

These would overstate the current evidence.

Use instead:

```text
Observation
Diagnostic result
Empirical transition
Exploratory support
Pre-confirmatory evidence
```

---

## 7. Suggested math section title options

Possible titles:

```text
Mathematical Setup
Toy-Model Formalism
Model Definition and Diagnostics
Vector-Graph Construction
Mathematical Apparatus of GCMS-D0
```

Recommended for article:

```text
Model Definition and Diagnostics
```

Reason:

```text
It avoids overclaiming and emphasizes that the mathematics defines a computational model plus audit metrics.
```

---

## 8. Proposed main-text paragraph

Draft:

```text
We model a world as N vectors v_i in R^d and define the global residual K = sum_i v_i. A compensated world is obtained by subtracting the mean vector from every state, making K approximately zero. Because this operation preserves all pairwise distances, a distance-only relation cannot test whether global compensation is causally involved in local structure. We therefore introduce compensation-aware relation variants, focusing here on Variant 2, where the edge relation depends both on pairwise distance and on the alignment of a pair sum with the global residual. Thresholding this relation produces a graph whose connected components define candidate local sectors. A sector is counted as structure_success only if its clustering is significant against both Erdos-Renyi and degree-preserving baselines and it satisfies lifetime and size constraints. The primary endpoint is the attempted-denominator compensation effect between compensated and uncompensated paired worlds.
```

---

## 9. Relation to limitations

The math section should explicitly connect to limitations:

```text
The equations define the toy model.
They do not prove physical realism.
The empirical result depends on diagnostics against graph sparsification, fragmentation, degree-distribution shifts, and failure-mode concentration.
```

This should appear either at the end of the math section or in limitations.

---

## 10. Current decision

For the article:

```text
Use equations for model definition and endpoints.
Use one lemma for distance-invariance if helpful.
Avoid theorem/proof structure unless a future analytic result is actually developed.
Place detailed statistical formulas and graph diagnostics in an appendix if the main text becomes too dense.
```
