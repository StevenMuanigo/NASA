import { Canvas } from '@react-three/fiber'
import { OrbitControls, Stars } from '@react-three/drei'
import { Suspense } from 'react'
import SimulationScene from './components/SimulationScene'
import ControlPanel from './components/ControlPanel'
import Header from './components/Header'
import './App.css'

function App() {
  return (
    <div className="app-container">
      <Header />
      <div className="canvas-container">
        <Canvas
          camera={{ position: [0, 0, 50], fov: 60 }}
          gl={{ antialias: true }}
        >
          <Suspense fallback={null}>
            <ambientLight intensity={0.5} />
            <pointLight position={[0, 0, 0]} intensity={1} color="#FFD700" />
            <Stars radius={300} depth={50} count={5000} factor={4} />
            <SimulationScene />
            <OrbitControls
              enablePan={true}
              enableZoom={true}
              enableRotate={true}
              minDistance={5}
              maxDistance={200}
            />
          </Suspense>
        </Canvas>
      </div>
      <ControlPanel />
    </div>
  )
}

export default App

