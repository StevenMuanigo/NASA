"""
Physical constants for orbital mechanics
NASA/JPL standard values
"""
import numpy as np

# Universal gravitational constant (m³ kg⁻¹ s⁻²)
G = 6.67430e-11

# Solar mass (kg)
SOLAR_MASS = 1.989e30

# Astronomical Unit (meters)
AU = 1.496e11

# Earth mass (kg)
EARTH_MASS = 5.972e24

# Speed of light (m/s) - for relativistic corrections (optional)
C = 299792458

# Standard gravitational parameter for Sun (m³ s⁻²)
MU_SUN = G * SOLAR_MASS

# Time step for simulation (seconds)
DEFAULT_TIME_STEP = 3600  # 1 hour

# Simulation speed multiplier
DEFAULT_SPEED_MULTIPLIER = 86400  # 1 day per second

