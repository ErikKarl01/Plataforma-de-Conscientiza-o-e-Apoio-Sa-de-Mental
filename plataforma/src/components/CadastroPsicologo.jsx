import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaArrowLeft, FaBrain } from 'react-icons/fa';

function CadastroPsicologo() {
  const [nome, setNome] = useState('');
  const [crp, setCrp] = useState('');
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
      const dataToSend = { nome, crp, email, telefone, senha };
        //colocar link da api/back 
      const response = await fetch('http://127.0.0.1:5000/cadastrar', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(dataToSend),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.message || 'Falha no cadastro. Tente novamente.');
      }

      setIsSuccess(true);

      setTimeout(() => {
        navigate('/login');
      }, 2000);

    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <Link to="/" className="back-link">
        <FaArrowLeft /> Voltar para login
      </Link>

      <header className="header">
        <FaBrain className="logo-icon" />
        <h1>Cadastro de Psicólogo</h1>
        <p>Preencha seus dados para começar a gerenciar sua agenda</p>
      </header>

      {!isSuccess ? (
        <form className="form-container" onSubmit={handleSubmit}>
          <h2>Criar Conta</h2>
          <p className="form-subtitle">Preencha o formulário a baixo para criar sua conta</p>
          
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
              <label htmlFor="crp">CRP</label>
              <input
                type="text"
                id="crp"
                placeholder="00/0000"
                value={crp}
                onChange={(e) => setCrp(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="email">E-mail</label>
              <input
                type="email"
                id="email"
                placeholder="email@email.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="telefone">Telefone</label>
              <input
                type="tel"
                id="telefone"
                placeholder="(00) 9 9999-9999"
                value={telefone}
                onChange={(e) => setTelefone(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="senha">Senha</label>
              <input
                type="password"
                id="senha"
                placeholder="Digite sua senha"
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
                placeholder="Confirme sua senha"
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

export default CadastroPsicologo;