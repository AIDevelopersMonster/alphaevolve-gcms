"""
Postprocess connectivity audit CI pairing.

Reads existing outputs from connectivity audit.
Computes paired seed summary, Wilson CIs, bootstrap CI for non_bridge_edge_count >= 19.

Usage:
    python tools/postprocess_connectivity_audit_ci_pairing.py --input-prefix smoke_connectivity_entanglement_audit_variant2 --output-prefix postprocess_ci_pairing

Outputs:
    outputs/paired_seed_summary_<output_prefix>.csv
    outputs/wilson_cis_<output_prefix>.csv
    outputs/bootstrap_ci_non_bridge_ge19_<output_prefix>.csv
"""

import argparse
import os
from typing import Dict, Any, List
import numpy as np
import pandas as pd
from scipy import stats


def wilson_ci(p: float, n: int, confidence: float = 0.95) -> tuple[float, float]:
    """Compute Wilson confidence interval for proportion."""
    if n == 0:
        return (0.0, 1.0)
    z = stats.norm.ppf((1 + confidence) / 2)
    denominator = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denominator
    spread = z * np.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denominator
    return (center - spread, center + spread)


def bootstrap_ci(data: np.ndarray, statistic: callable, n_boot: int = 1000, confidence: float = 0.95) -> tuple[float, float]:
    """Compute bootstrap confidence interval."""
    boot_stats = []
    n = len(data)
    for _ in range(n_boot):
        sample = np.random.choice(data, size=n, replace=True)
        boot_stats.append(statistic(sample))
    boot_stats = np.array(boot_stats)
    lower = np.percentile(boot_stats, (1 - confidence) / 2 * 100)
    upper = np.percentile(boot_stats, (1 + confidence) / 2 * 100)
    return (float(lower), float(upper))


