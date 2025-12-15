import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBrain, FaArrowLeft } from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';

export default function CadastroAluno() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ nome: '', telefone: '', email: '', senha: '', confirmSenha: '' });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (form.senha !== form.confirmSenha) return alert("As senhas não coincidem!");

    try {
        const res = await fetch(`${API_URL}/cadastrar_estudante`, {
            method: 'POST', headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(form)
        });
        const data = await res.json();
        if(res.ok) { alert("Cadastro realizado com sucesso!"); navigate('/login?tipo=aluno'); } 
        else alert(data.erro || "Erro ao cadastrar.");
    } catch (err) { alert("Erro de conexão.", err); }
  };

  return (
    <div className="page-wrapper">
      <div className="container-custom">
        
        <div className="nav-header">
          <div className="btn-back" onClick={() => navigate('/login?tipo=aluno')}>
            <FaArrowLeft /> <span>Voltar para login</span>
          </div>
          <div className="logo-box"><FaBrain /></div>
        </div>

        <div className="form-container-wide">
          <div style={{textAlign:'center'}}>
            <h1 className="page-headline">Cadastro Aluno</h1>
            <p className="page-subheadline">Preencha seus dados para começar a gerenciar sua agenda</p>
          </div>

          <div className="card-auth">
            <h2 style={{fontSize:'1.25rem', fontWeight:'600', marginBottom:'0.5rem'}}>Criar Conta</h2>
            <p style={{fontSize:'0.875rem', color:'var(--text-muted)', marginBottom:'1.5rem'}}>Preencha o formulário abaixo para criar sua conta</p>

            <form onSubmit={handleSubmit}>
              <div className="form-grid">
                <div>
                  <label className="input-label">Nome completo</label>
                  <input className="input-field" placeholder="ex. Maria da Silva" required
                         value={form.nome} onChange={e => setForm({...form, nome: e.target.value})} />
                </div>
                <div>
                  <label className="input-label">Telefone</label>
                  <input className="input-field" placeholder="(88) 9 9999-9999" required
                         value={form.telefone} onChange={e => setForm({...form, telefone: e.target.value})} />
                </div>
              </div>

              <div className="form-grid">
                <div>
                  <label className="input-label">E-mail</label>
                  <input type="email" className="input-field" placeholder="email@gmail.com" required
                         value={form.email} onChange={e => setForm({...form, email: e.target.value})} />
                </div>
                <div>
                  <label className="input-label">Senha</label>
                  <input type="password" className="input-field" placeholder="••••••••" required
                         value={form.senha} onChange={e => setForm({...form, senha: e.target.value})} />
                </div>
              </div>

              <div className="form-grid">
                <div style={{gridColumn: '1 / -1'}}> 
                  <label className="input-label">Confirmar senha</label>
                  <input type="password" className="input-field" placeholder="••••••••" required
                         value={form.confirmSenha} onChange={e => setForm({...form, confirmSenha: e.target.value})} />
                </div>
              </div>

              <button type="submit" className="btn-primary-full">Criar conta</button>
            </form>
          </div>
        </div>

      </div>
    </div>
  );
}