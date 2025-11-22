"""
Newtonian gravity calculations
F = G * (m1 * m2) / r²
"""
import numpy as np
from typing import List
from .vector3d import Vector3D
from .constants import G


class CelestialBody:
    """Celestial body (planet, asteroid, etc.)"""
    
    def __init__(
        self,
        name: str,
        mass: float,
        position: Vector3D,
        velocity: Vector3D,
        radius: float = 0.0,
        color: str = "#ffffff"
    ):
        self.name = name
        self.mass = float(mass)  # kg
        self.position = position
        self.velocity = velocity
        self.radius = float(radius)  # meters (for visualization)
        self.color = color
        self.trajectory: List[Vector3D] = []
        self.acceleration = Vector3D(0, 0, 0)
    
    def calculate_gravitational_force(
        self,
        other: 'CelestialBody'
    ) -> Vector3D:
        """
        Calculate gravitational force from another body
        F = G * (m1 * m2) / r² * r̂
        """
        # Position vector from self to other
        r_vector = other.position - self.position
        r = r_vector.magnitude()
        
        # Avoid division by zero
        if r < 1e-6:
            return Vector3D(0, 0, 0)
        
        # Unit vector in direction of force
        r_hat = r_vector.normalize()
        
        # Gravitational force magnitude
        force_magnitude = G * self.mass * other.mass / (r * r)
        
        # Force vector
        force = r_hat * force_magnitude
        
        return force
    
    def calculate_acceleration(
        self,
        bodies: List['CelestialBody']
    ) -> Vector3D:
        """
        Calculate total acceleration from all other bodies
        a = F / m = Σ(G * m_other / r² * r̂)
        """
        total_force = Vector3D(0, 0, 0)
        
        for body in bodies:
            if body is self:
                continue
            
            force = self.calculate_gravitational_force(body)
            total_force = total_force + force
        
        # Acceleration = Force / Mass
        acceleration = total_force / self.mass
        self.acceleration = acceleration
        
        return acceleration
    
    def update_position(self, dt: float):
        """Update position using velocity"""
        self.position = self.position + self.velocity * dt
    
    def update_velocity(self, dt: float):
        """Update velocity using acceleration"""
        self.velocity = self.velocity + self.acceleration * dt
    
    def get_kinetic_energy(self) -> float:
        """Calculate kinetic energy: KE = 0.5 * m * v²"""
        v = self.velocity.magnitude()
        return 0.5 * self.mass * v * v
    
    def get_potential_energy(self, sun: 'CelestialBody') -> float:
        """Calculate potential energy: PE = -G * m * M / r"""
        r_vector = self.position - sun.position
        r = r_vector.magnitude()
        if r < 1e-6:
            return float('-inf')
        return -G * self.mass * sun.mass / r
    
    def get_total_energy(self, sun: 'CelestialBody') -> float:
        """Total energy: E = KE + PE"""
        return self.get_kinetic_energy() + self.get_potential_energy(sun)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for API"""
        return {
            "name": self.name,
            "mass": self.mass,
            "position": self.position.to_dict(),
            "velocity": self.velocity.to_dict(),
            "radius": self.radius,
            "color": self.color,
            "acceleration": self.acceleration.to_dict()
        }


def create_sun() -> CelestialBody:
    """Create the Sun"""
    from .constants import SOLAR_MASS
    return CelestialBody(
        name="Sun",
        mass=SOLAR_MASS,
        position=Vector3D(0, 0, 0),
        velocity=Vector3D(0, 0, 0),
        radius=6.96e8,  # Solar radius in meters
        color="#FFD700"
    )

