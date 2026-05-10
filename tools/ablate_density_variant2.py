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
    density-matched ablation tool

Status:
    smoke mode implemented and validated
    full mode implemented but not executed

Purpose:
    Generate density-matched ablation datasets for Variant 2 compensated graphs
    by randomly removing edges to target edge counts and recomputing raw
    connectivity diagnostics.

Allowed actions:
    Read experiment code.
    Run smoke ablation from a local .venv.
    Run full ablation only after explicit human authorization.

Forbidden actions:
    Do not modify experiment success criteria.
    Do not change existing experiment presets.
    Do not run the full density-matched ablation sweep without explicit authorization.
    Do not commit generated outputs by default.

Inputs:
    --mode smoke
    --mode full
    --mode lcf_smoke
    --out-prefix <prefix>

Outputs:
    outputs/raw_<prefix>.csv
    outputs/summary_<prefix>.csv
    outputs/per_seed_<prefix>.csv (full mode, lcf_smoke mode)

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
    "max_seed_scan": 51,
}

FULL_CONFIG = {
    **SMOKE_CONFIG,
    "target_edge_counts": [25, 30, 35, 40],
    "seeds": 100,
    "repetitions_per_target": 10,
    "baseline_count": 100,
    "subsampling_method": "random_edge_removal_preliminary",
    "max_seed_scan": 10000,
}

LCF_SMOKE_CONFIG = {
    **SMOKE_CONFIG,
    "target_edge_counts": [25, 30],
    "subsampling_method": "greedy_non_bridge_removal_with_LCF_constraint",
    "lcf_min_threshold": 0.85,
    "max_attempts_per_seed": 100,
}

