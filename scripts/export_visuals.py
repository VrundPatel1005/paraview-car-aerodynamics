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


def _render_view(geometry, *, scalars, cmap, bar_title, filename, title, outline, opacity=1.0) -> None:
    """Render one framed screenshot. Every view shares camera, body, and styling."""
    plotter = pv.Plotter(off_screen=True, window_size=(1600, 1000))
    plotter.add_mesh(geometry, scalars=scalars, cmap=cmap, opacity=opacity, scalar_bar_args={"title": bar_title})
    plotter.add_mesh(outline, color="black", line_width=1)
    _add_body(plotter)
    # Keep every screenshot framed the same way so the image set feels coherent.
    plotter.add_text(title, position="upper_left", font_size=12, color="black")
    plotter.set_background("white")
    plotter.show_grid(color="lightgray")
    plotter.camera_position = [(5.2, -4.2, 2.6), (0.7, 0.0, 0.55), (0.0, 0.0, 1.0)]
    plotter.screenshot(SCREENSHOTS_DIR / filename)
    plotter.close()


def _build_views(mesh: pv.DataSet) -> list[dict]:
    """Describe each screenshot as a config so adding a view is a one-line change."""
    # Glyphs get messy fast, so sample the grid before drawing arrows.
    sample_every = max(mesh.n_points // 350, 1)
    glyph_source = mesh.extract_points(range(0, mesh.n_points, sample_every), adjacent_cells=True)
    glyphs = glyph_source.glyph(orient="velocity", scale="velocity_magnitude", factor=0.018)

    return [
        # A centerline slice is the easiest first view: it shows the high-pressure
        # nose region and the low-pressure wake without hiding everything in 3D.
        dict(geometry=mesh.slice(normal="y"), scalars="pressure", cmap="coolwarm", opacity=0.92,
             bar_title="Pressure", filename="pressure_centerline_slice.png",
             title="Pressure distribution on centerline slice"),
        dict(geometry=mesh.slice(normal="y"), scalars="velocity_magnitude", cmap="viridis", opacity=0.95,
             bar_title="Velocity", filename="velocity_centerline_slice.png",
             title="Velocity magnitude and wake deficit"),
        dict(geometry=mesh.slice(normal="z", origin=(0, 0, 0.55)), scalars="turbulence_proxy", cmap="inferno",
             opacity=0.95, bar_title="Turbulence proxy", filename="turbulence_plan_view.png",
             title="Turbulence proxy in the wake region"),
        dict(geometry=glyphs, scalars="velocity_magnitude", cmap="plasma",
             bar_title="Velocity", filename="velocity_vector_glyphs.png",
             title="Velocity vector glyphs around the car body"),
        dict(geometry=mesh.contour(isosurfaces=[0.16, 0.28], scalars="wake_indicator"), scalars="wake_indicator",
             cmap="magma", opacity=0.58, bar_title="Wake", filename="wake_iso_surface.png",
             title="Iso-surface of low-speed wake structure"),
    ]


def export_visuals(input_path: str) -> None:
    ensure_project_dirs()
    mesh = pv.read(resolve_path(input_path))
    require_array(mesh, "velocity_magnitude")
    require_array(mesh, "pressure")

    outline = mesh.outline()
    for view in _build_views(mesh):
        _render_view(outline=outline, **view)

    print(f"Exported screenshots to {SCREENSHOTS_DIR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export still CFD visualization images.")
    parser.add_argument("--input", default="data/processed/sample_car_flow.vtu", help="Input VTK dataset.")
    args = parser.parse_args()
    export_visuals(args.input)


if __name__ == "__main__":
    main()
