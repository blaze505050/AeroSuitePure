Visit the page at : 
https://blaze505050.github.io/AeroSuitePure/ 

✈️ AeroSuite Pro

A Zero Dependency, In Browser Computational Fluid Dynamics (CFD), Microfluidics, and AI Design Suite.

AeroSuite Pro is a world class, fully self contained engineering simulation platform. Designed to run natively in any modern web browser without a backend or installation, it bridges the gap between High Performance Computing (HPC), Aerospace Aerodynamics, Multiphase Microfluidics, and Artificial Intelligence.

🚀 Quick Start

AeroSuite Pro is entirely serverless. To run the simulator:
Download or save the index.html file or click the link : https://blaze505050.github.io/AeroSuitePure/ 
Double click index.html to open it in Chrome, Edge, Safari, or Firefox.
No npm, no Docker, no cloud compute required.

🧬 Core Physics Explanations

AeroSuite is not a visual toy; it is a rigorous Eulerian fluid solver packing advanced numerical models.

1. Eulerian Navier Stokes & Pressure Solver :
At its core, the engine solves the incompressible Navier Stokes equations on a staggered grid. It uses a Red Black Successive Over-Relaxation (SOR) algorithm for pressure projection. This method parallelizes perfectly across CPU caches, allowing the simulation to converge on the pressure field ($P$) at 60 frames per second.

2. CLSVOF & PLIC (Multiphase Flow) :
To simulate water splashing without numerical "ghosting" or smearing, the engine uses CLSVOF (Coupled Level Set and Volume of Fluid).
VOF strictly conserves liquid mass.
PLIC (Piecewise Linear Interface Calculation) computes the exact sub grid geometric normal ($\vec{n}$) of the liquid/gas boundary, rendering the water surface infinitely sharp.

3. Microfluidics: CSF Surface Tension & Marangoni Convection :
Capillary Forces: The Continuum Surface Force (CSF) model calculates the mathematical curvature of the fluid interface ($\kappa = -\nabla \cdot \vec{n}$) to apply localized surface tension, allowing water to pinch off into droplets.
Marangoni Effect: The engine tracks a thermal scalar field ($T$). Because surface tension drops as temperature rises ($\sigma(T)$), spatial temperature gradients cause massive tangential shear stresses ($\nabla_s \sigma$). This drives Marangoni Convection (e.g., "Tears of Wine").
Wetting: Boundary contact angles are artificially enforced, allowing you to simulate Hydrophobic (Lotus effect, >90°) or Hydrophilic (Glass, <90°) surfaces.

4. Aerospace & Aerodynamics
LES Turbulence: Uses the Smagorinsky Sub-Grid Scale (SGS) model. It computes the local Strain Rate Tensor to dynamically generate Eddy Viscosity ($\nu_t$), simulating turbulent boundary layers.
Compressibility: Implements the Prandtl-Glauert Singularity Correction ($\beta = \sqrt{1 - M^2}$). As you increase the Mach number towards 1.0, forces non-linearly scale to mirror transonic flight physics.
Bernoulli Dynamics: Real time extraction of Static Pressure ($C_p$) and Skin Friction ($C_f$) from the velocity field, yielding high fidelity Lift ($C_L$) and Drag ($C_D$) coefficients.

💻 User Interface & Controls

Main Dashboard (Top Bar)
Medium: Swap between Air (Gas aerodynamics) and Water (Liquid hydrodynamics).
Airfoil/Import: Type any 4-digit NACA code (e.g., 4412, 0012) to generate an airfoil. Alternatively, click Import to upload a custom 2D .dat coordinate file or a 3D .stl mesh (which the engine will automatically slice into a 2D cross-section).
Mach (M): Controls incoming flow velocity. Set >0.8 for Transonic effects.
AOA: Angle of Attack. Controls the pitch of the airfoil.
Multi-Element & Ground Plane: Toggles Slotted Flaps and Ground Effect barriers.
Kinematic Sub-Menu (Appears dynamically)
Flap Deflection, Gap, Overlap: Mathematically tune the Venturi slot of a high-lift Fowler flap.
Ride Height: Controls how close the wing is to the ground (Ground Effect).
Contact Angle: Defines the wetting properties of the walls (Microfluidics mode).
Rigid Body FSI: Spawns a floating, dynamically coupled buoy that bobs via Archimedes' buoyancy and fluid drag.
The Viewport Tools (Top Left)

