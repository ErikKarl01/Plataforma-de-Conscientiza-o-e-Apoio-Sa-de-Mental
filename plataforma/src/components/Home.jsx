import React from 'react';
import { Link } from 'react-router-dom';
import { FaBrain } from 'react-icons/fa'; 

function Home() {
  return (
    <div className="home-container">
      <main className="home-main">
        <Link to="/" className="home-logo-link" style={{ marginBottom: '2rem' }}>
          <FaBrain />
        </Link>
        
        <h1>Plataforma de Conscientização e Apoio à Saúde Mental</h1>
        <p>
          Plataforma Online de Conscientização e Apoio à Saúde Mental, que atuará como
          o canal primário para conscientizar os alunos sobre a importância da saúde mental.
          Facilitar o acesso e o agendamento de consultas com profissionais de psicologia,
          fornecer ferramentas de autoavaliação e acompanhamento emocional.
        </p>

        <Link to="/login" className="home-login-btn" style={{ marginTop: '2.5rem' }}>
          Login
        </Link>
      </main>
    </div>
  );
}

export default Home;
