"""Smoke test for the synthetic sample-case generator.

Run from the project root with:

    pytest

This exercises the field-generation core (no ParaView/OpenGL required) and
checks that the expected aerodynamic arrays exist with consistent shapes.
"""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

# Make scripts/ importable without installing the project.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from setup_case import build_flow_grid, car_surface  # noqa: E402

EXPECTED_ARRAYS = {
    "velocity",
    "velocity_magnitude",
    "pressure",
    "turbulence_proxy",
    "vorticity_proxy",
    "wake_indicator",
}


def test_flow_grid_has_expected_arrays_and_shapes():
    nx, ny, nz = 12, 8, 6
    grid = build_flow_grid(nx, ny, nz)

    assert grid.n_points == nx * ny * nz
    assert EXPECTED_ARRAYS.issubset(set(grid.array_names))

    velocity = np.asarray(grid["velocity"])
    assert velocity.shape == (nx * ny * nz, 3)

    speed = np.asarray(grid["velocity_magnitude"])
    # velocity_magnitude must equal the norm of the velocity vectors.
    assert np.allclose(speed, np.linalg.norm(velocity, axis=1))


def test_flow_fields_are_finite():
    grid = build_flow_grid(12, 8, 6)
    for name in EXPECTED_ARRAYS:
        assert np.all(np.isfinite(np.asarray(grid[name]))), f"{name} contains non-finite values"


def test_car_surface_is_non_empty():
    surface = car_surface()
    assert surface.n_points > 0
    assert surface.n_cells > 0
