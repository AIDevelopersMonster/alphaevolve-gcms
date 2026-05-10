"""
AlphaEvolve-GCMS v0.10.2

Methodology-correction experiment for GCMS.

Why v0.10 exists:
- v0.9.1 used R_ij = exp(-alpha * ||I_i - I_j||^2).
- Global compensation was implemented as subtracting the mean vector.
- Subtracting the same mean from all vectors does not change pairwise distances.
- Therefore v0.9.1 could show non-random local graph sectors, but could not
  prove that global compensation caused them.

This script separates:
- compensation_valid: whether global sum is numerically zero;
- structure_success: whether a local sector is statistically non-random;
- strict_success: compensation_valid AND structure_success.

It compares compensated, uncompensated, and residual modes across relation variants.

Allowed actions:
    Run simulations and write outputs/raw_*.csv, summary_*.csv,
    comparison_*.csv, residual_*.csv.

Forbidden actions:
    Do not change success criteria after seeing results.
    Do not commit generated CSV outputs unless explicitly archived.
    Do not claim physical theory from toy-model outputs.

Inputs:
    CLI arguments: --mode, --out-prefix

Outputs:
    outputs/raw_<prefix>.csv
    outputs/summary_<prefix>.csv
    outputs/comparison_<prefix>.csv
    outputs/residual_<prefix>.csv

Output policy:
    Generated outputs are local artifacts and should normally remain untracked.
    Interpretations belong in docs/results/.

Verification:
    python -m py_compile experiments/ae_v010_2.py
    python experiments/ae_v010_2.py --mode smoke_v010 --out-prefix v010_smoke
    Check expected output files and required columns.

Last updated:
    2026-05-10
"""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from itertools import product
from typing import Any, Dict, Iterable, List, Optional, Set, Tuple

import networkx as nx
import numpy as np
import pandas as pd


PRESETS = {
    "smoke_v010": {
        "N": 80,
        "d": 4,
        "steps": 25,
        "seeds": 2,
        "baseline_count": 10,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated"],
        "relation_variants": [0, 2, 4],
        "betas": [0.0, 0.05],
        "epsilon_norms": [0.0],
        "lambda_values": [0.0, 0.01],
    },
    "mini_v010": {
        "N": 100,
        "d": 4,
        "steps": 50,
        "seeds": 3,
        "baseline_count": 20,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated", "residual"],
        "relation_variants": [0, 2, 3, 4],
        "betas": [0.0, 0.05],
        "epsilon_norms": [0.0, 1e-2],
        "lambda_values": [0.0, 0.01],
    },
    "local_v010": {
        "N": 150,
        "d": 4,
        "steps": 200,
        "seeds": 50,
        "baseline_count": 100,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated", "residual"],
        "relation_variants": [0, 1, 2, 3, 4],
        "betas": [0.0, 0.05, 0.5],
        "epsilon_norms": [0.0, 1e-2, 1e-1],
        "lambda_values": [0.0, 0.001, 0.01, 0.05],
    },
    "focused_v010": {
        "N": 150,
        "d": 4,
        "steps": 200,
        "seeds": 50,
        "baseline_count": 100,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated"],
        "relation_variants": [0, 2],
        "betas": [0.0, 0.05, 0.5],
        "epsilon_norms": [0.0],
        "lambda_values": [0.0],
    },
    "beta_grid_v010": {
        "N": 150,
        "d": 4,
        "steps": 200,
        "seeds": 50,
        "baseline_count": 100,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated"],
        "relation_variants": [2],
        "betas": [0.0, 0.001, 0.002, 0.005, 0.01, 0.02, 0.05],
        "epsilon_norms": [0.0],
        "lambda_values": [0.0],
    },
    "fine_beta_v010": {
        "N": 150,
        "d": 4,
        "steps": 200,
        "seeds": 100,
        "baseline_count": 100,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated"],
        "relation_variants": [2],
        "betas": [0.003, 0.004, 0.005, 0.006, 0.007, 0.008],
        "epsilon_norms": [0.0],
        "lambda_values": [0.0],
    },
    "confirm_connectivity_variant2": {
        "N": 150,
        "d": 4,
        "steps": 200,
        "seeds": 100,
        "baseline_count": 100,
        "alpha": 0.5,
        "threshold": 0.75,
        "mutation_rate": 0.10,
        "model_modes": ["compensated", "uncompensated"],
        "relation_variants": [2],
        "betas": [0.003, 0.005, 0.007],
        "epsilon_norms": [0.0],
        "lambda_values": [0.0],
    },
}


