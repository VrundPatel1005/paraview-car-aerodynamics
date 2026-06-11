"""Create a portable synthetic CFD-style sample case.

The generated field is not a CFD solver result. It is a lightweight
visualization training dataset shaped like flow around a simplified
Ahmed-body/car silhouette, with velocity, pressure, turbulence, and
vorticity-like scalar fields.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import pyvista as pv

from common import PROCESSED_DIR, ensure_project_dirs


def car_surface() -> pv.PolyData:
    """Return a simplified car/Ahmed-body surface for visualization context."""
    # The model is intentionally simple. It gives the flow fields a recognizable
    # body to wrap around without pretending to be a production vehicle CAD mesh.
    body = pv.Box(bounds=(-1.05, 1.05, -0.42, 0.42, 0.0, 0.58))
    cabin = pv.Box(bounds=(-0.35, 0.55, -0.34, 0.34, 0.58, 0.98))
    nose = pv.Cone(center=(-1.1, 0.0, 0.29), direction=(-1, 0, 0), height=0.55, radius=0.42, resolution=4)
    spoiler = pv.Box(bounds=(0.98, 1.12, -0.45, 0.45, 0.72, 0.82))
    wheels = []
    for x in (-0.65, 0.65):
        for y in (-0.48, 0.48):
            wheels.append(
                pv.Cylinder(center=(x, y, 0.12), direction=(0, 1, 0), radius=0.16, height=0.12, resolution=32)
            )
    return body.merge(cabin).merge(nose).merge(spoiler).merge(wheels)


def build_flow_grid(nx: int, ny: int, nz: int) -> pv.StructuredGrid:
    """Generate a structured field with plausible wake and pressure patterns."""
    x = np.linspace(-3.0, 5.0, nx)
    y = np.linspace(-1.8, 1.8, ny)
    z = np.linspace(0.0, 2.4, nz)
    xx, yy, zz = np.meshgrid(x, y, z, indexing="ij")

    # A few smooth Gaussian fields stand in for familiar aerodynamic features:
    # blockage near the car, acceleration over the roof, and a slow wake behind it.
    u_inf = 30.0
    r2 = yy**2 + ((zz - 0.42) / 0.78) ** 2
    blockage = np.exp(-((xx + 0.15) / 0.9) ** 2 - r2 / 0.55)
    wake = np.exp(-((xx - 1.35) / 1.65) ** 2 - yy**2 / 0.42 - ((zz - 0.45) ** 2) / 0.32)
    roof_accel = np.exp(-((xx + 0.05) / 1.0) ** 2 - yy**2 / 0.8 - ((zz - 1.0) ** 2) / 0.12)
    ground_shear = np.exp(-(zz / 0.22) ** 2)

    u = u_inf * (1.0 - 0.58 * blockage - 0.48 * wake + 0.22 * roof_accel - 0.12 * ground_shear)
    v = 3.2 * yy * wake - 1.8 * yy * blockage
    w = 2.4 * (zz - 0.45) * wake + 2.2 * roof_accel - 0.8 * ground_shear
    velocity = np.column_stack([u.ravel(order="F"), v.ravel(order="F"), w.ravel(order="F")])
    speed = np.linalg.norm(velocity, axis=1)

    pressure = (
        420.0 * np.exp(-((xx + 1.05) / 0.45) ** 2 - yy**2 / 0.55 - ((zz - 0.35) ** 2) / 0.30)
        - 260.0 * roof_accel
        - 180.0 * wake
    )
    turbulence = 0.02 + 0.22 * wake + 0.08 * blockage + 0.04 * np.exp(-((zz - 0.16) / 0.18) ** 2)

    # This is a visualization-friendly vorticity proxy, not a validated CFD result.
    du_dy, du_dz = np.gradient(u, y, z, axis=(1, 2))
    dv_dx = np.gradient(v, x, axis=0)
    dw_dx = np.gradient(w, x, axis=0)
    vorticity_proxy = np.sqrt((dw_dx) ** 2 + (du_dz) ** 2 + (dv_dx - du_dy) ** 2)

    grid = pv.StructuredGrid(xx, yy, zz)
    grid.point_data["velocity"] = velocity
    grid.point_data["velocity_magnitude"] = speed
    grid.point_data["pressure"] = pressure.ravel(order="F")
    grid.point_data["turbulence_proxy"] = turbulence.ravel(order="F")
    grid.point_data["vorticity_proxy"] = vorticity_proxy.ravel(order="F")
    grid.point_data["wake_indicator"] = wake.ravel(order="F")
    return grid


def write_metrics(path: Path) -> None:
    """Write simple educational force-coefficient history for plotting."""
    iterations = np.arange(0, 201)
    cd = 0.34 + 0.08 * np.exp(-iterations / 45.0) + 0.006 * np.sin(iterations / 8.0)
    cl = 0.06 * np.exp(-iterations / 65.0) * np.cos(iterations / 13.0) - 0.015
    residual = 1e-1 * np.exp(-iterations / 26.0) + 2e-5
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["iteration", "drag_coefficient", "lift_coefficient", "residual"])
        writer.writerows(zip(iterations, cd, cl, residual))


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a synthetic car aerodynamics VTK sample case.")
    parser.add_argument("--nx", type=int, default=72, help="Number of points in the streamwise direction.")
    parser.add_argument("--ny", type=int, default=40, help="Number of points across the car.")
    parser.add_argument("--nz", type=int, default=32, help="Number of points vertically.")
    parser.add_argument(
        "--formats",
        nargs="+",
        choices=["vts", "vtu", "vtk"],
        default=["vts", "vtu", "vtk"],
        help="Flow-field formats to write. Downstream scripts read .vtu by default; "
        "the ParaView docs also use .vts/.vtk. Pass e.g. '--formats vtu' to write just one.",
    )
    args = parser.parse_args()

    ensure_project_dirs()
    grid = build_flow_grid(args.nx, args.ny, args.nz)
    surface = car_surface()
    root = PROCESSED_DIR.parents[0]

    formats = set(args.formats)
    if "vts" in formats:
        path = PROCESSED_DIR / "sample_car_flow.vts"
        grid.save(path)
        print(f"Saved flow field: {path.relative_to(root)}")
    if "vtu" in formats:
        path = PROCESSED_DIR / "sample_car_flow.vtu"
        grid.cast_to_unstructured_grid().save(path)
        print(f"Saved VTU field:  {path.relative_to(root)}")
    if "vtk" in formats:
        path = PROCESSED_DIR / "sample_car_flow.vtk"
        grid.save(path)
        print(f"Saved legacy VTK: {path.relative_to(root)}")

    # The car body and metrics are always written; the visualization scripts need them.
    surface_path = PROCESSED_DIR / "sample_car_body.vtp"
    metrics_path = PROCESSED_DIR / "metrics.csv"
    surface.save(surface_path)
    write_metrics(metrics_path)
    print(f"Saved car body:   {surface_path.relative_to(root)}")
    print(f"Saved metrics:    {metrics_path.relative_to(root)}")


if __name__ == "__main__":
    main()
