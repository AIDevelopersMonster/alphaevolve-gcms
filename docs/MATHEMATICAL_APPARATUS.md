# GCMS-D0 Mathematical Apparatus Reference Map

**Status:** working reference map  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Purpose:** list the mathematical topics and concrete equations currently used in the GCMS-D0 toy-model experiments, organized as a study pyramid for reference rather than manual calculation.

---

## 1. How to use this document

This document is not a textbook.

It is a map of the mathematics currently used in GCMS-D0, so that Aleksey can review the relevant ideas in a separate chat or external sources without losing the project context.

The goal is not to calculate everything manually.

The goal is to know:

```text
what mathematical object is being used;
where it appears in the experiment;
which equation defines it;
why it matters for interpretation.
```

---

## 2. Pyramid of importance

### Level 1 — Must know for GCMS-D0

These are the core objects of the project:

```text
vectors;
mean subtraction / compensation;
Euclidean distance;
global residual vector;
local relation function;
graph thresholding;
connected components;
empirical p-values;
paired comparison.
```

### Level 2 — Needed to interpret results

These explain whether the result is real or an artifact:

```text
graph density;
degree and degree variance;
largest connected component;
clustering coefficient;
Erdos-Renyi baseline;
degree-preserving baseline;
Wilson confidence interval;
McNemar exact test;
multiple-testing discipline.
```

### Level 3 — Needed for paper / preprint quality

These support stronger scientific framing:

```text
random graph theory;
configuration-model intuition;
ablation logic;
effect-size interpretation;
failure-mode taxonomy;
statistical power / sample size reasoning;
robustness across parameters;
causal language discipline.
```

### Level 4 — Future theory layer

These are not required for the current run, but may matter later:

```text
dynamical systems;
phase transitions / bifurcation intuition;
statistical mechanics of graphs;
information geometry;
manifold / metric-space interpretations;
percolation and fragmentation theory.
```

---

## 3. Vector space and world state

Each world contains `N` states in `d` dimensions.

```math
v_i \in \mathbb{R}^d, \quad i = 1,\dots,N
```

The full world matrix is:

```math
X = \begin{bmatrix} v_1^T \\ v_2^T \\ \cdots \\ v_N^T \end{bmatrix} \in \mathbb{R}^{N \times d}
```

In the current experiments:

```text
N = 150
d = 4
```

Why it matters:

```text
GCMS-D0 studies how global constraints on these vectors affect local graph structure.
```

---

## 4. Global compensation

The global vector is:

```math
K = \sum_{i=1}^{N} v_i
```

The global error is:

```math
\|K\|_2
```

A compensated world is created by subtracting the mean vector:

```math
\bar{v} = \frac{1}{N}\sum_{i=1}^{N} v_i
```

```math
v_i' = v_i - \bar{v}
```

Then:

```math
\sum_{i=1}^{N} v_i' = 0
```

Compensation-valid condition in code:

```math
\|K\|_2 < 10^{-12}
```

Why it matters:

```text
This is the global condition whose local consequences we are testing.
```

---

## 5. Why v0.9.1 was methodologically insufficient

v0.9.1 used a distance-only local relation:

```math
R_{ij} = \exp\left(-\alpha \|v_i - v_j\|^2\right)
```

But mean subtraction does not change pairwise differences:

```math
(v_i - \bar{v}) - (v_j - \bar{v}) = v_i - v_j
```

Therefore:

```math
\| (v_i - \bar{v}) - (v_j - \bar{v}) \| = \| v_i - v_j \|
```

Meaning:

```text
A purely distance-based graph cannot test whether global compensation causes the local graph structure.
```

This is the central reason v0.10 introduced compensation-aware relation variants.

---

## 6. Relation variants

### Variant 0 — distance-only control

```math
R_{ij}^{(0)} = \exp\left(-\alpha \|v_i - v_j\|^2\right)
```

Expected role:

```text
Control. It should be mostly insensitive to mean subtraction.
```

### Variant 2 — compensation-alignment relation

```math
R_{ij}^{(2)} = \exp\left(-\alpha \|v_i - v_j\|^2 - \beta |(v_i + v_j) \cdot K|\right)
```

Where:

```math
K = \sum_i v_i
```

Why it matters:

```text
Variant 2 makes the local relation sensitive to how a pair aligns with the global residual vector.
This is the current main experimental variant.
```

Current important beta values:

```text
beta=0.003 — leading clean positive candidate
beta=0.005 — prior transition / practical middle candidate
beta=0.007 — peak effect / high-confound reference point
```

### Variant 3 — pair-residual relation

```math
R_{ij}^{(3)} = \exp\left(-\alpha \|v_i - v_j\|^2 - \beta \|v_i + v_j\|^2\right)
```

Why it matters:

```text
Tests whether pairwise residual cancellation, rather than global K alignment, drives structure.
```

### Variant 4 — pressure-to-zero dynamics

Variant 4 keeps a distance-like relation but applies global pressure:

```math
v_i \leftarrow v_i - \lambda \frac{K}{N}
```

Why it matters:

