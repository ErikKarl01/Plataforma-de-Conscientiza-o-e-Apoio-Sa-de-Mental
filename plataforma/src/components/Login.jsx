import React, { useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { FaBrain, FaArrowLeft, FaEnvelope, FaLock } from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';

export default function Login() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const tipoParam = searchParams.get('tipo'); 

  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/login`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, senha })
      });
      const data = await res.json();
      
      if (res.ok) {
        if (data.tipo === 'estudante') {
            localStorage.setItem("dadosAluno", JSON.stringify(data.usuario));
            navigate('/portal-aluno');
        } else if (data.tipo === 'psicologo') {
            localStorage.setItem("idPsicologo", data.usuario.id);
            navigate('/portal-psicologo');
        }
      } else {
        alert(data.erro || "Falha no login. Verifique as credenciais.");
      }
    } catch (err) { alert("Erro de conexão com o servidor.", err); } 
    finally { setLoading(false); }
  };

  const irParaCadastro = () => {
      if(tipoParam === 'psicologo') navigate('/cadastro-psicologo');
      else navigate('/cadastro-aluno');
  };

  return (
    <div className="page-wrapper">
      <div className="container-custom">
        
        <div className="nav-header">
          <div className="btn-back" onClick={() => navigate('/escolha-perfil')}>
            <FaArrowLeft /> <span>Voltar</span>
          </div>
          <div className="logo-box"><FaBrain /></div>
        </div>

        <div className="form-container-narrow">
          <h1 className="page-headline">Login</h1>
          <p className="page-subheadline">Gerenciamento dos atendimentos</p>

          <div className="card-auth">
            <h2 style={{fontSize:'1.25rem', fontWeight:'600', marginBottom:'0.5rem'}}>Entrar</h2>
            <p style={{fontSize:'0.875rem', color:'var(--text-muted)', marginBottom:'1.5rem'}}>Digite suas credenciais para acessar</p>

            <form onSubmit={handleLogin}>
              <div className="input-group">
                <label className="input-label">Email</label>
                <div className="input-wrapper">
                  <FaEnvelope className="input-icon-left" />
                  <input type="email" className="input-field with-icon" required
                         value={email} onChange={e => setEmail(e.target.value)} />
                </div>
              </div>

              <div className="input-group">
                <label className="input-label">Senha</label>
                <div className="input-wrapper">
                  <FaLock className="input-icon-left" />
                  <input type="password" className="input-field with-icon" required
                         value={senha} onChange={e => setSenha(e.target.value)} />
                </div>
              </div>

              <button type="submit" className="btn-primary-full" disabled={loading}>
                {loading ? 'Entrando...' : 'Entrar'}
              </button>
            </form>
          </div>

          <p style={{textAlign:'center', marginTop:'1.5rem', color:'var(--text-muted)'}}>
            Ainda não tem cadastro? <span className="text-link" onClick={irParaCadastro}>Cadastre-se</span>
          </p>
        </div>

      </div>
    </div>
  );
}