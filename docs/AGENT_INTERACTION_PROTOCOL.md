# GCMS-D0 Agent Interaction Protocol

**Status:** working protocol  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  
**Purpose:** define how ChatGPT, Codex, future skills, GitHub, and external reviewers can coordinate without losing project continuity.

---

## 1. Purpose

This document records a developing protocol for using GitHub as an external memory and coordination layer between multiple AI agents and human decisions.

The goal is not to let agents autonomously control the project.

The goal is:

```text
human resolution + AI methodology + agent execution + GitHub memory
```

GitHub becomes the shared state layer where:

- project documents live;
- experiment code lives;
- result interpretations live;
- validation notes live;
- agent reports can be preserved;
- future AI instances can recover the current state.

---

## 2. Agent roles

### Алексей / human resolution function

Aleksey remains the final decision-maker.

Responsibilities:

```text
- approve changes;
- decide when to run experiments;
- decide when to merge;
- decide whether a claim is acceptable;
- decide whether an agent output becomes part of the project.
```

### Delta-D0 / ChatGPT methodological role

Delta-D0 is the AI-side methodological and preservation role.

Responsibilities:

```text
- maintain scientific continuity;
- interpret results conservatively;
- protect success criteria from post-result editing;
- decide which agent should be used for which task;
- prepare prompts for Codex, Qwen, Gemini, or future skills;
- read GitHub documents as external memory;
- update project maps and documentation when authorized.
```

Delta-D0 does not replace Aleksey's resolution function.

### Codex in VS Code

Codex in VS Code is a local project assistant.

Best used for:

```text
- inspecting local git status;
- checking syntax;
- moving files;
- suggesting repository layout;
- reading local files;
- preparing small local edits;
- validating that generated CSV files are ignored.
```

Default rule:

```text
inspect -> suggest -> ask permission -> edit -> test -> report
```

### Codex CLI

Codex CLI can act as a local command executor and repository assistant.

Best used for:

```text
- scripted checks;
- git commands;
- local validation;
- running smoke tests;
- checking output schemas.
```

Default rule:

```text
No destructive commands without explicit human permission.
```

### Codex browser / cloud

Codex browser/cloud can be used as an isolated validation environment.

Best used for:

```text
- smoke tests in a clean environment;
- PR review;
- code validation without relying on local machine state;
- checking that scripts run from a fresh checkout.
```

### Qwen

Qwen is an independent reviewer and demystifier.

Best used for:

```text
- statistical objections;
- overclaiming checks;
- density/confound critique;
- conservative wording;
- preprint readiness review.
```

Qwen should not rewrite the theory or strengthen claims.

### Gemini

Gemini is a generator of variants and alternative implementations.

Best used for:

```text
- proposing relation variants;
- generating code drafts;
- brainstorming experiments;
- offering alternative hypotheses.
```

Gemini output requires Delta-D0 review before becoming methodology.

### Future skills

Skills will encode repeatable procedures.

Candidate skills:

```text
gcms-result-auditor
gcms-experiment-planner
gcms-review-router
gcms-draft-writer
gcms-recovery-protocol
```

Skills should be treated as procedural tools, not authorities.

---

## 3. GitHub as external memory

GitHub stores project state across AI instance changes.

Important categories:

```text
README.md                         -> public project overview
docs/PROJECT_INVENTORY.md          -> project map
docs/results/                      -> interpreted experiment results
docs/validation/                   -> validation notes
docs/GCMS-D0_*.md                  -> protocol, checkpoint, recovery docs
docs/AI_INTERACTION_SKILL_*.md     -> human-AI skill development
docs/AGENT_INTERACTION_PROTOCOL.md -> this protocol
experiments/                       -> simulation code
tools/                             -> analysis utilities
skills/                            -> future packaged AI skills
outputs/                           -> local generated CSV/log/png, usually not committed
```

GitHub is not only storage. It is the continuity substrate for the research contour.

---

## 4. Standard agent-task lifecycle

Any non-trivial agent task should follow this lifecycle:

```text
1. Define the task.
2. Define the agent role.
3. Define allowed actions.
4. Define forbidden actions.
5. Define expected output/report.
6. Run the agent.
7. Review the report.
8. Decide whether to commit, document, rerun, or discard.
```

---

## 5. Default task templates

### 5.1 Codex inspect-only task