LCF_FULL_CONFIG = {
    **SMOKE_CONFIG,
    "target_edge_counts": [25, 30, 35],
    "seeds": 100,
    "repetitions_per_target": 5,
    "baseline_count": 100,
    "subsampling_method": "greedy_non_bridge_removal_with_LCF_constraint",
    "lcf_min_threshold": 0.85,
    "max_attempts_per_seed": 100,
    "max_seed_scan": 10000,
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


def largest_component_fraction(g: nx.Graph) -> float:
    n = g.number_of_nodes()
    if n == 0:
        return 0.0
    components = list(nx.connected_components(g))
    largest_component = max((len(c) for c in components), default=0)
    return float(largest_component / n)


def lcf_constrained_edge_removal(
    g: nx.Graph,
    target_edge_count: int,
    lcf_min_threshold: float,
    rng: np.random.Generator,
    max_attempts: int,
) -> Tuple[nx.Graph, bool, bool, str, int, int]:
    h = g.copy()
    removal_attempts = 0
    removal_failures = 0
    while h.number_of_edges() > target_edge_count and removal_attempts < max_attempts:
        removal_attempts += 1
        bridge_edges = {tuple(sorted(e)) for e in nx.bridges(h)}
        candidates = [e for e in h.edges() if tuple(sorted(e)) not in bridge_edges]
        if not candidates:
            return h, False, largest_component_fraction(h) >= lcf_min_threshold, "failed_no_non_bridge_edges", removal_attempts, removal_failures

        edge = tuple(rng.choice(candidates))
        h_candidate = h.copy()
        h_candidate.remove_edge(*edge)
        lcf_after = largest_component_fraction(h_candidate)
        if lcf_after >= lcf_min_threshold:
            h = h_candidate
        else:
            removal_failures += 1

    actual_lcf = largest_component_fraction(h)
    target_reached = h.number_of_edges() == target_edge_count
    connectivity_preserved = actual_lcf >= lcf_min_threshold
    if not target_reached:
        if removal_attempts >= max_attempts:
            reason = "failed_max_attempts"
        else:
            reason = "not_reached"
    elif connectivity_preserved:
        reason = "preserved"
    else:
        reason = "failed_lcf_constraint"

    return h, target_reached, connectivity_preserved, reason, removal_attempts, removal_failures


def find_reachable_seeds(max_target_edge: int, required_seeds: int, config: Dict[str, Any]) -> List[int]:
    selected: List[int] = []
    for seed in range(config["max_seed_scan"]):
        world = World(
            config["N"],
            config["d"],
            config["model_mode"],
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
        structure_success_rate_attempted_all=("structure_success", "mean"),
        mean_actual_edge_count_all=("actual_edge_count", "mean"),
        mean_original_edge_count_all=("original_edge_count", "mean"),
    ).reset_index()
    reached_df = df[df["target_reached"]]
    reached = reached_df.groupby(keys).agg(
        structure_success_rate_attempted_reached=("structure_success", "mean"),
        structure_success_rate_analyzed_reached=("structure_success", "mean"),
        mean_actual_edge_count_reached=("actual_edge_count", "mean"),
        mean_edge_removal_fraction_reached=("edge_removal_fraction", "mean"),
        mean_sector_size_reached=("sector_size", "mean"),
        mean_density_reached=("density", "mean"),
        mean_n_components_reached=("n_components", "mean"),
        mean_largest_component_fraction_reached=("largest_component_fraction", "mean"),
        mean_degree_variance_reached=("degree_variance", "mean"),
        failed_p_gnp_rate_reached=("failed_p_gnp", "mean"),
        failed_p_dp_rate_reached=("failed_p_dp", "mean"),
        failed_dp_valid_rate_reached=("failed_dp_valid", "mean"),
        failed_lifetime_rate_reached=("failed_lifetime", "mean"),
        failed_sector_size_rate_reached=("failed_sector_size", "mean"),
        mean_dp_valid_reached=("dp_valid", "mean"),
        mean_dp_swap_success_rate_reached=("dp_swap_success_rate", "mean"),
    ).reset_index()
    summary = summary.merge(reached, on=keys, how="left")
    # Fill NaN with appropriate defaults
    summary["structure_success_rate_attempted_reached"] = summary["structure_success_rate_attempted_reached"].fillna(0.0)
    summary["structure_success_rate_analyzed_reached"] = summary["structure_success_rate_analyzed_reached"].fillna(0.0)
    return summary


def make_per_seed(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["target_edge_count", "seed"]
    per_seed = df[df["target_reached"]].groupby(keys).agg(
        reached_repetitions=("target_reached", "count"),
        success_count=("structure_success", "sum"),
        success_fraction_per_seed_target=("structure_success", "mean"),
        majority_success_per_seed_target=("structure_success", lambda x: (x.sum() > len(x) / 2).astype(int)),
        mean_largest_component_fraction_per_seed_target=("largest_component_fraction", "mean"),
        mean_failed_p_gnp_per_seed_target=("failed_p_gnp", "mean"),
        mean_sector_size_per_seed_target=("sector_size", "mean"),
    ).reset_index()
    return per_seed


def make_lcf_summary(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["subsampling_method", "target_edge_count"]
    summary = df.groupby(keys).agg(
        attempted_runs_all=("seed", "count"),
        target_reached_count=("target_reached", "sum"),
        target_reached_rate=("target_reached", "mean"),
        target_connectivity_preserved_count=("target_connectivity_preserved", "sum"),
        target_connectivity_preserved_rate=("target_connectivity_preserved", "mean"),
        valid_lcf_matched_count=("valid_lcf_matched", "sum"),
        valid_lcf_matched_rate=("valid_lcf_matched", "mean"),
        mean_removal_attempts=("removal_attempts", "mean"),
        mean_removal_failures=("removal_failures", "mean"),
        failed_no_non_bridge_edges_count=("connectivity_preservation_reason", lambda x: (x == "failed_no_non_bridge_edges").sum()),
        failed_max_attempts_count=("connectivity_preservation_reason", lambda x: (x == "failed_max_attempts").sum()),
        failed_lcf_constraint_count=("connectivity_preservation_reason", lambda x: (x == "failed_lcf_constraint").sum()),
        preserved_count=("connectivity_preservation_reason", lambda x: (x == "preserved").sum()),
    ).reset_index()
    summary["failed_no_non_bridge_edges_rate"] = summary["failed_no_non_bridge_edges_count"] / summary["attempted_runs_all"]
    summary["failed_max_attempts_rate"] = summary["failed_max_attempts_count"] / summary["attempted_runs_all"]
    summary["failed_lcf_constraint_rate"] = summary["failed_lcf_constraint_count"] / summary["attempted_runs_all"]
    summary["preserved_rate"] = summary["preserved_count"] / summary["attempted_runs_all"]

    valid_df = df[df["valid_lcf_matched"]]
    valid = valid_df.groupby(keys).agg(
        structure_success_rate_valid=("structure_success", "mean"),
        mean_actual_edge_count_valid=("actual_edge_count", "mean"),
        mean_largest_component_fraction_valid=("largest_component_fraction", "mean"),
        mean_n_components_valid=("n_components", "mean"),
        mean_degree_variance_valid=("degree_variance", "mean"),
        mean_sector_size_valid=("sector_size", "mean"),
        failed_p_gnp_rate_valid=("failed_p_gnp", "mean"),
        failed_p_dp_rate_valid=("failed_p_dp", "mean"),
        failed_dp_valid_rate_valid=("failed_dp_valid", "mean"),
        mean_dp_valid_valid=("dp_valid", "mean"),
        mean_dp_swap_success_rate_valid=("dp_swap_success_rate", "mean"),
    ).reset_index()
    summary = summary.merge(valid, on=keys, how="left")
    summary = summary.fillna(
        {
            "structure_success_rate_valid": 0.0,
            "mean_actual_edge_count_valid": 0.0,
            "mean_largest_component_fraction_valid": 0.0,
            "mean_n_components_valid": 0.0,
            "mean_degree_variance_valid": 0.0,
            "mean_sector_size_valid": 0.0,
            "failed_p_gnp_rate_valid": 0.0,
            "failed_p_dp_rate_valid": 0.0,
            "failed_dp_valid_rate_valid": 0.0,
            "mean_dp_valid_valid": 0.0,
            "mean_dp_swap_success_rate_valid": 0.0,
        }
    )
    return summary


def make_lcf_per_seed(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["target_edge_count", "seed"]
    all_group = df.groupby(keys).agg(
        connectivity_preservation_fraction_per_seed_target=("target_connectivity_preserved", "mean"),
        failed_no_non_bridge_edges_count=("connectivity_preservation_reason", lambda x: (x == "failed_no_non_bridge_edges").sum()),
        failed_max_attempts_count=("connectivity_preservation_reason", lambda x: (x == "failed_max_attempts").sum()),
        failed_lcf_constraint_count=("connectivity_preservation_reason", lambda x: (x == "failed_lcf_constraint").sum()),
        preserved_count=("connectivity_preservation_reason", lambda x: (x == "preserved").sum()),
    )
    valid_group = df[df["valid_lcf_matched"]].groupby(keys).agg(
        valid_repetitions=("valid_lcf_matched", "count"),
        success_count_valid=("structure_success", "sum"),
        success_fraction_per_seed_target_valid=("structure_success", "mean"),
        mean_largest_component_fraction_per_seed_target_valid=("largest_component_fraction", "mean"),
        mean_failed_p_gnp_per_seed_target_valid=("failed_p_gnp", "mean"),
        mean_sector_size_per_seed_target_valid=("sector_size", "mean"),
    )
    per_seed = all_group.join(valid_group, how="left").reset_index()
    per_seed["valid_repetitions"] = per_seed["valid_repetitions"].fillna(0).astype(int)
    per_seed["success_count_valid"] = per_seed["success_count_valid"].fillna(0).astype(int)
    per_seed["success_fraction_per_seed_target_valid"] = per_seed["success_fraction_per_seed_target_valid"].fillna(0.0)
    per_seed["majority_success_per_seed_target_valid"] = (
        (per_seed["success_count_valid"] > (per_seed["valid_repetitions"] / 2)).astype(int)
    )
    per_seed["mean_largest_component_fraction_per_seed_target_valid"] = per_seed["mean_largest_component_fraction_per_seed_target_valid"].fillna(0.0)
    per_seed["mean_failed_p_gnp_per_seed_target_valid"] = per_seed["mean_failed_p_gnp_per_seed_target_valid"].fillna(0.0)
    per_seed["mean_sector_size_per_seed_target_valid"] = per_seed["mean_sector_size_per_seed_target_valid"].fillna(0.0)
    per_seed["connectivity_preservation_fraction_per_seed_target"] = per_seed["connectivity_preservation_fraction_per_seed_target"].fillna(0.0)
    per_seed["failed_no_non_bridge_edges_count"] = per_seed["failed_no_non_bridge_edges_count"].fillna(0).astype(int)
    per_seed["failed_max_attempts_count"] = per_seed["failed_max_attempts_count"].fillna(0).astype(int)
    per_seed["failed_lcf_constraint_count"] = per_seed["failed_lcf_constraint_count"].fillna(0).astype(int)
    per_seed["preserved_count"] = per_seed["preserved_count"].fillna(0).astype(int)
    return per_seed


def run_smoke(out_prefix: str) -> None:
    rows: List[Dict[str, Any]] = []
    max_target_edge = max(SMOKE_CONFIG["target_edge_counts"])
    selected_seeds = find_reachable_seeds(max_target_edge, SMOKE_CONFIG["seeds"], SMOKE_CONFIG)
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


def run_full(out_prefix: str) -> None:
    rows: List[Dict[str, Any]] = []
    max_target_edge = max(FULL_CONFIG["target_edge_counts"])
    selected_seeds = find_reachable_seeds(max_target_edge, FULL_CONFIG["seeds"], FULL_CONFIG)
    if len(selected_seeds) < FULL_CONFIG["seeds"]:
        print(
            f"Warning: only found {len(selected_seeds)} reachable full seed(s) "
            f"for max_target_edge={max_target_edge}."
        )
    if not selected_seeds:
        raise RuntimeError(
            f"No full seeds found with original_edge_count >= {max_target_edge}."
        )

    for seed in selected_seeds:
        world = World(
            FULL_CONFIG["N"],
            FULL_CONFIG["d"],
            FULL_CONFIG["model_mode"],
            FULL_CONFIG["epsilon_norm"],
            seed,
        )
        sim = SimulatorWithNodes(
            world=world,
            relation_variant=FULL_CONFIG["relation_variant"],
            alpha=FULL_CONFIG["alpha"],
            threshold=FULL_CONFIG["threshold"],
            beta=FULL_CONFIG["beta"],
            lambda_val=FULL_CONFIG["lambda_val"],
            baseline_count=FULL_CONFIG["baseline_count"],
        )

        for step in range(FULL_CONFIG["steps"]):
            sim.mutate_and_step(FULL_CONFIG["mutation_rate"], step_seed=seed * 100000 + step)

        cluster_nodes: Optional[Set[int]] = None
        cluster_lifetime = 0
        if sim.valid_size(sim.current_indices) and sim.lifetime > 20:
            sim.deep_analysis(sim.current_indices, seed=seed * 99991 + FULL_CONFIG["steps"])
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
            relation_variant=FULL_CONFIG["relation_variant"],
            alpha=FULL_CONFIG["alpha"],
            threshold=FULL_CONFIG["threshold"],
            beta=FULL_CONFIG["beta"],
            lambda_val=FULL_CONFIG["lambda_val"],
            baseline_count=FULL_CONFIG["baseline_count"],
        )

        for target_edge_count in FULL_CONFIG["target_edge_counts"]:
            for rep in range(FULL_CONFIG["repetitions_per_target"]):
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
                    FULL_CONFIG["baseline_count"],
                    analysis_seed=seed * 1000000 + target_edge_count * 100 + rep,
                    baseline_sim=baseline_sim,
                )
                rows.append(
                    {
                        "model_mode": FULL_CONFIG["model_mode"],
                        "relation_variant": FULL_CONFIG["relation_variant"],
                        "beta": FULL_CONFIG["beta"],
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
                        "subsampling_method": FULL_CONFIG["subsampling_method"],
                        "target_reachable": bool(target_reachable),
                        "target_reached": bool(target_reached),
                        "reachability_reason": reachability_reason,
                        "N": FULL_CONFIG["N"],
                        "d": FULL_CONFIG["d"],
                        "steps": FULL_CONFIG["steps"],
                        "baseline_count": FULL_CONFIG["baseline_count"],
                        "mutation_rate": FULL_CONFIG["mutation_rate"],
                        **metrics,
                    }
                )

    df = pd.DataFrame(rows)
    os.makedirs("outputs", exist_ok=True)
    raw_path = f"outputs/raw_{out_prefix}.csv"
    summary_path = f"outputs/summary_{out_prefix}.csv"
    per_seed_path = f"outputs/per_seed_{out_prefix}.csv"
    df.to_csv(raw_path, index=False)
    make_summary(df).to_csv(summary_path, index=False)
    make_per_seed(df).to_csv(per_seed_path, index=False)
    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {per_seed_path}")


def run_lcf_ablation(config: Dict[str, Any], out_prefix: str) -> None:
    rows: List[Dict[str, Any]] = []
    max_target_edge = max(config["target_edge_counts"])
    selected_seeds = find_reachable_seeds(max_target_edge, config["seeds"], config)
    if len(selected_seeds) < config["seeds"]:
        print(
            f"Warning: only found {len(selected_seeds)} reachable {config['subsampling_method']} seed(s) "
            f"for max_target_edge={max_target_edge}."
        )
    if not selected_seeds:
        raise RuntimeError(
            f"No {config['subsampling_method']} seeds found with original_edge_count >= {max_target_edge}."
        )

    for seed in selected_seeds:
        world = World(
            config["N"],
            config["d"],
            config["model_mode"],
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
            continue

        g_original = sim.build_graph(cluster_nodes)
        original_edge_count = g_original.number_of_edges()
        baseline_sim = SimulatorWithNodes(
            world=world,
            relation_variant=config["relation_variant"],
            alpha=config["alpha"],
            threshold=config["threshold"],
            beta=config["beta"],
            lambda_val=config["lambda_val"],
            baseline_count=config["baseline_count"],
        )

        for target_edge_count in config["target_edge_counts"]:
            for rep in range(config["repetitions_per_target"]):
                rng = np.random.default_rng(seed * 100000 + target_edge_count * 1000 + rep)
                subsampled, target_reached, target_connectivity_preserved, connectivity_preservation_reason, removal_attempts, removal_failures = lcf_constrained_edge_removal(
                    g_original,
                    target_edge_count,
                    config["lcf_min_threshold"],
                    rng,
                    config["max_attempts_per_seed"],
                )
                actual_edge_count = subsampled.number_of_edges()
                target_reachable = original_edge_count >= target_edge_count
                target_reached_flag = target_reachable and actual_edge_count == target_edge_count
                if target_reachable:
                    reachability_reason = "reached" if target_reached_flag else "failed_to_reach"
                else:
                    reachability_reason = "unreachable_original_edge_count"

                actual_lcf = largest_component_fraction(subsampled)
                valid_lcf_matched = bool(target_reached_flag and target_connectivity_preserved)

                metrics = analyze_graph(
                    subsampled,
                    world,
                    cluster_lifetime,
                    config["baseline_count"],
                    analysis_seed=seed * 1000000 + target_edge_count * 100 + rep,
                    baseline_sim=baseline_sim,
                )
                rows.append(
                    {
                        "model_mode": config["model_mode"],
                        "relation_variant": config["relation_variant"],
                        "beta": config["beta"],
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
                        "subsampling_method": config["subsampling_method"],
                        "target_reachable": bool(target_reachable),
                        "target_reached": bool(target_reached_flag),
                        "reachability_reason": reachability_reason,
                        "target_connectivity_preserved": bool(target_connectivity_preserved),
                        "connectivity_preservation_reason": connectivity_preservation_reason,
                        "lcf_min_threshold": config["lcf_min_threshold"],
                        "actual_largest_component_fraction": actual_lcf,
                        "removal_attempts": removal_attempts,
                        "removal_failures": removal_failures,
                        "valid_lcf_matched": bool(valid_lcf_matched),
                        "N": config["N"],
                        "d": config["d"],
                        "steps": config["steps"],
                        "baseline_count": config["baseline_count"],
                        "mutation_rate": config["mutation_rate"],
                        **metrics,
                    }
                )

    df = pd.DataFrame(rows)
    os.makedirs("outputs", exist_ok=True)
    raw_path = f"outputs/raw_{out_prefix}.csv"
    summary_path = f"outputs/summary_{out_prefix}.csv"
    per_seed_path = f"outputs/per_seed_{out_prefix}.csv"
    reason_path = f"outputs/reason_counts_{out_prefix}.csv"
    df.to_csv(raw_path, index=False)
    make_lcf_summary(df).to_csv(summary_path, index=False)
    make_lcf_per_seed(df).to_csv(per_seed_path, index=False)
    df[["subsampling_method", "target_edge_count", "connectivity_preservation_reason"]].groupby(
        ["subsampling_method", "target_edge_count", "connectivity_preservation_reason"]
    ).size().reset_index(name="count").to_csv(reason_path, index=False)
    print(f"Wrote {raw_path}")
    print(f"Wrote {summary_path}")
    print(f"Wrote {per_seed_path}")
    print(f"Wrote {reason_path}")


def run_lcf_smoke(out_prefix: str) -> None:
    run_lcf_ablation(LCF_SMOKE_CONFIG, out_prefix)


def run_lcf_full(out_prefix: str) -> None:
    run_lcf_ablation(LCF_FULL_CONFIG, out_prefix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["smoke", "full", "lcf_smoke", "lcf_full"], default="smoke")
    parser.add_argument("--out-prefix", default="density_ablation_variant2")
    args = parser.parse_args()

    if args.mode == "smoke":
        run_smoke(args.out_prefix)
    elif args.mode == "full":
        run_full(args.out_prefix)
    elif args.mode == "lcf_smoke":
        run_lcf_smoke(args.out_prefix)
    elif args.mode == "lcf_full":
        run_lcf_full(args.out_prefix)
    else:
        raise ValueError(f"Unsupported mode: {args.mode}")


if __name__ == "__main__":
    main()