```text
Tests dynamic correction toward global compensation rather than changing only the relation function.
```

---

## 7. Graph construction

A graph is built by thresholding relations:

```math
A_{ij} = \mathbf{1}\{R_{ij} > \theta\}
```

where current threshold is:

```math
\theta = 0.75
```

The graph is:

```math
G = (V, E)
```

with:

```math
V = \{1,\dots,N\}
```

and:

```math
(i,j) \in E \iff R_{ij} > \theta
```

Why it matters:

```text
The entire local structure is measured through this thresholded graph.
```

---

## 8. Connected components and sectors

Connected components are maximal node sets where every node is reachable through graph edges.

A component is valid if:

```math
s_{min} \le |C| \le s_{max}
```

Current code settings:

```text
min_size = 5
max_size = 60
```

The selected sector is the valid component with largest chi.

---

## 9. Sector chi

For a sector `C`, chi is:

```math
\chi(C) = \left\| \sum_{i \in C} v_i \right\|_2
```

Why it matters:

```text
It selects a locally strong sector among valid components.
```

---

## 10. Graph density

For an undirected graph with `n` nodes and `m` edges:

```math
\rho = \frac{2m}{n(n-1)}
```

Why it matters:

```text
Density helps decide whether a result is structural or just caused by graph sparsification/collapse.
```

Important observed issue:

```text
In fine_beta_v010, uncompensated edge_count decreases as beta increases,
while density may increase because sector_size shrinks.
Therefore density alone is not enough.
```

---

## 11. Degree and degree variance

The degree of node `i` is:

```math
k_i = \sum_j A_{ij}
```

Mean degree:

```math
\bar{k} = \frac{1}{n}\sum_{i=1}^{n} k_i = \frac{2m}{n}
```

Degree variance:

```math
\operatorname{Var}(k) = \frac{1}{n}\sum_{i=1}^{n} (k_i - \bar{k})^2
```

Why it matters:

```text
Degree variance helps detect whether graph structure changes because connectivity becomes distorted.
```

---

## 12. Largest component fraction

If connected components have sizes:

```math
c_1, c_2, \dots, c_r
```

then:

```math
\operatorname{LCF} = \frac{\max_k c_k}{n}
```

Why it matters:

```text
This checks whether the sector graph is still meaningfully connected or fragmented.
```

Qwen threshold suggestion:

```math
\operatorname{LCF} > 0.5
```

---

## 13. Clustering coefficient

Local clustering around a node measures how often its neighbors are connected.

For node `i`:

```math
C_i = \frac{2e_i}{k_i(k_i - 1)}
```

where `e_i` is the number of edges among neighbors of `i`.

Average clustering:

```math
C = \frac{1}{n}\sum_i C_i
```

Why it matters:

```text
GCMS structure_success asks whether observed clustering is unusually high compared to random baselines.
```

---

## 14. Erdos-Renyi baseline

The random graph baseline is:

```math
G(n,p)
```

where:

```math
p = \rho
```

and `rho` is the observed graph density.

The experiment samples many random graphs and compares clustering.

Why it matters:

```text
This tests whether observed clustering is higher than expected from a random graph with the same density.
```

---

## 15. Degree-preserving baseline

The degree-preserving baseline randomizes edges while trying to preserve the degree sequence.

Conceptually:

```math
G_{DP} \sim \text{RandomGraphsWithSameDegreeSequence}(G)
```

In code, this uses double-edge swaps.

Why it matters:

```text
This is a stronger control than G(n,p), because clustering can be caused by degree distribution.
```

---

## 16. Empirical p-values

For observed statistic `T_obs` and baseline samples `T_1,...,T_B`, the empirical p-value is:

```math
p = \frac{1 + \#\{b : T_b \ge T_{obs}\}}{B + 1}
```

Used for:

```text
p_gnp_empirical
p_dp_empirical
```

Why it matters:

```text
It avoids assuming a parametric distribution for clustering under the random baselines.
```

---

## 17. Structure success

Current structure success criterion:

```math
p_{GNP} < 0.05
```

and:

```math
p_{DP} < 0.05
```

and:

```math
DP\_valid = \text{true}
```

and:

```math
lifetime > 20
```

and:

```math
5 \le sector\_size \le 60
```

Together:

```math
structure\_success =
(p_{GNP}<0.05) \land (p_{DP}<0.05) \land DP\_valid \land (lifetime>20) \land (5 \le n \le 60)
```

Why it matters:

```text
This is the main binary endpoint used in the current result tables.
```

---

## 18. Strict success

Strict success is:

```math
strict\_success = compensation\_valid \land structure\_success
```

Why it matters:

```text
It separates local structure from global compensation validity.
```

---

## 19. Compensation effect

Primary endpoint:

```math
\Delta_{attempted}(\beta) =
P(structure\_success \mid compensated, \beta) -
P(structure\_success \mid uncompensated, \beta)
```

Empirically:

```math
\hat{\Delta}(\beta) = \hat{p}_{comp}(\beta) - \hat{p}_{uncomp}(\beta)
```

Why attempted denominator:

