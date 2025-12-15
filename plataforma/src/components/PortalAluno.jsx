import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import '../portal-aluno.css'; // Importa o CSS portado do v0

const API_URL = 'http://127.0.0.1:5000';

export default function PortalAluno() {
  const navigate = useNavigate();
  const [aluno, setAluno] = useState(null);
  
  // Estados de UI
  const [activeTab, setActiveTab] = useState("horarios"); // 'horarios' | 'consultas'
  const [selectedSlot, setSelectedSlot] = useState(null);
  const [notes, setNotes] = useState("");
  
  // Estados de Dados
  const [availableSlots, setAvailableSlots] = useState([]);
  const [appointments, setAppointments] = useState([]);

  useEffect(() => {
    const stored = localStorage.getItem('dadosAluno');
    if (stored) {
      const alunoObj = JSON.parse(stored);
      setAluno(alunoObj);
      carregarDados(alunoObj.id);
    } else {
      navigate('/login');
    }
  }, [navigate]);

  const carregarDados = async (idAluno) => {
    try {
      // 1. Buscar Horários Livres (De todos os psicólogos)
      // Como o backend ainda não tem '/listar_todos_livres', vamos simular pegando de um endpoint de listagem
      // Se você implementou a rota global, use-a. Se não, aqui vai um fetch simulado:
      const resLivres = await fetch(`${API_URL}/listar_todos_horarios_livres`);
      if (resLivres.ok) {
        const dataLivres = await resLivres.json();
        setAvailableSlots(Array.isArray(dataLivres) ? dataLivres : []);
      }
      // 2. Buscar Minhas Consultas
      const resMinhas = await fetch(`${API_URL}/listar_consultas_aluno`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ idAluno })
      });
      const dataMinhas = await resMinhas.json();
      setAppointments(Array.isArray(dataMinhas) ? dataMinhas : []);

    } catch (error) { console.error(error); }
  };

  const handleConfirmAppointment = async () => {
    if (selectedSlot && aluno) {
      try {
        const res = await fetch(`${API_URL}/solicitar_agendamento`, {
          method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({
            idConsulta: selectedSlot.id,
            idAluno: aluno.id,
            nomeAluno: aluno.nome
          })
        });
        
        if(res.ok) {
          alert("Agendamento solicitado com sucesso!");
          setSelectedSlot(null);
          setNotes("");
          carregarDados(aluno.id);
          setActiveTab("consultas");
        } else {
          alert("Erro ao agendar.");
        }
      } catch (err) { alert("Erro de conexão", err); }
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('dadosAluno');
    navigate('/');
  };

  // Agrupar slots por data (Lógica do v0)
  const groupSlotsByDate = (slots) => {
    const grouped = {};
    slots.forEach((slot) => {
      // Formata data para "dd/mm/aaaa"
      const dateKey = slot.data; 
      if (!grouped[dateKey]) grouped[dateKey] = [];
      grouped[dateKey].push(slot);
    });
    return grouped;
  };

  const groupedSlots = groupSlotsByDate(availableSlots);

  if (!aluno) return null;

  return (
    <div className="portal-aluno-wrapper">
      <div className="portal-container">
        
        {/* HEADER */}
        <header className="pa-header">
          <div className="pa-header-content">
            <div className="pa-logo-section">
              <div className="pa-logo">
                <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
                  <rect width="48" height="48" rx="12" fill="#A8D5D5" />
                  <path d="M18 20C18 17.7909 19.7909 16 22 16C24.2091 16 26 17.7909 26 20C26 22.2091 24.2091 24 22 24C19.7909 24 18 22.2091 18 20Z" stroke="#1F5F5F" strokeWidth="2" />
                  <path d="M26 20C26 17.7909 27.7909 16 30 16C32.2091 16 34 17.7909 34 20C34 22.2091 32.2091 24 30 24C27.7909 24 26 22.2091 26 20Z" stroke="#1F5F5F" strokeWidth="2" />
                  <path d="M22 24C22 21.7909 23.7909 20 26 20C28.2091 20 30 21.7909 30 24C30 26.2091 28.2091 28 26 28C23.7909 28 22 26.2091 22 24Z" stroke="#1F5F5F" strokeWidth="2" />
                  <path d="M14 28C14 25.7909 15.7909 24 18 24C20.2091 24 22 25.7909 22 28C22 30.2091 20.2091 32 18 32C15.7909 32 14 30.2091 14 28Z" stroke="#1F5F5F" strokeWidth="2" />
                  <path d="M30 28C30 25.7909 31.7909 24 34 24C36.2091 24 38 25.7909 38 28C38 30.2091 36.2091 32 34 32C31.7909 32 30 30.2091 30 28Z" stroke="#1F5F5F" strokeWidth="2" />
                </svg>
              </div>
              <div>
                <h1 className="pa-title">Portal do Aluno</h1>
                <p className="pa-subtitle">Olá, {aluno.nome}</p>
              </div>
            </div>
            <button className="pa-exit-button" onClick={handleLogout}>
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M13 14L17 10M17 10L13 6M17 10H7M7 3H5C3.89543 3 3 3.89543 3 5V15C3 16.1046 3.89543 17 5 17H7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></svg>
              Sair
            </button>
          </div>
        </header>

        {/* MAIN CONTENT */}
        <main className="pa-main">
          
          {/* TABS */}
          <div className="pa-tabs">
            <button className={`pa-tab ${activeTab === "horarios" ? "pa-tab-active" : ""}`} onClick={() => setActiveTab("horarios")}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><rect x="4" y="4" width="16" height="16" rx="2" stroke="currentColor" strokeWidth="2" /><path d="M4 9H20" stroke="currentColor" strokeWidth="2" /><path d="M9 4V20" stroke="currentColor" strokeWidth="2" /></svg>
              Horários Disponíveis
            </button>
            <button className={`pa-tab ${activeTab === "consultas" ? "pa-tab-active" : ""}`} onClick={() => setActiveTab("consultas")}>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none"><circle cx="12" cy="12" r="9" stroke="currentColor" strokeWidth="2" /><path d="M12 6V12L16 14" stroke="currentColor" strokeWidth="2" strokeLinecap="round" /></svg>
              Minhas Consultas
            </button>
          </div>

          {/* TAB: HORÁRIOS */}
          {activeTab === "horarios" ? (
            <div className="pa-content-grid">
              
              {/* COLUNA ESQUERDA: LISTA DE HORÁRIOS */}
              <div className="pa-slots-section">
                {Object.keys(groupedSlots).length === 0 && (
                  <p style={{color:'#6b7280'}}>Nenhum horário disponível no momento.</p>
                )}
                {Object.entries(groupedSlots).map(([date, slots]) => (
                  <div key={date} className="pa-date-group">
                    <h3 className="pa-date-title">{date}</h3>
                    <div className="pa-slots-grid">
                      {slots.map((slot) => (
                        <button
                          key={slot.id}
                          className={`pa-slot-button ${selectedSlot?.id === slot.id ? "pa-slot-selected" : ""}`}
                          onClick={() => setSelectedSlot(slot)}
                        >
                          <div className="pa-slot-time">
                            <svg width="16" height="16" viewBox="0 0 16 16" fill="none"><circle cx="8" cy="8" r="7" stroke="currentColor" strokeWidth="1.5" /><path d="M8 4V8L10.5 10.5" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" /></svg>
                            {slot.hora}
                          </div>
                          <div className="pa-slot-duration">50 minutos</div>
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* COLUNA DIREITA: RESUMO (STICKY) */}
              <div className="pa-summary-card">
                <h3 className="pa-summary-title">Resumo da consulta</h3>
                {selectedSlot ? (
                  <div className="pa-summary-content">
                    <div className="pa-summary-info">
                      <div className="pa-summary-label">Data e hora selecionada</div>
                      <div className="pa-summary-date">{selectedSlot.data}</div>
                      <div className="pa-summary-time">{selectedSlot.hora}</div>
                      <div className="pa-summary-duration">Duração 50min</div>
                    </div>
                    <textarea
                      className="pa-summary-notes"
                      placeholder="Descreva brevemente o motivo..."
                      value={notes}
                      onChange={(e) => setNotes(e.target.value)}
                    />
                    <button className="pa-confirm-button" onClick={handleConfirmAppointment}>
                      Confirmar agendamento
                    </button>
                  </div>
                ) : (
                  <div className="pa-summary-empty">Selecione um horário disponível</div>
                )}
              </div>
            </div>
          ) : (
            
            /* TAB: MINHAS CONSULTAS */
            <div className="pa-appointments-section">
              {appointments.length === 0 && <p style={{color:'#6b7280'}}>Você não tem consultas agendadas.</p>}
              {appointments.map((appointment) => (
                <div key={appointment.id} className={`pa-appointment-card pa-appointment-${appointment.status}`}>
                  <div className="pa-appointment-header">
                    
                    {/* ÍCONE STATUS: CONFIRMADO */}
                    {appointment.status === "confirmado" && (
                      <>
                        <div className="pa-appointment-icon">
                          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="9" fill="#10B981" stroke="#10B981" strokeWidth="2" /><path d="M6 10L9 13L14 7" stroke="white" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" /></svg>
                        </div>
                        <span className="pa-appointment-status" style={{color:'#111827'}}>Confirmada</span>
                      </>
                    )}

                    {/* ÍCONE STATUS: PENDENTE */}
                    {appointment.status === "pendente" && (
                      <>
                        <div className="pa-appointment-icon">
                          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><circle cx="10" cy="10" r="9" fill="#F59E0B" stroke="#F59E0B" strokeWidth="2" /><path d="M10 6V10L13 12" stroke="white" strokeWidth="2" strokeLinecap="round" /></svg>
                        </div>
                        <span className="pa-appointment-status" style={{color:'#111827'}}>Aguardando confirmação</span>
                      </>
                    )}

                  </div>
                  <div className="pa-appointment-details">
                    {appointment.data} às {appointment.hora}
                  </div>
                </div>
              ))}
            </div>
          )}

        </main>
      </div>
    </div>
  );
}