@dataclass
class State:
    idx: int
    v: np.ndarray


class World:
    def __init__(self, N: int, d: int, mode: str, epsilon_norm: float, seed: int):
        self.N = N
        self.d = d
        self.mode = mode
        self.rng = np.random.default_rng(seed)

        raw = self.rng.standard_normal((N, d))

        if mode == "compensated":
            data = raw - raw.mean(axis=0)
        elif mode == "uncompensated":
            data = raw
        elif mode == "residual":
            eps_vec = self.rng.standard_normal(d)
            norm = np.linalg.norm(eps_vec)
            if norm == 0:
                eps_vec = np.zeros(d)
            else:
                eps_vec = eps_vec / norm * epsilon_norm
            data = (raw - raw.mean(axis=0)) + eps_vec / N
        else:
            raise ValueError(f"Unknown mode: {mode}")

        self.states = [State(i, data[i].astype(float).copy()) for i in range(N)]

    def matrix(self) -> np.ndarray:
        return np.vstack([s.v for s in self.states])

    def global_vector(self) -> np.ndarray:
        return self.matrix().sum(axis=0)

    def global_error(self) -> float:
        return float(np.linalg.norm(self.global_vector()))

    def mutate_pairwise(self, mutation_rate: float):
        a, b = self.rng.choice(self.N, size=2, replace=False)
        delta = self.rng.normal(size=self.d) * mutation_rate
        self.states[a].v += delta
        self.states[b].v -= delta

    def apply_pressure_to_zero(self, lambda_val: float):
        if lambda_val <= 0:
            return
        K = self.global_vector()
        correction = lambda_val * K / self.N
        for s in self.states:
            s.v -= correction


