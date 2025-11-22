"""
3D Vector operations for orbital mechanics
"""
import numpy as np
from typing import Tuple


class Vector3D:
    """3D vector class for position, velocity, acceleration"""
    
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
    
    def __add__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other: 'Vector3D') -> 'Vector3D':
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __rmul__(self, scalar: float) -> 'Vector3D':
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: float) -> 'Vector3D':
        return Vector3D(self.x / scalar, self.y / scalar, self.z / scalar)
    
    def magnitude(self) -> float:
        """Calculate vector magnitude"""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)
    
    def normalize(self) -> 'Vector3D':
        """Normalize vector to unit length"""
        mag = self.magnitude()
        if mag == 0:
            return Vector3D(0, 0, 0)
        return self / mag
    
    def dot(self, other: 'Vector3D') -> float:
        """Dot product"""
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def cross(self, other: 'Vector3D') -> 'Vector3D':
        """Cross product"""
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def to_array(self) -> np.ndarray:
        """Convert to numpy array"""
        return np.array([self.x, self.y, self.z])
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {"x": self.x, "y": self.y, "z": self.z}
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'Vector3D':
        """Create from numpy array"""
        return cls(arr[0], arr[1], arr[2])
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Vector3D':
        """Create from dictionary"""
        return cls(data.get("x", 0), data.get("y", 0), data.get("z", 0))
    
    def __repr__(self) -> str:
        return f"Vector3D({self.x:.2e}, {self.y:.2e}, {self.z:.2e})"

