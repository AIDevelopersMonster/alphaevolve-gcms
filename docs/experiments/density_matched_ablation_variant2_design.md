# Design Checkpoint: density_matched_ablation_variant2

**Status:** design checkpoint / not yet implemented / not yet executed  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `density_matched_ablation_variant2`  
**Related result note:** `docs/results/v010_confirm_connectivity_variant2.md`  
**Related Qwen review:** `docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md`  
**Related design protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Current experiment script:** `experiments/ae_v010_2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This checkpoint defines the next required ablation before any implementation or execution.

The `confirm_connectivity_variant2` experiment reproduced the Variant 2 pattern and substantially reduced the fragmentation concern at `beta=0.003`.

However, Qwen identified the remaining core blocker:

```text
Density/edge-count confound remains unresolved.
```

At `beta=0.003`, compensated graphs maintain approximately:

```text
edge_count ≈ 45
```

while uncompensated graphs have approximately:

```text
edge_count ≈ 25
```

Therefore, the observed +0.20 compensation effect may still be caused by higher compensated connectivity rather than a compensation-aware mechanism.

This ablation directly tests whether the compensated advantage persists after reducing compensated graphs to match uncompensated edge-count regimes.

---

## 2. Research question

Primary question:

```text
Does the Variant 2 compensation effect at beta=0.003 persist when compensated graphs are edge-count matched to the uncompensated regime?
```

Secondary questions:

```text
1. Is the beta=0.003 effect primarily a connectivity artifact?
2. Does structure_success survive when compensated graphs are subsampled to edge_count ≈ 25?
3. How does failed_p_gnp_rate change under edge-count matching?
4. Does largest_component_fraction remain high after subsampling?
5. Is beta=0.003 still eligible as the clean candidate after density matching?
```

---

## 3. Why beta=0.003 first

`beta=0.003` is selected first because it has the best current signal-to-confound ratio.

Current status after Qwen review:

```text
beta=0.003:
    leading clean positive candidate;
    fragmentation concern substantially addressed;
    density/edge-count confound remains.
```

Qwen classification:

```text
Leading clean positive candidate, fragmentation resolved; density confound remains.
```

Reason for not starting with `beta=0.005` or `beta=0.007`:

```text
beta=0.005 has stronger effect but more degradation;
beta=0.007 is peak-effect/high-confound and not suitable for clean mechanism claims.
```

If the effect does not survive density matching at `beta=0.003`, stronger claims should be blocked or reframed before testing higher beta values.

---

## 4. Core ablation idea

The ablation starts from compensated Variant 2 graphs and removes edges until their edge counts match target values from the uncompensated beta=0.003 regime.

Conceptual comparison:

```text
original compensated graph
    edge_count ≈ 45
    structure_success ≈ 0.72

uncompensated beta=0.003 graph
    edge_count ≈ 25
    structure_success ≈ 0.52

subsampled compensated graph
    edge_count target = 25, 30, 35, 40
    re-evaluate structure_success and diagnostics
```

The key test is whether compensated structure_success remains above uncompensated structure_success when edge count is matched or reduced toward the uncompensated regime.

---

## 5. Proposed design

Experiment name:

```text
density_matched_ablation_variant2
```

Initial scope:

```text
relation_variant = 2
beta = 0.003
source mode = compensated
reference mode = uncompensated beta=0.003 from confirm_connectivity_variant2
seeds = 100
baseline_count = 100
N = 150
d = 4
steps = 200
alpha = 0.5
threshold = 0.75
mutation_rate = 0.10
epsilon_norm = 0.0
lambda_val = 0.0
```

Subsampling targets:

```text
target_edge_counts = [25, 30, 35, 40]
```

Repetitions per target:

```text
repetitions_per_target = 10
```

Expected ablation evaluations:

```text
100 seeds * 4 target_edge_counts * 10 repetitions = 4000 subsampled graph evaluations
```

Important distinction:

```text
This should not require rerunning the full world-generation simulation 4000 times.
The preferred implementation should reuse or regenerate per-seed compensated graphs, then apply graph-level edge subsampling and re-run graph diagnostics.
```

---

## 6. Subsampling method

Qwen recommended:

```text
degree-preserving edge removal
```

Practical implementation may need a staged approach:

### Stage A — simple edge-count matched removal

```text
Randomly remove edges from compensated graphs until target_edge_count is reached.
Repeat 10 times per target per seed.
```

Pros:

```text
simple;
fast;
directly tests edge-count sensitivity.
```

Cons:

```text
does not preserve degree distribution;
may introduce artificial fragmentation;
weaker than degree-preserving removal.
```

### Stage B — degree-aware / degree-preserving removal

Possible approaches:

```text
1. remove edges while minimizing deviation from original degree distribution;
2. remove edges to match the uncompensated degree distribution as closely as possible;
3. use constrained random removal with rejection if largest_component_fraction falls below threshold;
4. use degree-sequence-targeted pruning if feasible.
```

Design decision before implementation:

```text
Stage A can be used as a fast preliminary ablation.
Stage B is required for stronger preprint-level support.
```

This checkpoint prefers implementing Stage A first only if it is clearly labeled preliminary. The stronger target remains degree-aware/density-matched ablation.

---

## 7. Required outputs

Raw ablation output should include at minimum:

```text
model_mode
relation_variant
beta
seed
subsample_rep
target_edge_count
actual_edge_count
original_edge_count
edge_removal_count
edge_removal_fraction
subsampling_method
N
d
steps
baseline_count
mutation_rate
sector_size
edge_count
density
clustering
chi
lifetime
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
n_components
largest_component_fraction
degree_variance
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Summary output should include:

