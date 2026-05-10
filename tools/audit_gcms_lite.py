#!/usr/bin/env python3
"""Lite deterministic auditor for GCMS raw CSV outputs.

This tool is intentionally small. It recomputes the basic rates and effect
sizes from a raw GCMS output CSV so that key reported numbers do not drift
between conversations.

Example:
    python tools/audit_gcms_lite.py \
        --raw outputs/raw_v010_beta_grid_variant2.csv \
        --out-prefix v010_beta_grid_variant2_lite
"""

from __future__ import annotations

import argparse
import math
import os
from pathlib import Path
from typing import Iterable

import pandas as pd


REQUIRED_COLUMNS = [
    "model_mode",
    "relation_variant",
    "beta",
    "seed",
    "structure_success",
    "analyzed",
    "edge_count",
    "density",
    "sector_size",
    "lifetime",
    "dp_valid",
]


PREFERRED_MODE_ORDER = ["compensated", "uncompensated", "residual"]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute stable GCMS lite audit tables and an effect-vs-beta chart."
    )
    parser.add_argument(
        "--raw",
        required=True,
        help="Path to raw GCMS CSV file, for example outputs/raw_v010_beta_grid_variant2.csv.",
    )
    parser.add_argument(
        "--out-prefix",
        required=True,
        help="Output prefix. Files are written under outputs/ unless a directory is included.",
    )
    parser.add_argument(
        "--relation-variant",
        type=int,
        default=None,
        help="Optional relation_variant filter.",
    )
    return parser.parse_args()


def ensure_bool_like(series: pd.Series) -> pd.Series:
    """Convert bool/int/string-like truth values to 0/1 integers."""
    if series.dtype == bool:
        return series.astype(int)
    if pd.api.types.is_numeric_dtype(series):
        return series.fillna(0).astype(int)
    return series.astype(str).str.lower().isin(["true", "1", "yes", "y"]).astype(int)


def validate_columns(df: pd.DataFrame, required: Iterable[str]) -> list[str]:
    return [col for col in required if col not in df.columns]


def safe_mean_degree(edge_count: float, sector_size: float) -> float:
    if pd.isna(edge_count) or pd.isna(sector_size) or sector_size <= 0:
        return 0.0
    return 2.0 * float(edge_count) / float(sector_size)


def format_float(value: float, digits: int = 6) -> str:
    if pd.isna(value):
        return "nan"
    return f"{value:.{digits}f}"


def mode_sort_key(mode: str) -> tuple[int, str]:
    try:
        return (PREFERRED_MODE_ORDER.index(mode), mode)
    except ValueError:
        return (len(PREFERRED_MODE_ORDER), mode)


def compute_summary(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["structure_success_int"] = ensure_bool_like(df["structure_success"])
    df["analyzed_int"] = ensure_bool_like(df["analyzed"])
    df["dp_valid_int"] = ensure_bool_like(df["dp_valid"])
    df["mean_degree"] = df.apply(
        lambda row: safe_mean_degree(row["edge_count"], row["sector_size"]), axis=1
    )

    group_cols = ["relation_variant", "beta", "model_mode"]
    rows = []
    for keys, g in df.groupby(group_cols, dropna=False):
        relation_variant, beta, model_mode = keys
        attempted = len(g)
        successes = int(g["structure_success_int"].sum())
        analyzed = int(g["analyzed_int"].sum())
        rows.append(
            {
                "relation_variant": relation_variant,
                "beta": beta,
                "model_mode": model_mode,
                "attempted": attempted,
                "structure_success_count": successes,
                "structure_success_rate": successes / attempted if attempted else math.nan,
                "analyzed_count": analyzed,
                "analyzed_rate": analyzed / attempted if attempted else math.nan,
                "mean_edge_count": g["edge_count"].mean(),
                "mean_density": g["density"].mean(),
                "mean_sector_size": g["sector_size"].mean(),
                "mean_lifetime": g["lifetime"].mean(),
                "mean_dp_valid": g["dp_valid_int"].mean(),
                "mean_degree": g["mean_degree"].mean(),
            }
        )

    out = pd.DataFrame(rows)
    if out.empty:
        return out
    out["_mode_order"] = out["model_mode"].map(mode_sort_key)
    out = out.sort_values(["relation_variant", "beta", "_mode_order"]).drop(columns=["_mode_order"])
    return out.reset_index(drop=True)


def compute_effect(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (relation_variant, beta), g in summary.groupby(["relation_variant", "beta"], dropna=False):
        by_mode = {row["model_mode"]: row for _, row in g.iterrows()}
        comp = by_mode.get("compensated")
        uncomp = by_mode.get("uncompensated")
        if comp is None or uncomp is None:
            continue
        effect = comp["structure_success_rate"] - uncomp["structure_success_rate"]
        rows.append(
            {
                "relation_variant": relation_variant,
                "beta": beta,
                "compensated_rate": comp["structure_success_rate"],
                "uncompensated_rate": uncomp["structure_success_rate"],
                "compensation_effect_attempted": effect,
                "compensated_analyzed_count": comp["analyzed_count"],
                "uncompensated_analyzed_count": uncomp["analyzed_count"],
                "compensated_mean_edge_count": comp["mean_edge_count"],
                "uncompensated_mean_edge_count": uncomp["mean_edge_count"],
                "compensated_mean_density": comp["mean_density"],
                "uncompensated_mean_density": uncomp["mean_density"],
                "compensated_mean_degree": comp["mean_degree"],
                "uncompensated_mean_degree": uncomp["mean_degree"],
                "compensated_mean_sector_size": comp["mean_sector_size"],
                "uncompensated_mean_sector_size": uncomp["mean_sector_size"],
                "compensated_mean_lifetime": comp["mean_lifetime"],
                "uncompensated_mean_lifetime": uncomp["mean_lifetime"],
            }
        )
    out = pd.DataFrame(rows)
    if out.empty:
        return out
    return out.sort_values(["relation_variant", "beta"]).reset_index(drop=True)


def write_chart(effect: pd.DataFrame, path: Path) -> None:
    """Write a simple effect-vs-beta PNG chart using matplotlib."""
    if effect.empty:
        return

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 4.8))
    for relation_variant, g in effect.groupby("relation_variant"):
        g = g.sort_values("beta")
        ax.plot(
            g["beta"],
            g["compensation_effect_attempted"],
            marker="o",
            label=f"variant {relation_variant}",
        )
    ax.axhline(0, linewidth=1)
    ax.set_xlabel("beta")
    ax.set_ylabel("compensation effect attempted")
    ax.set_title("GCMS compensation effect vs beta")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)


