import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaBrain, FaSignOutAlt, FaCalendarAlt, FaClock, FaCheckCircle, 
  FaBell, FaPlus, FaTrash, FaUser, FaCalendarCheck, FaTimes, FaCheck, FaUserEdit, FaHourglassHalf 
} from 'react-icons/fa';

import '../portal-psicologo.css';

const API_URL = 'http://127.0.0.1:5000';

export default function PortalAgenda() {
  const navigate = useNavigate();
  
  // -- DADOS --
  const [idPsi, setIdPsi] = useState(null);
  const [agendamentos, setAgendamentos] = useState([]); 
  const [meusHorarios, setMeusHorarios] = useState([]); 
  const [solicitacoes, setSolicitacoes] = useState([]); 
  const [concluidas, setConcluidas] = useState([]); 

  // -- UI --
  const [activeTab, setActiveTab] = useState('agenda');
  const [showNotifications, setShowNotifications] = useState(false);
  const [loading, setLoading] = useState(false);

  // -- MODAIS --
  const [showModalFree, setShowModalFree] = useState(false);   // Horário Livre
  const [showModalManual, setShowModalManual] = useState(false); // Consulta Manual

  // -- FORMULÁRIOS --
  const [newSchedule, setNewSchedule] = useState({ date: '', time: '', duration: 50 });
  // Atualizado: Adicionado duration no form manual
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

    } catch (error) { console.error("Erro dados:", error); }
  }, []);

  // --- 1. ADICIONAR HORÁRIO LIVRE ---
  const handleAddFreeSlot = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/adicionar_horario`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
          idPsicologo: idPsi, 
          data: newSchedule.date, 
          hora: newSchedule.time, 
          duracao: newSchedule.duration 
        })
      });
      if(res.ok) {
        setShowModalFree(false);
        setNewSchedule({ date: '', time: '', duration: 50 });
        carregarDados(idPsi);
      }
    } catch (err) { alert("Erro conexão", err); } 
    finally { setLoading(false); }
  };

  // --- 2. MARCAR CONSULTA MANUALMENTE (ATUALIZADO COM DURAÇÃO) ---
  const handleManualBooking = async (e) => {
    e.preventDefault();
    if(!manualForm.patientName || !manualForm.date || !manualForm.time) return;
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/marcar_consulta`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ 
          idPsicologo: idPsi, 
          nomePaciente: manualForm.patientName,
          data: manualForm.date, 
          hora: manualForm.time,
          duracao: manualForm.duration // Envia a duração
        })
      });
      
      if(res.ok) {
        setShowModalManual(false);
        setManualForm({ patientName: '', date: '', time: '', duration: 50 });
        carregarDados(idPsi);
        alert("Consulta agendada com sucesso!");
      } else {
        alert("Erro ao marcar consulta.");
      }
    } catch (err) { alert("Erro conexão", err); } 
    finally { setLoading(false); }
  };

  // --- AÇÕES GERAIS ---
  const handleAcao = async (idConsulta, acao) => {
    const endpoint = acao === 'confirmar' ? '/confirmar_agendamento' : '/cancelar_reserva';
    try {
      const res = await fetch(`${API_URL}${endpoint}`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id: idConsulta })
      });
      if (res.ok) carregarDados(idPsi);
    } catch (err) { console.error(err); }
  };

  const handleDeleteSlot = async (id) => {
    if(!window.confirm("Remover horário?")) return;
    try {
      await fetch(`${API_URL}/remover_consulta`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ id: id, acao: 'remover_fisicamente' })
      });
      carregarDados(idPsi);
    } catch (err) { console.error(err); }
  };

  const formatDate = (dateString) => {
    if(!dateString) return '';
    const [ano, mes, dia] = dateString.split('-');
    return `${dia}/${mes}/${ano}`;
  };

  return (
    <div className="portal-psi-wrapper">
      <header className="psi-header">
        <div className="psi-header-content">
          <div className="psi-brand">
            <div className="psi-logo-box"><FaBrain size={24} /></div>
            <div className="psi-title"><h1>Portal do Psicólogo</h1><p>Gerenciamento de Agenda</p></div>
          </div>
          <button className="psi-btn-logout" onClick={() => { localStorage.removeItem('idPsicologo'); navigate('/'); }}>
            <FaSignOutAlt /> Sair
          </button>
        </div>
      </header>

      <main className="psi-container">
        <div className="psi-actions-bar">
          <div className="psi-tabs-list">
            <button className={`psi-tab-trigger ${activeTab === 'agenda' ? 'active' : ''}`} onClick={() => setActiveTab('agenda')}>
              <FaCalendarAlt /> Minha Agenda
            </button>
            <button className={`psi-tab-trigger ${activeTab === 'schedules' ? 'active' : ''}`} onClick={() => setActiveTab('schedules')}>
              <FaClock /> Meus Horários
            </button>
            <button className={`psi-tab-trigger ${activeTab === 'completed' ? 'active' : ''}`} onClick={() => setActiveTab('completed')}>
              <FaCalendarCheck /> Concluídas
            </button>
          </div>

          <div style={{display:'flex', gap:'1rem'}}>
            <button className="psi-icon-btn" onClick={() => setShowNotifications(!showNotifications)}>
              <FaBell />
              {solicitacoes.length > 0 && <span className="psi-badge-dot">{solicitacoes.length}</span>}
            </button>
            
            {/* BOTÕES DIFERENTES POR ABA */}
            {activeTab === 'agenda' && (
              <button className="psi-btn-primary" onClick={() => setShowModalManual(true)}>
                <FaPlus /> Nova Consulta
              </button>
            )}
            {activeTab === 'schedules' && (
              <button className="psi-btn-primary" onClick={() => setShowModalFree(true)}>
                <FaPlus /> Novo Horário
              </button>
            )}
          </div>
        </div>

        {/* NOTIFICAÇÕES */}
        {showNotifications && (
          <div className="psi-card" style={{borderLeft:'4px solid #F59E0B', marginBottom:'2rem'}}>
            <div className="psi-card-header">
              <h3 className="psi-card-title" style={{color:'#D97706'}}><FaBell /> Solicitações Pendentes</h3>
            </div>
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

        {/* TAB 1: MINHA AGENDA (CONFIRMADOS) */}
        {activeTab === 'agenda' && (
          <div className="psi-card">
            <div className="psi-card-header"><h3 className="psi-card-title">Consultas Agendadas</h3></div>
            <div className="psi-card-body">
              {agendamentos.length === 0 ? (
                <div className="psi-empty-state">
                  <FaCalendarAlt size={40} style={{marginBottom:'1rem', opacity:0.3}} />
                  <p>Nenhuma consulta futura.</p>
                </div>
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
                            {/* AQUI ESTÁ A EXIBIÇÃO DA DURAÇÃO NA AGENDA */}
                            <span style={{display:'flex', alignItems:'center', gap:'0.3rem', color:'var(--primary)'}}>
                              <FaHourglassHalf size={10}/> {ag.duracao || 50} min
                            </span>
                          </div>
                        </div>
                      </div>
                      <button className="psi-btn-danger" onClick={() => handleAcao(ag.id, 'cancelar')}><FaTimes /> Cancelar</button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: MEUS HORÁRIOS LIVRES */}
        {activeTab === 'schedules' && (
          <div>
            <h2 style={{fontSize:'1.2rem', fontWeight:600, marginBottom:'1rem'}}>Gerenciar Disponibilidade</h2>
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
          </div>
        )}

        {/* TAB 3: CONCLUÍDAS */}
        {activeTab === 'completed' && (
          <div className="psi-card">
            <div className="psi-card-header"><h3 className="psi-card-title">Histórico</h3></div>
            <div className="psi-card-body">
              <div className="psi-slot-list">
                {concluidas.map(c => (
                  <div key={c.id} className="psi-slot-item" style={{opacity:0.7, background:'#F3F4F6'}}>
                    <div className="psi-slot-info">
                      <div className="psi-avatar" style={{background:'#E5E7EB', color:'#6B7280'}}><FaCheckCircle /></div>
                      <div>
                        <h4>{c.nomeAluno}</h4>
                        <div className="psi-slot-meta"><span>{formatDate(c.data)} às {c.hora}</span></div>
                      </div>
                    </div>
                    <span style={{fontSize:'0.75rem', fontWeight:600, background:'#E5E7EB', padding:'0.25rem 0.5rem', borderRadius:'99px'}}>Concluída</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
      </main>

      {/* --- MODAL 1: ADICIONAR HORÁRIO LIVRE --- */}
      {showModalFree && (
        <div className="psi-modal-overlay" onClick={() => setShowModalFree(false)}>
          <div className="psi-modal-content" onClick={e => e.stopPropagation()}>
            <div className="psi-modal-header">
              <h3 style={{fontSize:'1.25rem', fontWeight:700}}>Disponibilizar Horário</h3>
              <p style={{color:'var(--muted-fg)', fontSize:'0.9rem'}}>Crie um espaço na sua agenda para alunos.</p>
            </div>
            <form onSubmit={handleAddFreeSlot}>
              <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'1rem'}}>
                <div className="psi-form-group">
                  <label className="psi-label">Data</label>
                  <input type="date" className="psi-input" required value={newSchedule.date} onChange={e => setNewSchedule({...newSchedule, date:e.target.value})} />
                </div>
                <div className="psi-form-group">
                  <label className="psi-label">Hora</label>
                  <input type="time" className="psi-input" required value={newSchedule.time} onChange={e => setNewSchedule({...newSchedule, time:e.target.value})} />
                </div>
                <div className="psi-form-group">
                  <label className="psi-label">Duração(min)</label>
                  <input type="number" className="psi-input" required value={newSchedule.duration} onChange={e => setNewSchedule({...newSchedule, duration:e.target.value})} />
                </div>
              </div>
              <div className="psi-modal-actions">
                <button type="button" className="psi-btn-cancel" onClick={() => setShowModalFree(false)}>Cancelar</button>
                <button type="submit" className="psi-btn-confirm" disabled={loading}>Salvar</button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* --- MODAL 2: MARCAR CONSULTA MANUAL (COM DURAÇÃO) --- */}
      {showModalManual && (
        <div className="psi-modal-overlay" onClick={() => setShowModalManual(false)}>
          <div className="psi-modal-content" onClick={e => e.stopPropagation()}>
            <div className="psi-modal-header">
              <h3 style={{fontSize:'1.25rem', fontWeight:700, display:'flex', alignItems:'center', gap:'0.5rem'}}>
                <FaUserEdit /> Nova Consulta Manual
              </h3>
              <p style={{color:'var(--muted-fg)', fontSize:'0.9rem'}}>Marque um atendimento direto na agenda.</p>
            </div>
            <form onSubmit={handleManualBooking}>
              <div className="psi-form-group">
                <label className="psi-label">Nome do Paciente</label>
                <input type="text" className="psi-input" placeholder="Ex: João da Silva" required 
                       value={manualForm.patientName} onChange={e => setManualForm({...manualForm, patientName:e.target.value})} />
              </div>
              <div style={{display:'grid', gridTemplateColumns:'1fr 1fr 1fr', gap:'1rem'}}>
                <div className="psi-form-group">
                  <label className="psi-label">Data</label>
                  <input type="date" className="psi-input" required value={manualForm.date} onChange={e => setManualForm({...manualForm, date:e.target.value})} />
                </div>
                <div className="psi-form-group">
                  <label className="psi-label">Hora</label>
                  <input type="time" className="psi-input" required value={manualForm.time} onChange={e => setManualForm({...manualForm, time:e.target.value})} />
                </div>
                {/* CAMPO DURAÇÃO ADICIONADO AQUI */}
                <div className="psi-form-group">
                  <label className="psi-label">Duração(min)</label>
                  <input type="number" className="psi-input" required min="15" step="5"
                         value={manualForm.duration} onChange={e => setManualForm({...manualForm, duration:e.target.value})} />
                </div>
              </div>
              <div className="psi-modal-actions">
                <button type="button" className="psi-btn-cancel" onClick={() => setShowModalManual(false)}>Cancelar</button>
                <button type="submit" className="psi-btn-confirm" disabled={loading}>Agendar Consulta</button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}