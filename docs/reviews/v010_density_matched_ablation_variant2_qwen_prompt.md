# Qwen Review Prompt: v010_density_matched_ablation_variant2_random_preliminary

**Status:** review packet / prompt for external methodological review  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Experiment mode:** `density_matched_ablation_variant2`  
**Subsampling method:** `random_edge_removal_preliminary`  
**Reviewed result note:** `docs/results/v010_density_matched_ablation_variant2_random_preliminary.md`  
**Related Qwen review:** `docs/reviews/v010_confirm_connectivity_variant2_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## Prompt to send to Qwen

```text
You are an independent methodological reviewer for GCMS-D0.

Please review the preliminary random-removal density ablation:

experiment:
  density_matched_ablation_variant2
subsampling_method:
  random_edge_removal_preliminary
status:
  preliminary / not final density-matched proof

Do not strengthen claims.
Do not treat this as a physical theory.
Review it as a computational toy-model confound-isolation experiment.

Project context:
GCMS-D0 studies whether global compensation constraints can produce locally distinguishable graph structures under compensation-aware relation functions.

Current main relation:
Variant 2 compensation-alignment relation.

Previous result:
confirm_connectivity_variant2 reproduced the Variant 2 pattern at beta=0.003, 0.005, 0.007 and added connectivity/failure diagnostics.
Your prior review classified:
- beta=0.003: leading clean positive candidate, fragmentation resolved; density confound remains
- beta=0.005: practical transition point
- beta=0.007: peak-effect/high-confound

Your prior core blocker:
Density/edge-count confound remained unresolved because compensated beta=0.003 graphs had higher edge count than uncompensated beta=0.003 graphs.

Reference from confirm_connectivity_variant2:
- compensated beta=0.003 structure_success attempted = 0.72
- uncompensated beta=0.003 structure_success attempted = 0.52
- uncompensated beta=0.003 mean edge count ≈ 25
- uncompensated beta=0.003 largest_component_fraction ≈ 0.949

New ablation:
The tool reduced compensated Variant 2 graphs to target edge counts:
25, 30, 35, 40
using random edge removal.

Important method note:
This is not degree-preserving or connectivity-preserving edge removal.
It is a preliminary random-removal stress test.

Generated outputs:
outputs/raw_v010_density_matched_ablation_variant2.csv
outputs/summary_v010_density_matched_ablation_variant2.csv
outputs/per_seed_v010_density_matched_ablation_variant2.csv

Technical integrity:
- raw rows = 4000
- 100 seeds x 4 targets x 10 repetitions = 4000
- per-seed rows = 100 per target
- target_reached_rate = 1.0 for all targets
- actual edge count exactly reached at all targets

Reachability check:

target 25:
rows = 1000
target_reached_count = 1000
target_reached_rate = 1.0
actual_edge_count min/mean/max = 25/25.0/25

target 30:
rows = 1000
target_reached_count = 1000
target_reached_rate = 1.0
actual_edge_count min/mean/max = 30/30.0/30

target 35:
rows = 1000
target_reached_count = 1000
target_reached_rate = 1.0
actual_edge_count min/mean/max = 35/35.0/35

target 40:
rows = 1000
target_reached_count = 1000
target_reached_rate = 1.0
actual_edge_count min/mean/max = 40/40.0/40

Main summary:

target 25:
structure_success_rate_reached = 0.345
mean_actual_edge_count = 25.0
mean_original_edge_count = 65.29
mean_sector_size = 42.56
mean_largest_component_fraction = 0.307
mean_n_components = 19.621
failed_p_gnp_rate = 0.610
failed_p_dp_rate = 0.602

target 30:
structure_success_rate_reached = 0.496
mean_actual_edge_count = 30.0
mean_original_edge_count = 65.29
mean_sector_size = 42.56
mean_largest_component_fraction = 0.391
mean_n_components = 16.135
failed_p_gnp_rate = 0.453
failed_p_dp_rate = 0.432