class Simulator:
    def __init__(
        self,
        world: World,
        relation_variant: int,
        alpha: float,
        threshold: float,
        beta: float,
        lambda_val: float,
        baseline_count: int,
        min_size: int = 5,
        max_size: int = 60,
        overlap_limit: float = 0.5,
    ):
        self.world = world
        self.relation_variant = relation_variant
        self.alpha = alpha
        self.threshold = threshold
        self.beta = beta
        self.lambda_val = lambda_val
        self.baseline_count = baseline_count
        self.min_size = min_size
        self.max_size = max_size
        self.overlap_limit = overlap_limit

        self.current_indices: Set[int] = set()
        self.lifetime = 0
        self.best_sector_data: Optional[Dict[str, Any]] = None
        self.total_valid_steps = 0
        self.birth_count = 0
        self.death_count = 0

    def valid_size(self, nodes: Set[int]) -> bool:
        return self.min_size <= len(nodes) <= self.max_size

    def relation(self, i: int, j: int, K: np.ndarray) -> float:
        vi = self.world.states[i].v
        vj = self.world.states[j].v
        dist_sq = float(np.sum((vi - vj) ** 2))

        if self.relation_variant in (0, 4):
            return float(np.exp(-self.alpha * dist_sq))

        if self.relation_variant == 1:
            return float(np.exp(-self.alpha * dist_sq) * np.exp(-self.beta * float(np.sum(K**2))))

        if self.relation_variant == 2:
            alignment = abs(float(np.dot(vi + vj, K)))
            return float(np.exp(-self.alpha * dist_sq - self.beta * alignment))

        if self.relation_variant == 3:
            pair_residual_sq = float(np.sum((vi + vj) ** 2))
            return float(np.exp(-self.alpha * dist_sq - self.beta * pair_residual_sq))

        raise ValueError(f"Unknown relation_variant: {self.relation_variant}")

    def build_graph(self, nodes: Iterable[int]) -> nx.Graph:
        nodes_list = list(nodes)
        g = nx.Graph()
        g.add_nodes_from(nodes_list)
        K = self.world.global_vector()

        for a in range(len(nodes_list)):
            ia = nodes_list[a]
            for b in range(a + 1, len(nodes_list)):
                ib = nodes_list[b]
                if self.relation(ia, ib, K) > self.threshold:
                    g.add_edge(ia, ib)
        return g

    def clusters(self) -> List[Set[int]]:
        g = self.build_graph(range(self.world.N))
        return [set(c) for c in nx.connected_components(g)]

    def chi(self, nodes: Set[int]) -> float:
        if not nodes:
            return 0.0
        vec = sum((self.world.states[i].v for i in nodes), np.zeros(self.world.d))
        return float(np.linalg.norm(vec))

    def best_valid_cluster_by_chi(self, clusters: List[Set[int]]) -> Set[int]:
        best: Set[int] = set()
        best_chi = -1.0
        for c in clusters:
            if self.valid_size(c):
                c_chi = self.chi(c)
                if c_chi > best_chi:
                    best_chi = c_chi
                    best = set(c)
        return best

    @staticmethod
    def edge_signature(g: nx.Graph) -> Set[frozenset]:
        return set(map(frozenset, g.edges()))

    @staticmethod
    def empirical_p_greater(observed: float, baseline: List[float]) -> float:
        if not baseline:
            return 1.0
        return float((1 + sum(x >= observed for x in baseline)) / (len(baseline) + 1))

    def degree_preserving_baseline(self, g: nx.Graph, rng: np.random.Generator) -> Tuple[List[float], float]:
        m = g.number_of_edges()
        if m < 2:
            return [], 0.0

        original = self.edge_signature(g)
        samples: List[float] = []

        for _ in range(self.baseline_count):
            dg = g.copy()
            seed = int(rng.integers(0, 2**31 - 1))
            try:
                nx.double_edge_swap(
                    dg,
                    nswap=max(1, 5 * m),
                    max_tries=max(100, 50 * m),
                    seed=seed,
                )
            except (nx.NetworkXError, nx.NetworkXAlgorithmError):
                continue

            if self.edge_signature(dg) != original:
                samples.append(float(nx.average_clustering(dg)))

        return samples, len(samples) / max(1, self.baseline_count)

    def deep_analysis(self, nodes: Set[int], seed: int) -> Optional[Dict[str, Any]]:
        if not self.valid_size(nodes):
            return None

        g = self.build_graph(nodes)
        n = g.number_of_nodes()
        m = g.number_of_edges()
        if n < self.min_size or n > self.max_size or m < 1:
            return None

        clustering = float(nx.average_clustering(g))
        density = float(nx.density(g))
        components = list(nx.connected_components(g))
        n_components = len(components)
        largest_component = max((len(c) for c in components), default=0)
        largest_component_fraction = float(largest_component / n) if n else 0.0
        degrees = np.array([deg for _, deg in g.degree()], dtype=float)
        degree_variance = float(np.var(degrees)) if len(degrees) else 0.0
        rng = np.random.default_rng(seed)

        gnp_clusts: List[float] = []
        for _ in range(self.baseline_count):
            rg_seed = int(rng.integers(0, 2**31 - 1))
            rg = nx.fast_gnp_random_graph(n, density, seed=rg_seed)
            gnp_clusts.append(float(nx.average_clustering(rg)))

        dp_clusts, dp_swap_success_rate = self.degree_preserving_baseline(g, rng)
        dp_valid = len(dp_clusts) >= min(30, self.baseline_count)

        p_gnp = self.empirical_p_greater(clustering, gnp_clusts)
        p_dp = self.empirical_p_greater(clustering, dp_clusts) if dp_valid else 1.0

        structure_success = (
            p_gnp < 0.05
            and p_dp < 0.05
            and dp_valid
            and self.lifetime > 20
            and self.min_size <= n <= self.max_size
        )

        return {
            "sector_size": n,
            "edge_count": m,
            "density": density,
            "clustering": clustering,
            "chi": self.chi(set(g.nodes())),
            "lifetime": int(self.lifetime),
            "p_gnp_empirical": p_gnp,
            "p_dp_empirical": p_dp,
            "dp_valid": bool(dp_valid),
            "dp_swap_success_rate": float(dp_swap_success_rate),
            "structure_success": bool(structure_success),
            "n_components": n_components,
            "largest_component_fraction": largest_component_fraction,
            "degree_variance": degree_variance,
        }

    def mutate_and_step(self, mutation_rate: float, step_seed: int):
        self.world.mutate_pairwise(mutation_rate)
        if self.relation_variant == 4:
            self.world.apply_pressure_to_zero(self.lambda_val)
        self.update(step_seed)

    def update(self, step_seed: int):
        clusters = self.clusters()

        successor: Set[int] = set()
        best_overlap = -1.0
        if self.current_indices:
            for c in clusters:
                union = len(self.current_indices | c)
                overlap = len(self.current_indices & c) / union if union else 0.0
                if overlap > self.overlap_limit and overlap > best_overlap:
                    best_overlap = overlap
                    successor = set(c)

        if successor:
            self.current_indices = successor
            self.lifetime += 1
            if self.valid_size(successor):
                self.total_valid_steps += 1
            return

        if self.current_indices and self.lifetime > 20 and self.valid_size(self.current_indices):
            data = self.deep_analysis(self.current_indices, step_seed)
            if data is not None:
                if self.best_sector_data is None or data["lifetime"] > self.best_sector_data["lifetime"]:
                    self.best_sector_data = data

        if self.current_indices:
            self.death_count += 1

        new_c = self.best_valid_cluster_by_chi(clusters)
        if new_c:
            self.birth_count += 1
            self.current_indices = new_c
            self.lifetime = 1
            self.total_valid_steps += 1
        else:
            self.current_indices = set()
            self.lifetime = 0


