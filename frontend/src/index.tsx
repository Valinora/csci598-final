/* @refresh reload */
import { render } from 'solid-js/web'
import './index.css'
import App from './App.tsx'

const root = document.getElementById('root')

// biome-ignore lint/style/noNonNullAssertion: Root must exist, no valid workaround.
render(() => <App />, root!)