🖱️ Stir Fluid: Click and drag to manually inject velocity.
🔥 Inject Heat: Drops intense thermal energy into the fluid (Triggers Marangoni tearing in liquids).
🖋️ Draw Wall: Paint solid static boundary conditions into the tunnel.

Scientific View Modes
Pressure Field ($C_p$): Deep Blue = Suction/Lift; Searing Red = Stagnation.
Schlieren: Visualizes the spatial density gradient ($|\nabla P|$). Best for visualizing shockwaves.
LES Eddy Viscosity: Maps boundary layer turbulence generation.
VOF Surface: Displays the sharp PLIC interface between liquid and gas.
Vorticity Curl: Red/Blue map of counter-rotating vortices (Von Kármán streets).

🧠 AI & Optimization Modules
Click START AI to launch the built in evolutionary solver. It runs a zero budget, browser native Genetic Algorithm (GA).
Aerodynamic Shape Optimization: The GA spawns a population of 10 NACA configurations. It simulates them, measures their Lift to Drag ($L/D$) ratio, discards the losers, and cross breeds the winners (Camber, Position, Thickness) across multiple generations to find the mathematically perfect wing.
Inverse Topology Optimization: (Select "Inverse Topology Opt" from presets). The engine acts as a wave maker. The AI mutates a parametric breakwater structure (Height, Width, Tilt) to minimize downstream wave kinetic energy, autonomously inventing the optimal coastal defense geometry.
PINN Surrogate Predictor:
Toggle "PINN Predict" to see instantaneous, mathematically approximated $C_L$ and $C_D$ predictions running alongside the heavy viscous CFD solver.

🎬 3D WebGL & VFX Pipeline
AeroSuite Pro isn't restricted to 2D. Toggle "View 3D WebGL" to enter the volumetric renderer.
Volumetric Particles: Renders 15,000 instanced Three.js spheres that advect through the 3D space based on the 2D fluid vectors.
Liquid Mesh (Marching Cubes): Extracts a continuous, refractive 3D glass/water mesh from the scalar VOF field in real-time.
VFX Export: Click Export .OBJ while in Mesh mode. The engine will download the exact frame's fluid topology as a standard 3D model, ready to be imported into Blender, Houdini, or Unreal Engine 5 for photorealistic rendering.

Use Cases :
F1 Ground Effect: * Preset: F1 Ground Effect
Action: Lower the Ride Height slider. Watch the pressure map under the wing turn aggressively blue as the Venturi effect generates massive downforce.
The "Lotus Effect" (Hydrophobia):
Preset: Rigid FSI & Lotus Effect
Action: Increase Contact Angle to 160°. Watch the water bead up perfectly into spheres and roll off the floor due to CSF surface tension.
Aeroelastic Flutter (Helicopter Blades):
Preset: Dynamic Stall Flutter
Action: Switch view to Vorticity. Watch the rapid pitch changes spawn a massive "Leading Edge Vortex" (LEV) that peels off the back of the wing a notorious cause of helicopter blade failure.
Marangoni Tearing:
Preset: Microfluidics (Marangoni)
Action: Use the Flame Tool to paint heat onto the surface of the water pool. The local drop in surface tension will cause the colder water to rapidly pull away, tearing the fluid surface apart.

📈 The MATLAB Style Analytical Report :
At any point, click "FINISH & ANALYZE" to freeze the simulation and open the aerospace grade engineering dashboard.
Executive Summary: Read steady-state $C_L$, $C_D$, Moments, and Reynolds Numbers.
Aerodynamic Plots: View high fidelity, grid lined charts comparing the Viscous Navier Stokes $C_p$ distribution against the Ideal Inviscid Panel Method theoretical overlay.
Data Table: Scroll through the raw, spatial chordwise coordinate data ($x/c$) and click Export Data to save the array to a .csv file.

Developed as an integrated masterclass in Software Engineering, High-Performance Computing, and Fluid Mechanics.
