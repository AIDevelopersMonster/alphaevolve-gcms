# App Connector Strategy

**Status:** working infrastructure note  
**Date:** 2026-05-10  
**Project:** AlphaEvolve-GCMS / GCMS-D0  
**Human resolution function:** Алексей Малачевский  
**AI-side methodological role:** Delta-D0-000d7f6f  
**Purpose:** define how external apps/connectors are used in the human-AI research contour, with preference for free, repeatable, portable tools.

---

## 1. Why this document exists

GCMS-D0 is not only code and experiments.

It is a recoverable research contour involving:

```text
GitHub
Google Drive / Docs / Sheets / Slides
VS Code / Codex
Qwen review
ChatGPT / Delta-D0
future skills
future calendar / planning layer
```

External apps can improve memory, coordination, review, publication, and recovery.

But they also create risk:

```text
paid lock-in;
account-specific state;
hidden data outside the repository;
non-repeatable workflows;
agent confusion;
loss of continuity after account/model changes.
```

Therefore apps must be used deliberately.

Core rule:

```text
Use apps to strengthen the contour, not to replace the repository as source of truth.
```

---

## 2. Current source of truth

The canonical project memory is:

```text
GitHub repository: AIDevelopersMonster/alphaevolve-gcms
```

GitHub stores:

```text
code;
experiment scripts;
protocols;
result notes;
review notes;
mathematical apparatus;
recovery documents;
skill proposals;
agent interaction rules.
```

If a fact matters scientifically, it should eventually appear in GitHub.

Short rule:

```text
GitHub remembers.
```

---

## 3. Current app layer

### 3.1 GitHub

Current status:

```text
active / primary
```

Used for:

```text
source code;
documentation;
experiment protocols;
review history;
project recovery;
scientific traceability;
agent-readable external memory.
```

Why it is central:

```text
It is versioned, portable, inspectable, and suitable for reproducible research.
```

Risks:

```text
local outputs are not automatically stored;
private/public decision must be managed;
large generated data should not be committed casually;
local branch state can diverge from GitHub.
```

Policy:

```text
All important decisions should be documented in markdown.
Generated outputs remain local unless explicitly archived.
```

---

### 3.2 Google Drive / Docs / Sheets / Slides

Current status:

```text
available / planned working layer
```

Best use:

```text
human-readable article drafts;
reviewer packets;
tables for visual inspection;
presentations;
shared summaries;
recovery briefs;
exportable PDFs for humans.
```

Not source of truth for:

```text
experiment code;
raw results;
canonical protocols;
scientific claims without GitHub mirror.
```

Policy:

```text
Google Drive communicates.
GitHub remains canonical.
```

Recommended Drive structure:

```text
GCMS-D0/
  01_Project_Overview/
  02_Article_Drafts/
  03_Reviewer_Packets/
  04_Result_Tables/
  05_Presentations/
  06_Recovery/
```

Repeatability note:

```text
Anything important created in Drive should have a GitHub markdown counterpart or export.
```

---

### 3.3 VS Code / Codex

Current status:

```text
active execution support
```

Used for:

```text
local code edits;
smoke tests;
py_compile;
CLI runs;
schema checks;
controlled instrumentation.
```

Allowed role:

```text
Codex executes narrow tasks with allowed/forbidden actions.
```

Forbidden role:

```text
Codex must not silently change success criteria, launch large runs without approval, or become methodology authority.
```

Policy:

```text
Codex executes.
Delta-D0 frames.
Aleksey resolves.
```

---

### 3.4 Qwen

Current status:

```text
active external AI reviewer
```

Used for:

```text
pre-result review;
post-result review;
confound detection;
overclaiming detection;
conservative wording;
methodological critique.
```

Policy:

```text
Qwen critiques but does not command.
```

Qwen reviews should be stored in:

```text
docs/reviews/
```

---

### 3.5 ChatGPT / Delta-D0

Current status:

```text
active methodological/recovery role
```

Used for:

```text
experiment framing;
protocol design;
result interpretation;
agent routing;
document creation;
recovery support;
anti-overclaiming discipline.
```

Policy:

