"""Shared helpers for the car aerodynamics visualization scripts."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
SCREENSHOTS_DIR = PROJECT_ROOT / "screenshots"
ANIMATIONS_DIR = PROJECT_ROOT / "animations"


def ensure_project_dirs() -> None:
    """Create output directories used by the pipeline."""
    for path in (DATA_DIR / "raw", PROCESSED_DIR, DATA_DIR / "sample_cases", SCREENSHOTS_DIR, ANIMATIONS_DIR):
        path.mkdir(parents=True, exist_ok=True)


def resolve_path(path: str | Path) -> Path:
    """Resolve user input relative to the project root."""
    candidate = Path(path)
    if candidate.is_absolute():
        return candidate
    return PROJECT_ROOT / candidate


def require_array(dataset, name: str) -> None:
    """Raise a clear error if a VTK/PyVista dataset is missing an array."""
    if name not in dataset.array_names:
        arrays = ", ".join(dataset.array_names) or "none"
        raise ValueError(f"Missing required array '{name}'. Available arrays: {arrays}")
