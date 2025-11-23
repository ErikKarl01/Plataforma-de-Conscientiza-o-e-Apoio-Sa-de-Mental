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
  FaBell // Sino mantido
} from 'react-icons/fa';

const API_URL = 'http://127.0.0.1:5000';
const ID_PSICOLOGO = localStorage.getItem("idPsicologo");

function formatarDataParaAPI(dataString) {
  if (!dataString) return '';
  try {
    const [ano, mes, dia] = dataString.split('-');
    return `${dia}/${mes}/${ano}`;
  } catch (e) {
    console.error("Erro ao formatar data:", e);
    return '';
  }
}

function PortalAgenda() {
  // --- Estados de Controle de UI ---
  const [activeTab, setActiveTab] = useState('minhaAgenda');
  const [mostrarFormConsulta, setMostrarFormConsulta] = useState(false);
  const [mostrarFormHorario, setMostrarFormHorario] = useState(false);

  // --- Estados de Dados ---
  const [consultasReservadas, setConsultasReservadas] = useState([]);
  const [horariosLivres, setHorariosLivres] = useState([]);
  const [error, setError] = useState(null);
  
  
  const [solicitacoesPendentes] = useState([]);
  //lembrar de implementar essa função aqui e nao a de cima quando for fazer o aluno
 // const [solicitacoesPendentes, setSolicitacoesPendentes] = useState([]);

  // --- Estados de Formulário (Marcar Consulta - Aba Minha Agenda) ---
  const [nomePaciente, setNomePaciente] = useState('');
  const [dataConsulta, setDataConsulta] = useState('');
  const [horarioConsulta, setHorarioConsulta] = useState('');
  const [duracaoMarcarConsulta, setDuracaoMarcarConsulta] = useState('50');

  // --- Estados de Formulário (Adicionar Horário - Aba Meus Horários) ---
  const [dataNovoHorario, setDataNovoHorario] = useState('');
  const [horaNovoHorario, setHoraNovoHorario] = useState('');
  const [duracaoNovoHorario, setDuracaoNovoHorario] = useState('50');

  // ====================================================================
  // FUNÇÕES DE BUSCA DE DADOS
  // ====================================================================

  const fetchConsultas = async (rota, setter) => {
    try {
      const response = await fetch(`${API_URL}/${rota}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idPsicologo: ID_PSICOLOGO })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.mensagem || data.erro || `Não foi possível carregar dados de ${rota}.`);
      }
      
      setter(data);

    } catch (err) {
      setError(err.message);
    }
  };
  
  const agruparHorariosPorData = (horarios) => {
    return horarios.reduce((acc, current) => {
        const data = current.data;
        if (!acc[data]) {
            acc[data] = [];
        }
        acc[data].push(current);
        return acc;
    }, {});
  };


  useEffect(() => {
    setError(null);
    if (!ID_PSICOLOGO) {
        setError("ID do Psicólogo não encontrado. Faça login novamente.");
        return;
    }
    
    if (activeTab === 'minhaAgenda') {
      fetchConsultas('listarConsultas', setConsultasReservadas);
    } else if (activeTab === 'meusHorarios') {
      fetchConsultas('listarHorariosLivres', setHorariosLivres);
    }
    
    setMostrarFormConsulta(false);
    setMostrarFormHorario(false);
    
  }, [activeTab]);


  // ====================================================================
  // FLUXO MINHA AGENDA (Reservar para paciente)
  // ====================================================================

  const handleAddConsulta = async (e) => {
    e.preventDefault();
    setError(null);
    
    if (!nomePaciente || !dataConsulta || !horarioConsulta || !duracaoMarcarConsulta) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    const dataFormatada = formatarDataParaAPI(dataConsulta);

    try {
      // 1. Adicionar Horário (Disponibilizar) - Adiciona o slot livre
      const resEtapa1 = await fetch(`${API_URL}/adicionarHorario`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: dataFormatada,
          horario: horarioConsulta,
          idPsicologo: ID_PSICOLOGO,
          duracao: duracaoMarcarConsulta // Duração digitada
        })
      });

      if (!resEtapa1.ok) {
        const errorData = await resEtapa1.json();
        throw new Error(errorData.mensagem || 'Erro ao criar o horário no backend (Etapa 1).');
      }

      // 2. Marcar Consulta (Reservar para o paciente)
      const resEtapa2 = await fetch(`${API_URL}/marcarConsulta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idPsicologo: ID_PSICOLOGO,
          data: dataFormatada,
          horario: horarioConsulta,
          nomePaciente: nomePaciente,
          telPaciente: ""
        })
      });
      
      if (!resEtapa2.ok) {
        const errorData = await resEtapa2.json();
        throw new Error(errorData.mensagem || 'Erro ao marcar o paciente no horário (Etapa 2).');
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
    setDataConsulta('');
    setHorarioConsulta('');
    setDuracaoMarcarConsulta('50'); 
    setMostrarFormConsulta(false);
    setError(null);
  };
  
  const handleDeletarConsulta = async (consultaParaExcluir) => {
    setError(null);
    try {
      const response = await fetch(`${API_URL}/removerConsulta`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          idPsicologo: ID_PSICOLOGO,
          data: consultaParaExcluir.data,
          horario: consultaParaExcluir.horario
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.mensagem || 'Erro ao excluir a consulta.');
      }

      if (consultaParaExcluir.reservado) {
        setConsultasReservadas(prev => prev.filter(c => c.id !== consultaParaExcluir.id));
      } else {
        setHorariosLivres(prev => prev.filter(c => c.id !== consultaParaExcluir.id));
      }

    } catch (err) {
      setError(err.message);
    }
  };
  
  // ====================================================================
  // FLUXO MEUS HORÁRIOS (Adicionar Horário Disponível)
  // ====================================================================

  const handleAddNovoHorario = async (e) => {
      e.preventDefault();
      setError(null);
      
      if (!dataNovoHorario || !horaNovoHorario || !duracaoNovoHorario) {
          setError("Por favor, preencha todos os campos do horário.");
          return;
      }
      
      const dataFormatada = formatarDataParaAPI(dataNovoHorario);
      
      try {
          const response = await fetch(`${API_URL}/adicionarHorario`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify({
                  data: dataFormatada,
                  horario: horaNovoHorario,
                  idPsicologo: ID_PSICOLOGO,
                  duracao: duracaoNovoHorario // Duração digitada
              })
          });

          if (!response.ok) {
              const errorData = await response.json();
              throw new Error(errorData.mensagem || 'Erro ao adicionar o novo horário.');
          }

          const { consulta: novoHorario } = await response.json();
          setHorariosLivres(prev => [...prev, novoHorario]);
          handleCancelarNovoHorario(); 
          
      } catch (err) {
          setError(err.message);
      }
  };
  
  const handleCancelarNovoHorario = () => {
      setDataNovoHorario('');
      setHoraNovoHorario('');
      setDuracaoNovoHorario('50');
      setMostrarFormHorario(false);
      setError(null);
  };
  
  
  // ====================================================================
  // CONTEÚDO DAS ABAS
  // ====================================================================

  const TabContent = () => {
    
    // --- CONTEÚDO MINHA AGENDA ---
    if (activeTab === 'minhaAgenda') {
      return (
        <>
            <h2>Minha Agenda</h2>
            <p>Gerencie seus atendimentos e consultas</p>
            
            {/* Formulário de Adicionar Nova Consulta (Marcar para paciente) */}
            {mostrarFormConsulta && (
              <div className="form-nova-consulta">
                <h3>Adicionar nova consulta</h3>
                <p>Preencha os dados da consulta</p>

                <form onSubmit={handleAddConsulta}>
                  <div className="form-group-full">
                    <label htmlFor="nome-paciente">Nome do paciente</label>
                    <input
                      type="text"
                      id="nome-paciente"
                      placeholder="ex. josé fernando da silva"
                      value={nomePaciente}
                      onChange={(e) => setNomePaciente(e.target.value)}
                      required
                    />
                  </div>
                  
                  {/* Grid de 3 colunas para Data, Horário e Duração */}
                  <div className="form-grid-horario"> 
                    <div className="form-group">
                      <label htmlFor="data">Data</label>
                      <input
                        type="date"
                        id="data"
                        value={dataConsulta}
                        onChange={(e) => setDataConsulta(e.target.value)}
                        required
                      />
                    </div>

                    <div className="form-group">
                      <label htmlFor="horario">Horário</label>
                      <input
                        type="time"
                        id="horario"
                        value={horarioConsulta}
                        onChange={(e) => setHorarioConsulta(e.target.value)}
                        required
                      />
                    </div>
                    
                    {/* Duração como campo de entrada de número livre */}
                    <div className="form-group">
                      <label htmlFor="duracao-consulta">Duração (min)</label>
                      <input
                        type="number"
                        id="duracao-consulta"
                        placeholder="Ex: 50"
                        value={duracaoMarcarConsulta}
                        onChange={(e) => setDuracaoMarcarConsulta(e.target.value)}
                        required
                        min="10"
                      />
                    </div>
                    
                  </div>

                  <div className="form-actions">
                    <button type="submit" className="btn-adicionar">
                      Adicionar Consulta
                    </button>
                    <button 
                      type="button" 
                      className="btn-cancelar" 
                      onClick={handleCancelarConsulta}
                    >
                      Cancelar
                    </button>
                  </div>
                </form>
              </div>
            )}
            
            {/* Lista de Consultas Reservadas */}
            <div className="lista-consultas">
              {consultasReservadas.length === 0 && !error && !mostrarFormConsulta && (
                <p>Nenhuma consulta agendada.</p>
              )}

              {consultasReservadas.map(consulta => (
                <div key={consulta.id} className="item-consulta">
                  <div className="info-paciente">
                    <FaRegUser className="paciente-icon" />
                    <h3>{consulta.nomePaciente}</h3>
                  </div>

                  <div className="info-data-hora">
                    <span><FaRegCalendarAlt /> {consulta.data}</span>
                    <span><FaRegClock /> {consulta.horario} ({consulta.duracao || '50'} min)</span>
                  </div>

                  <button 
                    className="btn-deletar"
                    onClick={() => handleDeletarConsulta(consulta)}
                  >
                    <FaTrashAlt />
                  </button>
                </div>
              ))}
            </div>
        </>
      );
    } 

    // --- CONTEÚDO MEUS HORÁRIOS ---
    else if (activeTab === 'meusHorarios') {
        const horariosAgrupados = agruparHorariosPorData(horariosLivres);
        
        return (
            <>
                <h2>Meus Horários</h2>
                
                {/* Formulário de Adicionar Horário Disponível */}
                {mostrarFormHorario && (
                    <div className="form-novo-horario">
                        <h3>Adicionar horário</h3>
                        <p>Gerencie seus horários, veja os horários disponíveis</p>
                        
                        <form onSubmit={handleAddNovoHorario}>
                            <div className="form-grid-horario">
                                <div className="form-group">
                                    <label htmlFor="data-novo-horario">Data</label>
                                    <input
                                        type="date"
                                        id="data-novo-horario"
                                        placeholder="dd/mm/aaaa"
                                        value={dataNovoHorario}
                                        onChange={(e) => setDataNovoHorario(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="hora-novo-horario">Hora</label>
                                    <input
                                        type="time"
                                        id="hora-novo-horario"
                                        placeholder="--:--"
                                        value={horaNovoHorario}
                                        onChange={(e) => setHoraNovoHorario(e.target.value)}
                                        required
                                    />
                                </div>
                                <div className="form-group">
                                    <label htmlFor="duracao-novo-horario">Duração(min)</label>
                                    {/* Duração como campo de entrada de número livre */}
                                    <input
                                        type="number"
                                        id="duracao-novo-horario"
                                        placeholder="Ex: 50"
                                        value={duracaoNovoHorario}
                                        onChange={(e) => setDuracaoNovoHorario(e.target.value)}
                                        required
                                        min="10"
                                    />
                                </div>
                            </div>
                            
                            <div className="form-actions">
                                <button type="submit" className="btn-salvar">
                                    Salvar
                                </button>
                                <button 
                                    type="button" 
                                    className="btn-cancelar" 
                                    onClick={handleCancelarNovoHorario}
                                >
                                    Cancelar
                                </button>
                            </div>
                        </form>
                    </div>
                )}
                
                {/* Lista de Horários Cadastrados */}
                <div className="lista-horarios">
                    <h3>Horários Cadastrados</h3>
                    {Object.keys(horariosAgrupados).length === 0 && !error && !mostrarFormHorario && (
                        <p>Nenhum horário disponível cadastrado.</p>
                    )}
                    
                    {Object.keys(horariosAgrupados).map(dataAgrupada => (
                        <div key={dataAgrupada} className="horario-group-item">
                            <div className="horario-group-date">
                                <FaRegCalendarAlt /> {dataAgrupada}
                            </div>
                            <div className="horario-time-chip-container">
                                {horariosAgrupados[dataAgrupada].map(horario => (
                                    <div key={horario.id} className="horario-time-chip">
                                        <FaRegClock /> {horario.horario}
                                        <span className="duracao-min">{horario.duracao || '50'} minutos</span> 
                                        <button 
                                            className="btn-deletar-horario"
                                            onClick={() => handleDeletarConsulta(horario)}
                                        >
                                            <FaTrashAlt />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    ))}
                </div>
            </>
        );
    }
  };


  return (
    <div className="agenda-container">
      
      <header className="agenda-header">
        <div className="logo-section">
          <FaBrain className="logo-icon-agenda" />
          <div className="portal-info">
            <h1>Portal do Psicólogo</h1>
            <p>Gerenciamento de agenda</p>
          </div>
        </div>

        <Link to="/login" className="sair-link">
          <FaSignOutAlt /> Sair
        </Link>
      </header>

      <main className="agenda-main">
          
        {/* Nova Barra de Navegação por Abas */}
        <div className="tab-navigation">
            <button 
                className={`tab-button ${activeTab === 'minhaAgenda' ? 'active' : ''}`}
                onClick={() => setActiveTab('minhaAgenda')}
            >
                <FaCalendarAlt /> Minha Agenda
            </button>
            <button 
                className={`tab-button ${activeTab === 'meusHorarios' ? 'active' : ''}`}
                onClick={() => setActiveTab('meusHorarios')}
            >
                <FaClock /> Meus Horários
            </button>
            
            {/* Sino de Notificação MANTIDO */}
            <div className="notification-icon-container" onClick={() => setActiveTab('minhaAgenda')}>
                <FaBell className="notification-icon" />
                {solicitacoesPendentes.length > 0 && (
                    <span className="notification-badge">{solicitacoesPendentes.length}</span>
                )}
            </div>

            {/* Botão Nova Consulta / Adicionar Horário */}
            <div className="action-buttons-group">
              {(activeTab === 'minhaAgenda') ? (
                  <button 
                      className="btn-nova-consulta" 
                      onClick={() => setMostrarFormConsulta(prev => !prev)}
                  >
                      <FaPlus /> Nova consulta
                  </button>
              ) : (
                  <button 
                      className="btn-adicionar-horario" 
                      onClick={() => setMostrarFormHorario(prev => !prev)}
                  >
                      <FaPlus /> Adicionar horário
                  </button>
              )}
            </div>
        </div>

        {error && (
          <div className="message-container error-message">
            <p>{error}</p>
          </div>
        )}
        
        {/* Conteúdo da Aba Ativa */}
        <TabContent />

      </main>
    </div>
  );
}

export default PortalAgenda;