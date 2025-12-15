import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './style.css'  // <--- Carrega o estilo geral (Verde/Teal) para o app todo

// REMOVA a linha: import './App.css' daqui!

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)