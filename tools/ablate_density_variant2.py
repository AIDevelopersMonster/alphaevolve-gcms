#!/usr/bin/env python3
"""
GCMS-D0 TOOL PASSPORT
=====================

Project:
    AlphaEvolve-GCMS / GCMS-D0

Repository:
    AIDevelopersMonster/alphaevolve-gcms

Script:
    tools/ablate_density_variant2.py

Script type:
    smoke-mode ablation tool

Status:
    preliminary density-matched ablation smoke runner

Purpose:
    Generate a small pilot ablation dataset for Variant 2 compensated graphs
    by randomly removing edges to target edge counts and recomputing raw
    connectivity diagnostics.

Allowed actions:
    Read experiment code and run smoke ablation from a local .venv.

Forbidden actions:
    Do not modify experiment success criteria.
    Do not change existing experiment presets.
    Do not run the full density-matched ablation sweep.
    Do not commit generated outputs by default.

Inputs:
    --mode smoke
    --out-prefix <prefix>

Outputs:
    outputs/raw_<prefix>.csv
    outputs/summary_<prefix>.csv

Verification:
    python -m py_compile tools/ablate_density_variant2.py
    python tools/ablate_density_variant2.py --mode smoke --out-prefix smoke_density_ablation_variant2
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
    "model_mode": "compensated",
    "relation_variant": 2,
    "beta": 0.003,
    "target_edge_counts": [25, 35],
    "seeds": 2,
    "repetitions_per_target": 2,
    "baseline_count": 10,
    "subsampling_method": "random_edge_removal_preliminary",
    "N": 150,
    "d": 4,
    "steps": 200,
    "alpha": 0.5,
    "threshold": 0.75,
    "mutation_rate": 0.10,
    "epsilon_norm": 0.0,
    "lambda_val": 0.0,
}

FULL_CONFIG_DRAFT = {
    # Draft parameters for a future full density-matched ablation sweep.
    # Not implemented, not executable, and not authorized for use.
    **SMOKE_CONFIG,
    "target_edge_counts": [25, 30, 35, 40],
    "seeds": 100,
    "repetitions_per_target": 10,
    "baseline_count": 100,
    "subsampling_method": "random_edge_removal_preliminary",
}

MIN_SECTOR_SIZE = 5
MAX_SECTOR_SIZE = 60


class SimulatorWithNodes(Simulator):
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
    if not baseline:
        return 1.0
    return float((1 + sum(x >= observed for x in baseline)) / (len(baseline) + 1))


def chi_for_nodes(world: World, nodes: Iterable[int]) -> float:
    vec = sum((world.states[i].v for i in nodes), np.zeros(world.d))
    return float(np.linalg.norm(vec))


def analyze_graph(
    g: nx.Graph,
    world: World,
    lifetime: int,
    baseline_count: int,
    analysis_seed: int,
    baseline_sim: Simulator,
) -> Dict[str, Any]:
    n = g.number_of_nodes()
    m = g.number_of_edges()
    clustering = float(nx.average_clustering(g)) if n > 0 else 0.0
    density = float(nx.density(g)) if n > 0 else 0.0
    components = list(nx.connected_components(g))
    n_components = len(components)
    largest_component = max((len(c) for c in components), default=0)
    largest_component_fraction = float(largest_component / n) if n else 0.0
    degrees = np.array([deg for _, deg in g.degree()], dtype=float)
    degree_variance = float(np.var(degrees)) if len(degrees) else 0.0

    rng = np.random.default_rng(analysis_seed)
    if n > 0 and m > 0:
        gnp_clusts: List[float] = []
        for _ in range(baseline_count):
            rg_seed = int(rng.integers(0, 2**31 - 1))
            rg = nx.fast_gnp_random_graph(n, density, seed=rg_seed)
            gnp_clusts.append(float(nx.average_clustering(rg)))

        dp_clusts, dp_swap_success_rate = baseline_sim.degree_preserving_baseline(g, rng)
        dp_valid = len(dp_clusts) >= min(30, baseline_count)
        p_gnp = empirical_p_greater(clustering, gnp_clusts)
        p_dp = empirical_p_greater(clustering, dp_clusts) if dp_valid else 1.0
    else:
        dp_clusts = []
        dp_swap_success_rate = 0.0
        dp_valid = False
        p_gnp = 1.0
        p_dp = 1.0

    structure_success = (
        p_gnp < 0.05
        and p_dp < 0.05
        and dp_valid
        and lifetime > 20
        and MIN_SECTOR_SIZE <= n <= MAX_SECTOR_SIZE
    )

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
        "sector_size": n,
        "edge_count": m,
        "density": density,
        "clustering": clustering,
        "chi": chi_for_nodes(world, g.nodes()),
        "lifetime": lifetime,
        "p_gnp_empirical": p_gnp,
        "p_dp_empirical": p_dp,
        "dp_valid": bool(dp_valid),
        "dp_swap_success_rate": float(dp_swap_success_rate),
        "structure_success": bool(structure_success),
        "n_components": n_components,
        "largest_component_fraction": largest_component_fraction,
        "degree_variance": degree_variance,
        "failure_reason": "|".join(failure_reasons),
        "failed_p_gnp": bool(failed_p_gnp),
        "failed_p_dp": bool(failed_p_dp),
        "failed_dp_valid": bool(failed_dp_valid),
        "failed_lifetime": bool(failed_lifetime),
        "failed_sector_size": bool(failed_sector_size),
    }


def random_edge_removal(g: nx.Graph, target_edge_count: int, rng: np.random.Generator) -> nx.Graph:
    nodes = list(g.nodes())
    original_edges = list(g.edges())
    original_edge_count = len(original_edges)
    if target_edge_count >= original_edge_count:
        return g.copy()

    keep_count = max(0, target_edge_count)
    if keep_count <= 0:
        h = nx.Graph()
        h.add_nodes_from(nodes)
        return h

    chosen_edges = rng.choice(original_edges, size=keep_count, replace=False)
    h = nx.Graph()
    h.add_nodes_from(nodes)
    h.add_edges_from(chosen_edges)
    return h


def find_smoke_seeds(max_target_edge: int, required_seeds: int) -> List[int]:
    selected: List[int] = []
    for seed in range(51):
        world = World(
            SMOKE_CONFIG["N"],
            SMOKE_CONFIG["d"],
            SMOKE_CONFIG["model_mode"],
            SMOKE_CONFIG["epsilon_norm"],
            seed,
        )
        sim = SimulatorWithNodes(
            world=world,
            relation_variant=SMOKE_CONFIG["relation_variant"],
            alpha=SMOKE_CONFIG["alpha"],
            threshold=SMOKE_CONFIG["threshold"],
            beta=SMOKE_CONFIG["beta"],
            lambda_val=SMOKE_CONFIG["lambda_val"],
            baseline_count=SMOKE_CONFIG["baseline_count"],
        )
        for step in range(SMOKE_CONFIG["steps"]):
            sim.mutate_and_step(SMOKE_CONFIG["mutation_rate"], step_seed=seed * 100000 + step)

        cluster_nodes: Optional[Set[int]] = None
        if sim.valid_size(sim.current_indices) and sim.lifetime > 20:
            cluster_nodes = set(sim.current_indices)
        elif sim.best_sector_nodes is not None:
            cluster_nodes = sim.best_sector_nodes

        if not cluster_nodes:
            continue

        g_original = sim.build_graph(cluster_nodes)
        original_edge_count = g_original.number_of_edges()
        if original_edge_count >= max_target_edge:
            selected.append(seed)
            if len(selected) >= required_seeds:
                break

    return selected


def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["subsampling_method", "target_edge_count"]
    summary = df.groupby(keys).agg(
        attempted_runs_all=("seed", "count"),
        attempted_runs_reached=("target_reached", "sum"),
        target_reachable_count=("target_reachable", "sum"),
        target_reached_count=("target_reached", "sum"),
        target_reached_rate=("target_reached", "mean"),
        structure_success_rate_attempted=("structure_success", "mean"),
        structure_success_rate_analyzed=("structure_success", "mean"),
        mean_actual_edge_count=("actual_edge_count", "mean"),
        mean_original_edge_count=("original_edge_count", "mean"),
        mean_edge_removal_fraction=("edge_removal_fraction", "mean"),
        mean_sector_size=("sector_size", "mean"),
        mean_density=("density", "mean"),
        mean_n_components=("n_components", "mean"),
        mean_largest_component_fraction=("largest_component_fraction", "mean"),
        mean_degree_variance=("degree_variance", "mean"),
        failed_p_gnp_rate=("failed_p_gnp", "mean"),
        failed_p_dp_rate=("failed_p_dp", "mean"),
        failed_dp_valid_rate=("failed_dp_valid", "mean"),
        failed_lifetime_rate=("failed_lifetime", "mean"),
        failed_sector_size_rate=("failed_sector_size", "mean"),
        mean_dp_valid=("dp_valid", "mean"),
        mean_dp_swap_success_rate=("dp_swap_success_rate", "mean"),
    ).reset_index()
    reached = df[df["target_reached"]].groupby(keys).agg(
        structure_success_rate_attempted_reached=("structure_success", "mean"),
    ).reset_index()
    summary = summary.merge(reached, on=keys, how="left")
    summary["structure_success_rate_attempted_reached"] = summary["structure_success_rate_attempted_reached"].fillna(0.0)
    return summary


def run_smoke(out_prefix: str) -> None:
    rows: List[Dict[str, Any]] = []
    max_target_edge = max(SMOKE_CONFIG["target_edge_counts"])
    selected_seeds = find_smoke_seeds(max_target_edge, SMOKE_CONFIG["seeds"])
    if len(selected_seeds) < SMOKE_CONFIG["seeds"]:
        print(
            f"Warning: only found {len(selected_seeds)} reachable smoke seed(s) "
            f"for max_target_edge={max_target_edge}."
        )
    if not selected_seeds:
        raise RuntimeError(
            f"No smoke seeds found with original_edge_count >= {max_target_edge}."
        )

    for seed in selected_seeds:
        world = World(
            SMOKE_CONFIG["N"],
            SMOKE_CONFIG["d"],
            SMOKE_CONFIG["model_mode"],
            SMOKE_CONFIG["epsilon_norm"],
            seed,
        )
        sim = SimulatorWithNodes(
            world=world,
            relation_variant=SMOKE_CONFIG["relation_variant"],
            alpha=SMOKE_CONFIG["alpha"],
            threshold=SMOKE_CONFIG["threshold"],
            beta=SMOKE_CONFIG["beta"],
            lambda_val=SMOKE_CONFIG["lambda_val"],
            baseline_count=SMOKE_CONFIG["baseline_count"],
        )

        for step in range(SMOKE_CONFIG["steps"]):
            sim.mutate_and_step(SMOKE_CONFIG["mutation_rate"], step_seed=seed * 100000 + step)

        cluster_nodes: Optional[Set[int]] = None
        cluster_lifetime = 0
        if sim.valid_size(sim.current_indices) and sim.lifetime > 20:
            sim.deep_analysis(sim.current_indices, seed=seed * 99991 + SMOKE_CONFIG["steps"])
            cluster_nodes = set(sim.current_indices)
            cluster_lifetime = sim.lifetime
        elif sim.best_sector_nodes is not None:
            cluster_nodes = sim.best_sector_nodes
            cluster_lifetime = sim.best_sector_lifetime

        if not cluster_nodes:
            continue

        g_original = sim.build_graph(cluster_nodes)
        original_edge_count = g_original.number_of_edges()
        baseline_sim = SimulatorWithNodes(
            world=world,
            relation_variant=SMOKE_CONFIG["relation_variant"],
            alpha=SMOKE_CONFIG["alpha"],
            threshold=SMOKE_CONFIG["threshold"],
            beta=SMOKE_CONFIG["beta"],
            lambda_val=SMOKE_CONFIG["lambda_val"],
            baseline_count=SMOKE_CONFIG["baseline_count"],
        )

        for target_edge_count in SMOKE_CONFIG["target_edge_counts"]:
            for rep in range(SMOKE_CONFIG["repetitions_per_target"]):
                rng = np.random.default_rng(seed * 100000 + target_edge_count * 1000 + rep)
                subsampled = random_edge_removal(g_original, target_edge_count, rng)
                actual_edge_count = subsampled.number_of_edges()
                target_reachable = original_edge_count >= target_edge_count
                target_reached = target_reachable and actual_edge_count == target_edge_count
                if target_reachable:
                    reachability_reason = "reached" if target_reached else "failed_to_reach"
                else:
                    reachability_reason = "unreachable_original_edge_count"

                metrics = analyze_graph(
                    subsampled,
                    world,
                    cluster_lifetime,
                    SMOKE_CONFIG["baseline_count"],
                    analysis_seed=seed * 1000000 + target_edge_count * 100 + rep,
                    baseline_sim=baseline_sim,
                )
                rows.append(
                    {
                        "model_mode": SMOKE_CONFIG["model_mode"],
                        "relation_variant": SMOKE_CONFIG["relation_variant"],
                        "beta": SMOKE_CONFIG["beta"],
                        "seed": seed,
                        "subsample_rep": rep,
                        "target_edge_count": target_edge_count,
                        "actual_edge_count": actual_edge_count,
                        "original_edge_count": original_edge_count,
                        "edge_removal_count": max(0, original_edge_count - actual_edge_count),
                        "edge_removal_fraction": (
                            float(original_edge_count - actual_edge_count) / original_edge_count
                            if original_edge_count > 0
                            else 0.0
                        ),
                        "subsampling_method": SMOKE_CONFIG["subsampling_method"],
                        "target_reachable": bool(target_reachable),
                        "target_reached": bool(target_reached),
                        "reachability_reason": reachability_reason,
                        "N": SMOKE_CONFIG["N"],
                        "d": SMOKE_CONFIG["d"],
                        "steps": SMOKE_CONFIG["steps"],
                        "baseline_count": SMOKE_CONFIG["baseline_count"],
                        "mutation_rate": SMOKE_CONFIG["mutation_rate"],
                        **metrics,
                    }
                )

    df = pd.DataFrame(rows)
    os.makedirs("outputs", exist_ok=True)
    raw_path = f"outputs/raw_{out_prefix}.csv"
    summary_path = f"outputs/summary_{out_prefix}.csv"
    df.to_csv(raw_path, index=False)
    make_summary(df).to_csv(summary_path, index=False)
    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke"], default="smoke")
    parser.add_argument("--out-prefix", default="density_ablation_variant2")
    args = parser.parse_args()

    if args.mode == "smoke":
        run_smoke(args.out_prefix)
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")


if __name__ == "__main__":
    main()
