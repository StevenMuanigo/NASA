"""
Orbital mechanics simulator
Uses Verlet integration for numerical stability
"""
import numpy as np
from typing import List, Optional, Callable
from .gravity import CelestialBody, create_sun
from .vector3d import Vector3D
from .constants import DEFAULT_TIME_STEP, AU
from .kepler import calculate_orbital_elements


class OrbitalSimulator:
    """Main simulation engine"""
    
    def __init__(
        self,
        time_step: float = DEFAULT_TIME_STEP,
        speed_multiplier: float = 1.0
    ):
        self.time_step = time_step
        self.speed_multiplier = speed_multiplier
        self.bodies: List[CelestialBody] = []
        self.sun = create_sun()
        self.bodies.append(self.sun)
        self.time = 0.0
        self.is_running = False
        self.trajectory_history: List[dict] = []
        self.max_trajectory_points = 1000
    
    def add_body(
        self,
        name: str,
        mass: float,
        position: Vector3D,
        velocity: Vector3D,
        radius: float = 0.0,
        color: str = "#ffffff"
    ) -> CelestialBody:
        """Add a celestial body to simulation"""
        body = CelestialBody(name, mass, position, velocity, radius, color)
        self.bodies.append(body)
        return body
    
    def add_body_from_parameters(
        self,
        name: str,
        mass: float,
        distance_from_sun: float,  # in AU
        initial_velocity: float,  # in m/s
        angle: float = 0.0,  # angle in degrees
        radius: float = 0.0,
        color: str = "#ffffff"
    ) -> CelestialBody:
        """
        Add body with simplified parameters
        distance_from_sun: Distance in AU
        initial_velocity: Velocity magnitude in m/s
        angle: Initial angle in degrees (0 = right, 90 = up)
        """
        # Convert AU to meters
        distance_m = distance_from_sun * AU
        
        # Position (in x-y plane)
        angle_rad = np.radians(angle)
        position = Vector3D(
            distance_m * np.cos(angle_rad),
            distance_m * np.sin(angle_rad),
            0
        )
        
        # Velocity (perpendicular to position for circular orbit)
        # For stable orbit, velocity should be perpendicular
        velocity_angle = angle_rad + np.pi / 2
        velocity = Vector3D(
            initial_velocity * np.cos(velocity_angle),
            initial_velocity * np.sin(velocity_angle),
            0
        )
        
        return self.add_body(name, mass, position, velocity, radius, color)
    
    def step(self):
        """Perform one simulation step using Verlet integration"""
        if not self.is_running:
            return
        
        dt = self.time_step * self.speed_multiplier
        
        # Calculate accelerations for all bodies
        for body in self.bodies:
            if body is self.sun:
                continue
            body.calculate_acceleration(self.bodies)
        
        # Update positions and velocities (Verlet integration)
        for body in self.bodies:
            if body is self.sun:
                continue
            
            # Verlet: v(t+dt/2) = v(t) + a(t) * dt/2
            half_velocity = body.velocity + body.acceleration * (dt / 2)
            
            # x(t+dt) = x(t) + v(t+dt/2) * dt
            body.position = body.position + half_velocity * dt
            
            # Calculate new acceleration
            new_acceleration = body.calculate_acceleration(self.bodies)
            
            # v(t+dt) = v(t+dt/2) + a(t+dt) * dt/2
            body.velocity = half_velocity + new_acceleration * (dt / 2)
            body.acceleration = new_acceleration
            
            # Store trajectory
            if len(body.trajectory) < self.max_trajectory_points:
                body.trajectory.append(Vector3D(body.position.x, body.position.y, body.position.z))
            else:
                body.trajectory.pop(0)
                body.trajectory.append(Vector3D(body.position.x, body.position.y, body.position.z))
        
        self.time += dt
        
        # Store state for history
        self._store_state()
    
    def _store_state(self):
        """Store current state for trajectory analysis"""
        state = {
            "time": self.time,
            "bodies": [body.to_dict() for body in self.bodies if body is not self.sun]
        }
        if len(self.trajectory_history) < self.max_trajectory_points:
            self.trajectory_history.append(state)
        else:
            self.trajectory_history.pop(0)
            self.trajectory_history.append(state)
    
    def start(self):
        """Start simulation"""
        self.is_running = True
    
    def stop(self):
        """Stop simulation"""
        self.is_running = False
    
    def reset(self):
        """Reset simulation"""
        self.time = 0.0
        self.is_running = False
        self.bodies = [self.sun]
        self.trajectory_history = []
        for body in self.bodies:
            body.trajectory = []
    
    def get_state(self) -> dict:
        """Get current simulation state"""
        return {
            "time": self.time,
            "bodies": [body.to_dict() for body in self.bodies],
            "is_running": self.is_running
        }
    
    def get_orbital_elements(self, body_name: str) -> Optional[dict]:
        """Get orbital elements for a body"""
        body = next((b for b in self.bodies if b.name == body_name), None)
        if not body or body is self.sun:
            return None
        
        return calculate_orbital_elements(
            body.position,
            body.velocity,
            self.sun.mass
        )
    
    def get_energy_analysis(self) -> dict:
        """Get energy analysis for all bodies"""
        analysis = {}
        for body in self.bodies:
            if body is self.sun:
                continue
            
            ke = body.get_kinetic_energy()
            pe = body.get_potential_energy(self.sun)
            total = body.get_total_energy(self.sun)
            
            analysis[body.name] = {
                "kinetic_energy": ke,
                "potential_energy": pe,
                "total_energy": total
            }
        
        return analysis

