"""
Benchmark du temps d'inférence search + rerank.

Lance 10 recherches avec torch.cuda.synchronize() entre chaque
pour mesurer le temps réel GPU.

Usage: switcherooctl launch uv run test/benchmark.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
import torch
from utils.prepare import prepare
from utils.embedding_search import search
from utils.rerank_with_crossencoder import rerank

QUERIES = [
    "où manger",
    "parking vélo",
    "faire les courses",
    "aéroport",
    "toilettes accessibles",
    "piste cyclable",
    "fontaine eau potable",
    "distributeur de billets",
    "pharmacie de garde",
    "terrain de foot",
]


def benchmark():
    candidates, search_settings, rerank_settings = prepare()

    # Warmup (le premier appel est toujours plus lent)
    torch.cuda.synchronize()
    search_results = search(QUERIES[0], candidates, search_settings)
    rerank(QUERIES[0], search_results, rerank_settings)
    torch.cuda.synchronize()
    print("Warmup done.\n")

    search_times = []
    rerank_times = []
    total_times = []

    for i, query in enumerate(QUERIES):
        # Search
        torch.cuda.synchronize()
        t0 = time.perf_counter()
        search_results = search(query, candidates, search_settings)
        torch.cuda.synchronize()
        t1 = time.perf_counter()

        # Rerank
        rerank_results = rerank(query, search_results, rerank_settings)
        torch.cuda.synchronize()
        t2 = time.perf_counter()

        s_ms = (t1 - t0) * 1000
        r_ms = (t2 - t1) * 1000
        total_ms = (t2 - t0) * 1000

        search_times.append(s_ms)
        rerank_times.append(r_ms)
        total_times.append(total_ms)

        print(f"[{i+1:2d}/10] {query:<30s}  search={s_ms:6.1f}ms  rerank={r_ms:6.1f}ms  total={total_ms:6.1f}ms  ({len(rerank_results)} results)")

    print(f"\n{'='*70}")
    print(f"{'Étape':<10} {'Min':>8} {'Max':>8} {'Avg':>8} {'Median':>8}")
    print(f"{'-'*70}")
    for name, times in [("Search", search_times), ("Rerank", rerank_times), ("Total", total_times)]:
        s = sorted(times)
        avg = sum(s) / len(s)
        median = s[len(s) // 2]
        print(f"{name:<10} {s[0]:>7.1f}ms {s[-1]:>7.1f}ms {avg:>7.1f}ms {median:>7.1f}ms")


if __name__ == "__main__":
    benchmark()
