import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaBrain, 
  FaSignOutAlt, 
  FaClipboardList, 
  FaCheckCircle,
  FaRegClock,
  FaTimesCircle,
  FaUserMd
} from 'react-icons/fa';

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

  const dadosAluno = useMemo(() => {
    return JSON.parse(localStorage.getItem("dadosAluno"));
  }, []);

  const fetchHorariosLivres = useCallback(async () => {
      try {
          const response = await fetch(`${API_URL}/listar_horarios_livres`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({}) 
          });
          if (response.ok) {
              const data = await response.json();
              setHorariosLivres(data);
          } else {
              setHorariosLivres([]);
          }
      } catch {
          setError("Erro ao carregar horários. Verifique sua conexão.");
      }
  }, []);

  const fetchMinhasConsultas = useCallback(async () => {
      if (!dadosAluno) return;
      try {
          const response = await fetch(`${API_URL}/listar_minhas_solicitacoes`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({ id: dadosAluno.id })
          });
          if (response.ok) {
              const data = await response.json();
              const dataComStatus = data.map(c => ({
                  ...c,
                  status: c.status || 'pendente' 
              }));
              setMinhasConsultas(dataComStatus);
          }
      } catch (err) {
          console.error("Erro ao buscar consultas", err);
      }
  }, [dadosAluno]);

  useEffect(() => {
    if (!dadosAluno) {
        navigate('/login');
    } else {
        if (activeTab === 'horariosDisponiveis') {
            fetchHorariosLivres();
        } else if (activeTab === 'minhasConsultas') {
            fetchMinhasConsultas();
        }
    }
  }, [activeTab, dadosAluno, navigate, fetchHorariosLivres, fetchMinhasConsultas]);

  const formatarDataExtenso = (dataString, horaString) => {
      try {
          const [dia, mes, ano] = dataString.split('/');
          const dataObj = new Date(`${ano}-${mes}-${dia}T${horaString}`);
          const opcoes = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
          let dataFormatada = dataObj.toLocaleDateString('pt-BR', opcoes);
          return `${dataFormatada} às ${horaString}`;
      } catch {
          return `${dataString} às ${horaString}`;
      }
  };

  const handleSelecionarHorario = (h) => {
      setHorarioSelecionado(h);
      setSuccessMsg(null);
      setError(null);
  };

  const handleConfirmarAgendamento = async () => {
      if (!horarioSelecionado) return;
      setError(null);
      setSuccessMsg(null);

      try {
          const payload = {
              // ENVIAR ID DO ESTUDANTE PARA VINCULAR A CONSULTA
              idEstudante: dadosAluno.id, 

              nomePaci: dadosAluno.nome,
              emailPaci: dadosAluno.email,
              telefonePaci: dadosAluno.telefone,
              nome: horarioSelecionado.nomePsi, 
              email: horarioSelecionado.emailPsi,   
              data: horarioSelecionado.data,
              horario: horarioSelecionado.horario,
              causa: motivoConsulta
          };

          const response = await fetch(`${API_URL}/reservar_data_horario`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
          });

          if (!response.ok) {
              const data = await response.json();
              throw new Error(data.mensagem || 'Erro ao reservar.');
          }

          setSuccessMsg("Solicitação enviada com sucesso! Aguarde a confirmação.");
          setHorarioSelecionado(null);
          setMotivoConsulta('');
          fetchHorariosLivres();
          setTimeout(() => setActiveTab('minhasConsultas'), 2000);

      } catch (err) {
          setError(err.message);
      }
  };

  const handleCancelar = async (consulta) => {
      if(!window.confirm("Tem certeza que deseja cancelar esta solicitação?")) return;
      try {
          const response = await fetch(`${API_URL}/cancelar_reserva`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  nome: consulta.nomePsi, 
                  email: consulta.emailPsi,
                  data: consulta.data,
                  horario: consulta.horario
              })
          });
          if (response.ok) {
              alert("Solicitação cancelada.");
              fetchMinhasConsultas();
          } else {
              throw new Error("Falha ao cancelar");
          }
      } catch {
          alert("Erro ao cancelar. Tente novamente.");
      }
  };

  const agruparHorarios = (horarios) => {
      return horarios.reduce((acc, curr) => {
          const data = curr.data;
          if (!acc[data]) acc[data] = [];
          acc[data].push(curr);
          return acc;
      }, {});
  };

  const horariosAgrupados = agruparHorarios(horariosLivres);

  const renderCardConsulta = (consulta) => {
      const dataFormatada = formatarDataExtenso(consulta.data, consulta.horario);

      const renderCardBody = () => (
          <div className="status-body">
              {dataFormatada}
              <div style={{fontSize:'0.9rem', marginTop:'0.5rem', color:'#555'}}>
                 Profissional: <strong>{consulta.nomePsi}</strong>
              </div>
              {consulta.causa && (
                  <div style={{
                      marginTop: '0.8rem',
                      padding: '0.6rem',
                      backgroundColor: 'rgba(0,0,0,0.03)',
                      borderRadius: '6px',
                      fontSize: '0.85rem',
                      color: '#555',
                      borderLeft: '3px solid #ccc'
                  }}>
                      <span style={{fontWeight:'600', display:'block', marginBottom:'2px'}}>Observação:</span>
                      "{consulta.causa}"
                  </div>
              )}
          </div>
      );

      if (consulta.status === 'confirmada') {
          return (
              <div key={consulta.id} className="status-card card-confirmada">
                  <div className="status-header">
                      <FaCheckCircle className="icon-status" />
                      <span>Confirmada</span>
                  </div>
                  {renderCardBody()}
              </div>
          );
      }

      if (consulta.status === 'rejeitada') {
          return (
              <div key={consulta.id} className="status-card card-rejeitada">
                  <div className="status-header">
                      <FaTimesCircle className="icon-status" />
                      <span>Rejeitada</span>
                  </div>
                  {renderCardBody()}
                  <button className="btn-tentar-novamente" onClick={() => setActiveTab('horariosDisponiveis')}>
                      Tentar novamente
                  </button>
              </div>
          );
      }

      return (
          <div key={consulta.id} className="status-card card-aguardando">
              <div className="status-header">
                  <FaRegClock className="icon-status" />
                  <span>Aguardando confirmação</span>
              </div>
              {renderCardBody()}
              <button className="btn-cancelar-reserva" onClick={() => handleCancelar(consulta)}>
                  Cancelar
              </button>
          </div>
      );
  };

  return (
    <div className="agenda-container">
      <header className="agenda-header">
        <div className="logo-section">
          <div className="logo-icon-agenda"><FaBrain /></div>
          <div className="portal-info">
            <h1>Portal do Aluno</h1>
            <p>Gerenciamento de agenda</p>
          </div>
        </div>
        <button onClick={() => { localStorage.removeItem("dadosAluno"); navigate('/login'); }} className="sair-link" style={{background:'none', border:'none', cursor:'pointer', fontSize:'1rem'}}>
          <FaSignOutAlt /> Sair
        </button>
      </header>

      <div className="tab-navigation" style={{justifyContent: 'flex-start', marginBottom: '2rem'}}>
          <button className={`tab-button ${activeTab === 'horariosDisponiveis' ? 'active' : ''}`} onClick={() => setActiveTab('horariosDisponiveis')}>
              <FaClipboardList /> Horários Disponíveis
          </button>
          <button className={`tab-button ${activeTab === 'minhasConsultas' ? 'active' : ''}`} onClick={() => setActiveTab('minhasConsultas')}>
              <FaCheckCircle /> Minhas Consultas
          </button>
      </div>

      <main className="agenda-main" style={{ display: 'flex', gap: '2rem', alignItems: 'flex-start' }}>

        {activeTab === 'horariosDisponiveis' && (
            <>
                <div style={{ flex: 2 }}>
                    <div className="lista-horarios">
                        {Object.keys(horariosAgrupados).length === 0 && (
                            <p style={{padding: '1rem'}}>Nenhum horário disponível encontrado.</p>
                        )}
                        {Object.keys(horariosAgrupados).map(data => (
                            <div key={data} className="horario-group-item">
                                <div className="horario-group-date">{data}</div>
                                <div className="horario-time-chip-container">
                                    {horariosAgrupados[data].map(h => (
                                        <button key={h.id} className={`horario-chip-btn ${horarioSelecionado?.id === h.id ? 'selected' : ''}`} onClick={() => handleSelecionarHorario(h)}>
                                            <div className="chip-time"><FaRegClock /> {h.horario}</div>
                                            <div className="chip-duration">{h.duracao || 50} minutos</div>
                                            <div style={{fontSize:'0.7rem', color:'#888', marginTop:'4px'}}>{h.nomePsi}</div>
                                        </button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div style={{ flex: 1 }}>
                    <div className="resumo-card">
                        {horarioSelecionado ? (
                            <>
                                <h3>Resumo da consulta</h3>
                                <div className="resumo-header">
                                    Data e hora selecionada
                                    <strong>{horarioSelecionado.data}</strong>
                                    <span className="resumo-hora">{horarioSelecionado.horario}</span>
                                    <span className="resumo-duracao">Duração {horarioSelecionado.duracao || 50}min</span>
                                    <span style={{fontSize:'0.8rem', marginTop:'0.5rem', color:'#333'}}>
                                        <FaUserMd style={{marginRight:'5px'}}/> 
                                        {horarioSelecionado.nomePsi}
                                    </span>
                                </div>
                                <div className="resumo-body">
                                    <textarea className="resumo-textarea" placeholder="Descreva brevemente o motivo da consulta..." value={motivoConsulta} onChange={(e) => setMotivoConsulta(e.target.value)}></textarea>
                                </div>
                                {error && <p className="error-text">{error}</p>}
                                {successMsg && <p className="success-text">{successMsg}</p>}
                                <button className="btn-confirmar" onClick={handleConfirmarAgendamento}>Confirmar agendamento</button>
                            </>
                        ) : (
                            <div className="resumo-placeholder">
                                <h3>Resumo da consulta</h3>
                                <p style={{fontSize: '0.8rem', marginTop: '1rem'}}>selecione um horario disponível</p>
                            </div>
                        )}
                    </div>
                </div>
            </>
        )}

        {activeTab === 'minhasConsultas' && (
            <div style={{ width: '100%' }}>
                {minhasConsultas.length === 0 ? (
                    <p>Você ainda não possui solicitações de consulta.</p>
                ) : (
                    <div className="lista-status-cards">
                        {minhasConsultas.map(consulta => renderCardConsulta(consulta))}
                    </div>
                )}
            </div>
        )}

      </main>
    </div>
  );
}

export default PortalAluno;