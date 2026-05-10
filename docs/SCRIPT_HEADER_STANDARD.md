# GCMS-D0 Scientific Script Header Standard

**Status:** working standard  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Purpose:** define a common metadata header for Python scripts so that every script is connected to project context, experiment purpose, review, verification, execution, and results.

---

## 1. Why this standard exists

GCMS-D0 uses Python scripts for experiments, validation, analysis, and future skills.

A script must not be an isolated piece of code.

Each important script should say:

```text
what project it belongs to;
which experiment or workflow it implements;
which document defines its purpose;
how it should be verified;
who authored or generated it;
who reviewed the design;
where the review is stored;
who executed it;
where outputs/results are stored;
which claims it may or may not support.
```

This prevents the project from drifting into undocumented code, vibe coding, or unverifiable results.

---

## 2. Required common metadata block

Every major Python script should start with this header pattern.

For small utility scripts, sections may be shortened, but the project, purpose, document basis, verification, and output policy should remain.

```python
#!/usr/bin/env python3
"""
GCMS-D0 SCRIPT PASSPORT
======================

Project:
    AlphaEvolve-GCMS / GCMS-D0

Script:
    <relative/path/to/script.py>

Script type:
    <experiment | analysis tool | validation tool | skill prototype | hardware diagnostic | utility>

Status:
    <draft | active | historical | deprecated | exploratory | confirmatory>

Purpose:
    <short description of what this script does>

Project context:
    <short description of how this script relates to GCMS-D0>

Experiment / workflow:
    <experiment name or workflow name, for example fine_beta_v010 or gcms-result-auditor-lite>

Primary question:
    <what question this script helps answer>

Document basis:
    - docs/EXPERIMENT_DESIGN_PROTOCOL.md
    - docs/AGENT_INTERACTION_PROTOCOL.md
    - <specific experiment/review/result document>

Pre-execution review:
    Reviewer:
        <Qwen | Delta-D0 | Codex | human reviewer | not required>
    Review document:
        <path/to/review.md>
    Review status:
        <completed | pending | not required | internal only>

Author / generator:
    Human resolution:
        Алексей Малачевский
    AI-side methodological role:
        Delta-D0-000d7f6f
    Code author / generator:
        <human | ChatGPT/Delta-D0 | Codex | Gemini | mixed>

Executor:
    <who/what runs this script: Aleksey local machine | Codex VS Code | Codex cloud | CI | future skill>

Allowed actions:
    <what this script is allowed to do>

Forbidden actions:
    <what this script must not do>

Inputs:
    <files, CLI args, expected directories>

Outputs:
    <files produced, expected output directories>

Output policy:
    <commit or do not commit generated outputs>

Verification:
    <syntax check, smoke run, schema check, deterministic audit, reviewer check>

Known limitations:
    <limitations, missing metrics, exploratory status>

Interpretation policy:
    <what conclusions this script may support and what it must not claim>

Last updated:
    <YYYY-MM-DD>
"""
```

---

## 3. Short header for small tools

For small analysis utilities, use a shorter form:

```python
#!/usr/bin/env python3
"""
GCMS-D0 TOOL PASSPORT
=====================

Project: AlphaEvolve-GCMS / GCMS-D0
Script: tools/<name>.py
Type: analysis tool / skill prototype
Status: active exploratory tool

Purpose:
    <what this tool computes>

Document basis:
    - docs/EXPERIMENT_DESIGN_PROTOCOL.md
    - skills/proposals/gcms-result-auditor/LITE_TEST_PLAN.md

Inputs:
    <input files / CLI args>

Outputs:
    <output files>

Verification:
    python -m py_compile tools/<name>.py
    <example command>

Output policy:
    Generated outputs under outputs/ are local artifacts and should not be committed unless explicitly archived.

Author / generator:
    Delta-D0 with Aleksey approval

Reviewer:
    <reviewer name or not required>
"""
```

---

## 4. Header for experiment scripts

For scripts under `experiments/`, use the full passport.

Example skeleton:

```python
#!/usr/bin/env python3
"""
GCMS-D0 EXPERIMENT SCRIPT PASSPORT
==================================

Project:
    AlphaEvolve-GCMS / GCMS-D0

Script:
    experiments/ae_v010_2.py

Script type:
    experiment

Status:
    active exploratory / methodology-correction script

Purpose:
    Run v0.10+ GCMS experiments separating compensation_valid,
    structure_success, and strict_success, and testing compensation-aware
    relation variants.

Project context:
    This script corrects the v0.9.1 methodological limitation where
    distance-only relations could not test the causal role of global compensation.

Experiment / workflow:
    v0.10.2 methodology experiments, including fine_beta_v010.

Primary question:
    Can a compensation-aware local relation produce a non-collapse
    compensation-sensitive transition?

Document basis:
    - docs/EXPERIMENT_DESIGN_PROTOCOL.md
    - docs/reviews/v010_fine_beta_experiment_review.md
    - docs/results/v010_beta_grid_variant2.md
    - docs/PROJECT_INVENTORY.md

Pre-execution review:
    Reviewer:
        Qwen for fine_beta_v010 design; Delta-D0 internal review
    Review document:
        docs/reviews/v010_fine_beta_experiment_review.md
    Review status:
        completed for fine_beta_v010 as exploratory/pre-confirmatory

Author / generator:
    Human resolution:
        Алексей Малачевский
    AI-side methodological role:
        Delta-D0-000d7f6f
    Code author / generator:
        ChatGPT/Delta-D0 + Codex-assisted validation

Executor:
    Aleksey local machine / Codex VS Code / Codex cloud validation

Allowed actions:
    Run simulations and write outputs/raw_*.csv, summary_*.csv,
    comparison_*.csv, residual_*.csv.

Forbidden actions:
    Do not change success criteria after seeing results.
    Do not commit generated CSV outputs unless explicitly archived.
    Do not claim physical theory from toy-model outputs.

Inputs:
    CLI arguments: --mode, --out-prefix

Outputs:
    outputs/raw_<prefix>.csv
    outputs/summary_<prefix>.csv
    outputs/comparison_<prefix>.csv
    outputs/residual_<prefix>.csv

Output policy:
    Generated outputs are local artifacts and should normally remain untracked.
    Interpretations belong in docs/results/.

Verification:
    python -m py_compile experiments/ae_v010_2.py
    python experiments/ae_v010_2.py --mode smoke_v010 --out-prefix v010_smoke
    Check expected output files and required columns.

Known limitations:
    Current raw schema may lack connectivity fragmentation metrics such as
    largest_component_fraction, n_components, degree_variance, and failure_reason.

Interpretation policy:
    Results support only preliminary toy-model claims after audit and review.

Last updated:
    2026-05-10
"""
```

