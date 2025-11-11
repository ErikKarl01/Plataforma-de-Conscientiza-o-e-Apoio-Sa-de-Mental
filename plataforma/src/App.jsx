import React from 'react'
import { Routes, Route } from 'react-router-dom'
import CadastroSelecao from './components/CadastroSelecao'
import CadastroPsicologo from './components/CadastroPsicologo'

function App() {
  return (
    <Routes>
      {/* Rota inicial - Tela de Seleção */}
      <Route path="/" element={<CadastroSelecao />} />
      
      {/* Rota para o cadastro do psicólogo */}
      <Route path="/cadastro-psicologo" element={<CadastroPsicologo />} />
      
      {/* Você pode adicionar a rota para /cadastro-aluno aqui quando criar o componente */}
      {/* <Route path="/cadastro-aluno" element={<CadastroAluno />} /> */}

      {/* Rota de login (para o link "Voltar") */}
      {/* <Route path="/login" element={<Login />} /> */}
    </Routes>
  )
}

export default App