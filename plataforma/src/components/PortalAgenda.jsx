import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaBrain, FaSignOutAlt, FaCalendarAlt, FaClock, FaCheckCircle, 
  FaBell, FaPlus, FaTrash, FaUser, FaCalendarCheck, FaTimes, FaCheck, 
  FaUserEdit, FaExchangeAlt, FaHourglassHalf 
} from 'react-icons/fa';

import '../portal-psicologo.css';

const API_URL = 'http://127.0.0.1:5000';

export default function PortalAgenda() {
  const navigate = useNavigate();
  const [idPsi, setIdPsi] = useState(null);
  
  // -- DADOS --
  const [agendamentos, setAgendamentos] = useState([]); 
  const [meusHorarios, setMeusHorarios] = useState([]); 
  const [solicitacoes, setSolicitacoes] = useState([]); 
  const [concluidas, setConcluidas] = useState([]); 

  // -- UI --
  const [activeTab, setActiveTab] = useState('agenda');
  const [showNotifications, setShowNotifications] = useState(false);
  const [loading, setLoading] = useState(false); // Variável que estava sem uso

  // -- MODAIS --
  const [showModalFree, setShowModalFree] = useState(false);   
  const [showModalManual, setShowModalManual] = useState(false);
  const [showModalRemarcar, setShowModalRemarcar] = useState(false);
  const [itemParaRemarcar, setItemParaRemarcar] = useState(null);

  // -- FORMS --
  const [newSchedule, setNewSchedule] = useState({ date: '', time: '', duration: 50 });
  const [manualForm, setManualForm] = useState({ patientName: '', date: '', time: '', duration: 50 });

  useEffect(() => {
    const storedId = localStorage.getItem('idPsicologo');
    if (!storedId) { navigate('/login'); return; }
    setIdPsi(storedId);
    carregarDados(storedId);
  }, [navigate]);

  const carregarDados = useCallback(async (id) => {
    try {
      const [resConf, resLivre, resSol] = await Promise.all([
        fetch(`${API_URL}/listar_consultas`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idPsicologo: id }) }),
        fetch(`${API_URL}/listar_horarios_livres_psi`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idPsicologo: id }) }),
        fetch(`${API_URL}/listar_solicitacoes_atendimento`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ idPsicologo: id }) })
      ]);

      const dataConf = await resConf.json();
      const dataLivre = await resLivre.json();
      const dataSol = await resSol.json();

      setMeusHorarios(Array.isArray(dataLivre) ? dataLivre : []);
      setSolicitacoes(Array.isArray(dataSol) ? dataSol : []);

      const listaConfirmada = Array.isArray(dataConf) ? dataConf : [];
      const hoje = new Date().toISOString().split('T')[0];
      
      setAgendamentos(listaConfirmada.filter(c => c.data >= hoje));
      setConcluidas(listaConfirmada.filter(c => c.data < hoje));

    } catch (error) { console.error(error); }
  }, []);

  // --- HANDLERS ---
  const handleAddFreeSlot = async (e) => {
    e.preventDefault(); 
    setLoading(true); // Ativa loading
    try {
      const res = await fetch(`${API_URL}/adicionar_horario`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ idPsicologo: idPsi, data: newSchedule.date, hora: newSchedule.time, duracao: newSchedule.duration })
      });
      if(res.ok) { setShowModalFree(false); setNewSchedule({ date: '', time: '', duration: 50 }); carregarDados(idPsi); }
    } catch (err) { alert("Erro conexão", err); } 
    finally { setLoading(false); } // Desativa loading
  };

  const handleManualBooking = async (e) => {
    e.preventDefault();
    if(!manualForm.patientName || !manualForm.date || !manualForm.time) return;
    setLoading(true); // Ativa loading
    try {
      const res = await fetch(`${API_URL}/marcar_consulta`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
          idPsicologo: idPsi, 
          nomePaciente: manualForm.patientName, 
          data: manualForm.date, 
          hora: manualForm.time, 
          duracao: manualForm.duration 
        })
      });
      if(res.ok) { 
        setShowModalManual(false); 
        setManualForm({ patientName: '', date: '', time: '', duration: 50 }); 
        carregarDados(idPsi); 
        alert("Agendado!"); 
      }
    } catch (err) { alert("Erro conexão", err); } 
    finally { setLoading(false); } // Desativa loading
  };

  const handleAcao = async (idConsulta, acao) => {
    const endpoint = acao === 'confirmar' ? '/confirmar_agendamento' : '/cancelar_reserva';
    try {
      const res = await fetch(`${API_URL}${endpoint}`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: idConsulta }) });
      if (res.ok) carregarDados(idPsi);
    } catch (err) { console.error(err); }
  };

  const handleDeleteSlot = async (id) => {
    if(!window.confirm("Remover este horário?")) return;
    try {
      await fetch(`${API_URL}/remover_consulta`, { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({ id: id, acao: 'remover_fisicamente' }) });
      carregarDados(idPsi);
    } catch (err) { console.error(err); }
  };

  // --- REMARCAÇÃO ---
  const abrirModalRemarcar = (idConsulta) => {
    setItemParaRemarcar(idConsulta);
    setShowModalRemarcar(true);
  };

  const confirmarRemarcacaoPsi = async (idNovoSlot) => {
    if(!window.confirm("Trocar para este horário?")) return;
    try {
      const res = await fetch(`${API_URL}/remarcar_consulta_psi`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ idAntiga: itemParaRemarcar, idNova: idNovoSlot })
      });
      if(res.ok) {
        alert("Remarcado com sucesso!");
        setShowModalRemarcar(false);
        setItemParaRemarcar(null);
        carregarDados(idPsi);
      } else { alert("Erro ao remarcar"); }
    } catch (err) { alert("Erro conexão", err); }
  };

  const handleLogout = () => { localStorage.removeItem('idPsicologo'); navigate('/'); };
  const formatDate = (d) => { if(!d) return ''; const [a,m,dia] = d.split('-'); return `${dia}/${m}/${a}`; };

  return (
    <div className="portal-psi-wrapper">
      <header className="psi-header">
        <div className="psi-header-content">
          <div className="psi-brand">
            <div className="psi-logo-box"><FaBrain size={24} /></div>
            <div className="psi-title"><h1>Portal do Psicólogo</h1><p>Agenda</p></div>
          </div>
          <button className="psi-btn-logout" onClick={handleLogout}><FaSignOutAlt /> Sair</button>
        </div>
      </header>

      <main className="psi-container">
        <div className="psi-actions-bar">
          <div className="psi-tabs-list">
            <button className={`psi-tab-trigger ${activeTab === 'agenda' ? 'active' : ''}`} onClick={() => setActiveTab('agenda')}><FaCalendarAlt /> Minha Agenda</button>
            <button className={`psi-tab-trigger ${activeTab === 'schedules' ? 'active' : ''}`} onClick={() => setActiveTab('schedules')}><FaClock /> Meus Horários</button>
            <button className={`psi-tab-trigger ${activeTab === 'completed' ? 'active' : ''}`} onClick={() => setActiveTab('completed')}><FaCalendarCheck /> Concluídas</button>
          </div>
          <div style={{display:'flex', gap:'1rem'}}>
            <button className="psi-icon-btn" onClick={() => setShowNotifications(!showNotifications)}>
              <FaBell /> {solicitacoes.length > 0 && <span className="psi-badge-dot">{solicitacoes.length}</span>}
            </button>
            
            {activeTab === 'agenda' && <button className="psi-btn-primary" onClick={() => setShowModalManual(true)}><FaPlus /> Nova Consulta</button>}
            {activeTab === 'schedules' && <button className="psi-btn-primary" onClick={() => setShowModalFree(true)}><FaPlus /> Novo Horário</button>}
          </div>
        </div>

        {/* NOTIFICAÇÕES */}
        {showNotifications && (
          <div className="psi-card" style={{borderLeft:'4px solid #F59E0B', marginBottom:'2rem'}}>
            <div className="psi-card-header"><h3 className="psi-card-title" style={{color:'#D97706'}}><FaBell /> Solicitações Pendentes</h3></div>
            <div className="psi-card-body">
              {solicitacoes.length === 0 ? <p style={{color:'var(--muted-fg)'}}>Nenhuma solicitação.</p> : (
                <div className="psi-slot-list">
                  {solicitacoes.map(sol => (
                    <div key={sol.id} className="psi-slot-item" style={{background:'#FFFBEB', borderColor:'#FCD34D'}}>
                      <div className="psi-slot-info">
                        <div className="psi-avatar" style={{background:'#FEF3C7', color:'#D97706'}}><FaUser /></div>
                        <div>
                          <h4 style={{color:'#111827'}}>{sol.nomeAluno || 'Aluno'}</h4>
                          <div className="psi-slot-meta"><span>{formatDate(sol.data)} às {sol.hora}</span></div>
                        </div>
                      </div>
                      <div style={{display:'flex', gap:'0.5rem'}}>
                        <button className="psi-btn-primary" style={{padding:'0.5rem', background:'#10B981'}} onClick={() => handleAcao(sol.id, 'confirmar')}><FaCheck /></button>
                        <button className="psi-btn-danger" onClick={() => handleAcao(sol.id, 'recusar')}><FaTimes /></button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 1: AGENDA */}
        {activeTab === 'agenda' && (
          <div className="psi-card">
            <div className="psi-card-header"><h3 className="psi-card-title">Consultas Agendadas</h3></div>
            <div className="psi-card-body">
              {agendamentos.length === 0 ? (
                <div className="psi-empty-state"><FaCalendarAlt size={40} style={{marginBottom:'1rem', opacity:0.3}} /><p>Nenhuma consulta futura.</p></div>
              ) : (
                <div className="psi-slot-list">
                  {agendamentos.map(ag => (
                    <div key={ag.id} className="psi-slot-item" style={{borderLeft:'4px solid var(--primary)'}}>
                      <div className="psi-slot-info">
                        <div className="psi-avatar"><FaUser /></div>
                        <div>
                          <h4>{ag.nomeAluno}</h4>
                          <div className="psi-slot-meta">
                            <span><FaCalendarAlt size={12}/> {formatDate(ag.data)}</span>
                            <span><FaClock size={12}/> {ag.hora}</span>
                            <span style={{color:'var(--primary)', fontWeight:'bold', display:'flex', alignItems:'center', gap:'0.3rem'}}>
                              <FaHourglassHalf size={10} /> {ag.duracao || 50} min
                            </span>
                          </div>
                        </div>
                      </div>
                      <div style={{display:'flex', gap:'0.5rem'}}>
                        <button className="psi-btn-primary" style={{background:'white', color:'var(--primary)', border:'1px solid var(--primary)', padding:'0.5rem'}} onClick={() => abrirModalRemarcar(ag.id)}>
                          <FaExchangeAlt /> Remarcar
                        </button>
                        <button className="psi-btn-danger" onClick={() => handleAcao(ag.id, 'cancelar')}><FaTimes /></button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: HORARIOS LIVRES */}
        {activeTab === 'schedules' && (
          <div className="psi-grid-3">
            {meusHorarios.map(h => (
              <div key={h.id} className="psi-time-card">
                <div>
                  <div style={{fontSize:'0.85rem', color:'var(--muted-fg)', marginBottom:'0.2rem'}}>{formatDate(h.data)}</div>
                  <div className="psi-time-display">{h.hora}</div>
                  <div style={{fontSize:'0.8rem', color:'var(--muted-fg)'}}>{h.duracao || 50} min</div>
                </div>
                <button className="psi-btn-danger" onClick={() => handleDeleteSlot(h.id)}><FaTrash /></button>
              </div>
            ))}
          </div>
        )}

        {/* TAB 3: CONCLUIDAS */}
        {activeTab === 'completed' && (
          <div className="psi-card">
            <div className="psi-card-body">
              {concluidas.map(c => (
                <div key={c.id} className="psi-slot-item" style={{opacity:0.7}}>
                  <div className="psi-slot-info"><h4>{c.nomeAluno}</h4><span>{formatDate(c.data)} - {c.hora}</span></div>
                  <span>Concluída</span>
                </div>
              ))}
            </div>
          </div>
        )}
      </main>

      {/* MODAL 1: ADD FREE SLOT */}
      {showModalFree && (
        <div className="psi-modal-overlay" onClick={() => setShowModalFree(false)}>
          <div className="psi-modal-content" onClick={e => e.stopPropagation()}>
            <h3>Disponibilizar Horário</h3>
            <form onSubmit={handleAddFreeSlot} style={{marginTop:'1rem'}}>
              <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'1rem'}}>
                <input type="date" className="psi-input" required value={newSchedule.date} onChange={e=>setNewSchedule({...newSchedule, date:e.target.value})} />
                <input type="time" className="psi-input" required value={newSchedule.time} onChange={e=>setNewSchedule({...newSchedule, time:e.target.value})} />
                <input type="number" className="psi-input" required value={newSchedule.duration} onChange={e=>setNewSchedule({...newSchedule, duration:e.target.value})} placeholder="Min" />
              </div>
              <div className="psi-modal-actions">
                <button type="button" className="psi-btn-cancel" onClick={() => setShowModalFree(false)}>Cancelar</button>
                {/* AQUI ESTÁ O USO DO LOADING */}
                <button type="submit" className="psi-btn-confirm" disabled={loading}>
                  {loading ? 'Salvando...' : 'Salvar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 2: MANUAL BOOKING */}
      {showModalManual && (
        <div className="psi-modal-overlay" onClick={() => setShowModalManual(false)}>
          <div className="psi-modal-content" onClick={e => e.stopPropagation()}>
            <h3>Nova Consulta Manual</h3>
            <form onSubmit={handleManualBooking} style={{marginTop:'1rem'}}>
              <input type="text" className="psi-input" placeholder="Nome Paciente" required value={manualForm.patientName} onChange={e=>setManualForm({...manualForm, patientName:e.target.value})} style={{marginBottom:'1rem'}} />
              <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'1rem'}}>
                <input type="date" className="psi-input" required value={manualForm.date} onChange={e=>setManualForm({...manualForm, date:e.target.value})} />
                <input type="time" className="psi-input" required value={manualForm.time} onChange={e=>setManualForm({...manualForm, time:e.target.value})} />
                <input type="number" className="psi-input" required value={manualForm.duration} onChange={e=>setManualForm({...manualForm, duration:e.target.value})} placeholder="Min" />
              </div>
              <div className="psi-modal-actions">
                <button type="button" className="psi-btn-cancel" onClick={() => setShowModalManual(false)}>Cancelar</button>
                {/* AQUI ESTÁ O USO DO LOADING */}
                <button type="submit" className="psi-btn-confirm" disabled={loading}>
                  {loading ? 'Agendando...' : 'Agendar'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL 3: REMARCAR */}
      {showModalRemarcar && (
        <div className="psi-modal-overlay" onClick={() => setShowModalRemarcar(false)}>
          <div className="psi-modal-content" onClick={e => e.stopPropagation()} style={{maxWidth:'600px'}}>
            <h3>Remarcar Consulta</h3>
            <p style={{marginBottom:'1rem', color:'gray'}}>Selecione um novo horário livre para mover este paciente:</p>
            {meusHorarios.length === 0 ? <p>Não há horários livres. Crie um novo horário primeiro.</p> : (
              <div className="psi-grid-3">
                {meusHorarios.map(h => (
                  <button key={h.id} className="psi-time-card" style={{cursor:'pointer', width:'100%', alignItems:'center', background:'#F0FDFA', border:'1px solid var(--primary)'}} onClick={() => confirmarRemarcacaoPsi(h.id)}>
                    <div style={{textAlign:'left'}}>
                      <div style={{fontWeight:'bold', color:'var(--primary)'}}>{h.hora}</div>
                      <div style={{fontSize:'0.8rem'}}>{formatDate(h.data)}</div>
                    </div>
                    <FaExchangeAlt color="var(--primary)" />
                  </button>
                ))}
              </div>
            )}
            <div className="psi-modal-actions"><button className="psi-btn-cancel" onClick={() => setShowModalRemarcar(false)}>Cancelar</button></div>
          </div>
        </div>
      )}

    </div>
  );
}