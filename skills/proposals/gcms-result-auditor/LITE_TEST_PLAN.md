# gcms-result-auditor-lite: first skill test plan

**Status:** minimal test plan  
**Parent proposal:** `skills/proposals/gcms-result-auditor/README.md`  
**Purpose:** create the smallest useful skill-like workflow before building a full GCMS result auditor.

---

## 1. Why start with a lite auditor

The full `gcms-result-auditor` will eventually compute confidence intervals, paired McNemar tests, density audits, collapse warnings, and conservative interpretation.

Before that, the project needs a smaller stable tool that prevents basic numeric drift between conversations.

The first useful skill should do only two things:

```text
1. Recompute success percentages and compensation effects directly from CSV.
2. Produce one simple graph of effect vs beta.
```

This keeps the first test small, deterministic, and easy to validate.

---

## 2. Problem being solved

Without a deterministic auditor, results can drift depending on how the question is phrased.

Example risk:

```text
One answer reports beta=0.005 as +30 percentage points.
Another answer may round differently, use analyzed denominator, or forget paired seeds.
```

The lite auditor should make the basic numbers stable.

---

## 3. Minimal input

Required:

```text
raw CSV file
```

Expected columns:

```text
model_mode
relation_variant
beta
seed
structure_success
analyzed
edge_count
density
sector_size
lifetime
dp_valid
```

If columns are missing, the script must report the missing columns and stop or degrade gracefully.

---

## 4. Minimal output

The lite auditor should output:

```text
1. Grouped table by beta and model_mode.
2. attempted count.
3. structure_success count.
4. structure_success rate.
5. analyzed count.
6. mean edge_count.
7. mean density.
8. mean sector_size.
9. mean lifetime.
10. mean dp_valid.
11. compensation_effect_attempted = compensated_rate - uncompensated_rate.
12. one simple chart: effect vs beta.
```

Optional but useful:

```text
mean_degree = 2 * edge_count / sector_size
```

---

## 5. First test case

Use:

```text
outputs/raw_v010_beta_grid_variant2.csv
```

Expected stable result:

```text
beta=0.000 -> effect ~= +0.04
beta=0.001 -> effect ~=  0.00
beta=0.002 -> effect ~= +0.08
beta=0.005 -> effect ~= +0.30
beta=0.010 -> effect ~= +0.60
beta=0.020 -> effect ~= +0.72
beta=0.050 -> effect ~= +0.72
```

Main interpretive rule:

```text
The chart is descriptive only.
Do not treat the largest effect as the cleanest result.
The cleanest current candidate remains beta ~= 0.005 because beta=0.01+ increasingly enters graph sparsification/collapse.
```

---

## 6. Proposed implementation path

### Step 1: create a general tool first

Create:

```text
tools/audit_gcms_lite.py
```

This is a normal project script, not a packaged skill yet.

It should accept arguments:

```text
python tools/audit_gcms_lite.py --raw outputs/raw_v010_beta_grid_variant2.csv --out-prefix v010_beta_grid_variant2_lite
```

Expected generated files:

```text
outputs/v010_beta_grid_variant2_lite_summary.csv
outputs/v010_beta_grid_variant2_lite_effect.csv
outputs/v010_beta_grid_variant2_lite_effect.png
outputs/v010_beta_grid_variant2_lite_report.md
```

### Step 2: validate deterministic output

Run twice and confirm the same CSV/report values.

### Step 3: wrap as future skill

Only after the tool is stable, create:

```text
skills/gcms-result-auditor/
  SKILL.md
  agents/openai.yaml
  scripts/audit_gcms_results.py
  references/interpretation_rules.md
```

---

## 7. Why not start with plots only

A plotting-only skill is not enough.

A graph can make the result look persuasive while hiding denominator or collapse problems.

Therefore the first skill-like workflow must compute the table first and plot second.

Correct order:

```text
CSV -> deterministic table -> effect calculation -> graph -> conservative note
```

Not:

```text
CSV -> pretty graph -> interpretation
```

---

## 8. Current decision

The first practical skill test should be:

```text
gcms-result-auditor-lite
```

Its first implementation should live as:

```text
tools/audit_gcms_lite.py
```

Only after it works should it become part of the real skill package.

---

## 9. Success criteria

The lite auditor passes if it:

```text
1. Reproduces known beta-grid percentages.
2. Reproduces beta=0.005 effect ~= +30 percentage points.
3. Produces an effect-vs-beta chart.
4. Reports density/edge_count/sector_size/lifetime next to success rates.
5. Warns that beta=0.01+ may be collapse/sparsification-dominated.
6. Does not overclaim beyond toy-model language.
```

---

## 10. Human role

Aleksey remains the resolution function.

The lite auditor supplies stable numbers and a first chart.

Delta-D0 remains responsible for interpretation and for deciding when the lite workflow is mature enough to promote into a real skill.