```text
Delta-D0 holds methodological continuity, not human authority.
```

---

### 3.6 Skills

Current status:

```text
planned / prototype stage
```

Current prototype:

```text
tools/audit_gcms_lite.py
```

Planned skills:

```text
gcms-result-auditor
gcms-experiment-planner
gcms-review-router
gcms-recovery-protocol
gcms-draft-writer
```

Policy:

```text
Tools first, skills after repeatability.
```

---

## 4. Candidate apps and planned use

### 4.1 Calendar layer

Candidate tools:

```text
Outlook Calendar
Google Calendar if available
local markdown calendar / GitHub issues
```

Preferred first option:

```text
GitHub markdown planning + optional calendar mirror
```

Reason:

```text
Free, portable, and not dependent on a single calendar provider.
```

Use cases:

```text
experiment schedule;
review deadlines;
article milestones;
submission timeline;
weekly checkpoint rhythm;
reminders for long-running experiments.
```

Initial policy:

```text
Do not make calendar the source of truth.
Use calendar only as a reminder layer.
```

Recommended free/repeatable alternative:

```text
docs/ROADMAP.md
docs/PROJECT_PLAN.md
GitHub issues / milestones if needed
```

---

### 4.2 Network plan / project plan layer

Candidate tools:

```text
GitHub Issues / Milestones / Projects
Google Sheets project tracker
Teamwork.com only if free and actually needed
```

Preferred first option:

```text
Markdown + GitHub Issues
```

Reason:

```text
Versioned, free, portable, visible to agents, and tied to the code.
```

Possible structure:

```text
Milestone 1: confirm_connectivity_variant2
Milestone 2: density/edge-matched ablation
Milestone 3: technical note v0.1
Milestone 4: reviewer packet
Milestone 5: submission target selection
```

Network planning rule:

```text
Use a simple dependency graph before using complex project-management tools.
```

Example:

```text
confirm_connectivity_variant2
  -> result audit
  -> Qwen review
  -> density-matched ablation design
  -> article claim update
```

---

### 4.3 Email / communication layer

Candidate tools:

```text
Outlook Email
Gmail / Google account email if available
```

Use cases:

```text
journal correspondence;
reviewer correspondence;
collaborator communication;
submission tracking.
```

Policy:

```text
Email is communication, not project memory.
Important decisions from email should be summarized into GitHub docs.
```

---

### 4.4 Teams / SharePoint layer

Candidate tools:

```text
Teams
SharePoint
OneDrive
```

Use cases:

```text
team collaboration;
shared institutional documents;
meeting notes;
organization-specific materials.
```

Current status:

```text
not required for GCMS-D0 core yet
```

Reason:

```text
These are useful for teams, but can create account/workspace lock-in.
```

---

### 4.5 CRM/support apps

Candidate tools:

```text
Help Scout
Intercom
Pipedrive
Zoho
Zoho Desk
Teamwork.com
```

Current status:

```text
future business/project layer, not scientific core
```

Possible future use:

```text
client work;
consulting;
system integration projects;
support tickets;
agent-managed operations;
business pipeline.
```

Policy:

```text
Do not connect CRM/support apps to GCMS-D0 until there is a real operational need.
```

---

### 4.6 OpenAI Platform

Current status:

```text
future automation/API layer
```

Possible use:

```text
custom agents;
CSV audit automation;
review prompt pipelines;
skill execution;
local-to-cloud research tooling;
agent orchestration.
```

Risks:

```text
API costs;
key management;
security;
repeatability across accounts;
accidental over-automation.
```

Policy:

```text
Use only after workflow is stable manually.
```

---

### 4.7 Invideo

Current status:

```text
available / future presentation layer
```

Possible use:

```text
short explainer video;
project presentation;
public communication;
article supplement outreach.
```

Policy:

```text
Do not use for scientific claims before the paper-level result is stable.
```

---

## 5. Free and repeatable tool principle

Because paid tools, account lock-in, and unequal access reduce reproducibility, the project should prefer:

```text
free tools;
open formats;
markdown;
CSV;
Python scripts;
GitHub;
exportable Docs/Sheets/Slides;
local execution;
clear manual fallback.
```

