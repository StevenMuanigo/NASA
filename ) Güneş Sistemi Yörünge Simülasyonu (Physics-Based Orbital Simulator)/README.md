# Solar System Orbital Simulator


## Features

- **Real Physics**: Newton's law of gravitation and Kepler's three laws implemented
- **3D Visualization**: Interactive 3D solar system using Three.js
- **Real-time Simulation**: High-accuracy calculations using Verlet integration
- **Orbit Analysis**: Calculation of orbital elements and energy analysis
- **Web-based Interface**: User-friendly control panel built with React

### Backend
- 1. constants.py
Defines physical constants using NASA/JPL standard values:

Universal gravitational constant (G)

Solar mass

Astronomical Unit (AU)

Speed of light

Default time step and simulation speed multiplier

2. vector3d.py
Class for 3D vector operations. Basic operations include:

Addition, subtraction, multiplication, division

Magnitude calculation

Normalization

Dot and cross product

Conversion to/from JSON/dictionary

3. gravity.py
Newtonian gravity calculations. CelestialBody class includes:

Mass, position, velocity, acceleration properties

Gravitational force calculation

Acceleration calculation

Energy calculations (kinetic, potential, total)

Conversion to dictionary

4. kepler.py
Kepler laws implementation. Functions include:

Orbital elements calculation (a, e, i, Ω, ω, ν)

Orbital velocity calculation

Kepler equation solver

Position prediction

5. simulator.py
Main simulation engine (OrbitalSimulator class). Features:

Computation using Verlet integration

Management of celestial bodies

Simulation control (start/stop/reset)

Orbit trajectory tracking

Energy analysis

6. main.py
FastAPI web services. Endpoints include:

Health check

Add celestial body

Simulation control

Get simulation state

Orbital elements

Energy analysis

Trajectory history

### Frontend
- React 18
- TypeScript
- Three.js (3D visualization)
- @react-three/fiber (React-Three.js integration)
- @react-three/drei (Three.js helpers)

## Mit license 

an be improved, runnable and usable, errors can be fixed or can add somethings 

