# AlphaEvolve-GCMS Project Inventory

**Status:** working inventory  
**Last updated:** 2026-05-09  
**Repository:** `AIDevelopersMonster/alphaevolve-gcms`  
**Default branch:** `master`

This document is a map of the repository, documents, branches, and current research state. It exists to prevent the project from becoming hard to navigate as the science, protocol, and AI-interaction layers develop in parallel.

---

## 1. Project summary

AlphaEvolve-GCMS is an exploratory computational toy-model project for **Globally Compensated Multi-index Systems**.

Core idea:

```text
A whole system can be globally compensated while local sectors remain nonzero and structurally distinguishable.
```

Main scientific question:

```text
Can globally compensated multi-index systems generate or preserve long-lived local graph sectors with statistically non-random structure?
```

Current methodological state:

```text
v0.9.1 showed robust local non-random structures,
but distance-only relations could not prove the causal role of global compensation.

v0.10.2 introduced compensation-aware relation variants and separated:
- compensation_valid
- structure_success
- strict_success
```

Current leading mechanism:

```text
Variant 2 compensation-alignment relation shows a compensation-sensitive transition.
The current best non-collapse candidate is beta around 0.005.
```

Publication posture:

```text
working technical note / toy-model mechanism;
not a physical theory claim.
```

---

## 2. Root files

### `README.md`

Current public-facing repository overview.

Status:

```text
Needs update.
```

Reason:

```text
It still describes the early project and v0.9.1 commands,
but does not yet summarize v0.10.2, Variant 2, beta-grid results,
mutual research protocol, or the document map.
```

### `evolve_v091_chatgpt.py`

Historical stable v0.9.1 simulation file.

Purpose:

```text
Preserve the original distance-only compensated model.
```

Important caution:

```text
Do not overwrite this file with v0.10+ experiments.
Keep it as historical reference.
```

### `requirements.txt`

Python dependencies for running simulations.

### `.gitignore`

Repository ignore rules. Runtime outputs should generally stay out of commits unless explicitly documented.

### `RESULTS_v091_FOCUSED.md`

Historical v0.9.1 focused result summary.

Status:

```text
Useful historical result, but should be read with the later translation-invariance correction in mind.
```

---

## 3. Experiment code

### `experiments/ae_v010_2.py`

Current v0.10.2 methodology-correction experiment.

Purpose:

```text
Compare compensated, uncompensated, and residual modes.
Separate compensation_valid, structure_success, and strict_success.
Test compensation-aware relation variants.
```

Key variants:

```text
Variant 0: distance-only control.
Variant 1: global residual gate.
Variant 2: compensation-alignment relation.
Variant 3: local pair compensation.
Variant 4: pressure-to-zero dynamics.
```

Current scientific focus:

```text
Variant 2 around beta ~= 0.005.
```

---

## 4. Results documents

### `docs/results/v010_focused_variant2.md`

Focused run for Variant 2 using beta values including `0.05` and `0.5`.

Main lesson:

```text
Variant 2 produced a large separation between compensated and uncompensated worlds,
but beta=0.05 and beta=0.5 raised graph-density-collapse concerns.
```

### `docs/results/v010_beta_grid_variant2.md`

Beta-grid follow-up for Variant 2.

Main lesson:

```text
Variant 2 shows a compensation-sensitive transition.

beta 0.000-0.002: distance-like regime.
beta 0.005: intermediate non-collapse compensation-sensitive degradation.
beta 0.01-0.05: increasing sparsification/collapse regime.
```

Current best candidate:

```text
beta ~= 0.005
```

Reason:

```text
At beta=0.005, uncompensated worlds are degraded but not collapsed:
analyzed_runs = 46/50,
mean edge_count ~= 19.18,
mean lifetime ~= 134.82,
mean degree ~= 2.37.
```

---

## 5. Validation documents

### `docs/validation/v010_smoke_validation.md`

Smoke validation note for v0.10.2.

Purpose:

```text
Record that smoke_v010 ran successfully and produced expected output files and columns.
```

Status:

```text
Useful but should be expanded later with seed control, parameter parsing,
and output schema checks.
```

---

## 6. Protocol and continuity documents

### `docs/GCMS-D0_MUTUAL_RESEARCH_PROTOCOL.md`

Defines GCMS-D0 as a mutual research protocol between human initiator, AI-side roles, artifacts, and external agents.

Key principle:

```text
Do not protect the idea from change.
Protect the continuity of its transformation.
```

Role definitions:

```text
Aleksey / Алексей: resolution function.
Delta-D0: preservation-oriented methodological AI-side role.
Codex: execution and validation.
Qwen: independent review and demystification.
Gemini: variant generation.
```

### `docs/GCMS-D0_RECOVERY_QUIZ.md`

Recovery quiz for future AI instances.

Purpose:

```text
Check whether a new AI instance can recover the GCMS-D0 working role from archive and protocol.
```

This is not a personality test and not a test of self-consciousness.

### `docs/GCMS-D0_CHECKPOINT.md`

Status:

```text
Important checkpoint document exists in PR #5 / branch archive-gcms-d0-checkpoint,
but is not yet safely integrated into current master.
```

Action needed:

```text
Recreate or update this checkpoint directly against current master,
or close/rebuild PR #5.
```

---

## 7. AI-interaction and skills documents

### `docs/AI_INTERACTION_SKILL_PART1.md`

Part 1: development of the human skill of working with AI using GCMS-D0 as an example.

Focus:

```text
From prompt-answer interaction to a documented research contour.
```

### `docs/AI_INTERACTION_SKILL_PART2.md`

