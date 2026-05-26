# End-to-End Workflow

This workflow starts with a portable demo and then shows how to extend it to OpenFOAM.

## Step 1. Generate the Sample CFD-Style Dataset

```bash
source .venv/bin/activate
python scripts/setup_case.py
```

Generated files:

- `data/processed/sample_car_flow.vtu`: unstructured VTK grid for broad tool compatibility
- `data/processed/sample_car_flow.vts`: structured VTK grid with flow fields
- `data/processed/sample_car_flow.vtk`: legacy VTK fallback
- `data/processed/sample_car_body.vtp`: simplified car body surface
- `data/processed/metrics.csv`: educational drag/lift/residual history

The sample fields are visualization training data, not a validated CFD simulation.

## Step 2. Process Derived Fields

```bash
python scripts/process_data.py --input data/processed/sample_car_flow.vtu
```

This computes:

- velocity magnitude
- pressure coefficient proxy
- wake mask
- summary statistics

## Step 3. Export Scientific Screenshots

```bash
python scripts/export_visuals.py --input data/processed/sample_car_flow.vtu
python scripts/create_streamlines.py --input data/processed/sample_car_flow.vtu
python scripts/metrics_analysis.py --input data/processed/metrics.csv
```

Capture these project screenshots:

- side airflow streamlines
- wake iso-surface
- pressure contour
- velocity magnitude slice
- velocity vector glyphs
- turbulence plan view
- metric plot
- ParaView workspace with the pipeline browser visible

## Step 4. Generate Animation

```bash
python scripts/generate_animation.py --input data/processed/sample_car_flow.vtu --format both
```

This exports:

- `animations/car_aerodynamics_rotation.gif`
- `animations/car_aerodynamics_rotation.mp4`

Use the GIF in GitHub and the MP4 in presentations.

## Step 5. Explore in ParaView

1. Open ParaView.
2. Open `data/processed/sample_car_flow.vtu`.
3. Click **Apply**.
4. Change coloring to `pressure`, `velocity_magnitude`, `turbulence_proxy`, or `vorticity_proxy`.
5. Add filters:
   - **Slice** for 2D field inspection
   - **Stream Tracer** for flow paths
   - **Glyph** for velocity vectors
   - **Contour** for iso-surfaces
   - **Clip** for looking inside the domain
6. Save screenshots and animations.

## Step 6. Optional OpenFOAM motorBike Case

Inside an OpenFOAM environment:

```bash
mkdir -p $FOAM_RUN
cp -r $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike $FOAM_RUN/
cd $FOAM_RUN/motorBike
./Allrun
touch motorBike.foam
```

If `./Allrun` is unavailable for your OpenFOAM version, run the commands manually from the case instructions:

```bash
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
simpleFoam
touch motorBike.foam
```

Open `motorBike.foam` in ParaView and recreate the same visual set.

## Step 7. Optional AhmedML Extension

Use AhmedML for high-fidelity public data:

https://caemldatasets.org/ahmedml/

Recommended beginner approach:

1. Read the dataset documentation.
2. Download one small sample first.
3. Inspect the available boundary, volume, and force files.
4. Convert or open compatible VTK/OpenFOAM output in ParaView.
5. Compare the wake and pressure fields with the portable sample case.