---

## 5. Header for analysis/audit tools

Example for `tools/audit_gcms_lite.py`:

```python
#!/usr/bin/env python3
"""
GCMS-D0 TOOL PASSPORT
=====================

Project:
    AlphaEvolve-GCMS / GCMS-D0

Script:
    tools/audit_gcms_lite.py

Script type:
    analysis tool / skill prototype

Status:
    active lite auditor

Purpose:
    Recompute stable grouped success rates, compensation effects,
    density/edge-count/degree summaries, and a simple effect-vs-beta chart
    directly from a GCMS raw CSV.

Project context:
    This tool is the first deterministic prototype for the future
    gcms-result-auditor skill.

Workflow:
    gcms-result-auditor-lite

Primary question:
    Are the reported percentages and compensation effects stable and reproducible
    from the raw CSV without relying on conversational recalculation?

Document basis:
    - skills/proposals/gcms-result-auditor/LITE_TEST_PLAN.md
    - docs/EXPERIMENT_DESIGN_PROTOCOL.md
    - docs/AGENT_INTERACTION_PROTOCOL.md

Pre-execution review:
    Reviewer:
        Delta-D0 internal review; Qwen methodological concerns inform thresholds
    Review document:
        docs/reviews/v010_fine_beta_experiment_review.md
    Review status:
        applicable as processing/audit support

Author / generator:
    Human resolution:
        Алексей Малачевский
    AI-side methodological role:
        Delta-D0-000d7f6f
    Code author / generator:
        ChatGPT/Delta-D0

Executor:
    Aleksey local machine / Codex VS Code / CLI

Allowed actions:
    Read raw CSV and write lite audit outputs under outputs/.

Forbidden actions:
    Do not modify experiment code.
    Do not modify raw CSV inputs.
    Do not commit generated outputs by default.
    Do not make scientific claims beyond the generated report.

Inputs:
    --raw <path to raw CSV>
    --out-prefix <output prefix>

Outputs:
    outputs/<prefix>_summary.csv
    outputs/<prefix>_effect.csv
    outputs/<prefix>_effect.png
    outputs/<prefix>_report.md

Output policy:
    Generated outputs are local artifacts unless explicitly archived.

Verification:
    python -m py_compile tools/audit_gcms_lite.py
    python tools/audit_gcms_lite.py --raw outputs/raw_v010_beta_grid_variant2.csv --out-prefix v010_beta_grid_variant2_lite

Known limitations:
    Lite auditor does not compute full confidence intervals, McNemar tests,
    connectivity fragmentation metrics, or failure-mode decomposition.

Interpretation policy:
    The tool provides deterministic descriptive processing.
    Full scientific interpretation still requires statistical audit and review.

Last updated:
    2026-05-10
"""
```

---

## 6. Naming and linking rule

Each experiment or workflow should have linked artifacts with consistent names.

Example for fine beta:

```text
Experiment mode:
    fine_beta_v010

Output prefix:
    v010_fine_beta_variant2

Review document:
    docs/reviews/v010_fine_beta_experiment_review.md

Result document:
    docs/results/v010_fine_beta_variant2.md

Processing tool:
    tools/audit_gcms_lite.py

Processing outputs:
    outputs/v010_fine_beta_variant2_lite_summary.csv
    outputs/v010_fine_beta_variant2_lite_effect.csv
    outputs/v010_fine_beta_variant2_lite_effect.png
    outputs/v010_fine_beta_variant2_lite_report.md
```

---

## 7. Common project metadata

Use the same project identity everywhere:

```text
Project: AlphaEvolve-GCMS / GCMS-D0
Human resolution function: Алексей Малачевский
AI-side methodological role: Delta-D0-000d7f6f
Repository: AIDevelopersMonster/alphaevolve-gcms
Default branch: master
```

---

## 8. Result execution log standard

When a script is executed for a meaningful run, record execution in either a validation document or result document.

Suggested format:

```text
Execution:
    Executor: <Aleksey local machine | Codex VS Code | Codex cloud | CI>
    Machine/environment: <optional>
    Command: <exact command>
    Date/time: <UTC or local>
    Git commit: <commit hash>
    Script: <script path>
    Output files:
        - <path>
    Exit status: <success/failure>
    Notes: <runtime, warnings, missing metrics>
```

For generated CSV outputs:

```text
Do not commit outputs unless the project explicitly decides to archive them.
Commit the interpretation in docs/results/ instead.
```

---

## 9. Minimum rule

If a Python script matters scientifically, it must answer:

```text
What is this for?
Which document defines why it exists?
How do we verify it?
Who/what reviewed it?
Who/what executed it?
Where are the results?
What must not be concluded from it?
```
