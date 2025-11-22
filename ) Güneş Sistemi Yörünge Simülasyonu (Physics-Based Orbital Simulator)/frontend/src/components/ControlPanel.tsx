import { useState, useEffect } from 'react'
import api from '../lib/api'
import './ControlPanel.css'

interface BodyParams {
  name: string
  mass: number
  distance_from_sun: number
  initial_velocity: number
  angle: number
  color: string
}

export default function ControlPanel() {
  const [isRunning, setIsRunning] = useState(false)
  const [simulationTime, setSimulationTime] = useState(0)
  const [bodyParams, setBodyParams] = useState<BodyParams>({
    name: 'Asteroid',
    mass: 1e15, // kg
    distance_from_sun: 1.0, // AU
    initial_velocity: 30000, // m/s
    angle: 0,
    color: '#00ff00'
  })
  const [orbitalElements, setOrbitalElements] = useState<any>(null)

  useEffect(() => {
    const interval = setInterval(async () => {
      try {
        const state = await api.get('/simulation/state')
        setIsRunning(state.data.is_running)
        setSimulationTime(state.data.time)
      } catch (e) {
        console.error('Failed to fetch state:', e)
      }
    }, 100)
    return () => clearInterval(interval)
  }, [])

  const handleAddBody = async () => {
    try {
      await api.post('/simulation/add-body', bodyParams)
      alert(`Body "${bodyParams.name}" added to simulation!`)
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.detail || 'Failed to add body'}`)
    }
  }

  const handleStart = async () => {
    try {
      await api.post('/simulation/start')
      setIsRunning(true)
    } catch (error) {
      console.error('Failed to start:', error)
    }
  }

  const handleStop = async () => {
    try {
      await api.post('/simulation/stop')
      setIsRunning(false)
    } catch (error) {
      console.error('Failed to stop:', error)
    }
  }

  const handleReset = async () => {
    try {
      await api.post('/simulation/reset')
      setIsRunning(false)
      setSimulationTime(0)
      setOrbitalElements(null)
    } catch (error) {
      console.error('Failed to reset:', error)
    }
  }

  const handleGetOrbitalElements = async () => {
    try {
      const response = await api.get(`/simulation/orbital-elements/${bodyParams.name}`)
      setOrbitalElements(response.data)
    } catch (error: any) {
      alert(`Error: ${error.response?.data?.error || 'Failed to get orbital elements'}`)
    }
  }

  return (
    <div className="control-panel">
      <h2>🌌 Orbital Simulator</h2>
      
      <div className="section">
        <h3>Simulation Controls</h3>
        <div className="button-group">
          <button onClick={handleStart} disabled={isRunning}>
            ▶ Start
          </button>
          <button onClick={handleStop} disabled={!isRunning}>
            ⏸ Stop
          </button>
          <button onClick={handleReset}>🔄 Reset</button>
        </div>
        <div className="info">
          <p>Status: <span className={isRunning ? 'running' : 'stopped'}>
            {isRunning ? 'Running' : 'Stopped'}
          </span></p>
          <p>Time: {Math.floor(simulationTime / 86400)} days</p>
        </div>
      </div>

      <div className="section">
        <h3>Add Celestial Body</h3>
        <div className="form-group">
          <label>Name:</label>
          <input
            type="text"
            value={bodyParams.name}
            onChange={(e) => setBodyParams({ ...bodyParams, name: e.target.value })}
          />
        </div>
        <div className="form-group">
          <label>Mass (kg):</label>
          <input
            type="number"
            value={bodyParams.mass}
            onChange={(e) => setBodyParams({ ...bodyParams, mass: parseFloat(e.target.value) })}
          />
        </div>
        <div className="form-group">
          <label>Distance from Sun (AU):</label>
          <input
            type="number"
            step="0.1"
            value={bodyParams.distance_from_sun}
            onChange={(e) => setBodyParams({ ...bodyParams, distance_from_sun: parseFloat(e.target.value) })}
          />
        </div>
        <div className="form-group">
          <label>Initial Velocity (m/s):</label>
          <input
            type="number"
            value={bodyParams.initial_velocity}
            onChange={(e) => setBodyParams({ ...bodyParams, initial_velocity: parseFloat(e.target.value) })}
          />
        </div>
        <div className="form-group">
          <label>Angle (degrees):</label>
          <input
            type="number"
            step="1"
            value={bodyParams.angle}
            onChange={(e) => setBodyParams({ ...bodyParams, angle: parseFloat(e.target.value) })}
          />
        </div>
        <div className="form-group">
          <label>Color:</label>
          <input
            type="color"
            value={bodyParams.color}
            onChange={(e) => setBodyParams({ ...bodyParams, color: e.target.value })}
          />
        </div>
        <button onClick={handleAddBody} className="add-button">
          ➕ Add Body
        </button>
        <button onClick={handleGetOrbitalElements} className="info-button">
          📊 Get Orbital Elements
        </button>
      </div>

      {orbitalElements && (
        <div className="section">
          <h3>Orbital Elements</h3>
          <div className="orbital-info">
            <p>Semi-major axis: {orbitalElements.semi_major_axis?.toFixed(2)} m</p>
            <p>Eccentricity: {orbitalElements.eccentricity?.toFixed(4)}</p>
            <p>Inclination: {orbitalElements.inclination?.toFixed(2)}°</p>
            <p>Period: {orbitalElements.period ? (orbitalElements.period / 86400).toFixed(2) : 'N/A'} days</p>
            <p>Periapsis: {orbitalElements.periapsis ? (orbitalElements.periapsis / 1.496e11).toFixed(2) : 'N/A'} AU</p>
            <p>Apoapsis: {orbitalElements.apoapsis ? (orbitalElements.apoapsis / 1.496e11).toFixed(2) : 'N/A'} AU</p>
          </div>
        </div>
      )}
    </div>
  )
}

