import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom'; 
import { FaBrain, FaSignOutAlt, FaPlus, FaRegUser, FaRegCalendarAlt, FaRegClock, FaTrashAlt, FaCalendarAlt, FaClock, FaBell, FaPhone } from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';

function formatarDataParaAPI(dataString) {
  if (!dataString) return '';
  try { const [ano, mes, dia] = dataString.split('-'); return `${dia}/${mes}/${ano}`; } catch { return ''; }
}

function PortalAgenda() {
  const [activeTab, setActiveTab] = useState('minhaAgenda');
  const [mostrarFormConsulta, setMostrarFormConsulta] = useState(false);
  const [mostrarFormHorario, setMostrarFormHorario] = useState(false);
  const [mostrarNotificacoes, setMostrarNotificacoes] = useState(false);
  const [consultasReservadas, setConsultasReservadas] = useState([]);
  const [horariosLivres, setHorariosLivres] = useState([]);
  const [solicitacoesPendentes, setSolicitacoesPendentes] = useState([]);
  const [error, setError] = useState(null);
  
  const [nomePaciente, setNomePaciente] = useState('');
  const [telPaciente, setTelPaciente] = useState('');
  const [dataConsulta, setDataConsulta] = useState('');
  const [horarioConsulta, setHorarioConsulta] = useState('');
  const [duracaoMarcarConsulta, setDuracaoMarcarConsulta] = useState('50');
  const [dataNovoHorario, setDataNovoHorario] = useState('');
  const [horaNovoHorario, setHoraNovoHorario] = useState('');
  const [duracaoNovoHorario, setDuracaoNovoHorario] = useState('50');

  const navigate = useNavigate();
  const getIdPsicologo = () => localStorage.getItem("idPsicologo");

  const handleLogout = (msg) => { localStorage.clear(); sessionStorage.clear(); if(msg) alert(msg); navigate('/login'); };

  const fetchDados = async (rota, setter) => {
    const id = getIdPsicologo();
    if (!id) return;
    try {
      const response = await fetch(`${API_URL}/${rota}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idPsicologo: id })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.mensagem || 'Erro');
      setter(data);
    } catch (err) { setError(err.message); }
  };

  useEffect(() => {
    setError(null);
    const id = getIdPsicologo();
    if (!id) { navigate('/login'); return; }
    
    // Sempre carrega notificações
    fetchDados('listar_solicitacoes_atendimento', setSolicitacoesPendentes);

    if (activeTab === 'minhaAgenda') {
      fetchDados('listar_consultas', setConsultasReservadas);
    } else if (activeTab === 'meusHorarios') {
      fetchDados('listar_horarios_livres_psi', setHorariosLivres);
    }
    setMostrarFormConsulta(false);
    setMostrarFormHorario(false);
  }, [activeTab]);

  const handleAtualizarStatus = async (consulta, acao) => {
      try {
          if (acao === 'rejeitada') {
              // Rejeitar: Libera horário
              await fetch(`${API_URL}/cancelar_reserva`, {
                  method: 'POST', headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ nome: consulta.nomePsi || 'Self', idPsicologo: getIdPsicologo(), data: consulta.data, horario: consulta.horario })
              });
              alert("Solicitação recusada.");
          } else {
              // Aceitar: Confirma
              const response = await fetch(`${API_URL}/confirmar_agendamento`, {
                  method: 'POST', headers: { 'Content-Type': 'application/json' },
                  body: JSON.stringify({ idPsicologo: getIdPsicologo(), data: consulta.data, horario: consulta.horario })
              });
              if(!response.ok) throw new Error("Erro");
              alert("Confirmada com sucesso!");
          }
          fetchDados('listar_solicitacoes_atendimento', setSolicitacoesPendentes);
          if (activeTab === 'minhaAgenda') fetchDados('listar_consultas', setConsultasReservadas);
      } catch (err) { alert(err.message); }
  };

  const handleAddConsulta = async (e) => {
    e.preventDefault(); setError(null);
    const id = getIdPsicologo();
    const dataFormatada = formatarDataParaAPI(dataConsulta);
    try {
      await fetch(`${API_URL}/adicionar_horario`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ data: dataFormatada, horario: horarioConsulta, idPsicologo: id, duracao: duracaoMarcarConsulta }) });
      await fetch(`${API_URL}/marcar_consulta`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ idPsicologo: id, data: dataFormatada, horario: horarioConsulta, nomePaciente, telPaciente }) });
      fetchDados('listar_consultas', setConsultasReservadas);
      setMostrarFormConsulta(false);
    } catch (err) { setError(err.message); }
  };
  
  const handleDeletarConsulta = async (c) => {
    if(!window.confirm("Excluir?")) return;
    try {
      await fetch(`${API_URL}/remover_consulta`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ id: getIdPsicologo(), data: c.data, horario: c.horario }) });
      setConsultasReservadas(prev => prev.filter(item => item.id !== c.id));
      setHorariosLivres(prev => prev.filter(item => item.id !== c.id));
    } catch (err) { console.error(err); }
  };

  const handleAddNovoHorario = async (e) => {
      e.preventDefault();
      const dataFormatada = formatarDataParaAPI(dataNovoHorario);
      try {
          const response = await fetch(`${API_URL}/adicionar_horario`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ data: dataFormatada, horario: horaNovoHorario, idPsicologo: getIdPsicologo(), duracao: duracaoNovoHorario }) });
          if (response.ok) { fetchDados('listar_horarios_livres_psi', setHorariosLivres); setMostrarFormHorario(false); }
      } catch (err) { setError(err.message); }
  };

  const handleCancelarNovoHorario = () => { setDataNovoHorario(''); setHoraNovoHorario(''); setMostrarFormHorario(false); };

  const handleCancelarConsulta = () => { setNomePaciente(''); setTelPaciente(''); setMostrarFormConsulta(false); };

  const horariosAgrupados = horariosLivres.reduce((acc, curr) => {
      const d = curr.data; if(!acc[d]) acc[d]=[]; acc[d].push(curr); return acc;
  }, {});

  return (
    <div className="agenda-container">
      <header className="agenda-header">
        <div className="logo-section"><FaBrain className="logo-icon-agenda" /><h1>Portal Psicólogo</h1></div>
        <button onClick={() => handleLogout()} className="sair-link"><FaSignOutAlt /> Sair</button>
      </header>
      <main className="agenda-main">
        <div className="tab-navigation">
            <button className={activeTab === 'minhaAgenda' ? 'active' : ''} onClick={() => setActiveTab('minhaAgenda')}><FaCalendarAlt /> Agenda</button>
            <button className={activeTab === 'meusHorarios' ? 'active' : ''} onClick={() => setActiveTab('meusHorarios')}><FaClock /> Horários</button>
            <div className="notification-icon-container" onClick={() => { setActiveTab('minhaAgenda'); setMostrarNotificacoes(!mostrarNotificacoes); }}>
                <FaBell className="notification-icon" />
                {solicitacoesPendentes.length > 0 && <span className="notification-badge">{solicitacoesPendentes.length}</span>}
            </div>
            <div className="action-buttons-group">
              {activeTab === 'minhaAgenda' ? <button className="btn-nova-consulta" onClick={() => setMostrarFormConsulta(!mostrarFormConsulta)}><FaPlus /> Nova</button> : <button className="btn-adicionar-horario" onClick={() => setMostrarFormHorario(!mostrarFormHorario)}><FaPlus /> Horário</button>}
            </div>
        </div>
        {error && <div className="message-container error-message"><p>{error}</p></div>}
        
        {activeTab === 'minhaAgenda' && (
            <>
                {mostrarNotificacoes && (
                    <div className="solicitacoes-container">
                        <h3>Solicitações</h3>
                        {solicitacoesPendentes.map(s => (
                            <div key={s.id || Math.random()} className="solicitacao-item">
                                <strong>{s.nomePaciente}</strong> - {s.data} {s.horario}
                                <div>
                                    <button className="btn-aceitar" onClick={() => handleAtualizarStatus(s, 'confirmada')}>Aceitar</button>
                                    <button className="btn-recusar" onClick={() => handleAtualizarStatus(s, 'rejeitada')}>Recusar</button>
                                </div>
                            </div>
                        ))}
                    </div>
                )}
                
                {mostrarFormConsulta && (
                  <div className="form-nova-consulta">
                    <form onSubmit={handleAddConsulta}>
                      <input value={nomePaciente} onChange={e => setNomePaciente(e.target.value)} placeholder="Nome" required />
                      <input value={telPaciente} onChange={e => setTelPaciente(e.target.value)} placeholder="Tel" required />
                      <input type="date" value={dataConsulta} onChange={e => setDataConsulta(e.target.value)} required />
                      <input type="time" value={horarioConsulta} onChange={e => setHorarioConsulta(e.target.value)} required />
                      <input type="number" value={duracaoMarcarConsulta} onChange={e => setDuracaoMarcarConsulta(e.target.value)} placeholder="Duração" required />
                      <button type="submit">Salvar</button>
                      <button type="button" onClick={handleCancelarConsulta}>Cancelar</button>
                    </form>
                  </div>
                )}
                
                <div className="lista-consultas">
                  {consultasReservadas.length === 0 && !mostrarFormConsulta && <p>Nenhuma consulta confirmada.</p>}
                  {consultasReservadas.map(c => (
                    <div key={c.id || Math.random()} className="item-consulta">
                      <div className="info-paciente">
                        <FaRegUser className="paciente-icon" />
                        <div><h3>{c.nomePaciente}</h3><span style={{color:'green', fontSize:'0.8rem'}}>Confirmada</span></div>
                      </div>
                      <div className="info-data-hora"><span>{c.data}</span><span>{c.horario}</span></div>
                      <button className="btn-deletar" onClick={() => handleDeletarConsulta(c)}><FaTrashAlt /></button>
                    </div>
                  ))}
                </div>
            </>
        )}

        {activeTab === 'meusHorarios' && (
            <>
                {mostrarFormHorario && (
                    <div className="form-novo-horario">
                        <form onSubmit={handleAddNovoHorario}>
                            <input type="date" value={dataNovoHorario} onChange={e => setDataNovoHorario(e.target.value)} required />
                            <input type="time" value={horaNovoHorario} onChange={e => setHoraNovoHorario(e.target.value)} required />
                            <input type="number" value={duracaoNovoHorario} onChange={e => setDuracaoNovoHorario(e.target.value)} placeholder="Duração" required />
                            <button type="submit">Salvar</button>
                            <button type="button" onClick={handleCancelarNovoHorario}>Cancelar</button>
                        </form>
                    </div>
                )}
                <div className="lista-horarios">
                    {Object.keys(horariosAgrupados).map(d => (
                        <div key={d} className="horario-group-item">
                            <div className="horario-group-date"><FaRegCalendarAlt /> {d}</div>
                            <div className="horario-time-chip-container">{horariosAgrupados[d].map(h => (<div key={h.id} className="horario-time-chip"><FaRegClock /> {h.horario}<button className="btn-deletar-horario" onClick={() => handleDeletarConsulta(h)}><FaTrashAlt /></button></div>))}</div>
                        </div>
                    ))}
                </div>
            </>
        )}
      </main>
    </div>
  );
}
export default PortalAgenda;