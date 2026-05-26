"""Plot beginner-friendly aerodynamic metrics from CSV data."""

from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import pandas as pd

from common import SCREENSHOTS_DIR, ensure_project_dirs, resolve_path


def analyze_metrics(input_path: str) -> None:
    ensure_project_dirs()
    path = resolve_path(input_path)
    data = pd.read_csv(path)

    fig, axes = plt.subplots(3, 1, figsize=(10, 9), sharex=True)
    axes[0].plot(data["iteration"], data["drag_coefficient"], color="#005f73", linewidth=2)
    axes[0].set_ylabel("Cd")
    axes[0].set_title("Drag coefficient history")
    axes[0].grid(True, alpha=0.3)

    axes[1].plot(data["iteration"], data["lift_coefficient"], color="#9b2226", linewidth=2)
    axes[1].set_ylabel("Cl")
    axes[1].set_title("Lift coefficient history")
    axes[1].grid(True, alpha=0.3)

    axes[2].semilogy(data["iteration"], data["residual"], color="#6a4c93", linewidth=2)
    axes[2].set_xlabel("Iteration")
    axes[2].set_ylabel("Residual")
    axes[2].set_title("Solver residual trend")
    axes[2].grid(True, alpha=0.3)

    fig.tight_layout()
    output = SCREENSHOTS_DIR / "aerodynamic_metrics.png"
    fig.savefig(output, dpi=180)
    plt.close(fig)

    final = data.iloc[-1]
    notes = SCREENSHOTS_DIR / "aerodynamic_metrics_interpretation.txt"
    notes.write_text(
        "\n".join(
            [
                "Aerodynamic Metrics Interpretation",
                "==================================",
                f"Final drag coefficient proxy: {final['drag_coefficient']:.3f}",
                f"Final lift coefficient proxy: {final['lift_coefficient']:.3f}",
                f"Final residual proxy: {final['residual']:.2e}",
                "",
                "A lower drag coefficient generally indicates less aerodynamic resistance.",
                "A negative lift coefficient indicates downforce in this educational example.",
                "A decreasing residual trend suggests the numerical solution is stabilizing.",
                "These sample values are generated for visualization practice, not validation.",
            ]
        )
    )
    print(f"Saved metric plot to {output}")
    print(f"Saved interpretation notes to {notes}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create drag/lift/residual plots from metrics CSV.")
    parser.add_argument("--input", default="data/processed/metrics.csv", help="Metrics CSV path.")
    args = parser.parse_args()
    analyze_metrics(args.input)


if __name__ == "__main__":
    main()
