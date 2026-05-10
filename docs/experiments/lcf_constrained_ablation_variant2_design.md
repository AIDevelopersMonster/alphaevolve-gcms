# Design Checkpoint: lcf_constrained_ablation_variant2

**Status:** design checkpoint / not yet implemented / not yet executed  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `lcf_constrained_ablation_variant2`  
**Related result note:** `docs/results/v010_density_matched_ablation_variant2_random_preliminary.md`  
**Related Qwen review:** `docs/reviews/v010_density_matched_ablation_variant2_qwen_review.md`  
**Related design protocol:** `docs/EXPERIMENT_DESIGN_PROTOCOL.md`  
**Current ablation tool:** `tools/ablate_density_variant2.py`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This checkpoint defines the next required topology-preserving ablation before any new implementation or execution.

The previous experiment, `density_matched_ablation_variant2` with `random_edge_removal_preliminary`, achieved exact target edge-count matching but introduced severe fragmentation.

Key previous result at the primary target:

```text
random-removal compensated target_edge_count = 25
structure_success = 0.345
largest_component_fraction = 0.307
n_components ≈ 19.6
```

Reference from `confirm_connectivity_variant2`:

```text
uncompensated beta=0.003
structure_success = 0.52
largest_component_fraction ≈ 0.949
n_components ≈ 1.01
```

Therefore the previous comparison is not topology-matched.

This experiment tests whether the Variant 2 compensation signal survives edge-count matching when connectivity is preserved as much as possible.

---

## 2. Research question

Primary question:

```text
Does the beta=0.003 Variant 2 compensation signal persist when compensated graphs are reduced to the uncompensated edge-count regime while preserving largest-component connectivity?
```

Secondary questions:

```text
1. Can compensated graphs be reduced to target_edge_count≈25 while maintaining LCF >= 0.85?
2. If yes, is structure_success still above the uncompensated reference rate 0.52?
3. If no, does infeasibility itself show that edge-count matching plus topology preservation is structurally constrained?
4. How much does success depend on actual LCF after removal?
5. Does failure mode remain dominated by p_gnp / p_dp or shift to another criterion?
```

---

## 3. Why this experiment is required

Qwen classified the random-removal ablation as:

```text
Useful non-final random-removal stress test.
```

Qwen also stated:

```text
The target 25 comparison does not weaken beta=0.003 because it is invalidated by LCF collapse.
```

Main blocker:

```text
LCF=0.307 vs reference LCF≈0.949 creates a stronger fragmentation confound than the original edge-count gap.
```

Thus the next ablation must control not only edge count but also connectivity topology.

---

## 4. Experiment scope

Experiment name:

```text
lcf_constrained_ablation_variant2
```

Initial scope:

```text
relation_variant = 2
model_mode = compensated
beta = 0.003
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

Target edge counts:

```text
target_edge_counts = [25, 30, 35]
```

Reason for excluding 40 initially:

```text
40 is useful as a recovery point but is not close to the uncompensated beta=0.003 reference edge-count regime.
The initial LCF-constrained experiment should focus on the critical low-edge region.
```

Repetitions:

```text
repetitions_per_target = 5
```

Max attempts per seed/target/repetition:

```text
max_attempts_per_seed = 100
```

LCF threshold:

```text
LCF_min_threshold = 0.85
```

Reference tolerance:

```text
LCF should differ from uncompensated reference by no more than approximately 0.10 where feasible.
```

---

## 5. Proposed removal method

Method name:

```text
greedy_non_bridge_removal_with_LCF_constraint
```

Core idea:

```text
Remove edges from compensated graphs while avoiding edge removals that disconnect the largest component too severely.
```

Algorithm sketch:

```text
For each seed and target_edge_count:
    build original compensated graph;
    for each repetition:
        h = copy(original graph)
        while h.edge_count > target_edge_count:
            identify candidate removable edges;
            prefer non-bridge edges;
            randomly sample candidate edges or choose greedily;
            tentatively remove an edge;
            recompute largest_component_fraction;
            accept removal only if LCF >= LCF_min_threshold;
            if no acceptable edge exists after max_attempts:
                mark target_connectivity_preserved = false;
                stop or record failure;
        analyze h if target reached;
