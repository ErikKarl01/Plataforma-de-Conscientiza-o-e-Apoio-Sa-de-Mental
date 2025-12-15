import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaGraduationCap, FaBrain, FaArrowLeft } from 'react-icons/fa';

export default function EscolhaPerfil() {
  const navigate = useNavigate();

  return (
    <div className="page-wrapper">
      <div className="container-custom">
        {/* Header */}
        <div className="nav-header">
          <div className="btn-back" onClick={() => navigate('/')}>
            <FaArrowLeft /> <span>Voltar para login</span>
          </div>
          <div className="logo-box">
            <FaBrain />
          </div>
        </div>

        {/* Content */}
        <div className="form-container-wide" style={{textAlign:'center'}}>
          <h1 className="page-headline">Portal de atendimento</h1>
          <p className="page-subheadline">Como você deseja entrar?</p>

          <div className="profile-grid">
            {/* Card Aluno */}
            <div className="profile-card" onClick={() => navigate('/login?tipo=aluno')}>
              <div className="profile-icon"><FaGraduationCap /></div>
              <h2 className="profile-title">Aluno</h2>
            </div>

            {/* Card Psicólogo */}
            <div className="profile-card" onClick={() => navigate('/login?tipo=psicologo')}>
              <div className="profile-icon"><FaBrain /></div>
              <h2 className="profile-title">Psicólogo</h2>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}