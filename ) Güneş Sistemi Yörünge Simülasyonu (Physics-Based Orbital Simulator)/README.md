# Solar System Orbital Simulator

NASA-level physics-based orbital mechanics simulator. This project simulates the movement of planets and other celestial bodies around the sun in real-time.

## Features

- **Real Physics**: Newton's law of gravitation and Kepler's three laws implemented
- **3D Visualization**: Interactive 3D solar system using Three.js
- **Real-time Simulation**: High-accuracy calculations using Verlet integration
- **Orbit Analysis**: Calculation of orbital elements and energy analysis
- **Web-based Interface**: User-friendly control panel built with React

## Technologies

### Backend
- Python 3.x
- FastAPI (Web API)
- NumPy (Numerical computations)
- SciPy (Advanced mathematical operations)

### Frontend
- React 18
- TypeScript
- Three.js (3D visualization)
- @react-three/fiber (React-Three.js integration)
- @react-three/drei (Three.js helpers)

## Installation

### Backend Installation

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

API runs by default at `http://localhost:8000`.

### Frontend Installation

```bash
cd frontend
npm install
npm run dev
```

Frontend runs by default at `http://localhost:5173`.

## API Endpoints

- `GET /` - Health check
- `POST /simulation/add-body` - Add celestial body to simulation
- `POST /simulation/start` - Start simulation
- `POST /simulation/stop` - Stop simulation
- `POST /simulation/reset` - Reset simulation
- `GET /simulation/state` - Current simulation state
- `GET /simulation/orbital-elements/{body_name}` - Orbital elements
- `GET /simulation/energy-analysis` - Energy analysis
- `GET /simulation/trajectory/{body_name}` - Trajectory history

## Physical Constants

The project uses NASA/JPL standard values:
- Universal gravitational constant (G)
- Solar mass
- Astronomical Unit (AU)
- Speed of light

## Usage

1. Start the server (`uvicorn main:app`)
2. Start the frontend (`npm run dev`)
3. Go to `http://localhost:5173` in your browser
4. Manage simulation from control panel:
   - Add planets
   - Start/stop simulation
   - View orbital elements

## License

This project is for educational purposes.