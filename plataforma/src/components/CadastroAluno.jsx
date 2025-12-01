import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaArrowLeft, FaBrain } from 'react-icons/fa';

function CadastroAluno() {
  const [nome, setNome] = useState('');
  const [email, setEmail] = useState('');
  const [telefone, setTelefone] = useState('');
  const [senha, setSenha] = useState('');
  const [confirmarSenha, setConfirmarSenha] = useState('');

  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (senha !== confirmarSenha) {
      setError('As senhas não coincidem.');
      return;
    }

    setError(null);
    setIsSuccess(false);
    setIsLoading(true);

    try {
      // Remove caracteres não numéricos do telefone para enviar ao backend
      const telefoneLimpo = telefone.replace(/\D/g, "");

      const dataToSend = { 
        nome, 
        email, 
        telefone: telefoneLimpo, 
        senha 
      };

      // Rota específica do estudante definida no app.py
      const response = await fetch('http://127.0.0.1:5000/cadastrar_estudante', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.erro || 'Falha no cadastro. Tente novamente.');
      }

      setIsSuccess(true);
      // Redireciona para o login após 2 segundos
      setTimeout(() => navigate('/login'), 2000);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <Link to="/login" className="back-link">
        <FaArrowLeft /> Voltar para login
      </Link>

      <header className="header">
        <div className="logo-icon" style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <FaBrain />
        </div>
        <h1>Cadastro Aluno</h1>
        <p>Preencha seus dados para começar a gerenciar sua agenda</p>
      </header>

      {!isSuccess ? (
        <form className="form-container" onSubmit={handleSubmit}>
          <h2>Criar Conta</h2>
          <p className="form-subtitle">Preencha o formulário abaixo para criar sua conta</p>

          <div className="form-grid">
            <div className="form-group">
              <label htmlFor="nome">Nome completo</label>
              <input
                type="text"
                id="nome"
                placeholder="ex. maria da silva"
                value={nome}
                onChange={(e) => setNome(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="telefone">Telefone</label>
              <input
                type="tel"
                id="telefone"
                placeholder="(88) 9 9999-9999"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="email">E-mail</label>
              <input
                type="email"
                id="email"
                placeholder="email@gmail.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              {/* Espaço vazio para manter o grid alinhado ou pode ser removido se quiser 
                  que a senha ocupe a próxima linha. Mantendo a estrutura do design visual */}
               <label style={{ visibility: 'hidden' }}>Placeholder</label>
               <div style={{ height: '42px' }}></div>
            </div>

            <div className="form-group">
              <label htmlFor="senha">Senha</label>
              <input
                type="password"
                id="senha"
                placeholder=".................."
                value={senha}
                onChange={(e) => setSenha(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="confirmarSenha">Confirmar senha</label>
              <input
                type="password"
                id="confirmarSenha"
                placeholder=".................."
                value={confirmarSenha}
                onChange={(e) => setConfirmarSenha(e.target.value)}
                required
              />
            </div>
          </div>

          {error && (
            <div className="message-container error-message">
              <p>{error}</p>
            </div>
          )}

          <button type="submit" className="submit-button" disabled={isLoading}>
            {isLoading ? 'Cadastrando...' : 'Criar conta'}
          </button>
        </form>
      ) : (
        <div className="form-container message-container success-message">
          <h2>Cadastro realizado com sucesso!</h2>
          <p>Você será redirecionado para o login em instantes...</p>
        </div>
      )}
    </div>
  );
}

export default CadastroAluno;