```text
subsampling_method
target_edge_count
attempted_runs
analyzed_runs
structure_success_rate_attempted
structure_success_rate_analyzed
mean_actual_edge_count
mean_original_edge_count
mean_edge_removal_fraction
mean_sector_size
mean_density
mean_n_components
mean_largest_component_fraction
mean_degree_variance
failed_p_gnp_rate
failed_p_dp_rate
failed_dp_valid_rate
failed_lifetime_rate
failed_sector_size_rate
mean_dp_valid
mean_dp_swap_success_rate
```

Comparison output should include direct comparison against uncompensated beta=0.003:

```text
target_edge_count
subsampled_compensated_success_rate
uncompensated_success_rate_reference
matched_compensation_effect_attempted
reference_uncompensated_edge_count
mean_actual_edge_count
mcnemar_or_independent_test_note
```

---

## 8. Primary endpoint

Primary endpoint:

```text
matched_compensation_effect_attempted(target_edge_count) =
P(structure_success | compensated subsampled to target_edge_count)
-
P(structure_success | uncompensated beta=0.003 reference)
```

Reference uncompensated value from `confirm_connectivity_variant2`:

```text
P(structure_success | uncompensated, beta=0.003) = 0.52
```

Key target:

```text
target_edge_count ≈ 25
```

because this is the approximate uncompensated beta=0.003 edge-count regime.

---

## 9. Statistical comparison

The ideal comparison should preserve seed pairing where possible.

However, because subsampled compensated graphs include repeated random subsampling per seed, the analysis must avoid overstating independence.

Recommended reporting:

```text
1. per-seed mean success across repetitions for each target_edge_count;
2. paired comparison between per-seed subsampled compensated success and uncompensated seed success;
3. Wilson CI for aggregate success rates;
4. sensitivity plot across target_edge_count values;
5. exact McNemar only if binary paired outcomes are defined clearly per seed.
```

Possible paired binary rule:

```text
For each seed and target_edge_count, define subsampled_success_seed = majority(success across 10 repetitions).
Then compare subsampled_success_seed vs uncompensated_success_seed using McNemar.
```

Alternative:

```text
Use per-seed success fraction and report paired bootstrap or paired mean difference.
```

Do not treat all 4000 subsampled evaluations as independent seeds.

---

## 10. Success criteria

### Strong success

```text
At target_edge_count ≈ 25:
1. matched_compensation_effect_attempted remains positive;
2. paired evidence supports compensated subsampled > uncompensated;
3. largest_component_fraction remains > 0.90 on average;
4. failed_p_gnp_rate in subsampled compensated mode does not exceed uncompensated failed_p_gnp_rate by more than 0.10;
5. sector_size remains comfortably above the lower boundary;
6. result is stable across subsampling repetitions.
```

If this holds, beta=0.003 becomes much stronger as a clean toy-model candidate.

### Useful partial success

```text
Effect weakens but remains positive at target_edge_count 30 or 35;
effect disappears at 25;
connectivity threshold behavior is visible.
```

This would suggest the mechanism is partly connectivity-dependent and would guide future relation design.

### Negative result

```text
Effect disappears or reverses when compensated graphs are matched to edge_count ≈25.
```

This would imply the previous +0.20 effect was largely or primarily a connectivity artifact.

### Blocked result

Interpretation remains blocked if:

