"""Export clean still images from the car aerodynamics sample."""

from __future__ import annotations

import argparse

import pyvista as pv

from common import PROCESSED_DIR, SCREENSHOTS_DIR, ensure_project_dirs, require_array, resolve_path


pv.OFF_SCREEN = True


def _load_body() -> pv.PolyData | None:
    body_path = PROCESSED_DIR / "sample_car_body.vtp"
    return pv.read(body_path) if body_path.exists() else None


def _add_body(plotter: pv.Plotter) -> None:
    body = _load_body()
    if body is not None:
        plotter.add_mesh(body, color="#d8dee9", smooth_shading=True, specular=0.35, label="car body")


def _finish(plotter: pv.Plotter, filename: str, title: str) -> None:
    # Keep every screenshot framed the same way so the image set feels coherent.
    plotter.add_text(title, position="upper_left", font_size=12, color="black")
    plotter.set_background("white")
    plotter.show_grid(color="lightgray")
    plotter.camera_position = [(5.2, -4.2, 2.6), (0.7, 0.0, 0.55), (0.0, 0.0, 1.0)]
    plotter.screenshot(SCREENSHOTS_DIR / filename)
    plotter.close()


def export_visuals(input_path: str) -> None:
    ensure_project_dirs()
    mesh = pv.read(resolve_path(input_path))
    require_array(mesh, "velocity_magnitude")
    require_array(mesh, "pressure")

    outline = mesh.outline()

    # A centerline slice is the easiest first view: it shows the high-pressure
    # nose region and the low-pressure wake without hiding everything in 3D.
    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.add_mesh(mesh.slice(normal="y"), scalars="pressure", cmap="coolwarm", opacity=0.92, scalar_bar_args={"title": "Pressure"})
    p.add_mesh(outline, color="black", line_width=1)
    _add_body(p)
    _finish(p, "pressure_centerline_slice.png", "Pressure distribution on centerline slice")

    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.add_mesh(mesh.slice(normal="y"), scalars="velocity_magnitude", cmap="viridis", opacity=0.95, scalar_bar_args={"title": "Velocity"})
    p.add_mesh(outline, color="black", line_width=1)
    _add_body(p)
    _finish(p, "velocity_centerline_slice.png", "Velocity magnitude and wake deficit")

    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.add_mesh(mesh.slice(normal="z", origin=(0, 0, 0.55)), scalars="turbulence_proxy", cmap="inferno", opacity=0.95, scalar_bar_args={"title": "Turbulence proxy"})
    p.add_mesh(outline, color="black", line_width=1)
    _add_body(p)
    _finish(p, "turbulence_plan_view.png", "Turbulence proxy in the wake region")

    # Glyphs get messy fast, so sample the grid before drawing arrows.
    sample_every = max(mesh.n_points // 350, 1)
    glyph_source = mesh.extract_points(range(0, mesh.n_points, sample_every), adjacent_cells=True)
    glyphs = glyph_source.glyph(orient="velocity", scale="velocity_magnitude", factor=0.018)
    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.add_mesh(glyphs, scalars="velocity_magnitude", cmap="plasma", scalar_bar_args={"title": "Velocity"})
    p.add_mesh(outline, color="black", line_width=1)
    _add_body(p)
    _finish(p, "velocity_vector_glyphs.png", "Velocity vector glyphs around the car body")

    contour = mesh.contour(isosurfaces=[0.16, 0.28], scalars="wake_indicator")
    p = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    p.add_mesh(contour, scalars="wake_indicator", cmap="magma", opacity=0.58, scalar_bar_args={"title": "Wake"})
    p.add_mesh(outline, color="black", line_width=1)
    _add_body(p)
    _finish(p, "wake_iso_surface.png", "Iso-surface of low-speed wake structure")

    print(f"Exported screenshots to {SCREENSHOTS_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export still CFD visualization images.")
    parser.add_argument("--input", default="data/processed/sample_car_flow.vtu", help="Input VTK dataset.")
    args = parser.parse_args()
    export_visuals(args.input)


if __name__ == "__main__":
    main()
