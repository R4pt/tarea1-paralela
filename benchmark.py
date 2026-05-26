
from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import List, Sequence

import matplotlib.pyplot as plt
import numpy as np

from game_of_life import GameOfLife

def measure(size: int, iters: int = 50, warmup: int = 5, seed: int = 0) -> float:

    game = GameOfLife(size, size, seed=seed)

    game.run(warmup)

    start = time.perf_counter()
    game.run(iters)
    elapsed = time.perf_counter() - start

    return elapsed / iters


def run_benchmark(sizes: Sequence[int], iters: int, warmup: int) -> List[float]:
    times: List[float] = []
    print(f"{'Tamaño':>10} | {'Celdas':>10} | {'Tiempo/iter (ms)':>18}")
    print("-" * 46)
    for size in sizes:
        t = measure(size, iters=iters, warmup=warmup)
        times.append(t)
        print(f"{size:>4}x{size:<4} | {size * size:>10d} | {t * 1000:>15.4f}")
    return times


def plot_results(sizes: Sequence[int], times: Sequence[float], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    n_cells = np.array([s * s for s in sizes], dtype=np.float64)
    t = np.array(times, dtype=np.float64)

    n0, t0 = n_cells[0], t[0]
    linear = t0 * (n_cells / n0)
    nlogn = t0 * (n_cells * np.log2(n_cells)) / (n0 * np.log2(n0))
    quadratic = t0 * (n_cells / n0) ** 2

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(n_cells, t * 1000, "o-", label="Empírico", linewidth=2)
    ax.plot(n_cells, linear * 1000, "--", label="O(n)", alpha=0.7)
    ax.plot(n_cells, nlogn * 1000, "--", label="O(n log n)", alpha=0.7)
    ax.plot(n_cells, quadratic * 1000, "--", label="O(n²)", alpha=0.7)
    ax.set_xlabel("Número de celdas (n = filas × columnas)")
    ax.set_ylabel("Tiempo promedio por iteración (ms)")
    ax.set_title("Rendimiento del Juego de la Vida — escala lineal")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "benchmark_lineal.png", dpi=120)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.loglog(n_cells, t * 1000, "o-", label="Empírico", linewidth=2)
    ax.loglog(n_cells, linear * 1000, "--", label="O(n)", alpha=0.7)
    ax.loglog(n_cells, nlogn * 1000, "--", label="O(n log n)", alpha=0.7)
    ax.loglog(n_cells, quadratic * 1000, "--", label="O(n²)", alpha=0.7)
    ax.set_xlabel("Número de celdas (n)  [log]")
    ax.set_ylabel("Tiempo promedio por iteración (ms)  [log]")
    ax.set_title("Rendimiento del Juego de la Vida — escala log-log")
    ax.legend()
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_dir / "benchmark_loglog.png", dpi=120)
    plt.close(fig)

    slope, intercept = np.polyfit(np.log(n_cells), np.log(t), 1)
    print(f"\nPendiente ajustada en log-log: {slope:.3f}  "
          f"(≈ exponente empírico de complejidad respecto al número de celdas)")
    print(f"Figuras guardadas en: {out_dir.resolve()}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Benchmark del Juego de la Vida.")
    parser.add_argument(
        "--sizes", type=int, nargs="+",
        default=[32, 64, 128, 256, 512, 1024],
        help="Lista de tamaños N para grillas NxN.",
    )
    parser.add_argument("--iters", type=int, default=50,
                        help="Iteraciones medidas por tamaño.")
    parser.add_argument("--warmup", type=int, default=5,
                        help="Iteraciones de warmup (no medidas).")
    parser.add_argument("--out", type=str, default="resultados",
                        help="Carpeta donde guardar las gráficas.")
    args = parser.parse_args()

    times = run_benchmark(args.sizes, args.iters, args.warmup)
    plot_results(args.sizes, times, Path(args.out))


if __name__ == "__main__":
    main()