def valid_combo(model_mode: str, variant: int, beta: float, epsilon_norm: float, lambda_val: float) -> bool:
    if model_mode != "residual" and epsilon_norm != 0.0:
        return False
    if variant == 0 and (beta != 0.0 or lambda_val != 0.0):
        return False
    if variant in (1, 2, 3) and lambda_val != 0.0:
        return False
    if variant == 4 and beta != 0.0:
        return False
    return True


def run_single(cfg: Dict[str, Any], model_mode: str, variant: int, beta: float, epsilon_norm: float, lambda_val: float, seed: int) -> Dict[str, Any]:
    world = World(cfg["N"], cfg["d"], model_mode, epsilon_norm, seed)
    sim = Simulator(
        world,
        relation_variant=variant,
        alpha=cfg["alpha"],
        threshold=cfg["threshold"],
        beta=beta,
        lambda_val=lambda_val,
        baseline_count=cfg["baseline_count"],
    )

    for step in range(cfg["steps"]):
        sim.mutate_and_step(cfg["mutation_rate"], step_seed=seed * 100000 + step)

    final = None
    if sim.valid_size(sim.current_indices) and sim.lifetime > 20:
        final = sim.deep_analysis(sim.current_indices, seed=seed * 99991 + cfg["steps"])

    data = final if final is not None else sim.best_sector_data
    analyzed = data is not None

    if data is None:
        data = {
            "sector_size": 0,
            "edge_count": 0,
            "density": 0.0,
            "clustering": 0.0,
            "chi": 0.0,
            "lifetime": 0,
            "p_gnp_empirical": 1.0,
            "p_dp_empirical": 1.0,
            "dp_valid": False,
            "dp_swap_success_rate": 0.0,
            "structure_success": False,
            "n_components": 0,
            "largest_component_fraction": 0.0,
            "degree_variance": 0.0,
        }

    failed_p_gnp = data["p_gnp_empirical"] >= 0.05
    failed_dp_valid = not bool(data["dp_valid"])
    failed_p_dp = bool(data["dp_valid"]) and data["p_dp_empirical"] >= 0.05
    failed_lifetime = int(data["lifetime"]) <= 20
    failed_sector_size = int(data["sector_size"]) < sim.min_size or int(data["sector_size"]) > sim.max_size

    # NOTE: failed_sector_size is based on the raw sector_size field. If sector_size is zero or out of allowed bounds,
    # it is considered a sector-size failure. The current simulator only returns valid sectors for deep_analysis.

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

    global_error = world.global_error()
    compensation_valid = global_error < 1e-12
    strict_success = bool(compensation_valid and data["structure_success"])
    failure_reason = "|".join(failure_reasons)

    return {
        "model_mode": model_mode,
        "relation_variant": variant,
        "alpha": cfg["alpha"],
        "threshold": cfg["threshold"],
        "beta": beta,
        "epsilon_norm": epsilon_norm,
        "lambda_val": lambda_val,
        "seed": seed,
        "N": cfg["N"],
        "d": cfg["d"],
        "steps": cfg["steps"],
        "baseline_count": cfg["baseline_count"],
        "mutation_rate": cfg["mutation_rate"],
        "global_error": global_error,
        "compensation_valid": compensation_valid,
        "strict_success": strict_success,
        "analyzed": analyzed,
        "failure_reason": failure_reason,
        "failed_p_gnp": bool(failed_p_gnp),
        "failed_p_dp": bool(failed_p_dp),
        "failed_dp_valid": bool(failed_dp_valid),
        "failed_lifetime": bool(failed_lifetime),
        "failed_sector_size": bool(failed_sector_size),
        **data,
    }


