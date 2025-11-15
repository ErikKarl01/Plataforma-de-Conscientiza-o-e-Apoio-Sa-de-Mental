import { Routes, Route } from 'react-router-dom'
import CadastroSelecao from './components/CadastroSelecao'
import CadastroPsicologo from './components/CadastroPsicologo'
import PortalAgendas from './components/PortalAgenda'
import Home from './components/Home'
import Login from './components/Login'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/cadastro-psicologo" element={<CadastroPsicologo />} />
      <Route path="/agenda" element={<PortalAgendas />} />
      <Route path="/login" element={<Login />} /> 
      <Route path="/selecao" element={<CadastroSelecao />} />
    </Routes>
  )
}

export default App