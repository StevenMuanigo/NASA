import { useFrame } from '@react-three/fiber'
import { useRef, useEffect, useState } from 'react'
import * as THREE from 'three'
import api from '../lib/api'

interface Body {
  name: string
  position: { x: number; y: number; z: number }
  radius: number
  color: string
}

export default function SimulationScene() {
  const [bodies, setBodies] = useState<Body[]>([])
  const [trajectories, setTrajectories] = useState<{ [key: string]: THREE.Vector3[] }>({})
  const sunRef = useRef<THREE.Mesh>(null)

  useEffect(() => {
    // Fetch initial state
    fetchState()
    
    // Poll for updates
    const interval = setInterval(fetchState, 100) // 10 FPS
    return () => clearInterval(interval)
  }, [])

  const fetchState = async () => {
    try {
      const response = await api.get('/simulation/state')
      const state = response.data
      
      // Convert positions from meters to AU for visualization
      const scaledBodies = state.bodies.map((body: any) => ({
        ...body,
        position: {
          x: body.position.x / 1.496e11, // Convert to AU
          y: body.position.y / 1.496e11,
          z: body.position.z / 1.496e11
        }
      }))
      
      setBodies(scaledBodies)
      
      // Fetch trajectories
      for (const body of scaledBodies) {
        if (body.name !== 'Sun') {
          try {
            const trajResponse = await api.get(`/simulation/trajectory/${body.name}`)
            const trajectory = trajResponse.data.trajectory.map((point: any) => 
              new THREE.Vector3(
                point.x / 1.496e11,
                point.y / 1.496e11,
                point.z / 1.496e11
              )
            )
            setTrajectories(prev => ({ ...prev, [body.name]: trajectory }))
          } catch (e) {
            // Ignore trajectory errors
          }
        }
      }
    } catch (error) {
      console.error('Failed to fetch state:', error)
    }
  }

  useFrame(() => {
    if (sunRef.current) {
      sunRef.current.rotation.y += 0.001
    }
  })

  return (
    <>
      {/* Sun */}
      <mesh ref={sunRef} position={[0, 0, 0]}>
        <sphereGeometry args={[0.5, 32, 32]} />
        <meshStandardMaterial color="#FFD700" emissive="#FFD700" emissiveIntensity={0.5} />
      </mesh>
      
      {/* Celestial Bodies */}
      {bodies.map((body, index) => {
        if (body.name === 'Sun') return null
        
        return (
          <group key={body.name}>
            {/* Trajectory Line */}
            {trajectories[body.name] && trajectories[body.name].length > 1 && (
              <line>
                <bufferGeometry>
                  <bufferAttribute
                    attach="attributes-position"
                    count={trajectories[body.name].length}
                    array={new Float32Array(
                      trajectories[body.name].flatMap(v => [v.x, v.y, v.z])
                    )}
                    itemSize={3}
                  />
                </bufferGeometry>
                <lineBasicMaterial 
                  color={body.color} 
                  opacity={0.6} 
                  transparent 
                  linewidth={2}
                />
              </line>
            )}
            
            {/* Body */}
            <mesh
              position={[body.position.x, body.position.y, body.position.z]}
            >
              <sphereGeometry args={[Math.max(0.08, body.radius / 1.496e11), 16, 16]} />
              <meshStandardMaterial 
                color={body.color}
                emissive={body.color}
                emissiveIntensity={0.3}
              />
            </mesh>
          </group>
        )
      })}
    </>
  )
}

