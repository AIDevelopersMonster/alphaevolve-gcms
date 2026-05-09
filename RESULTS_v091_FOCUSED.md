# AlphaEvolve-GCMS v0.9.1 Focused Results

## Run configuration

- Model: GCMS strict-zero model
- Script: evolve_v091_chatgpt.py
- Mode: focused / fast-as-focused
- N: 100
- d: 4
- steps: 200
- seeds: 100
- baseline_count: 100
- mutation_rate: 0.10
- alpha: 0.5
- threshold: 0.75

## Main result

- Attempted runs: 100
- Analyzed runs: 93
- Strict success count: 34
- Strict success rate / attempted: 34%
- Strict success rate / analyzed: 36.56%
- Mean lifetime: ~156.4
- Median lifetime: 200
- Max lifetime: 200
- Mean sector size: ~14.27
- Sector size range: 5..31
- Max global compensation error: ~2.37e-14

## Interpretation

The focused v0.9.1 run supports the existence of reproducible long-lived local sectors in a globally compensated multi-index system.

A strict success means that the sector:

1. has valid local size;
2. lives longer than 20 steps;
3. preserves global compensation;
4. passes the G(n,p) clustering baseline;
5. passes the degree-preserving clustering baseline.

This does not prove a physical theory, but it provides a reproducible computational signal for the GCMS toy model.