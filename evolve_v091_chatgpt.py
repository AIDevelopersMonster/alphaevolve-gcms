"""
AlphaEvolve-GCMS v0.9.1
ChatGPT-reviewed local version.

Purpose:
- Test whether globally compensated multi-index systems can produce
  long-lived local sectors with statistically non-random graph structure.
- Uses strict global compensation:
      sum_B I_i ≈ 0
- Tracks local sectors of size 5..60.
- Compares clustering against:
      1) G(n,p) baseline
      2) degree-preserving edge-swap baseline
- Uses empirical p-values for strict success.

Recommended first run:
    python evolve_v091_chatgpt.py --mode fast

Then:
    python evolve_v091_chatgpt.py --mode local
"""

from __future__ import annotations

import argparse
import os
import time
from dataclasses import dataclass
from typing import Iterable, Optional, Dict, Any, List, Set, Tuple

import numpy as np
import pandas as pd
import networkx as nx
from scipy import stats


# -----------------------------
# Config presets
# -----------------------------

PRESETS = {
    "fast": {
        "N": 100,
        "d": 4,
        "steps": 200,
        "seeds": 100,
        "baseline_count": 100,
        "mutation_rate": 0.10,
        "params": [(0.5, 0.75)],
    },
    "local": {
        "N": 100,
        "d": 4,
        "steps": 100,
        "seeds": 50,
        "baseline_count": 100,
        "mutation_rate": 0.10,
        "params": [(0.5, 0.75), (1.0, 0.60)],
    },
    "mini": {
        "N": 60,
        "d": 4,
        "steps": 30,
        "seeds": 3,
        "baseline_count": 10,
        "mutation_rate": 0.10,
        "params": [(0.5, 0.75)],
    },
}


# -----------------------------
# Core data structures
# -----------------------------

@dataclass
class State:
    state_id: int
    index_vector: np.ndarray


class BigStructure:
    """Globally compensated multi-index structure."""

    def __init__(self, N: int, d: int, seed: int):
        self.N = N
        self.d = d
        self.rng = np.random.default_rng(seed)

        raw = self.rng.normal(size=(N, d))
        mean_v = raw.mean(axis=0)
        compensated = raw - mean_v

        self.states = [
            State(i, compensated[i].astype(float).copy())
            for i in range(N)
        ]

    def matrix(self) -> np.ndarray:
        return np.vstack([s.index_vector for s in self.states])

    def get_global_error(self) -> float:
        return float(np.linalg.norm(self.matrix().sum(axis=0)))

    def mutate_pairwise(self, mutation_rate: float):
        """Pair mutation that preserves global sum exactly up to floating point."""
        a, b = self.rng.choice(self.N, size=2, replace=False)
        delta = self.rng.normal(size=self.d) * mutation_rate
        self.states[a].index_vector += delta
        self.states[b].index_vector -= delta


