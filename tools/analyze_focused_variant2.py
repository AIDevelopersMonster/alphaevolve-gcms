import math
import pandas as pd
from statistics import NormalDist

RAW = "outputs/raw_v010_focused_variant2.csv"

df = pd.read_csv(RAW)

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return (float("nan"), float("nan"))
    p = k / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = z * math.sqrt((p*(1-p) + z*z/(4*n)) / n) / denom
    return center - half, center + half

def two_prop_ci(k1, n1, k2, n2, z=1.96):
    p1 = k1 / n1
    p2 = k2 / n2
    diff = p1 - p2
    se = math.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    return diff, diff - z*se, diff + z*se

def exact_mcnemar_p(b, c):
    # two-sided exact McNemar using Binomial(n=b+c, p=0.5)
    n = b + c
    if n == 0:
        return float("nan")
    x = min(b, c)
    prob = sum(math.comb(n, i) * (0.5 ** n) for i in range(x + 1))
    return min(1.0, 2 * prob)

def summarize_group(variant, beta):
    sub = df[(df["relation_variant"] == variant) & (df["beta"] == beta)]
    print("\n" + "=" * 72)
    print(f"Variant {variant}, beta={beta}")
    print("=" * 72)

    for mode in ["compensated", "uncompensated"]:
        m = sub[sub["model_mode"] == mode]
        n = len(m)
        k = int(m["structure_success"].sum())
        lo, hi = wilson_ci(k, n)
        print(f"\n{mode}")
        print(f"  attempted: {n}")
        print(f"  structure_success: {k}/{n} = {k/n:.3f}")
        print(f"  Wilson 95% CI: [{lo:.3f}, {hi:.3f}]")
        print(f"  analyzed_runs: {int(m['analyzed'].sum())}/{n}")
        print(f"  mean edge_count: {m['edge_count'].mean():.3f}")
        print(f"  mean density: {m['density'].mean():.6f}")
        print(f"  mean sector_size: {m['sector_size'].mean():.3f}")
        print(f"  mean lifetime: {m['lifetime'].mean():.3f}")
        print(f"  mean dp_valid: {m['dp_valid'].mean():.3f}")
        print(f"  mean p_gnp: {m['p_gnp_empirical'].mean():.6f}")
        print(f"  mean p_dp: {m['p_dp_empirical'].mean():.6f}")

    comp = sub[sub["model_mode"] == "compensated"].set_index("seed")
    uncomp = sub[sub["model_mode"] == "uncompensated"].set_index("seed")
    common = sorted(set(comp.index) & set(uncomp.index))

    b = 0  # comp success, uncomp fail
    c = 0  # comp fail, uncomp success
    both_success = 0
    both_fail = 0

    for seed in common:
        cs = bool(comp.loc[seed, "structure_success"])
        us = bool(uncomp.loc[seed, "structure_success"])
        if cs and us:
            both_success += 1
        elif cs and not us:
            b += 1
        elif not cs and us:
            c += 1
        else:
            both_fail += 1

    kc = int(comp["structure_success"].sum())
    ku = int(uncomp["structure_success"].sum())
    n = len(common)
    diff, dlo, dhi = two_prop_ci(kc, n, ku, n)
    p_mcnemar = exact_mcnemar_p(b, c)

    print("\nPaired comparison")
    print(f"  common seeds: {n}")
    print(f"  both_success: {both_success}")
    print(f"  comp_only: {b}")
    print(f"  uncomp_only: {c}")
    print(f"  both_fail: {both_fail}")
    print(f"  attempted effect: {diff:.3f}")
    print(f"  approx 95% CI for effect: [{dlo:.3f}, {dhi:.3f}]")
    print(f"  exact McNemar p-value: {p_mcnemar:.6g}")

for variant, beta in [(0, 0.0), (2, 0.0), (2, 0.05), (2, 0.5)]:
    summarize_group(variant, beta)