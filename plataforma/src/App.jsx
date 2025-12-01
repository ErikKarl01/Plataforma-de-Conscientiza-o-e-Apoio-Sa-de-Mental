import { Routes, Route } from 'react-router-dom';
import Home from './components/Home';
import Login from './components/Login';
import CadastroSelecao from './components/CadastroSelecao';
import CadastroPsicologo from './components/CadastroPsicologo';
import CadastroAluno from './components/CadastroAluno';
import PortalAgendas from './components/PortalAgenda';
import PortalAluno from './components/PortalAluno'; // Portal do Aluno

function App() {
  return (
    <Routes>
      {/* Página inicial */}
      <Route path="/" element={<Home />} />

      {/* Seleção de cadastro */}
      <Route path="/selecao" element={<CadastroSelecao />} />

      {/* Cadastros */}
      <Route path="/cadastro-psicologo" element={<CadastroPsicologo />} />
      <Route path="/cadastro-aluno" element={<CadastroAluno />} />

      {/* Portais (Áreas Logadas) */}
      <Route path="/agenda" element={<PortalAgendas />} /> {/* Psicólogo */}
      <Route path="/portal-aluno" element={<PortalAluno />} /> {/* Aluno */}

      {/* Login */}
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}

export default App;
