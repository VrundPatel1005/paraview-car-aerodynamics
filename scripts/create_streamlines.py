"""Create streamline renderings for airflow around the car body."""

from __future__ import annotations

import argparse

import numpy as np
import pyvista as pv

from common import PROCESSED_DIR, SCREENSHOTS_DIR, ensure_project_dirs, require_array, resolve_path


pv.OFF_SCREEN = True


def create_streamlines(input_path: str) -> None:
    ensure_project_dirs()
    mesh = pv.read(resolve_path(input_path))
    require_array(mesh, "velocity")

    seeds = pv.PolyData(
        np.array(
            [
                [-2.75, y, z]
                for y in np.linspace(-1.15, 1.15, 11)
                for z in np.linspace(0.18, 1.55, 8)
            ]
        )
    )
    # Seed the streamlines upstream so the curves read like air entering the domain.
    streamlines = mesh.streamlines_from_source(
        seeds,
        vectors="velocity",
        max_length=8.0,
        initial_step_length=0.05,
        integration_direction="forward",
    )

    plotter = pv.Plotter(off_screen=True, window_size=(1700, 1000))
    plotter.add_mesh(streamlines.tube(radius=0.012), scalars="velocity_magnitude", cmap="turbo", scalar_bar_args={"title": "Velocity"})
    body_path = PROCESSED_DIR / "sample_car_body.vtp"
    if body_path.exists():
        plotter.add_mesh(pv.read(body_path), color="#cfd8dc", smooth_shading=True, specular=0.35)
    plotter.add_mesh(mesh.outline(), color="black", line_width=1)
    plotter.add_text("Streamlines seeded upstream of the car body", position="upper_left", font_size=12, color="black")
    plotter.set_background("white")
    plotter.camera_position = [(5.0, -4.5, 2.8), (0.8, 0.0, 0.58), (0.0, 0.0, 1.0)]
    output = SCREENSHOTS_DIR / "streamlines_side_airflow.png"
    plotter.screenshot(output)
    plotter.close()
    print(f"Saved streamline screenshot to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Render streamlines from a vector field.")
    parser.add_argument("--input", default="data/processed/sample_car_flow.vtu", help="Input VTK dataset.")
    args = parser.parse_args()
    create_streamlines(args.input)


if __name__ == "__main__":
    main()