def collapse_warning(row: pd.Series) -> str:
    warnings = []
    if row.get("uncompensated_analyzed_count", math.inf) < 10:
        warnings.append("low uncompensated analyzed count")
    if row.get("uncompensated_mean_edge_count", math.inf) < 5:
        warnings.append("very low uncompensated edge count")
    if row.get("uncompensated_mean_sector_size", math.inf) < 5:
        warnings.append("very low uncompensated sector size")
    if row.get("uncompensated_mean_lifetime", math.inf) < 30:
        warnings.append("short uncompensated lifetime")
    return "; ".join(warnings) if warnings else "none"


def write_report(raw_path: Path, summary: pd.DataFrame, effect: pd.DataFrame, chart_path: Path, report_path: Path) -> None:
    lines = []
    lines.append("# GCMS Lite Audit Report")
    lines.append("")
    lines.append(f"**Raw input:** `{raw_path}`")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append("This report recomputes basic success rates and compensation effects directly from the raw CSV.")
    lines.append("It is descriptive and does not replace full statistical review.")
    lines.append("")

    if summary.empty:
        lines.append("No summary rows were produced.")
    else:
        lines.append("## Grouped rates")
        lines.append("")
        lines.append(summary.to_markdown(index=False))
        lines.append("")

    if effect.empty:
        lines.append("## Compensation effects")
        lines.append("")
        lines.append("No compensated/uncompensated pairs were available for effect calculation.")
    else:
        effect_with_warning = effect.copy()
        effect_with_warning["collapse_warning"] = effect_with_warning.apply(collapse_warning, axis=1)
        lines.append("## Compensation effects")
        lines.append("")
        lines.append(effect_with_warning.to_markdown(index=False))
        lines.append("")
        lines.append("## Chart")
        lines.append("")
        lines.append(f"![Effect vs beta]({chart_path.name})")
        lines.append("")
        lines.append("## Conservative interpretation rule")
        lines.append("")
        lines.append(
            "Do not treat the largest effect as the cleanest result if density, edge count, "
            "sector size, lifetime, or analyzed counts indicate graph sparsification/collapse."
        )
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")


def resolve_output_prefix(prefix: str) -> Path:
    path = Path(prefix)
    if path.parent == Path("."):
        return Path("outputs") / path.name
    return path


def main() -> int:
    args = parse_args()
    raw_path = Path(args.raw)
    if not raw_path.exists():
        raise FileNotFoundError(f"raw CSV not found: {raw_path}")

    df = pd.read_csv(raw_path)
    missing = validate_columns(df, REQUIRED_COLUMNS)
    if missing:
        print("Missing required columns:")
        for col in missing:
            print(f"- {col}")
        return 2

    if args.relation_variant is not None:
        df = df[df["relation_variant"] == args.relation_variant].copy()
        if df.empty:
            print(f"No rows found for relation_variant={args.relation_variant}")
            return 3

    out_prefix = resolve_output_prefix(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    summary = compute_summary(df)
    effect = compute_effect(summary)

    summary_path = out_prefix.with_name(out_prefix.name + "_summary.csv")
    effect_path = out_prefix.with_name(out_prefix.name + "_effect.csv")
    chart_path = out_prefix.with_name(out_prefix.name + "_effect.png")
    report_path = out_prefix.with_name(out_prefix.name + "_report.md")

    summary.to_csv(summary_path, index=False)
    effect.to_csv(effect_path, index=False)
    write_chart(effect, chart_path)
    write_report(raw_path, summary, effect, chart_path, report_path)

    print(f"Wrote {summary_path}")
    print(f"Wrote {effect_path}")
    if chart_path.exists():
        print(f"Wrote {chart_path}")
    print(f"Wrote {report_path}")

    if not effect.empty:
        print("\nEffect table:")
        cols = [
            "relation_variant",
            "beta",
            "compensated_rate",
            "uncompensated_rate",
            "compensation_effect_attempted",
        ]
        print(effect[cols].to_string(index=False))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