target 35:
structure_success_rate_reached = 0.688
mean_actual_edge_count = 35.0
mean_original_edge_count = 65.29
mean_sector_size = 42.56
mean_largest_component_fraction = 0.478
mean_n_components = 13.107
failed_p_gnp_rate = 0.292
failed_p_dp_rate = 0.258

target 40:
structure_success_rate_reached = 0.814
mean_actual_edge_count = 40.0
mean_original_edge_count = 65.29
mean_sector_size = 42.56
mean_largest_component_fraction = 0.573
mean_n_components = 10.384
failed_p_gnp_rate = 0.169
failed_p_dp_rate = 0.135

Per-seed majority result:

target 25:
majority_success seeds = 14/100
majority_success_rate = 0.14
mean success_fraction_per_seed = 0.345
min/max success_fraction = 0.0/1.0
mean LCF = 0.307
min/max LCF = 0.117/0.733

target 30:
majority_success seeds = 38/100
majority_success_rate = 0.38
mean success_fraction_per_seed = 0.496
min/max success_fraction = 0.1/1.0
mean LCF = 0.391
min/max LCF = 0.140/0.913

target 35:
majority_success seeds = 77/100
majority_success_rate = 0.77
mean success_fraction_per_seed = 0.688
min/max success_fraction = 0.2/1.0
mean LCF = 0.478
min/max LCF = 0.177/0.963

target 40:
majority_success seeds = 91/100
majority_success_rate = 0.91
mean success_fraction_per_seed = 0.814
min/max success_fraction = 0.3/1.0
mean LCF = 0.573
min/max LCF = 0.205/1.000

Delta-D0 preliminary interpretation:
1. Exact edge-count matching succeeded technically.
2. At the primary strict target edge_count=25, compensated subsampled success fell below the uncompensated beta=0.003 reference:
   0.345 vs 0.52.
3. However, random edge removal severely fragmented the compensated graphs:
   target 25 LCF = 0.307 vs uncompensated reference LCF ≈ 0.949.
4. Therefore this result should not be interpreted as final proof that the original effect was only an edge-count artifact.
5. It suggests the Variant 2 signal is strongly connectivity-sensitive and that naive random removal is too destructive.
6. The likely next blocker is connectivity-preserving or degree-aware edge removal.

Questions for review:

1. Is the conclusion correct that exact edge-count matching succeeded technically, but the method introduced a new fragmentation confound?
2. Does target 25 result (0.345 vs reference 0.52) weaken beta=0.003 as clean candidate, or is the comparison invalid because LCF fell to 0.307?
3. Should this be classified as a failed density-matched ablation, or as a useful but non-final random-removal stress test?
4. Does the monotonic recovery of success from target 25 -> 40 indicate connectivity threshold dependence?
5. Are failed_p_gnp and failed_p_dp trends consistent with fragmentation/connectivity loss rather than compensation-mechanism loss?
6. Is a connectivity-preserving / degree-aware ablation now mandatory before any stronger interpretation?
7. What should the next ablation method be?
   Options:
   - connectivity_preserving_edge_removal_preliminary
   - degree_aware_edge_removal_preliminary
   - lcf_constrained_edge_removal_preliminary
   - degree-distribution matched pruning
   - another method
8. What constraints should the next method enforce?
   Examples:
   - target edge count still reached
   - largest_component_fraction above threshold
   - avoid disconnecting largest component where possible
   - approximate uncompensated degree distribution
   - report target_connectivity_preserved separately
9. What exact conservative wording is now justified?
10. Should beta=0.003 remain the leading clean candidate, be downgraded, or be marked unresolved pending topology-preserving ablation?

Please answer as a skeptical methodological reviewer.
Do not praise generally.
Classify the result.
State what is resolved, what is newly confounded, and what remains blocked.
Give conservative wording suitable for a technical note.
```

---

## Delta-D0 expected use

After receiving Qwen's answer:

```text
1. Save the review as docs/reviews/v010_density_matched_ablation_variant2_qwen_review.md
2. Update interpretation only after review.
3. If Qwen agrees, create design checkpoint for connectivity-preserving / degree-aware ablation.
4. Do not claim density-confound resolved from random-removal result alone.
```
