"""
Orbital Simulator API
FastAPI backend for physics simulation
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
import asyncio
from typing import List, Optional
from pydantic import BaseModel

from physics.simulator import OrbitalSimulator
from physics.vector3d import Vector3D
from physics.constants import AU

app = FastAPI(
    title="Orbital Simulator API",
    description="NASA-level physics-based orbital mechanics simulator",
    version="1.0.0"
)

# CORS - Web site için
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5174", "http://localhost:5173", "*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Global simulator instance
simulator = OrbitalSimulator()


class BodyCreate(BaseModel):
    name: str
    mass: float  # kg
    distance_from_sun: float  # AU
    initial_velocity: float  # m/s
    angle: float = 0.0  # degrees
    radius: float = 0.0
    color: str = "#ffffff"


class BodyResponse(BaseModel):
    name: str
    mass: float
    position: dict
    velocity: dict
    radius: float
    color: str
    acceleration: dict


class SimulationState(BaseModel):
    time: float
    bodies: List[BodyResponse]
    is_running: bool


@app.get("/")
async def root():
    """Health check"""
    return {"status": "ok", "message": "Orbital Simulator API"}


@app.post("/simulation/add-body", response_model=BodyResponse)
async def add_body(body: BodyCreate):
    """Add a celestial body to simulation"""
    new_body = simulator.add_body_from_parameters(
        name=body.name,
        mass=body.mass,
        distance_from_sun=body.distance_from_sun,
        initial_velocity=body.initial_velocity,
        angle=body.angle,
        radius=body.radius,
        color=body.color
    )
    return BodyResponse(**new_body.to_dict())


@app.post("/simulation/start")
async def start_simulation():
    """Start simulation"""
    simulator.start()
    return {"message": "Simulation started", "is_running": True}


@app.post("/simulation/stop")
async def stop_simulation():
    """Stop simulation"""
    simulator.stop()
    return {"message": "Simulation stopped", "is_running": False}


@app.post("/simulation/reset")
async def reset_simulation():
    """Reset simulation"""
    simulator.reset()
    return {"message": "Simulation reset"}


@app.get("/simulation/state", response_model=SimulationState)
async def get_state():
    """Get current simulation state"""
    state = simulator.get_state()
    return SimulationState(**state)


@app.get("/simulation/step")
async def step_simulation():
    """Perform one simulation step"""
    simulator.step()
    return {"message": "Step completed", "time": simulator.time}


@app.get("/simulation/orbital-elements/{body_name}")
async def get_orbital_elements(body_name: str):
    """Get orbital elements for a body"""
    elements = simulator.get_orbital_elements(body_name)
    if not elements:
        return JSONResponse(
            status_code=404,
            content={"error": f"Body '{body_name}' not found"}
        )
    return elements


@app.get("/simulation/energy-analysis")
async def get_energy_analysis():
    """Get energy analysis for all bodies"""
    return simulator.get_energy_analysis()


@app.get("/simulation/trajectory/{body_name}")
async def get_trajectory(body_name: str):
    """Get trajectory history for a body"""
    body = next((b for b in simulator.bodies if b.name == body_name), None)
    if not body:
        return JSONResponse(
            status_code=404,
            content={"error": f"Body '{body_name}' not found"}
        )
    
    trajectory = [point.to_dict() for point in body.trajectory]
    return {
        "body_name": body_name,
        "trajectory": trajectory,
        "point_count": len(trajectory)
    }


# Background task for continuous simulation
@app.on_event("startup")
async def startup_event():
    """Start background simulation loop"""
    asyncio.create_task(simulation_loop())


async def simulation_loop():
    """Background simulation loop"""
    while True:
        if simulator.is_running:
            simulator.step()
        await asyncio.sleep(0.1)  # 10 updates per second

