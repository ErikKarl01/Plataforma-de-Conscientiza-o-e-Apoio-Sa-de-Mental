import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FaBrain, 
  FaSignOutAlt, 
  FaPlus, 
  FaRegUser,
  FaRegCalendarAlt,
  FaRegClock, 
  FaTrashAlt,
  FaCalendarAlt, 
  FaClock, 
  FaBell,
  FaPhone // <--- ADICIONADO QUE FALTAVA
} from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';

// Função auxiliar simples
function formatarDataParaAPI(dataString) {
  if (!dataString) return '';
  try {
    const [ano, mes, dia] = dataString.split('-');
    return `${dia}/${mes}/${ano}`;
  } catch {
    return '';
  }
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
  
  // FORMULÁRIO MANUAL
  const [nomePaciente, setNomePaciente] = useState('');
  const [telPaciente, setTelPaciente] = useState('');
  const [dataConsulta, setDataConsulta] = useState('');
  const [horarioConsulta, setHorarioConsulta] = useState('');
  const [duracaoMarcarConsulta, setDuracaoMarcarConsulta] = useState('50');

  // FORMULÁRIO HORÁRIO LIVRE
  const [dataNovoHorario, setDataNovoHorario] = useState('');
  const [horaNovoHorario, setHoraNovoHorario] = useState('');
  const [duracaoNovoHorario, setDuracaoNovoHorario] = useState('50');

  // --- Recuperar ID dentro do componente para garantir atualização ---
  const getIdPsicologo = () => localStorage.getItem("idPsicologo");

  // --- BUSCAS ---
  const fetchConsultas = async (rota, setter) => {
    const id = getIdPsicologo();
    if (!id) return;

    try {
      const response = await fetch(`${API_URL}/${rota}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idPsicologo: id })
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.mensagem || 'Erro ao carregar dados.');
      setter(data);
    } catch (err) {
      setError(err.message);
    }
  };

  const fetchSolicitacoes = async () => {
      const id = getIdPsicologo();
      if (!id) return;

      try {
          const response = await fetch(`${API_URL}/listar_solicitacoes_atendimento`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ idPsicologo: id })
          });
          if (response.ok) {
              const data = await response.json();
              setSolicitacoesPendentes(data);
          } else {
              setSolicitacoesPendentes([]);
          }
      } catch (err) {
          console.error(err);
      }
  };
  
  const agruparHorariosPorData = (horarios) => {
    return horarios.reduce((acc, current) => {
        const data = current.data;
        if (!acc[data]) acc[data] = [];
        acc[data].push(current);
        return acc;
    }, {});
  };

  useEffect(() => {
    setError(null);
    const id = getIdPsicologo();
    if (!id) {
        setError("Sessão expirada. Faça login novamente.");
        return;
    }
    
    fetchSolicitacoes(); 

    if (activeTab === 'minhaAgenda') {
      fetchConsultas('listarConsultas', setConsultasReservadas);
    } else if (activeTab === 'meusHorarios') {
      fetchConsultas('listarHorariosLivresPsi', setHorariosLivres);
    }
    
    setMostrarFormConsulta(false);
    setMostrarFormHorario(false);
  }, [activeTab]);

  // --- AÇÕES ---
  const handleAtualizarStatus = async (idConsulta, novoStatus) => {
      try {
          const response = await fetch(`${API_URL}/atualizar_status_consulta`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ 
                  idConsulta: idConsulta, 
                  status: novoStatus 
              })
          });

          if (!response.ok) {
              const errData = await response.json();
              throw new Error(errData.mensagem || "Erro ao atualizar status.");
          }

          alert(`Sucesso! Consulta ${novoStatus}.`);
          fetchSolicitacoes();
          if (activeTab === 'minhaAgenda') fetchConsultas('listarConsultas', setConsultasReservadas);

      } catch (err) {
          alert(err.message);
      }
  };

  const handleAddConsulta = async (e) => {
    e.preventDefault();
    setError(null);
    const id = getIdPsicologo();
    
    if (!nomePaciente || !telPaciente || !dataConsulta || !horarioConsulta) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    const dataFormatada = formatarDataParaAPI(dataConsulta);

    try {
      // 1. Criar Horário
      const resEtapa1 = await fetch(`${API_URL}/adicionarHorario`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: dataFormatada,
          horario: horarioConsulta,
          idPsicologo: id,
          duracao: duracaoMarcarConsulta 
        })
      });
      if (!resEtapa1.ok) {
          const err1 = await resEtapa1.json();
          throw new Error(err1.mensagem || 'Erro ao criar horário base.');
      }

      // 2. Marcar Paciente
      const resEtapa2 = await fetch(`${API_URL}/marcarConsulta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idPsicologo: id,
          data: dataFormatada,
          horario: horarioConsulta,
          nomePaciente: nomePaciente,
          telPaciente: telPaciente
        })
      });
      
      if (!resEtapa2.ok) {
          const errData = await resEtapa2.json();
          throw new Error(errData.mensagem || 'Erro ao marcar o paciente.');
      }

      const { consulta: consultaSalva } = await resEtapa2.json();
      setConsultasReservadas(prev => [...prev, consultaSalva]);
      handleCancelarConsulta();

    } catch (err) {
      setError(err.message);
    }
  };

  const handleCancelarConsulta = () => {
    setNomePaciente('');
    setTelPaciente('');
    setDataConsulta('');
    setHorarioConsulta('');
    setDuracaoMarcarConsulta('50'); 
    setMostrarFormConsulta(false);
    setError(null);
  };
  
  const handleDeletarConsulta = async (consultaParaExcluir) => {
    if(!window.confirm("Tem certeza que deseja excluir?")) return;
    const id = getIdPsicologo();
    
    setError(null);
    try {
      await fetch(`${API_URL}/removerConsulta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idPsicologo: id,
          data: consultaParaExcluir.data,
          horario: consultaParaExcluir.horario,
          id: consultaParaExcluir.id 
        })
      });
      setConsultasReservadas(prev => prev.filter(c => c.id !== consultaParaExcluir.id));
      setHorariosLivres(prev => prev.filter(c => c.id !== consultaParaExcluir.id));
    } catch (err) {
      console.error(err);
    }
  };

  const handleAddNovoHorario = async (e) => {
      e.preventDefault();
      const id = getIdPsicologo();
      const dataFormatada = formatarDataParaAPI(dataNovoHorario);
      
      try {
          const response = await fetch(`${API_URL}/adicionarHorario`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  data: dataFormatada,
                  horario: horaNovoHorario,
                  idPsicologo: id,
                  duracao: duracaoNovoHorario
              })
          });
          if (response.ok) {
              const { consulta } = await response.json();
              setHorariosLivres(prev => [...prev, consulta]);
              handleCancelarNovoHorario();
          } else {
              const errData = await response.json();
              setError(errData.mensagem || "Erro ao adicionar horário.");
          }
      } catch (err) { setError(err.message); }
  };

  const handleCancelarNovoHorario = () => {
      setDataNovoHorario('');
      setHoraNovoHorario('');
      setDuracaoNovoHorario('50');
      setMostrarFormHorario(false);
      setError(null);
  };

  const horariosAgrupados = agruparHorariosPorData(horariosLivres);

  // Renderização principal sem componente aninhado para evitar perda de foco
  return (
    <div className="agenda-container">
      <header className="agenda-header">
        <div className="logo-section">
          <FaBrain className="logo-icon-agenda" />
          <div className="portal-info"><h1>Portal do Psicólogo</h1><p>Gerenciamento de agenda</p></div>
        </div>
        <Link to="/login" className="sair-link"><FaSignOutAlt /> Sair</Link>
      </header>
      
      <main className="agenda-main">
        <div className="tab-navigation">
            <button className={`tab-button ${activeTab === 'minhaAgenda' ? 'active' : ''}`} onClick={() => setActiveTab('minhaAgenda')}><FaCalendarAlt /> Minha Agenda</button>
            <button className={`tab-button ${activeTab === 'meusHorarios' ? 'active' : ''}`} onClick={() => setActiveTab('meusHorarios')}><FaClock /> Meus Horários</button>
            
            <div className="notification-icon-container" onClick={() => { setActiveTab('minhaAgenda'); setMostrarNotificacoes(!mostrarNotificacoes); }}>
                <FaBell className="notification-icon" />
                {solicitacoesPendentes.length > 0 && <span className="notification-badge">{solicitacoesPendentes.length}</span>}
            </div>

            <div className="action-buttons-group">
              {activeTab === 'minhaAgenda' ? 
                  <button className="btn-nova-consulta" onClick={() => setMostrarFormConsulta(!mostrarFormConsulta)}><FaPlus /> Nova consulta</button> : 
                  <button className="btn-adicionar-horario" onClick={() => setMostrarFormHorario(!mostrarFormHorario)}><FaPlus /> Adicionar horário</button>
              }
            </div>
        </div>

        {error && <div className="message-container error-message"><p>{error}</p></div>}

        {/* --- CONTEÚDO MINHA AGENDA --- */}
        {activeTab === 'minhaAgenda' && (
            <>
                <h2>Minha Agenda</h2>
                
                {mostrarNotificacoes && (
                    <div className="solicitacoes-container">
                        <h3>Solicitações Pendentes</h3>
                        {solicitacoesPendentes.length === 0 ? <p>Nenhuma solicitação nova.</p> : 
                            solicitacoesPendentes.map(s => (
                                <div key={s.id} className="solicitacao-item">
                                    <div className="solicitacao-info">
                                        <strong>{s.nomePaciente}</strong>
                                        <span>{s.emailPaciente}</span>
                                        <p>{s.data} às {s.horario}</p>
                                        {s.causa && <p className="causa-tag">Motivo: {s.causa}</p>}
                                    </div>
                                    <div className="solicitacao-actions">
                                        <button className="btn-aceitar" onClick={() => handleAtualizarStatus(s.id, 'confirmada')}>Aceitar</button>
                                        <button className="btn-recusar" onClick={() => handleAtualizarStatus(s.id, 'rejeitada')}>Recusar</button>
                                    </div>
                                </div>
                            ))
                        }
                    </div>
                )}
                
                {mostrarFormConsulta && (
                  <div className="form-nova-consulta">
                    <h3>Agendar Manualmente</h3>
                    <form onSubmit={handleAddConsulta}>
                      <div className="form-grid-horario"> 
                        <div className="form-group">
                            <label>Nome do paciente</label>
                            <input type="text" value={nomePaciente} onChange={(e) => setNomePaciente(e.target.value)} required />
                        </div>
                        <div className="form-group">
                            <label>Telefone</label>
                            <input type="tel" placeholder="(00) 00000-0000" value={telPaciente} onChange={(e) => setTelPaciente(e.target.value)} required />
                        </div>
                        <div className="form-group">
                          <label>Data</label>
                          <input type="date" value={dataConsulta} onChange={(e) => setDataConsulta(e.target.value)} required />
                        </div>
                        <div className="form-group">
                          <label>Horário</label>
                          <input type="time" value={horarioConsulta} onChange={(e) => setHorarioConsulta(e.target.value)} required />
                        </div>
                        <div className="form-group">
                          <label>Duração (min)</label>
                          <input type="number" value={duracaoMarcarConsulta} onChange={(e) => setDuracaoMarcarConsulta(e.target.value)} required />
                        </div>
                      </div>
                      <div className="form-actions">
                        <button type="submit" className="btn-adicionar">Salvar Agenda</button>
                        <button type="button" className="btn-cancelar" onClick={handleCancelarConsulta}>Cancelar</button>
                      </div>
                    </form>
                  </div>
                )}
                
                <div className="lista-consultas">
                  {consultasReservadas.length === 0 && !mostrarFormConsulta && <p>Nenhuma consulta na agenda.</p>}
                  {consultasReservadas.map(c => (
                    <div key={c.id} className="item-consulta">
                      <div className="info-paciente">
                        <FaRegUser className="paciente-icon" />
                        <div>
                            <h3>{c.nomePaciente}</h3>
                            <span style={{
                                fontSize:'0.8rem', 
                                color: c.status === 'confirmada' ? 'green' : 'orange',
                                fontWeight: 'bold'
                            }}>
                                {c.status === 'confirmada' ? 'Confirmada' : 'Aguardando Aprovação'}
                            </span>
                        </div>
                      </div>
                      <div className="info-data-hora">
                        <span><FaRegCalendarAlt /> {c.data}</span>
                        <span><FaRegClock /> {c.horario}</span>
                        <span><FaPhone /> {c.telPaciente}</span>
                      </div>
                      <button className="btn-deletar" onClick={() => handleDeletarConsulta(c)}><FaTrashAlt /></button>
                    </div>
                  ))}
                </div>
            </>
        )}

        {/* --- CONTEÚDO MEUS HORÁRIOS --- */}
        {activeTab === 'meusHorarios' && (
            <>
                <h2>Meus Horários Livres</h2>
                {mostrarFormHorario && (
                    <div className="form-novo-horario">
                        <h3>Adicionar horário</h3>
                        <form onSubmit={handleAddNovoHorario}>
                            <div className="form-grid-horario">
                                <div className="form-group"><label>Data</label><input type="date" value={dataNovoHorario} onChange={(e) => setDataNovoHorario(e.target.value)} required /></div>
                                <div className="form-group"><label>Hora</label><input type="time" value={horaNovoHorario} onChange={(e) => setHoraNovoHorario(e.target.value)} required /></div>
                                <div className="form-group"><label>Duração</label><input type="number" value={duracaoNovoHorario} onChange={(e) => setDuracaoNovoHorario(e.target.value)} required /></div>
                            </div>
                            <div className="form-actions">
                                <button type="submit" className="btn-salvar">Salvar</button>
                                <button type="button" className="btn-cancelar" onClick={handleCancelarNovoHorario}>Cancelar</button>
                            </div>
                        </form>
                    </div>
                )}
                <div className="lista-horarios">
                    {Object.keys(horariosAgrupados).length === 0 && <p>Nenhum horário livre cadastrado.</p>}
                    {Object.keys(horariosAgrupados).map(data => (
                        <div key={data} className="horario-group-item">
                            <div className="horario-group-date"><FaRegCalendarAlt /> {data}</div>
                            <div className="horario-time-chip-container">
                                {horariosAgrupados[data].map(h => (
                                    <div key={h.id} className="horario-time-chip">
                                        <FaRegClock /> {h.horario}
                                        <span className="duracao-min">{h.duracao || '50'}min</span> 
                                        <button className="btn-deletar-horario" onClick={() => handleDeletarConsulta(h)}><FaTrashAlt /></button>
                                    </div>
                                ))}
                            </div>
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