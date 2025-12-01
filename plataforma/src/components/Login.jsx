import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaBrain, FaArrowLeft, FaEnvelope, FaLock } from 'react-icons/fa6'; 

// URL API
const API_URL = 'http://127.0.0.1:5000'; 

function Login() {
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError(null);

    if (!email || !senha) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    try {
      const response = await fetch(`${API_URL}/login`, { 
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.mensagem || 'Erro ao fazer login.');
      }

      // Login bem-sucedido
      if (data.usuario && data.tipo) {
        sessionStorage.setItem('tipoUsuario', data.tipo);

        if (data.tipo === 'psicologo') {
          // Psicólogo
          localStorage.setItem("idPsicologo", data.usuario.id); 
          localStorage.removeItem("dadosAluno"); // Limpa dados antigos se houver
          navigate('/agenda');
          window.location.reload();
        } else {
          // Estudante
          localStorage.setItem("dadosAluno", JSON.stringify(data.usuario));
          localStorage.removeItem("idPsicologo"); // Limpa id de psicólogo se houver
          navigate('/portal-aluno'); // Redireciona para portal do aluno
        }
      } else {
        setError('Resposta inválida do servidor.');
      }

    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="container">
      <Link to="/" className="back-link">
        <FaArrowLeft /> Voltar para home
      </Link>

      <div className="header">
        <FaBrain className="logo-icon" />
        <h1>Portal de Atendimento</h1>
        <p>Gerenciamento dos atendimentos</p>
      </div>

      <div className="form-container">
        <div className="login-intro">
          <h2>Entrar</h2>
          <p className="form-subtitle">Digite suas credenciais para acessar</p>
        </div>

        <form onSubmit={handleLogin}>
          <div className="form-group">
            <label htmlFor="email">Email</label>
            <div className="input-with-icon">
              <FaEnvelope className="input-icon" />
              <input
                type="email"
                id="email"
                placeholder="nome@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
          </div>

          <div className="form-group">
            <label htmlFor="senha">Senha</label>
            <div className="input-with-icon">
              <FaLock className="input-icon" />
              <input
                type="password"
                id="senha"
                placeholder="**********"
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
              />
            </div>
          </div>

          {error && (
            <div className="message-container error-message">
              <p>{error}</p>
            </div>
          )}

          <button type="submit" className="submit-button">
            Entrar
          </button>
        </form>
      </div>

      <p className="cadastro-link-text">
        Ainda não tem cadastro? <Link to="/selecao" className="link-highlight">Cadastre-se</Link>
      </p>
    </div>
  );
}

export default Login;