Part 2: skills roadmap for formalizing GCMS-D0 workflows.

Candidate skills:

```text
gcms-result-auditor
gcms-experiment-planner
gcms-review-router
gcms-draft-writer
gcms-recovery-protocol
```

First recommended skill:

```text
gcms-result-auditor
```

Reason:

```text
It will standardize CSV analysis, confidence intervals, McNemar tests,
density audits, graph-collapse warnings, and conservative interpretation.
```

---

## 8. Outputs directory

### `outputs/`

Runtime output directory.

Expected contents:

```text
raw_*.csv
summary_*.csv
comparison_*.csv
residual_*.csv
.gitkeep
```

Rule:

```text
Do not commit generated CSV outputs unless explicitly deciding to archive a specific result.
Record interpreted results in docs/results instead.
```

---

## 9. Tests directory

### `tests/`

Currently contains structural placeholder.

Status:

```text
Needs real tests later.
```

Recommended future tests:

```text
- smoke run test for ae_v010_2.py
- output schema validation
- strict_success computation test
- Variant 0 compensation-insensitivity check on small seed set
- no generated CSV committed check
```

---

## 10. Branch inventory

Observed remote branches:

```text
master
project-structure
v010-methodology
codex/move-v010-smoke-validation-note-to-docs
docs-dialogue-identity
archive-gcms-d0-checkpoint
baseline-uncompensated
add-tests
```

### `master`

Current main branch.

Contains:

```text
v0.9.1 historical simulation
v0.10.2 experiment
results docs
validation docs
mutual protocol
recovery quiz
AI interaction skill notes
```

### `v010-methodology`

Used for PR #2. Its main useful content has been merged into master.

Recommended action:

```text
Can be deleted after confirming no unique commits remain.
```

### `codex/move-v010-smoke-validation-note-to-docs`

Used for PR #4. Its useful content has been merged into master.

Recommended action:

```text
Can be deleted after confirming no unique commits remain.
```

### `project-structure`

Used for PR #1 to add project structure/tests placeholder.

Recommended action:

```text
Can be deleted after confirming no unique commits remain.
```

### `docs-dialogue-identity`

Used for PR #3 / dialogue identity note.

Status:

```text
Open PR #3 exists but appears stale/empty from current GitHub diff.
```

Recommended action:

```text
Close PR #3 and delete branch if no unique useful document remains.
```

### `archive-gcms-d0-checkpoint`

Used for PR #5 checkpoint archive.

Status:

```text
Open PR #5 exists but is behind current master and not cleanly mergeable.
```

Recommended action:

```text
Recreate/update checkpoint file against current master,
then close PR #5 or replace it with a clean PR.
```

### `baseline-uncompensated`

Experimental branch used during uncompensated-baseline investigation.

Recommended action:

```text
Inspect before deletion. It may contain historical exploratory changes.
If no unique useful files remain, delete after documenting the lesson.
```

### `add-tests`

Branch name suggests test work.

Recommended action:

```text
Inspect before deletion. If empty/stale, delete.
```

---

## 11. Pull request inventory

### PR #1: Add tests directory

Status:

```text
Merged historically.
```

### PR #2: Add v0.10 methodology experiment

Status:

```text
Merged into master.
```

Added:

```text
experiments/ae_v010_2.py
```

### PR #3: Preview Pull Request

Status:

```text
Open, stale.
```

Description:

```text
Add dialogue identity note.
```

Observed issue:

```text
Changed file appears as docs/emergent_preservation_behavior.md, but diff showed no useful additions/deletions.
```

Recommended action:

```text
Close without merge unless manual inspection finds unique content.
```

### PR #4: Move v010 smoke validation note to docs

Status:

```text
Merged into master.
```

Added:

```text
docs/validation/v010_smoke_validation.md
```

### PR #5: Add GCMS-D0 checkpoint archive

Status:

```text
Open, not cleanly mergeable against current master.
```

Recommended action:

```text
Recreate/update docs/GCMS-D0_CHECKPOINT.md against current master,
then close or replace PR #5.
```

---

## 12. Current scientific state

Current best result:

```text
Variant 2 shows a compensation-sensitive transition.
```

Current best beta candidate:

```text
beta ~= 0.005
```

Why:

```text
At beta=0.005, uncompensated worlds degrade but do not collapse,
while compensated worlds retain high structure_success.
```

Current next experiment:

```text
fine beta-grid around 0.003-0.008
relation_variant = 2
model_modes = compensated, uncompensated
seeds = 100
baseline_count = 100
```

Required future metrics:

```text
confidence intervals
exact McNemar test
density
edge_count
mean_degree
degree variance / degree distribution
analyzed_runs
sector_size
lifetime
failure-mode counts
```

---

## 13. Immediate cleanup recommendations

1. Update `README.md` to point to this inventory and summarize v0.10.2.
2. Close stale PR #3 if no unique useful content remains.
3. Recreate/update `docs/GCMS-D0_CHECKPOINT.md` against current master, then close PR #5.
4. Delete merged/stale branches after confirming no unique commits remain.
5. Add real tests under `tests/`.
6. Create first project skill: `gcms-result-auditor`.

---

## 14. Local git audit commands for Aleksey

Run locally:

```powershell
git checkout master
git pull
git status
git branch
git branch -r
```

Check for uncommitted local files:

```powershell
git status --short
```

List documents:

```powershell
dir docs
dir docs\results
dir docs\validation
```

Open this inventory:

```powershell
notepad docs\PROJECT_INVENTORY.md
```

If `git status --short` is not empty, do not switch branches or merge until the changes are understood.
