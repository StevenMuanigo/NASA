"""
Kepler's Laws calculations
1. Elliptical orbits
2. Equal area in equal time
3. T² ∝ a³
"""
import numpy as np
from typing import Tuple, Optional
from .vector3d import Vector3D
from .constants import G, MU_SUN, AU


def calculate_orbital_elements(
    position: Vector3D,
    velocity: Vector3D,
    sun_mass: float
) -> dict:
    """
    Calculate orbital elements from position and velocity
    Returns: a, e, i, Ω, ω, ν (semi-major axis, eccentricity, inclination, etc.)
    """
    mu = G * sun_mass
    
    # Position and velocity vectors
    r = position.magnitude()
    v = velocity.magnitude()
    
    # Specific angular momentum
    h_vector = position.cross(velocity)
    h = h_vector.magnitude()
    
    # Specific energy
    energy = 0.5 * v * v - mu / r
    
    # Semi-major axis
    if energy >= 0:
        # Hyperbolic orbit
        a = -mu / (2 * energy)
    else:
        # Elliptical orbit
        a = -mu / (2 * energy)
    
    # Eccentricity
    e_vector = (velocity.cross(h_vector) / mu) - position.normalize()
    e = e_vector.magnitude()
    
    # Inclination (angle from z-axis)
    i = np.arccos(h_vector.z / h) if h > 0 else 0
    
    # Longitude of ascending node
    n_vector = Vector3D(0, 0, 1).cross(h_vector)
    n = n_vector.magnitude()
    if n > 0:
        Omega = np.arccos(n_vector.x / n)
        if n_vector.y < 0:
            Omega = 2 * np.pi - Omega
    else:
        Omega = 0
    
    # Argument of periapsis
    if n > 0 and e > 0:
        omega = np.arccos((n_vector.dot(e_vector)) / (n * e))
        if e_vector.z < 0:
            omega = 2 * np.pi - omega
    else:
        omega = 0
    
    # True anomaly
    if e > 0:
        nu = np.arccos((e_vector.dot(position)) / (e * r))
        if position.dot(velocity) < 0:
            nu = 2 * np.pi - nu
    else:
        nu = 0
    
    # Orbital period (Kepler's third law)
    if a > 0:
        period = 2 * np.pi * np.sqrt(a**3 / mu)
    else:
        period = float('inf')
    
    return {
        "semi_major_axis": a,
        "eccentricity": e,
        "inclination": np.degrees(i),
        "longitude_of_ascending_node": np.degrees(Omega),
        "argument_of_periapsis": np.degrees(omega),
        "true_anomaly": np.degrees(nu),
        "period": period,
        "periapsis": a * (1 - e) if e < 1 else None,
        "apoapsis": a * (1 + e) if e < 1 else None
    }


def calculate_orbital_velocity(
    distance: float,
    sun_mass: float,
    circular: bool = False
) -> float:
    """
    Calculate orbital velocity at given distance
    For circular orbit: v = sqrt(G * M / r)
    """
    mu = G * sun_mass
    if circular:
        return np.sqrt(mu / distance)
    else:
        # For elliptical orbit, this is approximate
        return np.sqrt(mu * (2 / distance - 1 / distance))


def kepler_equation_solver(
    mean_anomaly: float,
    eccentricity: float,
    tolerance: float = 1e-10,
    max_iterations: int = 100
) -> float:
    """
    Solve Kepler's equation: M = E - e * sin(E)
    Returns eccentric anomaly
    """
    if eccentricity < 1e-6:
        return mean_anomaly
    
    E = mean_anomaly
    for _ in range(max_iterations):
        E_new = mean_anomaly + eccentricity * np.sin(E)
        if abs(E_new - E) < tolerance:
            return E_new
        E = E_new
    
    return E


def predict_position_from_elements(
    orbital_elements: dict,
    time: float,
    sun_mass: float
) -> Vector3D:
    """
    Predict position from orbital elements at given time
    Uses Kepler's equations
    """
    a = orbital_elements["semi_major_axis"]
    e = orbital_elements["eccentricity"]
    i = np.radians(orbital_elements["inclination"])
    Omega = np.radians(orbital_elements["longitude_of_ascending_node"])
    omega = np.radians(orbital_elements["argument_of_periapsis"])
    
    mu = G * sun_mass
    
    # Mean motion
    n = np.sqrt(mu / (a**3))
    
    # Mean anomaly
    M = n * time
    
    # Solve Kepler's equation
    E = kepler_equation_solver(M, e)
    
    # True anomaly
    nu = 2 * np.arctan2(
        np.sqrt(1 + e) * np.sin(E / 2),
        np.sqrt(1 - e) * np.cos(E / 2)
    )
    
    # Distance
    r = a * (1 - e * np.cos(E))
    
    # Position in orbital plane
    x_orbital = r * np.cos(nu)
    y_orbital = r * np.sin(nu)
    
    # Transform to 3D space (rotation matrices)
    # This is simplified - full transformation would use all angles
    x = x_orbital * np.cos(Omega) - y_orbital * np.sin(Omega)
    y = x_orbital * np.sin(Omega) + y_orbital * np.cos(Omega)
    z = r * np.sin(nu) * np.sin(i)
    
    return Vector3D(x, y, z)