def make_summary(df: pd.DataFrame) -> pd.DataFrame:
    keys = ["model_mode", "relation_variant", "beta", "epsilon_norm", "lambda_val"]
    summary = df.groupby(keys).agg(
        attempted_runs=("seed", "count"),
        analyzed_runs=("analyzed", "sum"),
        compensation_rate=("compensation_valid", "mean"),
        structure_success_rate_attempted=("structure_success", "mean"),
        strict_success_rate_attempted=("strict_success", "mean"),
        mean_global_error=("global_error", "mean"),
        mean_lifetime=("lifetime", "mean"),
        mean_sector_size=("sector_size", "mean"),
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

    analyzed = df[df["analyzed"]].groupby(keys).agg(
        structure_success_rate_analyzed=("structure_success", "mean"),
        strict_success_rate_analyzed=("strict_success", "mean"),
    ).reset_index()

    summary = summary.merge(analyzed, on=keys, how="left")
    summary["structure_success_rate_analyzed"] = summary["structure_success_rate_analyzed"].fillna(0.0)
    summary["strict_success_rate_analyzed"] = summary["strict_success_rate_analyzed"].fillna(0.0)
    return summary


def make_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    base_keys = ["relation_variant", "beta", "lambda_val"]
    comp = summary[(summary["model_mode"] == "compensated") & (summary["epsilon_norm"] == 0.0)].copy()
    uncomp = summary[(summary["model_mode"] == "uncompensated") & (summary["epsilon_norm"] == 0.0)].copy()

    keep = base_keys + [
        "structure_success_rate_attempted",
        "structure_success_rate_analyzed",
        "strict_success_rate_attempted",
        "strict_success_rate_analyzed",
        "mean_global_error",
        "analyzed_runs",
    ]

    merged = comp[keep].merge(uncomp[keep], on=base_keys, suffixes=("_comp", "_uncomp"))
    merged["compensation_effect_attempted"] = (
        merged["structure_success_rate_attempted_comp"] - merged["structure_success_rate_attempted_uncomp"]
    )
    merged["compensation_effect_analyzed"] = (
        merged["structure_success_rate_analyzed_comp"] - merged["structure_success_rate_analyzed_uncomp"]
    )
    return merged


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(PRESETS.keys()), default="smoke_v010")
    parser.add_argument("--out-prefix", default="v010")
    args = parser.parse_args()

    cfg = PRESETS[args.mode]
    os.makedirs("outputs", exist_ok=True)

    rows: List[Dict[str, Any]] = []
    combos = []
    for model_mode, variant, beta, epsilon_norm, lambda_val in product(
        cfg["model_modes"], cfg["relation_variants"], cfg["betas"], cfg["epsilon_norms"], cfg["lambda_values"]
    ):
        if valid_combo(model_mode, variant, beta, epsilon_norm, lambda_val):
            combos.append((model_mode, variant, beta, epsilon_norm, lambda_val))

    total = len(combos) * cfg["seeds"]
    print(f"AlphaEvolve-GCMS v0.10.2 | mode={args.mode} | attempts={total}")
    print("Goal: test whether compensation-aware relations create a real compensation effect.")

    start = time.perf_counter()
    k = 0
    for model_mode, variant, beta, epsilon_norm, lambda_val in combos:
        for seed in range(cfg["seeds"]):
            k += 1
            print(
                f"[{k}/{total}] mode={model_mode} var={variant} beta={beta} eps={epsilon_norm} lambda={lambda_val} seed={seed}"
            )
            rows.append(run_single(cfg, model_mode, variant, beta, epsilon_norm, lambda_val, seed))

    df = pd.DataFrame(rows)
    raw_path = f"outputs/raw_{args.out_prefix}.csv"
    summary_path = f"outputs/summary_{args.out_prefix}.csv"
    comparison_path = f"outputs/comparison_{args.out_prefix}.csv"
    residual_path = f"outputs/residual_{args.out_prefix}.csv"

    df.to_csv(raw_path, index=False)
    summary = make_summary(df)
    summary.to_csv(summary_path, index=False)
    make_comparison(summary).to_csv(comparison_path, index=False)
    summary[summary["model_mode"] == "residual"].to_csv(residual_path, index=False)

    print("\n--- OUTPUTS ---")
    print(raw_path)
    print(summary_path)
    print(comparison_path)
    print(residual_path)
    print(f"Runtime: {time.perf_counter() - start:.2f} sec")


if __name__ == "__main__":
    main()
