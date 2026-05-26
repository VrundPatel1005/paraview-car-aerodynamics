"""Generate rotating camera animations for the aerodynamic visualization."""

from __future__ import annotations

import argparse
import math

import imageio.v2 as imageio
import pyvista as pv

from common import ANIMATIONS_DIR, PROCESSED_DIR, ensure_project_dirs, require_array, resolve_path


pv.OFF_SCREEN = True


def _scene(mesh: pv.DataSet) -> pv.Plotter:
    plotter = pv.Plotter(off_screen=True, window_size=(1280, 800))
    plotter.add_mesh(mesh.slice(normal="y"), scalars="velocity_magnitude", cmap="viridis", opacity=0.82, scalar_bar_args={"title": "Velocity"})
    contour = mesh.contour(isosurfaces=[0.22], scalars="wake_indicator")
    plotter.add_mesh(contour, scalars="wake_indicator", cmap="magma", opacity=0.45)
    body_path = PROCESSED_DIR / "sample_car_body.vtp"
    if body_path.exists():
        plotter.add_mesh(pv.read(body_path), color="#eceff1", smooth_shading=True, specular=0.4)
    plotter.add_mesh(mesh.outline(), color="black", line_width=1)
    plotter.add_text("Rotating aerodynamic wake visualization", position="upper_left", font_size=11, color="black")
    plotter.set_background("white")
    return plotter


def generate_animation(input_path: str, output_format: str, frames: int) -> None:
    ensure_project_dirs()
    mesh = pv.read(resolve_path(input_path))
    require_array(mesh, "velocity_magnitude")
    require_array(mesh, "wake_indicator")

    frame_paths = []
    plotter = _scene(mesh)
    center = (0.7, 0.0, 0.6)
    radius = 6.0
    for frame in range(frames):
        theta = 2.0 * math.pi * frame / frames
        camera = (center[0] + radius * math.cos(theta), center[1] + radius * math.sin(theta), 2.65)
        plotter.camera_position = [camera, center, (0.0, 0.0, 1.0)]
        frame_path = ANIMATIONS_DIR / f"rotation_frame_{frame:03d}.png"
        plotter.screenshot(frame_path)
        frame_paths.append(frame_path)
    plotter.close()

    if output_format in {"gif", "both"}:
        gif_path = ANIMATIONS_DIR / "car_aerodynamics_rotation.gif"
        imageio.mimsave(gif_path, [imageio.imread(path) for path in frame_paths], duration=0.07)
        print(f"Saved GIF animation to {gif_path}")

    if output_format in {"mp4", "both"}:
        mp4_path = ANIMATIONS_DIR / "car_aerodynamics_rotation.mp4"
        imageio.mimsave(mp4_path, [imageio.imread(path) for path in frame_paths], fps=15)
        print(f"Saved MP4 animation to {mp4_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate rotating camera CFD animations.")
    parser.add_argument("--input", default="data/processed/sample_car_flow.vtu", help="Input VTK dataset.")
    parser.add_argument("--format", choices=["gif", "mp4", "both"], default="both", help="Animation output format.")
    parser.add_argument("--frames", type=int, default=72, help="Number of animation frames.")
    args = parser.parse_args()
    generate_animation(args.input, args.format, args.frames)


if __name__ == "__main__":
    main()
