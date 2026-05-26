from __future__ import annotations

import argparse
import sys

from game_of_life import GameOfLife
import patterns
from visualization import animate
from benchmark import plot_results, run_benchmark


def _build_game(args) -> GameOfLife:
    """Construye una instancia de GameOfLife según los argumentos CLI."""
    if args.pattern == "random":
        return GameOfLife(args.size, args.size, density=args.density, seed=args.seed)

    pattern = patterns.get(args.pattern)
    game = GameOfLife(args.size, args.size)
    game.clear()  # Partimos de un tablero vacío para sembrar solo el patrón.
    # Centramos el patrón en el tablero.
    top = (args.size - pattern.shape[0]) // 2
    left = (args.size - pattern.shape[1]) // 2
    game.set_cells(pattern, top=top, left=left)
    return game


def cmd_demo(args) -> None:
    game = _build_game(args)
    print(f"[demo] {game}")
    print(f"[demo] Patrón: {args.pattern}  |  pasos: {args.steps}")
    animate(
        game,
        steps=args.steps,
        interval=args.interval,
        title=f"Juego de la Vida — {args.pattern} ({args.size}x{args.size})",
        save_path=args.save,
        show=not args.no_show,
    )


def cmd_benchmark(args) -> None:
    from pathlib import Path
    times = run_benchmark(args.sizes, args.iters, args.warmup)
    plot_results(args.sizes, times, Path(args.out))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Juego de la Vida de Conway — Tarea 1 (Prog. Paralela y Distribuida)."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    # --- subcomando demo ---
    p_demo = sub.add_parser("demo", help="Lanza una demo animada del juego.")
    p_demo.add_argument(
        "--pattern", default="glider",
        choices=list(patterns.CATALOG) + ["random"],
        help="Patrón inicial a sembrar.",
    )
    p_demo.add_argument("--size", type=int, default=64,
                        help="Tamaño N de una grilla NxN.")
    p_demo.add_argument("--steps", type=int, default=200,
                        help="Número de generaciones a simular.")
    p_demo.add_argument("--interval", type=int, default=80,
                        help="Milisegundos entre cuadros de la animación.")
    p_demo.add_argument("--density", type=float, default=0.25,
                        help="Densidad inicial (solo aplica a --pattern random).")
    p_demo.add_argument("--seed", type=int, default=None,
                        help="Semilla para reproducibilidad del estado aleatorio.")
    p_demo.add_argument("--save", type=str, default=None,
                        help="Ruta para guardar la animación (.gif o .mp4).")
    p_demo.add_argument("--no-show", action="store_true",
                        help="No abrir la ventana de matplotlib (útil para solo guardar).")
    p_demo.set_defaults(func=cmd_demo)

    # --- subcomando benchmark ---
    p_bench = sub.add_parser("benchmark", help="Ejecuta el benchmark de rendimiento.")
    p_bench.add_argument("--sizes", type=int, nargs="+",
                         default=[32, 64, 128, 256, 512, 1024])
    p_bench.add_argument("--iters", type=int, default=50)
    p_bench.add_argument("--warmup", type=int, default=5)
    p_bench.add_argument("--out", type=str, default="resultados")
    p_bench.set_defaults(func=cmd_benchmark)

    return parser


def main(argv=None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
