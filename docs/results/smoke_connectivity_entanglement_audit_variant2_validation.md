# Smoke Validation: connectivity_entanglement_audit_variant2

**Status:** smoke validation / not full audit  
**Date:** 2026-05-11  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Mode:** `smoke`  
**Tool:** `tools/audit_connectivity_entanglement_variant2.py`  
**Design checkpoint:** `docs/experiments/connectivity_entanglement_audit_variant2_design.md`  
**Reframe:** `docs/experiments/connectivity_entanglement_reframe.md`  
**Qwen reframe review:** `docs/reviews/connectivity_entanglement_reframe_qwen_review.md`  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  

---

## 1. Purpose

This note validates the smoke implementation of `connectivity_entanglement_audit_variant2` before any full audit run.

This audit is not an edge-removal experiment.

It follows the new post-LCF reframe:

```text
Measure native topology first.
Do not prune.
Do not rescue.
```

The purpose of the smoke run is to verify that the new audit tool:

```text
1. creates native topology descriptors;
2. compares compensated and uncompensated modes;
3. writes raw, summary, per-seed, and threshold outputs;
4. does not run full audit;
5. does not modify the graph by pruning or edge removal.
```

---

## 2. Code state

The smoke audit tool was implemented and committed locally, then synchronized to GitHub:

```text
ae1e955 Add connectivity entanglement audit smoke tool
9d5c416 Merge branch 'master' of https://github.com/AIDevelopersMonster/alphaevolve-gcms
```

Current synchronized state after push:

```text
HEAD = origin/master = 9d5c416
working tree clean
```

---

## 3. Smoke command

Commands executed locally:

```powershell
.\.venv\Scripts\python.exe -m py_compile tools\audit_connectivity_entanglement_variant2.py
.\.venv\Scripts\python.exe tools\audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2
```

Generated outputs:

```text
outputs/raw_smoke_connectivity_entanglement_audit_variant2.csv
outputs/summary_smoke_connectivity_entanglement_audit_variant2.csv
outputs/per_seed_smoke_connectivity_entanglement_audit_variant2.csv
outputs/thresholds_smoke_connectivity_entanglement_audit_variant2.csv
```

Expected smoke rows:

```text
2 model_modes × 2 seeds = 4 rows
```

---

## 4. Raw output validation

Raw header includes the required native topology descriptors:

```text
bridge_count
bridge_fraction
non_bridge_edge_count
cycle_rank
largest_component_edge_count
largest_component_node_count
largest_component_cycle_rank
mean_degree
degree_variance
max_degree
clustering
spectral_gap_optional
spectral_gap_available
algebraic_connectivity_optional
algebraic_connectivity_available
```

It also retains structure outcome descriptors:

```text
p_gnp_empirical
p_dp_empirical
dp_valid
dp_swap_success_rate
structure_success
failure_reason
failed_p_gnp
failed_p_dp
failed_dp_valid
failed_lifetime
failed_sector_size
```

Validation result:

```text
Raw output schema is suitable for the native topology audit.
```

---

## 5. Summary output

From `outputs/summary_smoke_connectivity_entanglement_audit_variant2.csv`:

| model_mode | runs | structure_success | edge_count | density | n_components | LCF | bridge_count | bridge_fraction | non_bridge_edge_count | cycle_rank | LCC cycle rank |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| compensated | 2 | 0.0 | 20.0 | 0.3616 | 1.0 | 1.0 | 5.5 | 0.2304 | 14.5 | 6.5 | 6.5 |
| uncompensated | 2 | 0.0 | 26.5 | 0.1799 | 1.0 | 1.0 | 4.5 | 0.2136 | 22.0 | 10.0 | 10.0 |

Important note:

```text
Smoke values are not scientific effect estimates.
The smoke run has only 2 seeds per mode and should not be interpreted as evidence for or against the reframe.
```

The summary confirms that topology descriptors are computed and aggregated by mode.

---

## 6. Per-seed paired output

From `outputs/per_seed_smoke_connectivity_entanglement_audit_variant2.csv`:

| seed | edge_count_comp | edge_count_uncomp | delta_edge_count | bridge_fraction_comp | bridge_fraction_uncomp | delta_non_bridge_edge_count | delta_cycle_rank | delta_structure_success |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 34 | 19 | 15 | 0.2941 | 0.3684 | 12 | 6 | 0 |
| 1 | 6 | 34 | -28 | 0.1667 | 0.0588 | -27 | -13 | 0 |

Validation result:

```text
Per-seed compensated-vs-uncompensated paired comparison is present.
```

Smoke interpretation:

```text
The two-seed smoke sample is noisy by design. It validates paired reporting, not the scientific hypothesis.
```

---

## 7. Threshold output

From `outputs/thresholds_smoke_connectivity_entanglement_audit_variant2.csv`, thresholds are produced for:

```text
non_bridge_edge_count
cycle_rank
bridge_fraction_le
```

Validation result:

```text
Threshold table exists and is structurally suitable for full audit threshold analysis.
```

Smoke caveat:

```text
All smoke structure_success rates are 0.0 because the smoke sample is too small and not intended for inference.
```

---

## 8. Safety validation

Search/check results confirmed:

```text
run_full() exists only as a placeholder;
--mode full raises NotImplementedError;
no pruning or edge-removal logic is present;
no full audit outputs were created;
no global Python usage was required for validation;
no dependency files were modified.
```

The command:

```powershell
Get-ChildItem outputs\*v010_connectivity_entanglement_audit_variant2*
```

returned no files, confirming that full audit was not run.

---

## 9. Validation result

The smoke implementation passes validation:

```text
audit_connectivity_entanglement_variant2.py exists;
py_compile passes;
smoke run passes;
raw output includes required topology descriptors;
summary output exists;
per-seed paired output exists;
threshold output exists;
full mode is not implemented and was not run;
no pruning / edge removal occurred.
```

---

## 10. Next required step

Create extension plan for full audit:

```text
docs/experiments/connectivity_entanglement_audit_variant2_extension_plan.md
```

The extension plan must specify:

```text
1. full settings;
2. full output schemas;
3. threshold analysis plan;
4. per-seed paired comparison rules;
5. allowed descriptive/regression analysis;
6. strict prohibition on pruning/rescue logic;
7. no new dependencies;
8. full run only after explicit authorization.
```

---

## 11. Short conclusion

```text
The connectivity entanglement audit smoke tool is technically valid.
It measures native topology descriptors without pruning and produces the required smoke outputs.
The project may proceed to a full-audit extension plan, but not directly to full execution without that plan.
```
