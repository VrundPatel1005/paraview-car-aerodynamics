# Installation Guide

This project has two tracks:

- **Portable track**: Python generates sample CFD-style data and visuals immediately.
- **Full CFD track**: OpenFOAM runs a tutorial case and ParaView visualizes solver output.

Start with the portable track first. It gives you real files, screenshots, and animations before you install heavy CFD tools.

## 1. Python Setup

From the repository root:

```bash
bash setup.sh
source .venv/bin/activate
python scripts/setup_case.py
```

This installs:

- NumPy for array math
- PyVista and VTK for 3D scientific visualization
- Matplotlib for plots
- Pandas for metric CSV analysis
- imageio for GIF/MP4 export

## 2. ParaView Installation

ParaView is a free open-source scientific visualization application.

1. Go to https://www.paraview.org/download/
2. Download the macOS build.
3. Open ParaView.
4. Choose **File > Open**.
5. Select `data/processed/sample_car_flow.vtu`, `sample_car_flow.vts`, or `sample_car_flow.vtk`.
6. Click **Apply** in the Properties panel.

If `pvpython` is not available in your terminal, that is fine. The core scripts use PyVista and VTK directly. You can still use the ParaView GUI for interactive exploration.

## 3. Docker for OpenFOAM on macOS

OpenFOAM is easiest on macOS through Docker.

1. Install Docker Desktop: https://www.docker.com/products/docker-desktop/
2. Confirm Docker works:

```bash
docker --version
docker run hello-world
```

3. Use the official OpenFOAM macOS Docker launch scripts from:

https://dl.openfoam.org/docker/

The page includes scripts such as `openfoam11-macos`. Follow the matching OpenFOAM Foundation instructions for your chosen version.

## 4. OpenFOAM Concepts

An OpenFOAM case usually contains:

- `0/`: initial and boundary conditions for fields like velocity `U`, pressure `p`, turbulence `k`, and dissipation `epsilon`
- `constant/`: geometry, mesh, physical models, and material properties
- `system/`: solver controls, timesteps, numerical schemes, and output settings

Useful beginner commands inside an OpenFOAM environment:

```bash
cd $FOAM_TUTORIALS/incompressible/simpleFoam/motorBike
blockMesh
surfaceFeatureExtract
snappyHexMesh -overwrite
simpleFoam
touch motorBike.foam
```

Then open `motorBike.foam` in ParaView.

## 5. Troubleshooting

If Python rendering fails on macOS:

```bash
export PYVISTA_OFF_SCREEN=true
```

If ParaView opens the file but shows nothing:

- Click **Apply**.
- Press **Reset Camera**.
- Make sure the eye icon is enabled next to the dataset.
- Try coloring by `velocity_magnitude` or `pressure`.

If OpenFOAM commands are missing:

- You are probably outside the OpenFOAM container or environment.
- Use the Docker launch script again.
- Confirm `$FOAM_TUTORIALS` exists.