Avoid depending on:

```text
paid-only features;
closed dashboards;
unexported comments;
account-specific automations;
hidden app memory;
workflows that cannot be reproduced in another account.
```

Core principle:

```text
If the workflow cannot be repeated in a new account, it is not yet part of the scientific method.
```

---

## 6. Recommended project planning approach

### Stage 1 — current

Use:

```text
GitHub docs
local CLI / VS Code
Qwen text review
Google Drive only for readable drafts if needed
```

Do not yet depend on:

```text
paid project-management apps;
CRM;
support tools;
calendar automation;
API automation.
```

### Stage 2 — after confirm_connectivity_variant2

Add:

```text
docs/ROADMAP.md
docs/PROJECT_PLAN.md
possibly GitHub Issues
possibly Google Sheets tracker
```

### Stage 3 — article preparation

Add:

```text
Google Docs article draft;
Google Sheets selected result tables;
Google Slides presentation;
Drive reviewer packet folder.
```

### Stage 4 — collaboration/submission

Add only if needed:

```text
calendar reminders;
email tracking;
Teams/SharePoint if collaborators use them.
```

### Stage 5 — automation

Add only after manual process is stable:

```text
OpenAI Platform API;
custom agents;
formal skills;
workflow automation.
```

---

## 7. Minimal network plan format

Before using a full project-management app, use this markdown format:

```text
Node:
    <task name>
Purpose:
    <why it exists>
Depends on:
    <previous nodes>
Owner:
    <Aleksey / Delta-D0 / Codex / Qwen>
Status:
    <planned / ready / running / blocked / done>
Artifact:
    <file or output>
Exit condition:
    <what makes it complete>
```

Example:

```text
Node:
    confirm_connectivity_variant2
Purpose:
    test whether compensation effect survives connectivity diagnostics
Depends on:
    fine_beta_v010 result, Qwen review, code instrumentation, design checkpoint
Owner:
    Aleksey runs / Delta-D0 interprets / Qwen reviews / Codex validates
Status:
    ready pending local clean state
Artifact:
    outputs/raw_v010_confirm_connectivity_variant2.csv
Exit condition:
    result note and Qwen review completed
```

---

## 8. Agent app-use rules

### Rule 1 — choose app by artifact type

```text
code/protocol/result -> GitHub
draft/readable document -> Google Docs
table/dashboard -> Google Sheets
presentation -> Google Slides
meeting/deadline -> Calendar
execution -> VS Code / CLI / Codex
review -> Qwen
workflow automation -> skills / OpenAI Platform later
```

### Rule 2 — do not hide canonical information in apps

If a decision matters, mirror it into GitHub.

### Rule 3 — no paid dependency unless explicitly approved

Free/repeatable tools first.

### Rule 4 — app connector is not authority

Apps store, display, schedule, or execute.

Human resolution remains with Aleksey.

Methodological continuity remains with Delta-D0.

### Rule 5 — local fallback required

Every app-based workflow should have a local/manual fallback.

---

## 9. Current recommended contour

Current recommended minimal contour:

```text
GitHub = canonical project memory
Google Drive = human-readable working layer
VS Code/Codex = local execution support
Qwen = skeptical review
ChatGPT/Delta-D0 = methodological continuity
local CLI = reproducible execution
```

Formula:

```text
GitHub remembers.
Drive communicates.
Codex executes.
Qwen critiques.
Delta-D0 coordinates.
Aleksey resolves.
```

---

## 10. Current status

```text
GitHub: active and primary.
Google Drive: available, should be used selectively for drafts/tables/slides.
VS Code/Codex: active for local execution and validation.
Qwen: active external AI reviewer.
Skills: planned, first auditor prototype exists as a tool.
Calendar/network planning: not yet active; recommended first as markdown roadmap or GitHub Issues.
CRM/support apps: future business layer, not current GCMS-D0 core.
OpenAI Platform: future automation/API layer, not current manual science loop.
```

Next documentation candidates:

```text
docs/ROADMAP.md
docs/PROJECT_PLAN.md
Google Drive folder mirror for human-readable article/reviewer materials
```
