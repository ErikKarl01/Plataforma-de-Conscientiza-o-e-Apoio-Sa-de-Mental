import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  FaCalendarAlt, FaHistory, FaSignOutAlt, FaBrain, 
  FaUserMd, FaExchangeAlt, FaClock 
} from 'react-icons/fa';
import '../portal-aluno.css';

const API_URL = 'http://127.0.0.1:5000';

export default function PortalAluno() {
  const navigate = useNavigate();
  const [aluno, setAluno] = useState(null);
  
  // -- ESTADOS UI --
  const [activeTab, setActiveTab] = useState("horarios"); // 'horarios' | 'minhas'
  const [reschedulingId, setReschedulingId] = useState(null); // ID da consulta sendo trocada
  
  // -- DADOS --
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
      // 1. Buscar TODOS os horários livres (de todos os psicólogos)
      const resLivres = await fetch(`${API_URL}/listar_todos_horarios_livres`);
      if (resLivres.ok) {
        const dataLivres = await resLivres.json();
        setAvailableSlots(Array.isArray(dataLivres) ? dataLivres : []);
      }

      // 2. Buscar Consultas do Aluno
      const resMinhas = await fetch(`${API_URL}/listar_consultas_aluno`, {
        method: 'POST', headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ idAluno })
      });
      const dataMinhas = await resMinhas.json();
      setAppointments(Array.isArray(dataMinhas) ? dataMinhas : []);

    } catch (error) { console.error("Erro ao carregar dados:", error); }
  };

  // -- AÇÃO DE CLIQUE NO CARD DE HORÁRIO --
  const handleSlotAction = async (slot) => {
    // CENÁRIO A: REMARCANDO (TROCA)
    if (reschedulingId) {
      if(!window.confirm("Confirmar a troca para este novo horário?")) return;
      try {
        const res = await fetch(`${API_URL}/remarcar_consulta_aluno`, {
          method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ idAntiga: reschedulingId, idNova: slot.id })
        });
        
        if(res.ok) {
          alert("Consulta remarcada com sucesso! Aguarde a confirmação.");
          setReschedulingId(null);
          carregarDados(aluno.id);
          setActiveTab("minhas");
        } else {
          alert("Erro ao tentar remarcar.");
        }
      } catch (err) { alert("Erro de conexão.", err); }
    } 
    // CENÁRIO B: NOVO AGENDAMENTO
    else {
      if(!window.confirm("Solicitar este horário?")) return;
      try {
        const res = await fetch(`${API_URL}/solicitar_agendamento`, {
          method: 'POST', headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({ 
            idConsulta: slot.id, 
            idAluno: aluno.id, 
            nomeAluno: aluno.nome 
          })
        });
        
        if(res.ok) {
          alert("Solicitação enviada!");
          carregarDados(aluno.id);
          setActiveTab("minhas");
        }
      } catch (err) { alert("Erro de conexão.", err); }
    }
  };

  // -- INICIAR PROCESSO DE REMARCAÇÃO --
  const iniciarRemarcacao = (idConsulta) => {
    setReschedulingId(idConsulta);
    setActiveTab("horarios"); // Joga o usuário para a lista para escolher
    // Opcional: Scroll to top
    window.scrollTo(0, 0);
  };

  const cancelarRemarcacao = () => {
    setReschedulingId(null);
  };

  const handleLogout = () => { localStorage.removeItem('dadosAluno'); navigate('/'); };
  const formatDate = (d) => { if(!d) return ''; const [a,m,dia] = d.split('-'); return `${dia}/${m}/${a}`; };

  if (!aluno) return null;

  return (
    <div className="portal-aluno-wrapper">
      
      {/* HEADER */}
      <header className="pa-header">
        <div className="pa-header-content">
          <div className="pa-logo-section">
            <div className="pa-logo"><FaBrain size={30} color="#0D9488" /></div>
            <div><h1 className="pa-title">Portal do Aluno</h1><p className="pa-subtitle">Bem-vindo, {aluno.nome}</p></div>
          </div>
          <button className="pa-exit-button" onClick={handleLogout}><FaSignOutAlt /> Sair</button>
        </div>
      </header>

      <main className="pa-main">
        
        {/* BANNER DE AVISO (QUANDO ESTIVER REMARCANDO) */}
        {reschedulingId && (
          <div style={{background:'#FEF3C7', border:'1px solid #D97706', color:'#92400e', padding:'1rem', borderRadius:'8px', marginBottom:'1.5rem', display:'flex', justifyContent:'space-between', alignItems:'center'}}>
            <div style={{display:'flex', alignItems:'center', gap:'0.5rem'}}>
              <FaExchangeAlt /> 
              <span><strong>Modo de Remarcação:</strong> Escolha um novo horário disponível abaixo.</span>
            </div>
            <button onClick={cancelarRemarcacao} style={{background:'white', border:'1px solid #92400e', padding:'0.3rem 1rem', borderRadius:'4px', cursor:'pointer', color:'#92400e', fontWeight:'bold'}}>
              Cancelar Troca
            </button>
          </div>
        )}

        {/* NAVEGAÇÃO */}
        <div className="pa-tabs">
          <button className={`pa-tab ${activeTab === "horarios" ? "pa-tab-active" : ""}`} onClick={() => setActiveTab("horarios")}>
            <FaCalendarAlt /> Horários Disponíveis
          </button>
          <button className={`pa-tab ${activeTab === "minhas" ? "pa-tab-active" : ""}`} onClick={() => setActiveTab("minhas")}>
            <FaHistory /> Minhas Consultas
          </button>
        </div>

        {/* --- ABA 1: HORÁRIOS DISPONÍVEIS --- */}
        {activeTab === "horarios" && (
          <div className="pa-slots-grid">
            {availableSlots.length === 0 && <p style={{gridColumn:'1/-1', textAlign:'center', color:'#6B7280'}}>Nenhum horário disponível no momento.</p>}
            
            {availableSlots.map(item => (
              <div key={item.id} className="pa-appointment-card" style={{border: reschedulingId ? '2px solid #F59E0B' : '1px solid #E2E8F0'}}>
                <div className="pa-appointment-header">
                  <span className="pa-appointment-status" style={{color:'#0D9488', display:'flex', alignItems:'center', gap:'0.5rem'}}>
                    <FaUserMd /> {item.nomePsicologo || 'Psicólogo'}
                  </span>
                </div>
                
                <div className="pa-slot-time" style={{fontSize:'1.5rem', fontWeight:'bold', color:'#111827', marginTop:'0.5rem'}}>
                  {item.hora}
                </div>
                <div className="pa-appointment-details" style={{marginLeft:0, marginBottom:'1rem'}}>
                  {formatDate(item.data)} • {item.duracao || 50} min
                </div>
                
                <button 
                  className="pa-confirm-button" 
                  style={{
                    width:'100%', 
                    background: reschedulingId ? '#D97706' : '#0D9488',
                    display:'flex', justifyContent:'center', alignItems:'center', gap:'0.5rem'
                  }}
                  onClick={() => handleSlotAction(item)}
                >
                  {reschedulingId ? <><FaExchangeAlt /> Confirmar Troca</> : 'Solicitar Agendamento'}
                </button>
              </div>
            ))}
          </div>
        )}

        {/* --- ABA 2: MINHAS CONSULTAS --- */}
        {activeTab === "minhas" && (
          <div className="pa-appointments-section">
            {appointments.length === 0 && <p style={{textAlign:'center', color:'#6B7280'}}>Você não possui agendamentos.</p>}
            
            {appointments.map(item => (
              <div key={item.id} className={`pa-appointment-card pa-appointment-${item.status}`}>
                <div className="pa-appointment-header">
                  <span className={`pa-appointment-status`} style={{textTransform:'uppercase', fontSize:'0.8rem'}}>
                    {item.status === 'pendente' ? 'Aguardando Confirmação' : item.status}
                  </span>
                </div>
                
                <div className="pa-appointment-details" style={{fontSize:'1.2rem', fontWeight:'600', marginLeft:0, marginTop:'0.5rem'}}>
                  <FaCalendarAlt style={{marginRight:'0.5rem', color:'#6B7280'}} />
                  {formatDate(item.data)} às {item.hora}
                </div>
                <div style={{color:'#6B7280', fontSize:'0.9rem', marginTop:'0.2rem'}}>
                  Psicólogo(a): {item.nomePsicologo || 'Não informado'} ({item.duracao || 50} min)
                </div>

                <div className="pa-appointment-actions" style={{marginTop:'1rem', paddingTop:'1rem', borderTop:'1px solid #F3F4F6', display:'flex', gap:'0.5rem'}}>
                  {/* Botão Remarcar (Só para Pendente ou Confirmado) */}
                  {(item.status === 'pendente' || item.status === 'confirmado') && (
                    <button 
                      style={{
                        padding:'0.5rem 1rem', border:'1px solid #D1D5DB', borderRadius:'6px', 
                        background:'white', cursor:'pointer', display:'flex', alignItems:'center', gap:'0.5rem',
                        color:'#374151', fontWeight:'500'
                      }}
                      onClick={() => iniciarRemarcacao(item.id)}
                    >
                      <FaExchangeAlt /> Remarcar
                    </button>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

      </main>
    </div>
  );
}