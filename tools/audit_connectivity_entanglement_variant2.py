#!/usr/bin/env python3
"""
GCMS-D0 TOOL PASSPORT
=====================

Project:
    AlphaEvolve-GCMS / GCMS-D0

Repository:
    AIDevelopersMonster/alphaevolve-gcms

Script:
    tools/audit_connectivity_entanglement_variant2.py

Script type:
    native topology audit tool

Status:
    smoke mode implemented
    full mode implemented

Purpose:
    Audit the native topology produced by compensated and uncompensated 
    Variant 2 dynamics at beta=0.003.
    
    This is NOT an ablation by edge removal.
    This is NOT a pruning experiment.
    This is a native topology audit.
    
    Measure connectivity entanglement via topology descriptors on the 
    sector graph as produced by the simulation, without alteration.

Allowed actions:
    Read experiment code from experiments/ae_v010_2.py.
    Run smoke audit from local .venv.
    Reuse graph analysis logic from existing tools.

Forbidden actions:
    Do not modify experiments/ae_v010_2.py.
    Do not prune or remove edges.
    Do not apply rescue methods.
    Do not run full audit without explicit authorization.
    Do not commit generated outputs by default.

Inputs:
    --mode smoke
    --mode full (raises NotImplementedError)
    --out-prefix <prefix>

Outputs (smoke):
    outputs/raw_<prefix>.csv
    outputs/summary_<prefix>.csv
    outputs/per_seed_<prefix>.csv
    outputs/thresholds_<prefix>.csv

Verification:
    ./.venv/Scripts/python.exe -m py_compile tools/audit_connectivity_entanglement_variant2.py
    ./.venv/Scripts/python.exe tools/audit_connectivity_entanglement_variant2.py --mode smoke --out-prefix smoke_connectivity_entanglement_audit_variant2
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.ae_v010_2 import Simulator, World

SMOKE_CONFIG = {
    "relation_variant": 2,
    "model_modes": ["compensated", "uncompensated"],
    "beta": 0.003,
    "seeds": 2,
    "N": 150,
    "d": 4,
    "steps": 200,
    "alpha": 0.5,
    "threshold": 0.75,
    "mutation_rate": 0.10,
    "epsilon_norm": 0.0,
    "lambda_val": 0.0,
    "baseline_count": 10,
}

FULL_CONFIG = {
    **SMOKE_CONFIG,
    "seeds": 100,
    "baseline_count": 100,
}

MIN_SECTOR_SIZE = 5
MAX_SECTOR_SIZE = 60


class SimulatorWithNodes(Simulator):
    """Extended Simulator that tracks best sector nodes."""
    def __init__(
        self,
        world: World,
        relation_variant: int,
        alpha: float,
        threshold: float,
        beta: float,
        lambda_val: float,
        baseline_count: int,
    ):
        super().__init__(
            world=world,
            relation_variant=relation_variant,
            alpha=alpha,
            threshold=threshold,
            beta=beta,
            lambda_val=lambda_val,
            baseline_count=baseline_count,
        )
        self.best_sector_nodes: Optional[Set[int]] = None
        self.best_sector_lifetime: int = 0

    def deep_analysis(self, nodes: Set[int], seed: int) -> Optional[Dict[str, Any]]:
        data = super().deep_analysis(nodes, seed)
        if data is not None:
            if self.best_sector_data is None or data["lifetime"] > self.best_sector_data["lifetime"]:
                self.best_sector_nodes = set(nodes)
                self.best_sector_lifetime = int(data["lifetime"])
        return data


def empirical_p_greater(observed: float, baseline: List[float]) -> float:
    """Compute empirical p-value: fraction of baseline >= observed."""
    if not baseline:
        return 1.0
    return float((1 + sum(x >= observed for x in baseline)) / (len(baseline) + 1))


def chi_for_nodes(world: World, nodes: Iterable[int]) -> float:
    """Compute chi = norm of sum of state vectors."""
    vec = sum((world.states[i].v for i in nodes), np.zeros(world.d))
    return float(np.linalg.norm(vec))


def compute_topology_metrics(g: nx.Graph) -> Dict[str, Any]:
    """Compute native topology metrics on the graph."""
    n = g.number_of_nodes()
    m = g.number_of_edges()
    
    # Basic metrics
    edge_count = m
    density = float(nx.density(g)) if n > 0 else 0.0
    
    # Components
    components = list(nx.connected_components(g))
    n_components = len(components)
    largest_component = max((len(c) for c in components), default=0)
    largest_component_fraction = float(largest_component / n) if n else 0.0
    
    # Degree metrics
    degrees = np.array([deg for _, deg in g.degree()], dtype=float)
    mean_degree = float(2 * m / n) if n > 0 else 0.0
    degree_variance = float(np.var(degrees)) if len(degrees) else 0.0
    max_degree = int(max(degrees)) if len(degrees) > 0 else 0
    
    # Bridge metrics
    bridge_edges = set(nx.bridges(g))
    bridge_count = len(bridge_edges)
    bridge_fraction = float(bridge_count / m) if m > 0 else 0.0
    non_bridge_edge_count = m - bridge_count
    
    # Cycle rank (cyclomatic complexity)
    cycle_rank = m - n + n_components
    
    # Largest component cycle rank
    if largest_component > 0:
        lcc_nodes = max((set(c) for c in components), key=len)
        lcc_subgraph = g.subgraph(lcc_nodes)
        lcc_edges = lcc_subgraph.number_of_edges()
        lcc_nodes_count = lcc_subgraph.number_of_nodes()
        largest_component_cycle_rank = lcc_edges - lcc_nodes_count + 1
    else:
        largest_component_cycle_rank = 0
    
    # Clustering
    clustering = float(nx.average_clustering(g)) if n > 0 else 0.0
    
    # Optional spectral descriptors (attempt, but don't fail on error)
    spectral_gap_optional = 0.0
    spectral_gap_available = False
    algebraic_connectivity_optional = 0.0
    algebraic_connectivity_available = False
    
    if n >= 2 and nx.is_connected(g):
        try:
            # Try to compute spectral gap (second smallest eigenvalue of Laplacian)
            laplacian = nx.laplacian_matrix(g).astype(float)
            eigenvalues = np.linalg.eigvalsh(laplacian.toarray())
            eigenvalues = np.sort(eigenvalues)
            if len(eigenvalues) >= 2:
                spectral_gap_optional = float(eigenvalues[1])
                spectral_gap_available = True
        except (RuntimeError, ValueError, np.linalg.LinAlgError):
            pass
        
        try:
            # Algebraic connectivity = second smallest eigenvalue of Laplacian
            algebraic_connectivity_optional = float(nx.algebraic_connectivity(g, method='lanczos'))
            algebraic_connectivity_available = True
        except (RuntimeError, ValueError, nx.NetworkXError):
            pass
    
    return {
        "sector_size": n,
        "edge_count": edge_count,
        "density": density,
        "n_components": n_components,
        "largest_component_fraction": largest_component_fraction,
        "bridge_count": bridge_count,
        "bridge_fraction": bridge_fraction,
        "non_bridge_edge_count": non_bridge_edge_count,
        "cycle_rank": cycle_rank,
        "largest_component_edge_count": lcc_subgraph.number_of_edges() if largest_component > 0 else 0,
        "largest_component_node_count": largest_component,
        "largest_component_cycle_rank": largest_component_cycle_rank,
        "mean_degree": mean_degree,
        "degree_variance": degree_variance,
        "max_degree": max_degree,
        "clustering": clustering,
        "spectral_gap_optional": spectral_gap_optional,
        "spectral_gap_available": spectral_gap_available,
        "algebraic_connectivity_optional": algebraic_connectivity_optional,
        "algebraic_connectivity_available": algebraic_connectivity_available,
    }


def analyze_graph(
    g: nx.Graph,
    world: World,
    lifetime: int,
    baseline_count: int,
    analysis_seed: int,
    baseline_sim: Simulator,
) -> Dict[str, Any]:
    """Analyze graph for structure success using existing criteria."""
    n = g.number_of_nodes()
    m = g.number_of_edges()
    
    rng = np.random.default_rng(analysis_seed)
    if n > 0 and m > 0:
        # GNP baseline
        density = float(nx.density(g))
        gnp_clusts: List[float] = []
        for _ in range(baseline_count):
            rg_seed = int(rng.integers(0, 2**31 - 1))
            rg = nx.fast_gnp_random_graph(n, density, seed=rg_seed)
            gnp_clusts.append(float(nx.average_clustering(rg)))
        
        # Degree-preserving baseline
        dp_clusts, dp_swap_success_rate = baseline_sim.degree_preserving_baseline(g, rng)
        dp_valid = len(dp_clusts) >= min(30, baseline_count)
        
        clustering = float(nx.average_clustering(g))
        p_gnp = empirical_p_greater(clustering, gnp_clusts)
        p_dp = empirical_p_greater(clustering, dp_clusts) if dp_valid else 1.0
    else:
        dp_swap_success_rate = 0.0
        dp_valid = False
        p_gnp = 1.0
        p_dp = 1.0
    
    # Structure success: must satisfy all criteria
    structure_success = (
        p_gnp < 0.05
        and p_dp < 0.05
        and dp_valid
        and lifetime > 20
        and MIN_SECTOR_SIZE <= n <= MAX_SECTOR_SIZE
    )
    
    # Failure tracking
    failed_p_gnp = p_gnp >= 0.05
    failed_dp_valid = not dp_valid
    failed_p_dp = dp_valid and p_dp >= 0.05
    failed_lifetime = lifetime <= 20
    failed_sector_size = n < MIN_SECTOR_SIZE or n > MAX_SECTOR_SIZE
    
    failure_reasons: List[str] = []
    if failed_sector_size:
        failure_reasons.append("sector_size")
    if failed_lifetime:
        failure_reasons.append("lifetime")
    if failed_dp_valid:
        failure_reasons.append("dp_valid")
    if failed_p_gnp:
        failure_reasons.append("p_gnp")
    if failed_p_dp:
        failure_reasons.append("p_dp")
    if not failure_reasons:
        failure_reasons.append("none")
    
    return {
        "p_gnp_empirical": p_gnp,
        "p_dp_empirical": p_dp,
        "dp_valid": bool(dp_valid),
        "dp_swap_success_rate": float(dp_swap_success_rate),
        "structure_success": bool(structure_success),
        "failure_reason": "|".join(failure_reasons),
        "failed_p_gnp": bool(failed_p_gnp),
        "failed_p_dp": bool(failed_p_dp),
        "failed_dp_valid": bool(failed_dp_valid),
        "failed_lifetime": bool(failed_lifetime),
        "failed_sector_size": bool(failed_sector_size),
    }


def get_threshold_candidates(values: np.ndarray, max_candidates: int = 5) -> List[float]:
    unique_vals = sorted(np.unique(values))
    if len(unique_vals) <= max_candidates:
        return unique_vals
    positions = [0, len(unique_vals) // 4, len(unique_vals) // 2, (3 * len(unique_vals)) // 4, len(unique_vals) - 1]
    return sorted({unique_vals[pos] for pos in positions})


def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    summary_keys = ["model_mode", "relation_variant", "beta"]
    summary = df.groupby(summary_keys).agg(
        runs=("seed", "count"),
        structure_success_rate=("structure_success", "mean"),
        mean_edge_count=("edge_count", "mean"),
        mean_density=("density", "mean"),
        mean_n_components=("n_components", "mean"),
        mean_largest_component_fraction=("largest_component_fraction", "mean"),
        mean_bridge_count=("bridge_count", "mean"),
        mean_bridge_fraction=("bridge_fraction", "mean"),
        mean_non_bridge_edge_count=("non_bridge_edge_count", "mean"),
        mean_cycle_rank=("cycle_rank", "mean"),
        mean_largest_component_cycle_rank=("largest_component_cycle_rank", "mean"),
        mean_mean_degree=("mean_degree", "mean"),
        mean_degree_variance=("degree_variance", "mean"),
        mean_max_degree=("max_degree", "mean"),
        mean_sector_size=("sector_size", "mean"),
        mean_failed_p_gnp=("failed_p_gnp", "mean"),
        mean_failed_p_dp=("failed_p_dp", "mean"),
        mean_dp_valid=("dp_valid", "mean"),
        mean_dp_swap_success_rate=("dp_swap_success_rate", "mean"),
        mean_global_error=("global_error", "mean"),
        mean_global_vector_norm=("global_vector_norm", "mean"),
        mean_sector_chi=("sector_chi", "mean"),
    ).reset_index()

    for col in ["non_bridge_edge_count", "cycle_rank", "bridge_fraction"]:
        quantiles = df.groupby(summary_keys)[col].quantile([0.25, 0.50, 0.75]).unstack()
        quantiles.columns = [f"q{int(c*100)}_{col}" for c in quantiles.columns]
        summary = summary.merge(quantiles, left_on=summary_keys, right_index=True)

    return summary


def make_per_seed(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["seed"]
    model_values = {"compensated": df[df["model_mode"] == "compensated"].set_index("seed"),
                    "uncompensated": df[df["model_mode"] == "uncompensated"].set_index("seed")}
    cols = [
        "edge_count",
        "bridge_fraction",
        "non_bridge_edge_count",
        "cycle_rank",
        "largest_component_fraction",
        "structure_success",
        "failed_p_gnp",
        "failed_p_dp",
        "density",
        "bridge_count",
        "largest_component_cycle_rank",
        "sector_size",
    ]
    bool_cols = {"structure_success", "failed_p_gnp", "failed_p_dp"}

    rows: List[Dict[str, Any]] = []
    for seed in sorted(df["seed"].unique()):
        row: Dict[str, Any] = {"seed": seed}
        for col in cols:
            val_c = model_values["compensated"].loc[seed, col] if seed in model_values["compensated"].index else 0
            val_u = model_values["uncompensated"].loc[seed, col] if seed in model_values["uncompensated"].index else 0
            if col in bool_cols:
                val_c = int(bool(val_c))
                val_u = int(bool(val_u))
            row[f"{col}_compensated"] = val_c
            row[f"{col}_uncompensated"] = val_u
            row[f"delta_{col}"] = val_c - val_u
        rows.append(row)

    return pd.DataFrame(rows)


def make_thresholds(df: pd.DataFrame) -> pd.DataFrame:
    threshold_specs = [
        ("non_bridge_edge_count", "non_bridge_edge_count", lambda d, v: d[d["non_bridge_edge_count"] >= v], lambda d, v: d[d["non_bridge_edge_count"] < v]),
        ("cycle_rank", "cycle_rank", lambda d, v: d[d["cycle_rank"] >= v], lambda d, v: d[d["cycle_rank"] < v]),
        ("largest_component_cycle_rank", "largest_component_cycle_rank", lambda d, v: d[d["largest_component_cycle_rank"] >= v], lambda d, v: d[d["largest_component_cycle_rank"] < v]),
        ("edge_count", "edge_count", lambda d, v: d[d["edge_count"] >= v], lambda d, v: d[d["edge_count"] < v]),
        ("bridge_fraction_le", "bridge_fraction", lambda d, v: d[d["bridge_fraction"] <= v], lambda d, v: d[d["bridge_fraction"] > v]),
    ]
    threshold_rows: List[Dict[str, Any]] = []

    for threshold_type, col, above_fn, below_fn in threshold_specs:
        values = df[col].dropna().to_numpy()
        if len(values) == 0:
            continue
        for threshold_value in get_threshold_candidates(values):
            above = above_fn(df, threshold_value)
            below = below_fn(df, threshold_value)
            threshold_rows.append({
                "threshold_type": threshold_type,
                "threshold_value": threshold_value,
                "rows_above_threshold": len(above),
                "structure_success_rate_above_threshold": above["structure_success"].mean() if len(above) > 0 else 0,
                "rows_below_threshold": len(below),
                "structure_success_rate_below_threshold": below["structure_success"].mean() if len(below) > 0 else 0,
            })

    return pd.DataFrame(threshold_rows)


def make_correlations(df: pd.DataFrame) -> pd.DataFrame:
    features = [
        "edge_count",
        "density",
        "bridge_fraction",
        "non_bridge_edge_count",
        "cycle_rank",
        "largest_component_cycle_rank",
        "mean_degree",
        "degree_variance",
        "max_degree",
        "sector_size",
    ]
    targets = ["structure_success", "failed_p_gnp", "failed_p_dp"]
    rows: List[Dict[str, Any]] = []

    for feature in features:
        if feature not in df.columns:
            continue
        x = df[feature].to_numpy(dtype=float)
        for target in targets:
            y = df[target].to_numpy(dtype=float)
            if len(x) < 2 or len(y) < 2:
                continue
            try:
                corr = np.corrcoef(x, y)[0, 1]
            except Exception:
                corr = 0.0
            rows.append({
                "feature": feature,
                "method": "pearson",
                "target": target,
                "correlation_with_target": float(corr),
                "n_rows": int(len(df)),
            })
    return pd.DataFrame(rows)


def run_audit(config: Dict[str, Any], out_prefix: str) -> None:
    rows: List[Dict[str, Any]] = []

    for model_mode in config["model_modes"]:
        for seed in range(config["seeds"]):
            world = World(
                config["N"],
                config["d"],
                model_mode,
                config["epsilon_norm"],
                seed,
            )
            sim = SimulatorWithNodes(
                world=world,
                relation_variant=config["relation_variant"],
                alpha=config["alpha"],
                threshold=config["threshold"],
                beta=config["beta"],
                lambda_val=config["lambda_val"],
                baseline_count=config["baseline_count"],
            )

            for step in range(config["steps"]):
                sim.mutate_and_step(config["mutation_rate"], step_seed=seed * 100000 + step)

            # Compute diagnostics
            global_error = world.global_error()
            global_vector_norm = np.linalg.norm(world.global_vector())
            compensation_valid = global_error < 1e-12

            cluster_nodes: Optional[Set[int]] = None
            cluster_lifetime = 0
            if sim.valid_size(sim.current_indices) and sim.lifetime > 20:
                sim.deep_analysis(sim.current_indices, seed=seed * 99991 + config["steps"])
                cluster_nodes = set(sim.current_indices)
                cluster_lifetime = sim.lifetime
            elif sim.best_sector_nodes is not None:
                cluster_nodes = sim.best_sector_nodes
                cluster_lifetime = sim.best_sector_lifetime

            if not cluster_nodes:
                sector_chi = 0.0
                row = {
                    "model_mode": model_mode,
                    "relation_variant": config["relation_variant"],
                    "beta": config["beta"],
                    "seed": seed,
                    "N": config["N"],
                    "d": config["d"],
                    "steps": config["steps"],
                    "baseline_count": config["baseline_count"],
                    "mutation_rate": config["mutation_rate"],
                    "lifetime": 0,
                    "sector_size": 0,
                    "edge_count": 0,
                    "density": 0.0,
                    "n_components": 0,
                    "largest_component_fraction": 0.0,
                    "bridge_count": 0,
                    "bridge_fraction": 0.0,
                    "non_bridge_edge_count": 0,
                    "cycle_rank": 0,
                    "largest_component_edge_count": 0,
                    "largest_component_node_count": 0,
                    "largest_component_cycle_rank": 0,
                    "mean_degree": 0.0,
                    "degree_variance": 0.0,
                    "max_degree": 0,
                    "clustering": 0.0,
                    "spectral_gap_optional": 0.0,
                    "spectral_gap_available": False,
                    "algebraic_connectivity_optional": 0.0,
                    "algebraic_connectivity_available": False,
                    "p_gnp_empirical": 1.0,
                    "p_dp_empirical": 1.0,
                    "dp_valid": False,
                    "dp_swap_success_rate": 0.0,
                    "structure_success": False,
                    "failure_reason": "no_sector",
                    "failed_p_gnp": False,
                    "failed_p_dp": False,
                    "failed_dp_valid": True,
                    "failed_lifetime": False,
                    "failed_sector_size": True,
                    "global_error": global_error,
                    "global_vector_norm": global_vector_norm,
                    "compensation_valid": compensation_valid,
                    "sector_chi": sector_chi,
                }
                rows.append(row)
                continue

            g = sim.build_graph(cluster_nodes)
            topo_metrics = compute_topology_metrics(g)
            baseline_sim = SimulatorWithNodes(
                world=world,
                relation_variant=config["relation_variant"],
                alpha=config["alpha"],
                threshold=config["threshold"],
                beta=config["beta"],
                lambda_val=config["lambda_val"],
                baseline_count=config["baseline_count"],
            )
            structure_metrics = analyze_graph(
                g,
                world,
                cluster_lifetime,
                config["baseline_count"],
                analysis_seed=seed * 1000000,
                baseline_sim=baseline_sim,
            )
            sector_chi = chi_for_nodes(world, cluster_nodes)
            row = {
                "model_mode": model_mode,
                "relation_variant": config["relation_variant"],
                "beta": config["beta"],
                "seed": seed,
                "N": config["N"],
                "d": config["d"],
                "steps": config["steps"],
                "baseline_count": config["baseline_count"],
                "mutation_rate": config["mutation_rate"],
                "lifetime": cluster_lifetime,
                **topo_metrics,
                **structure_metrics,
                "global_error": global_error,
                "global_vector_norm": global_vector_norm,
                "compensation_valid": compensation_valid,
                "sector_chi": sector_chi,
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs("outputs", exist_ok=True)

    raw_path = f"outputs/raw_{out_prefix}.csv"
    df.to_csv(raw_path, index=False)
    print(f"Wrote {raw_path}")

    summary = make_summary(df)
    summary_path = f"outputs/summary_{out_prefix}.csv"
    summary.to_csv(summary_path, index=False)
    print(f"Wrote {summary_path}")

    per_seed_df = make_per_seed(df)
    per_seed_path = f"outputs/per_seed_{out_prefix}.csv"
    per_seed_df.to_csv(per_seed_path, index=False)
    print(f"Wrote {per_seed_path}")

    thresholds_df = make_thresholds(df)
    thresholds_path = f"outputs/thresholds_{out_prefix}.csv"
    thresholds_df.to_csv(thresholds_path, index=False)
    print(f"Wrote {thresholds_path}")

    correlations_df = make_correlations(df)
    if not correlations_df.empty:
        correlations_path = f"outputs/correlations_{out_prefix}.csv"
        correlations_df.to_csv(correlations_path, index=False)
        print(f"Wrote {correlations_path}")


def run_smoke(out_prefix: str) -> None:
    run_audit(SMOKE_CONFIG, out_prefix)


def run_full(out_prefix: str) -> None:
    run_audit(FULL_CONFIG, out_prefix)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Connectivity entanglement audit for Variant 2 native topology."
    )
    parser.add_argument(
        "--mode",
        choices=["smoke", "full"],
        default="smoke",
        help="Audit mode: smoke (2 seeds) or full (100 seeds)"
    )
    parser.add_argument(
        "--out-prefix",
        default="connectivity_entanglement_audit_variant2",
        help="Output file prefix"
    )
    args = parser.parse_args()
    
    if args.mode == "smoke":
        run_smoke(args.out_prefix)
    elif args.mode == "full":
        run_full(args.out_prefix)
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")


if __name__ == "__main__":
    main()