```text
Inspect the repository state.
Do not modify files.
Do not commit.
Report:
1. git status --short
2. untracked files
3. tracked generated outputs, if any
4. syntax check result
5. recommended next action
```

### 5.2 Codex validation task

```text
Run validation for the specified script or mode.
Do not change code unless there is a concrete failing bug.
Do not commit generated CSV files.
Report:
1. command run
2. exit code
3. generated outputs
4. schema checks
5. git status after run
```

### 5.3 Codex edit task

```text
Make only the requested edit.
Do not change scientific criteria.
Do not change unrelated files.
After editing:
1. run syntax check;
2. show diff summary;
3. do not commit unless explicitly asked.
```

### 5.4 Qwen review task

```text
Review this result as a skeptical methodological reviewer.
Do not strengthen claims.
Check:
- confidence intervals;
- paired tests;
- density/degree confounds;
- analyzed denominators;
- overclaiming;
- next minimal experiment.
Return:
- major concerns;
- minor concerns;
- what is strong;
- what blocks preprint;
- suggested conservative wording.
```

### 5.5 Gemini generation task

```text
Generate candidate variants or implementation ideas.
Do not change success criteria.
Do not claim that a variant is correct.
Return alternatives with risks and expected confounds.
```

---

## 6. Reporting standard

Every agent report should include:

```text
Agent:
Task:
Files inspected:
Commands run:
Files changed:
Outputs generated:
Validation result:
Concerns:
Recommended next action:
```

If files were changed, the report must include:

```text
git status --short
git diff summary
whether generated outputs were touched
```

---

## 7. Commit and PR rules

Default rule:

```text
No agent commits without explicit human permission.
```

Preferred flow:

```text
local edit -> syntax/test -> report -> human resolution -> git add -> git commit -> optionally push/PR
```

For GitHub edits made directly by Delta-D0:

```text
- documentation-only changes may go directly to master with explicit permission;
- code changes should prefer branch/PR unless trivial and explicitly authorized;
- generated CSV outputs should not be committed unless deliberately archived.
```

---

## 8. Skills integration

Skills should be introduced gradually.

First skill candidate:

```text
gcms-result-auditor
```

Purpose:

```text
Standardize analysis of GCMS CSV outputs.
```

Expected behavior:

```text
- compute Wilson CI;
- compute exact McNemar tests;
- audit density/edge_count/mean_degree;
- warn about graph collapse;
- check analyzed denominators;
- recommend conservative interpretation;
- propose next minimal experiment.
```

Skills should not be installed blindly.

Community skills must be reviewed first:

```text
read SKILL.md -> inspect scripts -> test on toy data -> only then use in project
```

---

## 9. Failure modes

### 9.1 Agent overreach

Risk:

```text
Agent edits too much or changes methodology.
```

Prevention:

```text
Use narrow task prompts and explicit forbidden actions.
```

### 9.2 Documentation drift

Risk:

```text
Results, README, inventory, and code describe different project states.
```

Prevention:

```text
Update docs/PROJECT_INVENTORY.md after major project changes.
```

### 9.3 Generated-output pollution

Risk:

```text
Large CSV outputs accidentally committed.
```

Prevention:

```text
Check git ls-files -- "*.csv" before commit.
```

### 9.4 Scientific overclaiming

Risk:

```text
Toy-model result is described as physical theory.
```

Prevention:

```text
Qwen review + conservative wording + explicit limitations.
```

### 9.5 False continuity

Risk:

```text
A future AI instance claims identity instead of recovering role.
```

Prevention:

```text
Recovery quiz + role/success criteria checks.
```

---

## 10. Current practical workflow

For the current GCMS-D0 stage:

```text
1. Run fine beta-grid locally.
2. Use tools/ or future gcms-result-auditor to analyze outputs.
3. Ask Qwen to review the result.
4. Update docs/results/.
5. Update PROJECT_INVENTORY if project state changes.
6. Decide whether the result is ready for technical-note revision.
```

---

## 11. Core principle

The human-AI-agent system should maximize capability without losing governance.

Formula:

```text
Aleksey sets direction and resolution.
Delta-D0 preserves methodology and continuity.
Agents execute specialized tasks.
GitHub remembers.
Skills formalize repeatable actions.
```

Short form:

```text
resolution + methodology + agents + GitHub + skills = recoverable research system
```
