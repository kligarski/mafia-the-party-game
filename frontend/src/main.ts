import './app.css'
import App from './App.svelte'

const gameCode = document.getElementById("game-code")?.textContent;

const app = new App({
  target: document.getElementById('app')!,
  props: {
    gameCode: gameCode ? String(gameCode.slice(1, -1)) : undefined
  }
})

export default app
