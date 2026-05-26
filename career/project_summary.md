# Project Summary

## Elevator Pitch

This project is a reproducible scientific visualization pipeline for car aerodynamics. It generates or loads CFD-style flow data, visualizes pressure and velocity fields, renders streamlines and wake structures, exports animations, and explains the aerodynamic meaning of each result.

## Recruiter-Friendly Summary

I built an exploratory CFD visualization project that demonstrates how ParaView, OpenFOAM workflows, and Python automation can be used to communicate airflow behavior around a car-like body. The project includes clear documentation, reproducible scripts, scientific renderings, and beginner-friendly theory notes.

## Technical Stack

- Python 3.11+
- NumPy
- Pandas
- Matplotlib
- VTK
- PyVista
- ParaView
- OpenFOAM
- Docker

## Project Scope

The project focuses on post-processing and visualization rather than developing a CFD solver. It uses a synthetic portable flow field for immediate practice and documents how to extend the workflow to OpenFOAM `motorBike` and Ahmed-body datasets.

## What I Learned

- How CFD results are organized into scalar and vector fields.
- How pressure, velocity, turbulence, and wake regions appear in visualization.
- How ParaView filters such as Slice, Contour, Glyph, Stream Tracer, and Clip support scientific interpretation.
- How Python can automate screenshots, animations, and metric analysis.
- How to communicate CFD results honestly and visually in technical project writeups.
