# Public Archive Publication Plan

**Status:** preparation checklist  
**Date:** 2026-05-17  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Purpose:** prepare the repository for publication as a curated human-AI research archive.

---

## 1. Publication posture

This repository should be published as two things at once:

```text
1. A computational toy-model research archive.
2. A documented human-AI research workflow archive.
```

It should not be presented as:

```text
a physical theory;
a proof of a causal compensation mechanism;
a density-independent proof;
a universal topology-threshold claim;
a claim about spacetime, gravity, photons, or physical constants;
a claim that an AI instance has persistent identity or consciousness.
```

The current v0.1 scientific posture is:

```text
confound-isolation / topology-threshold diagnostic in a computational toy model
```

The current process posture is:

```text
human resolution + AI methodology + agent execution/review + GitHub external memory
```

---

## 2. What should be public

Recommended public materials:

```text
README.md
LICENSE
CITATION.cff or citation note
requirements.txt
experiments/
tools/
tests/
docs/papers/
docs/results/
docs/reviews/
docs/validation/
docs/experiments/
docs/GCMS-D0_MUTUAL_RESEARCH_PROTOCOL.md
docs/AGENT_INTERACTION_PROTOCOL.md
docs/SYMBIOTIC_COHERENCE_PROTOCOL.md
docs/GCMS-D0_RECOVERY_QUIZ.md
docs/PROJECT_INVENTORY.md
docs/ARCHIVE_PUBLICATION_PLAN.md
docs/PUBLIC_ARCHIVE_INDEX.md
```

Reason:

```text
These files show the scientific result, the confound-isolation sequence,
the review trail, and the recoverable human-AI research process.
```

---

## 3. What should not be public without manual review

Before making the repository public, manually inspect and remove or rewrite:

```text
private links or share links;
API keys, tokens, local paths, machine-specific logs;
raw dialogue dumps not edited into a document;
files that imply AI identity continuity rather than role recovery;
intermediate notes that make physical, causal, or universal claims;
generated CSV outputs unless they are intentionally archived and documented;
large binary artifacts or temporary files;
branches that contain stale or duplicate drafts.
```

Raw chat history should remain private unless converted into a curated process appendix.

---

## 4. Core files for first public release

### Scientific note

```text
docs/papers/connectivity_entanglement_confound_isolation_v0_1.md
```

Role:

```text
Main v0.1 technical note.
```

### Release summary

```text
docs/releases/connectivity_entanglement_v0_1_release_summary.md
```

Role:

```text
Short entry point for the v0.1 release.
```

### Human-AI research protocol

```text
docs/AGENT_INTERACTION_PROTOCOL.md
docs/SYMBIOTIC_COHERENCE_PROTOCOL.md
docs/GCMS-D0_MUTUAL_RESEARCH_PROTOCOL.md
```

Role:

```text
Describes the team/process layer without claiming AI identity or autonomy.
```

### Review trail

```text
docs/reviews/
```

Role:

```text
Shows how overclaiming was blocked and how the result was reframed.
```

---

## 5. Branch cleanup recommendation

The following branches were previously documented as candidates for cleanup:

```text
v010-methodology
codex/move-v010-smoke-validation-note-to-docs
project-structure
docs-dialogue-identity
archive-gcms-d0-checkpoint
baseline-uncompensated
add-tests
```

Known current status from repository inspection:

```text
master                      -> keep
archive/public-v0.1-prep    -> temporary preparation branch, keep until merged
v010-methodology            -> likely safe to delete after confirming merged
codex/move-v010-smoke-validation-note-to-docs -> likely safe to delete after confirming merged
docs-dialogue-identity      -> PR #3 is closed and unmerged; delete if no useful unique content remains
archive-gcms-d0-checkpoint  -> PR #5 is open but not mergeable; replace with cleaned checkpoint on this branch, then close/delete old branch
```

Destructive branch deletion should be done manually by the repository owner after this PR is reviewed.

Recommended local commands after merging the cleanup PR:

```bash
git fetch --all --prune
git branch -r
```

Then delete only confirmed stale remote branches from GitHub UI or CLI.

---

## 6. Pull request cleanup recommendation

```text
PR #3: already closed, unmerged. No action except optional branch deletion.
PR #5: open, not mergeable. Close after the cleaned checkpoint/index files are merged from archive/public-v0.1-prep.
```

Recommended closing comment for PR #5:

```text
Superseded by the curated public archive preparation branch. The checkpoint content was replaced by a cleaner public archive index and publication plan.
```

---

## 7. Minimum release checklist

Before switching repository visibility to public:

```text
[ ] README has explicit toy-model / non-physical claim boundary.
[ ] README links to the v0.1 technical note.
[ ] README links to the human-AI research process documents.
[ ] PUBLIC_ARCHIVE_INDEX exists.
[ ] ARCHIVE_PUBLICATION_PLAN exists.
[ ] Old non-mergeable PR #5 is closed or marked superseded.
[ ] Stale merged branches are deleted or left intentionally.
[ ] No secrets or private machine paths are present.
[ ] No raw chat dumps are public.
[ ] No file claims AI consciousness or persistent identity.
[ ] Generated outputs are either ignored or intentionally documented.
[ ] License/citation posture is decided.
```

---

## 8. Recommended publication text

```text
This repository publishes a computational toy-model research archive and a documented human-AI research workflow. The v0.1 result is a conservative confound-isolation / topology-threshold diagnostic. It reports how an initially positive compensated-mode signal was weakened after topology controls and reframed as empirical compensation-connectivity coupling in a toy model. No physical, causal, universal, or AI-identity claim is made.
```
