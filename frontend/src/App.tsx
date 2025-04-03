import { createSignal } from 'solid-js'
// import './App.css'
import {Navbar} from './Navbar.tsx';

function App() {
  const [count, setCount] = createSignal(0)

  return (
      <Navbar active="index"/>
  )
}

export default App
