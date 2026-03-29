✈️ AeroSuite Pro :

A high fidelity, zero dependency, in browser Computational Fluid Dynamics (CFD) simulator and aerodynamic shape optimizer.
AeroSuite Pro is a masterclass in combining High Performance Computing (HPC) with advanced aerodynamic theory. Built entirely in a single HTML file, it features a custom built Eulerian Navier Stokes solver, Smagorinsky Large Eddy Simulation (LES) turbulence modeling, and a Stochastic Genetic Algorithm (GA) for real time airfoil shape optimization.

🚀 Features :

Advanced Fluid Dynamics :

Navier Stokes Eulerian Solver: A highly optimized staggered grid fluid solver running at 60 FPS in browser using V8 JIT compiled Float32Array architecture.
Transonic Compressibility: Implements the Prandtl-Glauert singularity correction factor ($\beta = \sqrt{1 - M^2}$) to accurately scale aerodynamic forces up to Mach 0.95.
LES Turbulence Modeling: Calculates the local Strain Rate Tensor to evaluate Sub-Grid Scale (SGS) Eddy Viscosity ($\nu_t$) via the Smagorinsky model.
Bernoulli Static Pressure Extraction: Real time integration of the pressure boundary field to calculate highly accurate Lift ($C_L$), Drag ($C_D$), and Pitching Moment ($C_{m_{c/4}}$) coefficients.
Viscous Skin Friction: Wall function gradient analysis to compute local shear stress ($\tau_w$) and Skin Friction ($C_f$).

Generative AI & Optimization :

Genetic Algorithm (GA) Optimizer: A real time evolutionary algorithm that breeds, crosses over, and mutates NACA profiles to autonomously find the most aerodynamically efficient shape (Max L/D ratio) for any given flow condition.
PINN Surrogate Prediction: Integrated Physics Informed Neural Network surrogate approximations for instant $C_L$ and $C_D$ evaluation.
Industry Grade Visualization
Schlieren & Vorticity Rendering: Cinematic vector field visualizations including Density Gradients (Schlieren shockwaves), Velocity Heatmaps, and Vorticity Curls.
Multi-Element High Lift Systems: Toggleable leading/trailing edge slotted flaps to demonstrate boundary layer re-energization and the Venturi effect.
MATLAB Style Telemetry Dashboard: Full-screen engineering reports detailing chordwise $C_p$ and $C_f$ distributions, comparing Viscous CFD results against Ideal Inviscid Panel Method approximations.
CSV Data Export: One click export of spatial chordwise data and time series convergence history.

🛠️ Getting Started :
AeroSuite Pro was engineered to be the ultimate frictionless tool. There are no build steps, no npm install, and no local servers required.
Clone or download this repository.
Double click index.html to open it in any modern web browser (Chrome, Edge, Firefox, Safari).

🔬 Architecture :

1. The Physics Engine :

Unlike standard WebGL shaders which obscure the physics, this solver is written in pure JavaScript to demonstrate algorithmic mastery.
Advection: Semi Lagrangian.
Pressure Projection: Red Black Successive Over Relaxation (SOR) algorithm highly cache friendly and converges exponentially faster than standard Gauss Seidel methods.

2. High Fidelity Rendering :

Vector Overlays: The airfoil geometry isn't drawn from blocky fluid cells. The exact polynomial coordinates are extracted, scaled, and rendered using HTML5 Canvas pathing with dynamic 3D drop shadows and metallic gradients.
Additive Tracers: Streamlines are rendered using globalCompositeOperation = "screen" to create a glowing, velocity scaled cinematic streak effect.

AeroSuite Pro is a masterclass in computational fluid dynamics and parametric aerodynamic design, engineered entirely as a zero dependency, self contained web application. Built to bridge the gap between High Performance Computing (HPC) and advanced aerospace theory, it provides real time, viscous flow simulation and shape optimization directly in the browser.Bypassing the overhead of standard WebGL shaders, AeroSuite Pro utilizes a custom built Eulerian fluid engine written in heavily optimized JavaScript (Float32Array). It employs a Red Black Successive Over Relaxation (SOR) pressure projection algorithm to sustain high-resolution grid calculations at a stable 60 FPS.

Technical & Aerodynamic Capabilities:Advanced 
Fluid Physics: Solves the 2D Navier Stokes equations with Smagorinsky Large Eddy Simulation (LES) sub grid scale modeling to accurately capture turbulence and vortex shedding.Transonic Compressibility: Integrates the Prandtl Glauert singularity correction factor ($\beta = \sqrt{1 - M^2}$) to accurately scale aerodynamic forces and simulate Mach numbers up to 0.95.Dynamic Aerodynamic Telemetry: Uses Bernoulli's principle to extract static pressure from the velocity field, yielding highly accurate Lift ($C_L$), Drag ($C_D$), and Pitching Moment ($C_{m}$) coefficients, alongside chordwise Pressure ($C_p$) and Skin Friction ($C_f$) distributions.Multi-Element & Motorsports Kinematics: Fully parametric support for multi element high lift devices (slotted flaps) with tunable gap/overlap kinematics, as well as a movable ground plane to simulate F1 style Venturi ground effect and extreme downforce.Generative AI Optimizer: Features an integrated Evolutionary Genetic Algorithm (GA) that autonomously breeds, mutates, and tests NACA airfoil profiles in real-time to find the mathematically optimal $L/D$ ratio for any given flow regime.Scientific Visualization & Reporting: Includes industry standard flow visualization modes (Schlieren shockwaves, Vorticity, Velocity Heatmaps) and a comprehensive MATLAB style analytical dashboard that compares Viscous CFD results against Ideal Inviscid Panel Method approximations.Architecture: Pure HTML5 / React 18 / Tailwind CSS / Babel Standalone. No build steps, no local servers, and no external dependencies required.

📊 Pre-Configured Scenarios :

Use the top navigation dropdown to instantly load industry-standard flow scenarios:
Transonic Regime: High Mach number flow with Schlieren visualization.
Deep Stall (Separation): High Angle of Attack (28°) to visualize Von Kármán vortex streets and boundary layer separation.
LES Turbulence Analysis: Visualizes the dynamically generated Eddy Viscosity field.
Hydrofoil Channel: Swaps the fluid medium to Water ($\rho = 997 kg/m^3$) to demonstrate kinematic force scaling.
Built as a capstone project to bridge the gap between High-Performance Software Engineering, Machine Learning, and Aerospace Aerodynamics.

License: MIT License. Feel free to fork, modify, and use this code for educational or commercial purposes.
