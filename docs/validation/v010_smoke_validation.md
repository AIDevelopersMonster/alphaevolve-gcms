# v0.10 smoke validation

Smoke test run on 2026-05-09 (UTC).

## Command

```bash
python experiments/ae_v010_2.py --mode smoke_v010 --out-prefix v010_smoke
```

## Result

Success, exit code 0.

## Verified outputs

- `outputs/raw_v010_smoke.csv`
- `outputs/summary_v010_smoke.csv`
- `outputs/comparison_v010_smoke.csv`
- `outputs/residual_v010_smoke.csv`

## Verified comparison columns

- `relation_variant`
- `beta`
- `lambda_val`
- `compensation_effect_attempted`
- `compensation_effect_analyzed`

## Observation

`relation_variant=0` rows are present in the comparison output, and compensation effect metrics are `0.0` in the smoke run.

This confirms that Variant 0 acts as the translation-invariant control for v0.10.2.