def main() -> None:
    parser = argparse.ArgumentParser(description="Postprocess connectivity audit CI pairing.")
    parser.add_argument("--input-prefix", required=True, help="Input prefix for existing outputs")
    parser.add_argument("--output-prefix", required=True, help="Output prefix")
    args = parser.parse_args()

    # Read inputs
    raw_path = f"outputs/raw_{args.input_prefix}.csv"
    per_seed_path = f"outputs/per_seed_{args.input_prefix}.csv"

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw file not found: {raw_path}")
    if not os.path.exists(per_seed_path):
        raise FileNotFoundError(f"Per-seed file not found: {per_seed_path}")

    raw_df = pd.read_csv(raw_path)
    per_seed_df = pd.read_csv(per_seed_path)

    os.makedirs("outputs", exist_ok=True)

    def summarize_delta(column: str) -> Dict[str, Any]:
        values = per_seed_df[column].dropna().to_numpy(dtype=float)
        n_pairs = int(len(values))
        positive_delta_count = int(np.sum(values > 0))
        negative_delta_count = int(np.sum(values < 0))
        zero_delta_count = int(np.sum(values == 0))
        return {
            "metric": column,
            "n_pairs": n_pairs,
            "mean_delta": float(np.mean(values)) if n_pairs > 0 else np.nan,
            "median_delta": float(np.median(values)) if n_pairs > 0 else np.nan,
            "std_delta": float(np.std(values, ddof=1)) if n_pairs > 1 else np.nan,
            "q25_delta": float(np.percentile(values, 25)) if n_pairs > 0 else np.nan,
            "q75_delta": float(np.percentile(values, 75)) if n_pairs > 0 else np.nan,
            "min_delta": float(np.min(values)) if n_pairs > 0 else np.nan,
            "max_delta": float(np.max(values)) if n_pairs > 0 else np.nan,
            "positive_delta_count": positive_delta_count,
            "negative_delta_count": negative_delta_count,
            "zero_delta_count": zero_delta_count,
            "positive_delta_fraction": float(positive_delta_count / n_pairs) if n_pairs > 0 else np.nan,
            "negative_delta_fraction": float(negative_delta_count / n_pairs) if n_pairs > 0 else np.nan,
            "zero_delta_fraction": float(zero_delta_count / n_pairs) if n_pairs > 0 else np.nan,
            "sign_test_positive_rate": float(positive_delta_count / n_pairs) if n_pairs > 0 else np.nan,
        }

    paired_rows: List[Dict[str, Any]] = []
    delta_columns = [
        "delta_edge_count",
        "delta_bridge_fraction",
        "delta_non_bridge_edge_count",
        "delta_cycle_rank",
        "delta_largest_component_fraction",
        "delta_structure_success",
        "delta_failed_p_gnp",
        "delta_failed_p_dp",
        "delta_density",
        "delta_bridge_count",
        "delta_largest_component_cycle_rank",
        "delta_sector_size",
    ]
    for col in delta_columns:
        paired_rows.append(summarize_delta(col))

    n_pairs = int(len(per_seed_df))
    comp_success = per_seed_df["structure_success_compensated"].astype(int)
    uncomp_success = per_seed_df["structure_success_uncompensated"].astype(int)
    compensated_only_success_count = int(np.sum((comp_success == 1) & (uncomp_success == 0)))
    uncompensated_only_success_count = int(np.sum((comp_success == 0) & (uncomp_success == 1)))
    both_success_count = int(np.sum((comp_success == 1) & (uncomp_success == 1)))
    both_failure_count = int(np.sum((comp_success == 0) & (uncomp_success == 0)))
    paired_success_delta_mean = float(np.mean(per_seed_df["delta_structure_success"].astype(float)))

    paired_rows.extend([
        {
            "metric": "compensated_only_success_count",
            "n_pairs": n_pairs,
            "mean_delta": compensated_only_success_count,
            "median_delta": np.nan,
            "std_delta": np.nan,
            "q25_delta": np.nan,
            "q75_delta": np.nan,
            "min_delta": np.nan,
            "max_delta": np.nan,
            "positive_delta_count": np.nan,
            "negative_delta_count": np.nan,
            "zero_delta_count": np.nan,
            "positive_delta_fraction": np.nan,
            "negative_delta_fraction": np.nan,
            "zero_delta_fraction": np.nan,
            "sign_test_positive_rate": np.nan,
        },
        {
            "metric": "uncompensated_only_success_count",
            "n_pairs": n_pairs,
            "mean_delta": uncompensated_only_success_count,
            "median_delta": np.nan,
            "std_delta": np.nan,
            "q25_delta": np.nan,
            "q75_delta": np.nan,
            "min_delta": np.nan,
            "max_delta": np.nan,
            "positive_delta_count": np.nan,
            "negative_delta_count": np.nan,
            "zero_delta_count": np.nan,
            "positive_delta_fraction": np.nan,
            "negative_delta_fraction": np.nan,
            "zero_delta_fraction": np.nan,
            "sign_test_positive_rate": np.nan,
        },
        {
            "metric": "both_success_count",
            "n_pairs": n_pairs,
            "mean_delta": both_success_count,
            "median_delta": np.nan,
            "std_delta": np.nan,
            "q25_delta": np.nan,
            "q75_delta": np.nan,
            "min_delta": np.nan,
            "max_delta": np.nan,
            "positive_delta_count": np.nan,
            "negative_delta_count": np.nan,
            "zero_delta_count": np.nan,
            "positive_delta_fraction": np.nan,
            "negative_delta_fraction": np.nan,
            "zero_delta_fraction": np.nan,
            "sign_test_positive_rate": np.nan,
        },
        {
            "metric": "both_failure_count",
            "n_pairs": n_pairs,
            "mean_delta": both_failure_count,
            "median_delta": np.nan,
            "std_delta": np.nan,
            "q25_delta": np.nan,
            "q75_delta": np.nan,
            "min_delta": np.nan,
            "max_delta": np.nan,
            "positive_delta_count": np.nan,
            "negative_delta_count": np.nan,
            "zero_delta_count": np.nan,
            "positive_delta_fraction": np.nan,
            "negative_delta_fraction": np.nan,
            "zero_delta_fraction": np.nan,
            "sign_test_positive_rate": np.nan,
        },
        {
            "metric": "paired_success_delta_mean",
            "n_pairs": n_pairs,
            "mean_delta": paired_success_delta_mean,
            "median_delta": np.nan,
            "std_delta": np.nan,
            "q25_delta": np.nan,
            "q75_delta": np.nan,
            "min_delta": np.nan,
            "max_delta": np.nan,
            "positive_delta_count": np.nan,
            "negative_delta_count": np.nan,
            "zero_delta_count": np.nan,
            "positive_delta_fraction": np.nan,
            "negative_delta_fraction": np.nan,
            "zero_delta_fraction": np.nan,
            "sign_test_positive_rate": np.nan,
        },
    ])

    paired_summary_df = pd.DataFrame(paired_rows)
    paired_summary_path = f"outputs/paired_seed_summary_{args.output_prefix}.csv"
    paired_summary_df.to_csv(paired_summary_path, index=False)
    print(f"Wrote {paired_summary_path}")

    # Wilson CIs for success rates
    z = 1.959963984540054
    wilson_rows: List[Dict[str, Any]] = []

    def wilson_row(group: str, subgroup: str, success_count: int, n: int) -> Dict[str, Any]:
        rate = float(success_count / n) if n > 0 else 0.0
        denominator = 1 + z**2 / n if n > 0 else 1.0
        center = (rate + z**2 / (2 * n)) / denominator if n > 0 else 0.0
        half_width = (
            z
            * np.sqrt((rate * (1 - rate) / n) + (z**2 / (4 * n * n)))
            / denominator
        ) if n > 0 else 0.0
        return {
            "group": group,
            "subgroup": subgroup,
            "success_count": success_count,
            "n": n,
            "rate": rate,
            "ci_method": "wilson_score",
            "ci_level": 0.95,
            "ci_low": float(max(0.0, center - half_width)) if n > 0 else 0.0,
            "ci_high": float(min(1.0, center + half_width)) if n > 0 else 1.0,
        }

    for model_mode in sorted(raw_df["model_mode"].unique()):
        subset = raw_df[raw_df["model_mode"] == model_mode]
        n = int(len(subset))
        success_count = int(subset["structure_success"].astype(int).sum())
        wilson_rows.append(wilson_row("model_mode", model_mode, success_count, n))

    above_df = raw_df[raw_df["non_bridge_edge_count"] >= 19]
    below_df = raw_df[raw_df["non_bridge_edge_count"] < 19]
    wilson_rows.append(wilson_row("non_bridge_edge_count_threshold", ">=19", int(above_df["structure_success"].astype(int).sum()), int(len(above_df))))
    wilson_rows.append(wilson_row("non_bridge_edge_count_threshold", "<19", int(below_df["structure_success"].astype(int).sum()), int(len(below_df))))

    for model_mode in sorted(raw_df["model_mode"].unique()):
        subset = raw_df[raw_df["model_mode"] == model_mode]
        n = int(len(subset))
        wilson_rows.append(wilson_row("failed_p_gnp", model_mode, int(subset["failed_p_gnp"].astype(int).sum()), n))
        wilson_rows.append(wilson_row("failed_p_dp", model_mode, int(subset["failed_p_dp"].astype(int).sum()), n))

    wilson_df = pd.DataFrame(wilson_rows)
    wilson_path = f"outputs/wilson_cis_{args.output_prefix}.csv"
    wilson_df.to_csv(wilson_path, index=False)
    print(f"Wrote {wilson_path}")

    # Bootstrap CI for non_bridge_edge_count >= 19
    rng = np.random.default_rng(20260512)
    above_n = int(len(above_df))
    below_n = int(len(below_df))
    above_success_count = int(above_df["structure_success"].astype(int).sum())
    below_success_count = int(below_df["structure_success"].astype(int).sum())
    above_rate = float(above_success_count / above_n) if above_n > 0 else 0.0
    below_rate = float(below_success_count / below_n) if below_n > 0 else 0.0
    rate_difference = above_rate - below_rate

    diff_boot = []
    for _ in range(1000):
        above_sample = rng.choice(above_df["structure_success"].astype(int).to_numpy(), size=above_n, replace=True)
        below_sample = rng.choice(below_df["structure_success"].astype(int).to_numpy(), size=below_n, replace=True)
        diff_boot.append(float(np.mean(above_sample) - np.mean(below_sample)))
    diff_boot = np.array(diff_boot)
    bootstrap_ci_low = float(np.percentile(diff_boot, 2.5))
    bootstrap_ci_high = float(np.percentile(diff_boot, 97.5))

    bootstrap_df = pd.DataFrame([{
        "threshold_type": "non_bridge_edge_count_threshold",
        "threshold_value": 19,
        "iterations": 1000,
        "random_seed": 20260512,
        "above_n": above_n,
        "above_success_count": above_success_count,
        "above_rate": above_rate,
        "below_n": below_n,
        "below_success_count": below_success_count,
        "below_rate": below_rate,
        "rate_difference": rate_difference,
        "bootstrap_ci_low": bootstrap_ci_low,
        "bootstrap_ci_high": bootstrap_ci_high,
        "ci_level": 0.95,
        "note": "post_hoc_threshold_same_data_exploratory",
    }])
    bootstrap_path = f"outputs/bootstrap_ci_non_bridge_ge19_{args.output_prefix}.csv"
    bootstrap_df.to_csv(bootstrap_path, index=False)
    print(f"Wrote {bootstrap_path}")


if __name__ == "__main__":
    main()