class UniverseSector:
    """Tracks candidate local sector and analyzes its graph structure."""

    def __init__(
        self,
        big: BigStructure,
        alpha: float,
        threshold: float,
        baseline_count: int,
        min_size: int = 5,
        max_size: int = 60,
        overlap_limit: float = 0.5,
    ):
        self.big = big
        self.alpha = alpha
        self.threshold = threshold
        self.baseline_count = baseline_count
        self.min_size = min_size
        self.max_size = max_size
        self.overlap_limit = overlap_limit

        self.current_indices: Set[int] = set()
        self.lifetime = 0
        self.current_valid_steps = 0

        self.total_valid_steps = 0
        self.birth_count = 0
        self.death_count = 0

        self.best_sector_data: Optional[Dict[str, Any]] = None

    def _is_valid_size(self, nodes: Set[int]) -> bool:
        return self.min_size <= len(nodes) <= self.max_size

    def _build_graph(self, nodes: Iterable[int]) -> nx.Graph:
        """Build graph over given nodes using index-vector distance."""
        nodes_list = list(nodes)
        g = nx.Graph()
        g.add_nodes_from(nodes_list)

        if len(nodes_list) < 2:
            return g

        states = self.big.states
        for a in range(len(nodes_list)):
            ia = nodes_list[a]
            va = states[ia].index_vector
            for b in range(a + 1, len(nodes_list)):
                ib = nodes_list[b]
                vb = states[ib].index_vector
                dist_sq = float(np.sum((va - vb) ** 2))
                r = float(np.exp(-self.alpha * dist_sq))
                if r > self.threshold:
                    g.add_edge(ia, ib)

        return g

    def _get_all_clusters(self) -> List[Set[int]]:
        """Build global graph and return connected components, including isolated nodes."""
        g = self._build_graph(range(self.big.N))
        return [set(c) for c in nx.connected_components(g)]

    def _cluster_chi(self, nodes: Set[int]) -> float:
        if not nodes:
            return 0.0
        vec = sum((self.big.states[i].index_vector for i in nodes), np.zeros(self.big.d))
        return float(np.linalg.norm(vec))

    def _best_valid_cluster_by_chi(self, clusters: List[Set[int]]) -> Set[int]:
        best_c: Set[int] = set()
        best_chi = -1.0
        for c in clusters:
            if self._is_valid_size(c):
                chi = self._cluster_chi(c)
                if chi > best_chi:
                    best_chi = chi
                    best_c = set(c)
        return best_c

    @staticmethod
    def _edge_signature(g: nx.Graph) -> Set[frozenset]:
        return set(map(frozenset, g.edges()))

    @staticmethod
    def _empirical_p_greater(observed: float, baseline: List[float]) -> float:
        """One-sided empirical p-value: probability baseline >= observed."""
        if not baseline:
            return 1.0
        count = sum(x >= observed for x in baseline)
        return float((1 + count) / (len(baseline) + 1))

    @staticmethod
    def _normal_p_greater(observed: float, baseline: List[float]) -> Tuple[float, float, float]:
        """One-sided normal-approx p-value and z-score."""
        if not baseline:
            return 0.0, 1.0, 0.0
        arr = np.asarray(baseline, dtype=float)
        mu = float(arr.mean())
        sigma = float(arr.std(ddof=0))
        if sigma <= 1e-12:
            z = 0.0
            p = 1.0
        else:
            z = float((observed - mu) / sigma)
            p = float(1 - stats.norm.cdf(z))
        return z, p, mu

    def _degree_preserving_baseline(
        self,
        g: nx.Graph,
        rng: np.random.Generator,
    ) -> Tuple[List[float], float]:
        """Generate degree-preserving randomized baselines using double-edge swap.

        Only accept a sample if edges actually changed.
        """
        m = g.number_of_edges()
        if m < 2:
            return [], 0.0

        samples: List[float] = []
        attempts = self.baseline_count
        original_edges = self._edge_signature(g)

        for _ in range(attempts):
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

            if self._edge_signature(dg) != original_edges:
                samples.append(float(nx.average_clustering(dg)))

        success_rate = len(samples) / max(1, attempts)
        return samples, success_rate

    def _deep_analysis(self, nodes: Set[int], seed: int) -> Optional[Dict[str, Any]]:
        """Analyze one candidate sector against GNP and degree-preserving baselines."""
        if not self._is_valid_size(nodes):
            return None

        g = self._build_graph(nodes)
        n = g.number_of_nodes()
        m = g.number_of_edges()

        if n < self.min_size or n > self.max_size or m < 1:
            return None

        density = float(nx.density(g))
        clustering = float(nx.average_clustering(g))
        chi = self._cluster_chi(set(g.nodes()))

        rng = np.random.default_rng(seed)

        # G(n,p) baseline
        gnp_clusts: List[float] = []
        for _ in range(self.baseline_count):
            rg_seed = int(rng.integers(0, 2**31 - 1))
            rg = nx.fast_gnp_random_graph(n, density, seed=rg_seed)
            gnp_clusts.append(float(nx.average_clustering(rg)))

        z_gnp, p_gnp_normal, mu_gnp = self._normal_p_greater(clustering, gnp_clusts)
        p_gnp_emp = self._empirical_p_greater(clustering, gnp_clusts)

        # Degree-preserving baseline
        dp_clusts, dp_swap_success_rate = self._degree_preserving_baseline(g, rng)
        dp_valid = len(dp_clusts) >= min(30, self.baseline_count)

        if dp_valid:
            z_dp, p_dp_normal, mu_dp = self._normal_p_greater(clustering, dp_clusts)
            p_dp_emp = self._empirical_p_greater(clustering, dp_clusts)
        else:
            z_dp, p_dp_normal, p_dp_emp, mu_dp = 0.0, 1.0, 1.0, 0.0

        strict_success = (
            p_gnp_emp < 0.05
            and p_dp_emp < 0.05
            and dp_valid
            and self.lifetime > 20
            and self.min_size <= n <= self.max_size
            and self.big.get_global_error() < 1e-12
        )

        return {
            "sector_size": n,
            "edge_count": m,
            "density": density,
            "clustering": clustering,
            "chi": chi,
            "lifetime": int(self.lifetime),
            "current_sector_valid_steps": int(self.current_valid_steps),
            "total_valid_steps": int(self.total_valid_steps),
            "birth_count": int(self.birth_count),
            "death_count": int(self.death_count),
            "gnp_clustering_mean": mu_gnp,
            "dp_clustering_mean": mu_dp,
            "z_clust_gnp": z_gnp,
            "z_clust_dp": z_dp,
            "p_clust_gnp_normal": p_gnp_normal,
            "p_clust_dp_normal": p_dp_normal,
            "p_clust_gnp_empirical": p_gnp_emp,
            "p_clust_dp_empirical": p_dp_emp,
            "dp_valid": bool(dp_valid),
            "dp_swap_success_rate": float(dp_swap_success_rate),
            "strict_success": bool(strict_success),
        }

    def update(self, step_seed: int):
        clusters = self._get_all_clusters()

        # Try to find successor by maximum overlap.
        best_overlap = -1.0
        successor: Set[int] = set()

        if self.current_indices:
            for c in clusters:
                union = len(self.current_indices | c)
                overlap = len(self.current_indices & c) / union if union > 0 else 0.0
                if overlap > self.overlap_limit and overlap > best_overlap:
                    best_overlap = overlap
                    successor = set(c)

        if successor:
            self.current_indices = successor
            self.lifetime += 1
            if self._is_valid_size(successor):
                self.current_valid_steps += 1
                self.total_valid_steps += 1
            return

        # Current sector died; analyze it if it lived long enough.
        if self.current_indices and self.lifetime > 20 and self._is_valid_size(self.current_indices):
            data = self._deep_analysis(self.current_indices, seed=step_seed)
            if data is not None:
                if self.best_sector_data is None or data["lifetime"] > self.best_sector_data["lifetime"]:
                    self.best_sector_data = data

        if self.current_indices:
            self.death_count += 1

        # Birth: choose best valid cluster by chi.
        new_c = self._best_valid_cluster_by_chi(clusters)
        if new_c:
            self.birth_count += 1
            self.current_indices = new_c
            self.lifetime = 1
            self.current_valid_steps = 1
            self.total_valid_steps += 1
        else:
            self.current_indices = set()
            self.lifetime = 0
            self.current_valid_steps = 0


