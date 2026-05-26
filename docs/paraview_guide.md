# ParaView Beginner Guide

ParaView is the main interactive tool for this project. It lets you open scientific datasets, apply filters, color fields, and export high-quality visualizations.

## Opening Files

For this project:

1. Open ParaView.
2. Select **File > Open**.
3. Choose `data/processed/sample_car_flow.vtu`.
4. Click **Apply**.
5. Press **Reset Camera**.

For OpenFOAM:

1. Create an empty marker file in the case folder:

```bash
touch motorBike.foam
```

2. Open `motorBike.foam` in ParaView.
3. Select mesh regions and fields.
4. Click **Apply**.

## Camera Controls

- Left drag: rotate
- Middle drag: pan
- Scroll: zoom
- Press **Reset Camera** if the model disappears
- Use camera bookmarks for repeatable views

Recommended presentation views:

- side view for streamlines
- rear view for wake
- top view for turbulence and velocity field spread
- three-quarter view for cinematic renders

## Color Maps

Color maps connect numbers to colors.

- Use `coolwarm` or blue-white-red for pressure.
- Use `viridis` or `turbo` for velocity magnitude.
- Use `inferno` or `magma` for turbulence and wake intensity.

Always show a scalar bar for scientific screenshots.

## Slice Filter

Use **Filters > Common > Slice**.

Purpose:

- Cut through the 3D domain.
- Show pressure or velocity on a plane.
- Inspect wake structure behind the car.

Recommended slices:

- centerline vertical slice: `normal = Y`
- horizontal wake slice: `normal = Z`
- rear cross-section: `normal = X`

## Stream Tracer

Use **Filters > Alphabetical > Stream Tracer**.

Purpose:

- Follow the velocity vector field.
- Show how air moves around the car.
- Make the wake visually understandable.

Beginner settings:

- Vectors: `velocity` or `U`
- Seed type: point cloud or line
- Place seeds upstream of the car
- Increase maximum streamline length if lines stop too early

## Glyph Filter

Use **Filters > Common > Glyph**.

Purpose:

- Draw arrows for vector fields.
- Show flow direction and local speed.

Beginner settings:

- Orientation array: `velocity`
- Scale array: `velocity_magnitude`
- Reduce glyph count so the view is readable

## Contour Filter

Use **Filters > Common > Contour**.

Purpose:

- Extract surfaces where a scalar field has a chosen value.
- Show wake regions, high turbulence zones, or pressure shells.

Good contour fields:

- `wake_indicator`
- `turbulence_proxy`
- `vorticity_proxy`

## Volume Rendering

Volume rendering displays semi-transparent scalar fields throughout the domain.

Use it carefully:

- Choose one scalar field.
- Lower opacity.
- Hide clutter.
- Combine it with the car body surface for context.

Best fields:

- vorticity
- turbulence
- wake intensity

## Exporting Screenshots

1. Set a clean camera angle.
2. Use a white or dark neutral background.
3. Keep the scalar bar visible.
4. Select **File > Save Screenshot**.
5. Use at least 1600 px width.

## Exporting Animations

1. Open **View > Animation View**.
2. Add a camera track.
3. Set keyframes around the car.
4. Preview the motion.
5. Export as image frames or video.

If video export fails, export PNG frames and assemble them with Python or ffmpeg.

## Saving State Files

ParaView state files preserve your pipeline.

1. Select **File > Save State**.
2. Save as `car_aero_visualization.pvsm`.
3. Reopen later with **File > Load State**.

State files are useful for recruiters because they show the visualization pipeline can be reproduced.
