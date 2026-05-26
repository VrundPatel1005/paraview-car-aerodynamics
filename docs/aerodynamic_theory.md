# Aerodynamic Theory for Beginners

This project focuses on visualizing airflow around a car-like body. The goal is to understand what CFD fields mean and how visualization turns raw solver data into engineering insight.

## What CFD Means

Computational Fluid Dynamics uses numerical methods to estimate how fluids move. In car aerodynamics, CFD is used to study air velocity, pressure, turbulence, drag, lift, and wake behavior.

## Scalar Fields and Vector Fields

A scalar field has one value at each point.

Examples:

- pressure
- temperature
- turbulence intensity
- velocity magnitude

A vector field has direction and magnitude.

Examples:

- velocity
- force
- vorticity vector

ParaView visualizes scalar fields with colors and vector fields with arrows, streamlines, or particles.

## Pressure Distribution

Air slows down near the front of a car, creating a high-pressure stagnation region. Air can accelerate over the hood and roof, creating lower pressure. Behind the vehicle, separated flow often leaves a low-pressure wake. This pressure difference contributes to pressure drag.

## Aerodynamic Drag

Drag is the force resisting forward motion.

Major sources:

- pressure drag from separated wake flow
- skin-friction drag from wall shear
- interference drag from wheels, mirrors, and body details

For a bluff body like an Ahmed body or simplified car, wake pressure drag is very important.

## Lift and Downforce

Lift is vertical aerodynamic force. In cars, engineers often want controlled negative lift, called downforce, because it increases tire grip. A visualization project can discuss lift qualitatively through pressure differences above and below the body.

## Reynolds Number

The Reynolds number compares inertial forces to viscous forces:

```text
Re = rho * U * L / mu
```

Where:

- `rho` is fluid density
- `U` is reference speed
- `L` is reference length
- `mu` is dynamic viscosity

Cars operate at high Reynolds numbers, where turbulence and separation strongly affect the wake.

## Turbulence

Turbulence is chaotic, three-dimensional, fluctuating fluid motion. In practical CFD, turbulence is often modeled instead of fully resolved because resolving every turbulent scale is extremely expensive.

Common CFD approaches:

- RANS: efficient time-averaged turbulence modeling
- LES: resolves larger turbulent structures
- DES/hybrid methods: combine RANS and LES ideas

## Wake Region

The wake is the disturbed flow downstream of the vehicle. It usually contains:

- low-speed air
- recirculation
- vortices
- turbulence
- lower pressure

A large low-pressure wake often means higher drag.

## Streamlines

A streamline follows the direction of the velocity vector field. Streamlines help viewers see how air moves around and behind the car.

Good streamline visualizations:

- start upstream of the body
- use color for speed
- avoid too many lines
- show the car body for context

## Iso-Surfaces

An iso-surface is a 3D surface where a scalar field has a constant value. In this project, wake iso-surfaces show the volume of low-speed/high-wake-intensity flow behind the car.

## Volume Rendering

Volume rendering displays a semi-transparent 3D scalar field. It is useful for showing turbulence or vorticity throughout a volume, but it can become visually cluttered. Use it with careful opacity settings.

## Ahmed Body

The Ahmed body is a simplified car-like shape used in vehicle aerodynamics research. It is important because it captures core flow features of cars while being simpler than a production vehicle:

- front stagnation
- roof acceleration
- rear separation
- wake vortices
- pressure drag

This makes it ideal for CFD validation, visualization practice, and machine learning datasets such as AhmedML.
