import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBrain, FaSignOutAlt, FaClipboardList, FaCheckCircle, FaRegClock } from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';

function PortalAluno() {
  const [activeTab, setActiveTab] = useState('horariosDisponiveis');
  const [horariosLivres, setHorariosLivres] = useState([]);
  const [minhasConsultas, setMinhasConsultas] = useState([]);
  const [horarioSelecionado, setHorarioSelecionado] = useState(null);
  const [motivoConsulta, setMotivoConsulta] = useState('');
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);
  const navigate = useNavigate();

  const dadosAluno = useMemo(() => JSON.parse(localStorage.getItem("dadosAluno")), []);
  const handleLogout = () => { localStorage.clear(); navigate('/login'); };

  const fetchLivres = useCallback(async () => {
      try {
          const res = await fetch(`${API_URL}/listar_horarios_livres`, { 
              method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({}) 
          });
          const data = await res.json();
          setHorariosLivres(Array.isArray(data) ? data : []);
      } catch (e) { console.error(e); }
  }, []);

  const fetchMinhas = useCallback(async () => {
      if(!dadosAluno) return;
      try {
          const res = await fetch(`${API_URL}/listar_minhas_solicitacoes`, {
              method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({id: dadosAluno.id})
          });
          if(res.ok) setMinhasConsultas(await res.json());
      } catch (e) { console.error(e); }
  }, [dadosAluno]);

  useEffect(() => {
      if(!dadosAluno) navigate('/login');
      else { fetchLivres(); fetchMinhas(); }
  }, [activeTab]);

  const confirmar = async () => {
      if(!horarioSelecionado) return;
      setError(null); setSuccessMsg(null);
      
      const payload = {
          idEstudante: dadosAluno.id,
          nomePaci: dadosAluno.nome, emailPaci: dadosAluno.email, telefonePaci: dadosAluno.telefone,
          
          // --- CORREÇÃO: ENVIA ID DIRETO ---
          idPsicologo: horarioSelecionado.idPsicologo, 
          nome: horarioSelecionado.nomePsi, 
          
          data: horarioSelecionado.data,
          horario: horarioSelecionado.horario,
          causa: motivoConsulta
      };
      
      console.log("Enviando:", payload); // Debug no console do navegador

      try {
          const res = await fetch(`${API_URL}/reservar_data_horario`, {
              method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify(payload)
          });
          const json = await res.json();
          if(!res.ok) throw new Error(json.erro || json.mensagem || 'Erro');
          
          setSuccessMsg("Solicitação enviada!");
          setHorarioSelecionado(null);
          setMotivoConsulta('');
          fetchLivres(); 
          setTimeout(() => setActiveTab('minhasConsultas'), 1500);
      } catch (e) { setError(e.message); }
  };

  const cancelar = async (c) => {
      if(!window.confirm("Cancelar?")) return;
      await fetch(`${API_URL}/cancelar_reserva`, {
          method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({nome: c.nomePsi, data: c.data, horario: c.horario, idPsicologo: c.idPsicologo})
      });
      fetchMinhas(); fetchLivres();
  };

  const agrupados = horariosLivres.reduce((acc, curr) => {
      const d = curr.data; if(!acc[d]) acc[d]=[]; acc[d].push(curr); return acc;
  }, {});

  return (
    <div className="agenda-container">
      <header className="agenda-header">
        <div className="logo-section"><h1>Portal Aluno</h1></div>
        <button onClick={handleLogout} className="sair-link"><FaSignOutAlt /> Sair</button>
      </header>
      <div className="tab-navigation">
          <button className={activeTab === 'horariosDisponiveis' ? 'active' : ''} onClick={() => setActiveTab('horariosDisponiveis')}><FaClipboardList /> Disponíveis</button>
          <button className={activeTab === 'minhasConsultas' ? 'active' : ''} onClick={() => setActiveTab('minhasConsultas')}><FaCheckCircle /> Minhas</button>
      </div>
      <main className="agenda-main" style={{display:'flex', gap:'20px'}}>
        {activeTab === 'horariosDisponiveis' && (
            <>
                <div style={{flex:2}}>
                    {Object.keys(agrupados).length === 0 && <p>Nenhum horário.</p>}
                    {Object.keys(agrupados).map(d => (
                        <div key={d} className="horario-group-item">
                            <strong>{d}</strong>
                            <div className="horario-time-chip-container">
                                {agrupados[d].map(h => (
                                    <button key={h.id} className={`horario-chip-btn ${horarioSelecionado?.id===h.id ? 'selected':''}`} onClick={() => setHorarioSelecionado(h)}>
                                        {h.horario} <small>({h.nomePsi})</small>
                                    </button>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
                <div style={{flex:1}} className="resumo-card">
                    {horarioSelecionado ? (
                        <>
                            <h3>Confirmar</h3>
                            <p>{horarioSelecionado.data} - {horarioSelecionado.horario}</p>
                            <p><strong>{horarioSelecionado.nomePsi}</strong></p>
                            <textarea placeholder="Motivo..." value={motivoConsulta} onChange={e => setMotivoConsulta(e.target.value)}></textarea>
                            {error && <p className="error-text">{error}</p>}
                            {successMsg && <p className="success-text">{successMsg}</p>}
                            <button className="btn-confirmar" onClick={confirmar}>Enviar</button>
                        </>
                    ) : <p>Selecione um horário</p>}
                </div>
            </>
        )}
        {activeTab === 'minhasConsultas' && (
            <div style={{width:'100%'}}>
                {minhasConsultas.map(c => (
                    <div key={c.id || Math.random()} className={`status-card ${c.status_desc==='Confirmada'?'card-confirmada':'card-pendente'}`} style={{border:'1px solid #ccc', padding:'10px', margin:'5px'}}>
                        <strong>{c.status_desc === 'Confirmada' ? 'CONFIRMADA' : 'PENDENTE'}</strong>
                        <div>{c.data} - {c.horario} com {c.nomePsi}</div>
                        <button onClick={() => cancelar(c)} style={{background:'#d9534f', color:'white', float:'right'}}>Cancelar</button>
                    </div>
                ))}
            </div>
        )}
      </main>
    </div>
  );
}
export default PortalAluno;