# -----------------------------
# Experiment runner
# -----------------------------

def run_experiment(
    alpha: float,
    threshold: float,
    seed: int,
    N: int,
    d: int,
    steps: int,
    mutation_rate: float,
    baseline_count: int,
) -> Optional[Dict[str, Any]]:
    big = BigStructure(N=N, d=d, seed=seed)
    sector = UniverseSector(
        big=big,
        alpha=alpha,
        threshold=threshold,
        baseline_count=baseline_count,
    )

    for step in range(steps):
        big.mutate_pairwise(mutation_rate=mutation_rate)
        sector.update(step_seed=seed * 100000 + step)

    # Analyze final sector if valid.
    final_data = None
    if sector._is_valid_size(sector.current_indices) and sector.lifetime > 20:
        final_data = sector._deep_analysis(sector.current_indices, seed=seed * 99991 + steps)

    # Choose final valid long-lived result, otherwise best historical champion.
    res = final_data if final_data is not None else sector.best_sector_data
    if res is None:
        return None

    res.update({
        "seed": seed,
        "alpha": alpha,
        "threshold": threshold,
        "global_error": big.get_global_error(),
        "N": N,
        "d": d,
        "steps": steps,
        "baseline_count": baseline_count,
        "mutation_rate": mutation_rate,
    })

    # Recompute strict_success after global fields are included.
    res["strict_success"] = bool(
        res["p_clust_gnp_empirical"] < 0.05
        and res["p_clust_dp_empirical"] < 0.05
        and res["dp_valid"]
        and res["lifetime"] > 20
        and 5 <= res["sector_size"] <= 60
        and res["global_error"] < 1e-12
    )

    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=list(PRESETS.keys()), default="fast")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()

    cfg = PRESETS[args.mode]
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)

    out_path = args.out or os.path.join(out_dir, f"summary_v091_{args.mode}.csv")

    start = time.perf_counter()
    rows: List[Dict[str, Any]] = []

    total_attempts = len(cfg["params"]) * cfg["seeds"]
    print(f"AlphaEvolve-GCMS v0.9.1 | mode={args.mode}")
    print(f"Attempts: {total_attempts}")
    print(f"Config: {cfg}")

    k = 0
    for alpha, threshold in cfg["params"]:
        for seed in range(cfg["seeds"]):
            k += 1
            print(f"[{k}/{total_attempts}] alpha={alpha}, threshold={threshold}, seed={seed}")
            row = run_experiment(
                alpha=alpha,
                threshold=threshold,
                seed=seed,
                N=cfg["N"],
                d=cfg["d"],
                steps=cfg["steps"],
                mutation_rate=cfg["mutation_rate"],
                baseline_count=cfg["baseline_count"],
            )
            if row is not None:
                rows.append(row)

    df = pd.DataFrame(rows)
    df.to_csv(out_path, index=False)

    elapsed = time.perf_counter() - start

    print("\n--- RESULTS ---")
    print(f"Output: {out_path}")
    print(f"Attempted runs: {total_attempts}")
    print(f"Analyzed runs: {len(df)}")

    if len(df) > 0:
        strict_rate_attempted = float(df["strict_success"].sum() / total_attempts)
        strict_rate_analyzed = float(df["strict_success"].mean())
        print(f"Strict success count: {int(df['strict_success'].sum())}")
        print(f"Strict success rate / attempted: {strict_rate_attempted:.2%}")
        print(f"Strict success rate / analyzed: {strict_rate_analyzed:.2%}")
        print(f"Max global error: {df['global_error'].max():.3e}")
        print(f"Mean dp swap success rate: {df['dp_swap_success_rate'].mean():.2%}")

        group_cols = ["alpha", "threshold"]
        summary = df.groupby(group_cols).agg(
            analyzed=("strict_success", "count"),
            strict_success_rate=("strict_success", "mean"),
            mean_lifetime=("lifetime", "mean"),
            mean_sector_size=("sector_size", "mean"),
            mean_p_gnp_emp=("p_clust_gnp_empirical", "mean"),
            mean_p_dp_emp=("p_clust_dp_empirical", "mean"),
            mean_dp_valid=("dp_valid", "mean"),
        ).reset_index()

        summary_path = os.path.join(out_dir, f"group_summary_v091_{args.mode}.csv")
        summary.to_csv(summary_path, index=False)
        print(f"Group summary: {summary_path}")
        print(summary.to_string(index=False))

    print(f"Runtime: {elapsed:.2f} sec")


if __name__ == "__main__":
    main()
