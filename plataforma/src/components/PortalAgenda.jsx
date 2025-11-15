import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { 
  FaBrain, 
  FaSignOutAlt,
  FaPlus, 
  FaRegUser,
  FaRegCalendarAlt,
  FaRegClock, 
  FaTrashAlt
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
  const [mostrarForm, setMostrarForm] = useState(false);

  const [nomePaciente, setNomePaciente] = useState('');
  const [dataConsulta, setDataConsulta] = useState('');
  const [horarioConsulta, setHorarioConsulta] = useState('');

  const [consultas, setConsultas] = useState([]);
  const [error, setError] = useState(null);

  const fetchConsultas = async () => {
    try {
      console.log("ID enviado:", ID_PSICOLOGO);
      const response = await fetch(`${API_URL}/listarConsultas`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ idPsicologo: ID_PSICOLOGO })
      });

      if (!response.ok) {
        throw new Error('Não foi possível carregar as consultas.');
      }

      const data = await response.json();
      console.log(data);
      setConsultas(data);
    } catch (err) {
      setError(err.message);
    }
  };

  useEffect(() => {
    fetchConsultas();
  }, []);

  const handleAddConsulta = async (e) => {
    e.preventDefault();
    setError(null);

    if (!nomePaciente || !dataConsulta || !horarioConsulta) {
      setError("Por favor, preencha todos os campos.");
      return;
    }

    const dataFormatada = formatarDataParaAPI(dataConsulta);

    try {
      const resEtapa1 = await fetch(`${API_URL}/adicionarHorario`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          data: dataFormatada,
          horario: horarioConsulta,
          idPsicologo: ID_PSICOLOGO
        })
      });

      if (!resEtapa1.ok) {
        throw new Error('Erro ao criar o horário no backend (Etapa 1).');
      }

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
        throw new Error('Erro ao marcar o paciente no horário (Etapa 2).');
      }

      const { consulta: consultaSalva } = await resEtapa2.json();
      setConsultas(prevConsultas => [...prevConsultas, consultaSalva]);

      handleCancelar();

    } catch (err) {
      setError(err.message);
    }
  };

  const handleCancelar = () => {
    setNomePaciente('');
    setDataConsulta('');
    setHorarioConsulta('');
    setMostrarForm(false);
    setError(null);
  };

  const handleDeletar = async (consultaParaExcluir) => {
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
        throw new Error('Erro ao excluir a consulta.');
      }

      setConsultas(consultas.filter(c => c.id !== consultaParaExcluir.id));

    } catch (err) {
      setError(err.message);
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
        <div className="agenda-title-bar">
          <div>
            <h2>Minha Agenda</h2>
            <p>Gerencie seus atendimentos e consultas</p>
          </div>

          <button 
            className="btn-nova-consulta" 
            onClick={() => setMostrarForm(true)}
          >
            <FaPlus /> Nova consulta
          </button>
        </div>

        {error && (
          <div className="message-container error-message">
            <p>{error}</p>
          </div>
        )}

        {mostrarForm && (
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

              <div className="form-grid-agenda">
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
              </div>

              <div className="form-actions">
                <button type="submit" className="btn-adicionar">
                  Adicionar Consulta
                </button>
                <button 
                  type="button" 
                  className="btn-cancelar" 
                  onClick={handleCancelar}
                >
                  Cancelar
                </button>
              </div>
            </form>
          </div>
        )}

        <div className="lista-consultas">
          {consultas.length === 0 && !error && (
            <p>Nenhuma consulta agendada.</p>
          )}

          {consultas.map(consulta => (
            <div key={consulta.id} className="item-consulta">
              <div className="info-paciente">
                <FaRegUser className="paciente-icon" />
                <h3>{consulta.nomePaciente}</h3>
              </div>

              <div className="info-data-hora">
                <span><FaRegCalendarAlt /> {consulta.data}</span>
                <span><FaRegClock /> {consulta.horario}</span>
              </div>

              <button 
                className="btn-deletar"
                onClick={() => handleDeletar(consulta)}
              >
                <FaTrashAlt />
              </button>
            </div>
          ))}
        </div>

      </main>
    </div>
  );
}

export default PortalAgenda;
