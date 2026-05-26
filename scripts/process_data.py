"""Post-process VTK/OpenFOAM-exported data and add derived fields."""

from __future__ import annotations

import argparse
import csv

import numpy as np
import pyvista as pv

from common import PROCESSED_DIR, ensure_project_dirs, resolve_path


def process_dataset(input_path: str, output_path: str | None = None) -> None:
    ensure_project_dirs()
    source = resolve_path(input_path)
    dataset = pv.read(source)

    if "velocity" in dataset.array_names:
        velocity = np.asarray(dataset["velocity"])
    elif "U" in dataset.array_names:
        velocity = np.asarray(dataset["U"])
        dataset.point_data["velocity"] = velocity
    else:
        raise ValueError("Input must contain a vector field named 'velocity' or OpenFOAM field 'U'.")

    speed = np.linalg.norm(velocity, axis=1)
    dataset.point_data["velocity_magnitude"] = speed

    pressure_name = "pressure" if "pressure" in dataset.array_names else "p" if "p" in dataset.array_names else None
    if pressure_name:
        pressure = np.asarray(dataset[pressure_name], dtype=float)
        q = 0.5 * 1.225 * max(float(np.nanmax(speed)) ** 2, 1e-9)
        dataset.point_data["pressure_coefficient_proxy"] = (pressure - float(np.nanmean(pressure))) / q

    threshold = np.nanpercentile(speed, 25)
    dataset.point_data["wake_mask"] = (speed < threshold).astype(float)

    output = resolve_path(output_path) if output_path else PROCESSED_DIR / f"{source.stem}_processed.vtk"
    dataset.save(output)

    metrics_path = PROCESSED_DIR / "processed_summary.csv"
    with metrics_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        writer.writerow(["points", dataset.n_points])
        writer.writerow(["cells", dataset.n_cells])
        writer.writerow(["velocity_min", float(np.nanmin(speed))])
        writer.writerow(["velocity_mean", float(np.nanmean(speed))])
        writer.writerow(["velocity_max", float(np.nanmax(speed))])
        writer.writerow(["wake_threshold_speed", float(threshold)])

    print(f"Processed dataset saved to {output}")
    print(f"Summary metrics saved to {metrics_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute derived aerodynamic visualization fields.")
    parser.add_argument("--input", required=True, help="Path to .vtk, .vts, .vtu, .vtp, or OpenFOAM-exported VTK data.")
    parser.add_argument("--output", default=None, help="Optional output VTK path.")
    args = parser.parse_args()
    process_dataset(args.input, args.output)


if __name__ == "__main__":
    main()
