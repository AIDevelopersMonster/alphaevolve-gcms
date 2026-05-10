import math
import pandas as pd

RAW = "outputs/raw_v010_beta_grid_variant2.csv"
df = pd.read_csv(RAW)

def wilson_ci(k, n, z=1.96):
    if n == 0:
        return float("nan"), float("nan")
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
    n = b + c
    if n == 0:
        return float("nan")
    x = min(b, c)
    prob = sum(math.comb(n, i) * (0.5 ** n) for i in range(x + 1))
    return min(1.0, 2 * prob)

def safe_mean_degree(row):
    n = row["sector_size"]
    e = row["edge_count"]
    if n <= 0:
        return 0.0
    return 2.0 * e / n

df["mean_degree_sector"] = df.apply(safe_mean_degree, axis=1)

print("\n=== Beta-grid summary: Variant 2 ===")
for beta in sorted(df["beta"].unique()):
    sub = df[(df["relation_variant"] == 2) & (df["beta"] == beta)]
    print("\n" + "=" * 72)
    print(f"beta = {beta}")
    print("=" * 72)

    rows = []
    for mode in ["compensated", "uncompensated"]:
        m = sub[sub["model_mode"] == mode]
        n = len(m)
        k = int(m["structure_success"].sum())
        lo, hi = wilson_ci(k, n)
        rows.append((mode, n, k, k/n if n else float("nan"), lo, hi))

        print(f"\n{mode}")
        print(f"  attempted: {n}")
        print(f"  structure_success: {k}/{n} = {k/n:.3f}")
        print(f"  Wilson 95% CI for success rate: [{lo:.3f}, {hi:.3f}]")
        print(f"  analyzed_runs: {int(m['analyzed'].sum())}/{n}")
        print(f"  mean edge_count: {m['edge_count'].mean():.3f}")
        print(f"  mean density: {m['density'].mean():.6f}")
        print(f"  mean degree inside sector: {m['mean_degree_sector'].mean():.3f}")
        print(f"  mean sector_size: {m['sector_size'].mean():.3f}")
        print(f"  mean lifetime: {m['lifetime'].mean():.3f}")
        print(f"  mean dp_valid: {m['dp_valid'].mean():.3f}")
        print(f"  mean p_gnp: {m['p_gnp_empirical'].mean():.6f}")
        print(f"  mean p_dp: {m['p_dp_empirical'].mean():.6f}")

    comp = sub[sub["model_mode"] == "compensated"].set_index("seed")
    uncomp = sub[sub["model_mode"] == "uncompensated"].set_index("seed")
    common = sorted(set(comp.index) & set(uncomp.index))

    both_success = comp_only = uncomp_only = both_fail = 0
    diffs = []
    for seed in common:
        cs = bool(comp.loc[seed, "structure_success"])
        us = bool(uncomp.loc[seed, "structure_success"])
        diffs.append(int(cs) - int(us))
        if cs and us:
            both_success += 1
        elif cs and not us:
            comp_only += 1
        elif not cs and us:
            uncomp_only += 1
        else:
            both_fail += 1

    kc = int(comp["structure_success"].sum())
    ku = int(uncomp["structure_success"].sum())
    diff, dlo, dhi = two_prop_ci(kc, len(common), ku, len(common))
    p = exact_mcnemar_p(comp_only, uncomp_only)

    print("\nPaired comparison")
    print(f"  common seeds: {len(common)}")
    print(f"  both_success: {both_success}")
    print(f"  comp_only: {comp_only}")
    print(f"  uncomp_only: {uncomp_only}")
    print(f"  both_fail: {both_fail}")
    print(f"  effect_attempted: {diff:.3f}")
    print(f"  approx 95% CI for effect: [{dlo:.3f}, {dhi:.3f}]")
    print(f"  exact McNemar p-value: {p:.6g}")

print("\n=== Focus table for beta=0.005 ===")
focus = df[(df["relation_variant"] == 2) & (df["beta"] == 0.005)]
cols = [
    "model_mode",
    "analyzed",
    "structure_success",
    "edge_count",
    "density",
    "mean_degree_sector",
    "sector_size",
    "lifetime",
    "dp_valid",
]
print(focus.groupby("model_mode")[cols[1:]].mean().to_string())