```text
subsampling method causes severe fragmentation;
actual edge counts do not match targets;
repetitions are treated incorrectly as independent seeds;
failure taxonomy is missing;
largest_component_fraction is not reported;
degree distribution is not reported or audited;
implementation silently changes original structure_success criteria.
```

---

## 11. Required diagnostics beyond success rate

The result must include:

```text
1. actual_edge_count distribution by target;
2. sector_size quantiles by target;
3. largest_component_fraction by target;
4. n_components by target;
5. degree_variance by target;
6. failed_p_gnp_rate by target;
7. failed_p_dp_rate by target;
8. failed_dp_valid_rate by target;
9. lifetime summary by target;
10. comparison against uncompensated beta=0.003 reference.
```

Qwen specifically requested:

```text
sector-size histogram or quantiles;
degree-distribution comparison;
exclusion-bias assessment;
conditional failure analysis p_gnp vs p_dp.
```

These may be included in the first implementation or as immediate post-processing scripts.

---

## 12. What must not change

The following must not be changed during this ablation:

```text
structure_success definition;
p_gnp threshold;
p_dp threshold;
DP_valid requirement;
lifetime threshold;
sector_size bounds;
baseline_count unless explicitly documented;
random seed handling without documentation;
Variant 2 relation definition;
interpretation after seeing results.
```

This ablation tests a confound.
It must not move the goalposts.

---

## 13. Expected implementation options

### Option 1 — modify `experiments/ae_v010_2.py`

Pros:

```text
keeps all experiment modes in one script;
can reuse existing graph analysis code;
consistent output style.
```

Cons:

```text
risk of disturbing validated experiment code;
large script becomes harder to manage.
```

### Option 2 — create separate tool/script

Possible path:

```text
tools/ablate_density_variant2.py
```

Pros:

```text
keeps ablation isolated;
safer for existing v0.10 script;
can be promoted later into a skill/tool.
```

Cons:

```text
may need to duplicate or import analysis functions;
requires careful consistency with existing structure_success logic.
```

Preferred initial choice:

```text
Create a separate tool/script unless code reuse from ae_v010_2.py is clean and low-risk.
```

Before implementation, Codex should be instructed:

```text
Do not change success criteria.
Do not change existing presets.
Do not launch full ablation run.
Implement smoke mode first.
Add output schema and run py_compile.
```

---

## 14. Smoke test before full run

Before full ablation, run a smoke configuration:

```text
beta = 0.003
seeds = 2
target_edge_counts = [25, 35]
repetitions_per_target = 2
baseline_count = 10 or existing smoke baseline
```

Smoke test must verify:

```text
raw output exists;
summary output exists;
actual_edge_count reaches targets;
structure_success columns exist;
connectivity columns exist;
failure flags exist;
no success criteria changed;
git status shows only expected code/doc changes.
```

---

## 15. Qwen review prompt after execution

After the ablation result, ask Qwen:

```text
You are an independent methodological reviewer for GCMS-D0.

Review density_matched_ablation_variant2.
Do not strengthen claims.
Focus on whether the density/edge-count confound from confirm_connectivity_variant2 is resolved.

Questions:
1. Does beta=0.003 remain a clean candidate after edge-count matching?
2. Does the compensation effect persist at target_edge_count ≈25?
3. Does structure_success degrade in subsampled compensated graphs as expected from connectivity alone?
4. Does failed_p_gnp_rate remain favorable compared with uncompensated reference?
5. Does largest_component_fraction remain high enough to avoid new fragmentation confound?
6. Are sector_size distributions safely away from boundary artifacts?
7. Is degree-distribution confounding reduced or still unresolved?
8. What exact conservative wording is now justified?
9. Is a preprint-level toy-model claim now acceptable, or is another ablation required?
```

---

## 16. Decision after ablation

Possible decisions:

```text
A. Effect persists at edge_count≈25 -> beta=0.003 becomes strong clean candidate; prepare technical note/preprint plan.
B. Effect weakens but persists at 30/35 -> mechanism is partly connectivity-dependent; design refined relation or threshold analysis.
C. Effect disappears at matched edge count -> reinterpret confirm result as primarily connectivity artifact.
D. Subsampling fragments graphs -> redesign ablation method using degree-aware removal.
E. Results are mixed -> run degree-distribution and sector-boundary audits before claim update.
```

---

## 17. Current status

```text
Design checkpoint created.
No code implementation yet.
No full run authorized.
Next action: implementation planning / Codex instruction for smoke-mode ablation script.
```

Short invariant:

```text
This is not a new claim experiment.
This is a confound-isolation experiment.
```