```

Important implementation detail:

```text
Use bridge detection relative to the current graph, not the original graph only.
```

---

## 6. Required reachability and preservation flags

Raw output must include both edge-count and connectivity-preservation flags:

```text
target_reachable
target_reached
reachability_reason
target_connectivity_preserved
connectivity_preservation_reason
lcf_min_threshold
actual_largest_component_fraction
removal_attempts
removal_failures
```

Definitions:

```text
target_reachable = original_edge_count >= target_edge_count
target_reached = actual_edge_count == target_edge_count
target_connectivity_preserved = largest_component_fraction >= LCF_min_threshold
```

Possible `connectivity_preservation_reason` values:

```text
preserved
failed_lcf_constraint
failed_no_non_bridge_edges
failed_max_attempts
not_reached
unreachable_original_edge_count
```

Primary valid rows:

```text
target_reached == True AND target_connectivity_preserved == True
```

---

## 7. Required raw output columns

The raw output should include all previous ablation columns plus LCF-constrained fields.

Required columns:

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
target_reachable
target_reached
reachability_reason
target_connectivity_preserved
connectivity_preservation_reason
lcf_min_threshold
actual_largest_component_fraction
removal_attempts
removal_failures
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

---

## 8. Required summary output

Summary must separate:

```text
all rows;
edge-count reached rows;
LCF-preserved rows;
valid rows where both target_reached and target_connectivity_preserved are true.
```

Required summary fields:

```text
subsampling_method
target_edge_count
attempted_runs_all
target_reached_count
target_reached_rate
target_connectivity_preserved_count
target_connectivity_preserved_rate
valid_lcf_matched_count
valid_lcf_matched_rate
structure_success_rate_valid
mean_actual_edge_count_valid
mean_largest_component_fraction_valid
mean_n_components_valid
mean_degree_variance_valid
mean_sector_size_valid
failed_p_gnp_rate_valid
failed_p_dp_rate_valid
failed_dp_valid_rate_valid
mean_dp_valid_valid
mean_dp_swap_success_rate_valid
mean_removal_attempts
mean_removal_failures
```

---

## 9. Per-seed aggregation

Because repetitions are nested under seed, per-seed aggregation is required.

Required per-seed columns:

```text
target_edge_count
seed
valid_repetitions
success_count_valid
success_fraction_per_seed_target_valid
majority_success_per_seed_target_valid
mean_largest_component_fraction_per_seed_target_valid
mean_failed_p_gnp_per_seed_target_valid
mean_sector_size_per_seed_target_valid
connectivity_preservation_fraction_per_seed_target
```

Do not treat all repetitions as independent seeds.

---

## 10. Primary endpoint

Primary endpoint:

```text
structure_success_rate_valid(target_edge_count=25)
```

where valid means:

```text
target_reached == True
AND
target_connectivity_preserved == True
```

Reference comparison:

```text
uncompensated beta=0.003 structure_success = 0.52
uncompensated beta=0.003 LCF ≈ 0.949
```

Primary question:

```text
Is structure_success_rate_valid at target_edge_count=25 greater than 0.52 while maintaining LCF >= 0.85?
```

---

## 11. Success criteria

### Strong success

```text
At target_edge_count = 25:
1. target_reached_rate is high enough to be meaningful;
2. target_connectivity_preserved_rate >= 0.80;
3. mean LCF valid >= 0.85;
4. structure_success_rate_valid > 0.52;
5. per-seed majority_success shows positive paired support versus uncompensated reference;
6. failed_p_gnp_rate_valid does not exceed reference by more than approximately 0.10.
```

### Partial success

```text
LCF-preserving target 25 is feasible but structure_success_rate_valid is near 0.52;
or target 25 is rarely feasible but target 30 succeeds with preserved connectivity.
```

Interpretation:

```text
The mechanism may require a minimum connectivity threshold.
```

### Negative result

```text
Target 25 is feasible with LCF >= 0.85 but structure_success_rate_valid remains below uncompensated reference.
```

Interpretation:

```text
The beta=0.003 signal is likely not robust under topology-preserving edge-count matching.
```

### Infeasible result

```text
Target 25 cannot be reached while preserving LCF >= 0.85 for most seeds.
```

Interpretation:

```text
Strict edge-count matching to 25 may be topologically incompatible with compensated graph structure under the current removal constraints.
The result remains informative but does not resolve the mechanism question.
```

---

## 12. What must not change

Do not change:

```text
structure_success definition;
p_gnp threshold;
p_dp threshold;
dp_valid requirement;
lifetime threshold;
sector_size bounds;
Variant 2 relation function;
existing confirm_connectivity result interpretation;
reference values after seeing the result.
```

Do not claim success merely because edge count is matched.

Do not claim failure merely because target 25 is infeasible.

---

## 13. Implementation strategy

Preferred path:

```text
Extend tools/ablate_density_variant2.py with a new mode:
--mode lcf
```

Do not replace:

```text
--mode smoke
--mode full
```

New CLI to implement but not initially run full-scale:

```powershell
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf --out-prefix v010_lcf_constrained_ablation_variant2
```

First implement smoke-only LCF validation:

```text
mode = lcf_smoke or --mode lcf_smoke
target_edge_counts = [25, 30]
seeds = 2
repetitions = 2
baseline_count = 10
LCF_min_threshold = 0.85
max_attempts_per_seed = 100
```

Recommended mode naming:

```text
lcf_smoke
lcf_full
```

rather than overloading `full`.

---

## 14. Smoke validation requirements

Before any full LCF run:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\ablate_density_variant2.py
.\.venv\Scripts\python.exe tools\ablate_density_variant2.py --mode lcf_smoke --out-prefix smoke_lcf_ablation_variant2
```

Then verify:

```text
raw output exists;
summary output exists;
target_reached flags exist;
target_connectivity_preserved flags exist;
valid_lcf_matched_count is reported;
failures are explicit, not silently averaged;
existing random-removal modes still work;
structure_success criteria unchanged;
full LCF mode is not run without explicit authorization.
```

---

## 15. Qwen review prompt after execution

After execution, Qwen should review:

```text
1. whether LCF-constrained removal actually preserved topology;
2. whether target 25 is feasible;
3. whether beta=0.003 remains leading clean candidate;
4. whether density/LCF confound is resolved, partially resolved, or still blocked;
5. whether preprint-level toy-model wording is now acceptable;
6. what additional graph controls remain required.
```

---

## 16. Current status

```text
Design checkpoint created.
No code changes yet.
No LCF-constrained smoke run yet.
No full LCF run authorized.
```

Short invariant:

```text
Edge count alone was not enough.
The next test must match edge count without destroying the largest component.
```
