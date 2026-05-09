# AlphaEvolve-GCMS

Exploratory simulations of globally compensated multi-index systems and emergent local graph structures.

## Status

This is an exploratory mathematical/computational toy model.  
It is not a physical theory yet.

## Core idea

Global compensation:

\[
\sum_{\mathcal B} \vec I_i \approx 0
\]

Local sector:

\[
\sum_{\mathcal U} \vec I_i = \vec K \neq 0
\]

## Run

```bash
python evolve_v091_chatgpt.py --mode mini
python evolve_v091_chatgpt.py --mode fast
python evolve_v091_chatgpt.py --mode local