```text
Failed and unanalyzable runs remain part of the outcome.
```

---

## 20. Wilson confidence interval

For a binomial proportion:

```math
\hat{p} = \frac{k}{n}
```

Wilson interval:

```math
\frac{\hat{p} + \frac{z^2}{2n}}{1 + \frac{z^2}{n}}
\pm
\frac{z}{1 + \frac{z^2}{n}}
\sqrt{\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}
```

For 95% CI:

```math
z \approx 1.96
```

Why it matters:

```text
Wilson intervals behave better than naive normal intervals, especially with finite n.
```

---

## 21. Paired McNemar test

For paired seeds, outcomes are arranged as:

| | uncomp success | uncomp fail |
|---|---:|---:|
| comp success | both_success | comp_only |
| comp fail | uncomp_only | both_fail |

McNemar focuses on discordant pairs:

```math
b = comp\_only
```

```math
c = uncomp\_only
```

Under the null hypothesis:

```math
b \sim Binomial(b+c, 0.5)
```

Exact two-sided p-value:

```math
p = 2 \cdot P\left(X \le \min(b,c)\right), \quad X \sim Binomial(b+c, 0.5)
```

Why it matters:

```text
Seeds are paired, so McNemar is more appropriate than treating groups as independent.
```

---

## 22. Multiple testing discipline

If many beta values are searched symmetrically, multiple testing matters.

Simple Bonferroni correction:

```math
\alpha' = \frac{\alpha}{m}
```

where `m` is the number of tested hypotheses.

Holm correction orders p-values:

```math
p_{(1)} \le p_{(2)} \le \dots \le p_{(m)}
```

and compares them to:

```math
\frac{\alpha}{m-k+1}
```

Why it matters:

```text
If we choose the best beta after seeing results, p-values become too optimistic.
```

Current discipline:

```text
beta=0.005 was prior candidate;
beta=0.003 emerged as earliest clean candidate;
confirm_connectivity_variant2 pre-specifies beta=0.003, 0.005, 0.007.
```

---

## 23. Ablation and density matching

Ablation asks whether an effect survives removal of a suspected confound.

For density/edge matching:

```text
Take compensated graphs and reduce their edge structure to match uncompensated edge_count or density.
Then re-evaluate structure_success.
```

Conceptual question:

```math
\Delta_{matched} = P(success \mid compensated, matched) - P(success \mid uncompensated)
```

If:

```math
\Delta_{matched} > 0
```

then the compensation effect is less likely to be explained only by higher connectivity.

Why it matters:

```text
This is Qwen's main remaining blocker after connectivity metrics.
```

---

## 24. Failure-mode taxonomy

Structure success is conjunctive, so failure can occur for different reasons.

Current failure flags:

```text
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Failure reason is a joined label:

```text
failure_reason = sector_size|lifetime|dp_valid|p_gnp|p_dp
```

Why it matters:

```text
If one criterion explains almost all failures, the apparent mechanism may be less general than it looks.
```

Qwen suggested threshold:

```math
\max_k P(failure\_mode = k) \le 0.70
```

as a rough preprint-level sanity check.

---

## 25. Main GCMS-D0 mathematical story

The current mathematical story is:

```text
1. Start with a high-dimensional vector world.
2. Define global compensation as zero global sum.
3. Show that distance-only relations cannot test compensation causality.
4. Introduce compensation-aware local relations.
5. Threshold local relations into graphs.
6. Track persistent local sectors.
7. Test whether sectors are non-random against random graph baselines.
8. Compare compensated vs uncompensated paired worlds.
9. Audit whether the effect survives graph-collapse, fragmentation, and failure-mode checks.
```

The project is currently between steps 8 and 9.

---

## 26. Suggested study order for Aleksey

### First pass — 1 hour

```text
Euclidean norm and mean subtraction
pairwise distance invariance
threshold graphs
connected components
graph density
empirical p-value
```

### Second pass — 2-3 hours

```text
clustering coefficient
Erdos-Renyi G(n,p)
degree sequence / degree-preserving randomization
Wilson confidence interval
McNemar test
```

### Third pass — article support

```text
multiple testing
ablation logic
configuration model
percolation / fragmentation intuition
statistical power
```

### Future theory pass

```text
dynamical systems
phase transitions
information geometry
statistical mechanics of graphs
```

---

## 27. Minimal glossary

```text
compensated world:
    world where global vector sum is approximately zero.

uncompensated world:
    world where raw random vectors are not mean-subtracted.

global residual K:
    sum of all state vectors.

relation:
    rule assigning strength R_ij to a pair of nodes.

threshold graph:
    graph formed by keeping edges where R_ij exceeds threshold.

sector:
    selected connected component satisfying size and lifetime criteria.

structure_success:
    sector passes random-baseline clustering tests and validity criteria.

strict_success:
    compensation_valid and structure_success.

compensation effect:
    difference in structure_success rate between compensated and uncompensated modes.

collapse / sparsification:
    when graph-sector quantities degrade enough that success differences may be artifact.

clean candidate:
    beta point where effect is positive and diagnostics do not indicate obvious collapse.
```
