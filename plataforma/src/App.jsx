import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './style.css'; // Importa o estilo global (Verde)

// Componentes
import LandingPage from './components/LandingPage';
import EscolhaPerfil from './components/EscolhaPerfil';
import Login from './components/Login';
import CadastroAluno from './components/CadastroAluno';
import CadastroPsicologo from './components/CadastroPsicologo';
import PortalAluno from './components/PortalAluno';
import PortalAgenda from './components/PortalAgenda';

function App() {
  return (
    <Router>
      <Routes>
        {/* Tela Inicial */}
        <Route path="/" element={<LandingPage />} />
        
        {/* Fluxo de Entrada */}
        <Route path="/escolha-perfil" element={<EscolhaPerfil />} />
        <Route path="/login" element={<Login />} />
        <Route path="/cadastro-aluno" element={<CadastroAluno />} />
        <Route path="/cadastro-psicologo" element={<CadastroPsicologo />} />
        
        {/* Portais (Área Logada) */}
        <Route path="/portal-aluno" element={<PortalAluno />} />
        <Route path="/portal-psicologo" element={<PortalAgenda />} />

        {/* Rota de segurança (qualquer erro volta pro início) */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;