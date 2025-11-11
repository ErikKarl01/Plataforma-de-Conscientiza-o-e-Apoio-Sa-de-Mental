import React from 'react';
import { Link } from 'react-router-dom';
// Importando ícones
import { FaArrowLeft, FaBrain, FaUserGraduate } from 'react-icons/fa';

function CadastroSelecao() {
  return (
    <div className="container">
      {/* Link para voltar (ajuste o 'to' para sua rota de login) */}
      <Link to="/login" className="back-link">
        <FaArrowLeft /> Voltar para login
      </Link>
      
      <header className="header">
        <FaBrain className="logo-icon" />
        <h1>Cadastro</h1>
        <p>Gerenciamento dos atendimento</p>
      </header>
      
      <div className="selection-container">
        {/* Card Aluno (ajuste o 'to' para a rota de aluno) */}
        <Link to="/cadastro-aluno" className="card">
          <FaUserGraduate className="card-icon" />
          <h3>Aluno</h3>
        </Link>
        
        {/* Card Psicólogo */}
        <Link to="/cadastro-psicologo" className="card">
          <FaBrain className="card-icon" />
          <h3>Psicólogo</h3>
        </Link>
      </div>
    </div>
  );
}

export default CadastroSelecao;