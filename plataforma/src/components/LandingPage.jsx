import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FaBrain } from 'react-icons/fa';
import '../App.css';

// Dados exatos do arquivo events-section.tsx
const events = [
  {
    title: "UFERSA - Elaboração do mês amarelo",
    image: "https://images.unsplash.com/photo-1531482615713-2afd69097998?auto=format&fit=crop&w=500&q=60",
    badge: "Evento", badgeColor: "badge-pink"
  },
  {
    title: "Nunca mais deixe de falar sobre saúde mental",
    image: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=500&q=60",
    badge: "Evento", badgeColor: "badge-pink"
  },
  {
    title: "Valorização da vida: O Setembro Amarelo funciona 24h",
    image: "https://images.unsplash.com/photo-1628102491629-778571d893a3?auto=format&fit=crop&w=500&q=60",
    badge: "Tema", badgeColor: "badge-primary"
  },
];

// Dados exatos do arquivo knowledge-section.tsx
const knowledgeItems = [
  {
    title: "Saúde mental é influenciada por fatores biológicos, ambientais e sociais",
    image: "https://images.unsplash.com/photo-1543269865-cbf427effbad?auto=format&fit=crop&w=800&q=60",
    badge: "Tema", badgeColor: "badge-primary"
  },
  {
    title: "A infância influencia fortemente a saúde mental do adulto...",
    subtitle: "Experiências positivas fortalecem o bem-estar.",
    image: "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?auto=format&fit=crop&w=800&q=60",
    badge: null, badgeColor: ""
  },
  {
    title: "O Quarto de Jack (Room, 2015)",
    subtitle: "Foco em trauma, adaptação e resiliência.",
    image: "https://images.unsplash.com/photo-1485846234645-a62644f84728?auto=format&fit=crop&w=800&q=60",
    badge: "Dica de Filme", badgeColor: "badge-destructive"
  },
];

export default function LandingPage() {
  const navigate = useNavigate();

  const scrollTo = (id) => {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
  };

  return (
    <div className="landing-page">
      {/* HEADER */}
      <header className="header-sticky">
        <div className="header-container">
          <div className="logo-box">
            <div className="logo-circle"><FaBrain /></div>
            <div>
              <div style={{fontWeight:'700', lineHeight:1.1}}>UFERSA</div>
              <div style={{fontSize:'0.75rem', color:'#64748B'}}>Saúde Mental</div>
            </div>
          </div>
          
          <nav className="nav-menu">
            <a href="#eventos" onClick={(e)=>{e.preventDefault(); scrollTo('eventos')}} className="nav-link">Eventos da temporada</a>
            <a href="#quer-saber" onClick={(e)=>{e.preventDefault(); scrollTo('quer-saber')}} className="nav-link">Quer saber?</a>
            <a href="#agendar" onClick={(e)=>{e.preventDefault(); scrollTo('agendar')}} className="nav-link">Agendar Consulta</a>
          </nav>

          <button className="btn-login" onClick={() => navigate('/escolha-perfil')}>Login</button>
        </div>
      </header>

      {/* HERO SECTION */}
      <section className="hero">
        <div className="container">
          <h1>Plataforma de Conscientização e Apoio à Saúde Mental</h1>
          <p>
            Plataforma Online de Conscientização e Apoio à Saúde Mental, que atua como canal primário para conscientizar
            os alunos sobre a importância da saúde mental. Facilitar o acesso e o agendamento de consultas com
            profissionais de psicologia, fornecer ferramentas de autoavaliação e um espaço com conteúdo educacional.
          </p>
        </div>
      </section>

      {/* EVENTOS */}
      <section id="eventos" className="section-py">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Eventos da temporada</h2>
            <p className="section-desc">
              Ao longo do ano, oferecemos palestras, rodas de conversa, workshops e atividades práticas conduzidas por
              profissionais qualificados.
            </p>
          </div>
          
          <div className="grid-cards">
            {events.map((evt, idx) => (
              <div key={idx} className="card">
                <div className="card-image-box">
                  <img src={evt.image} alt={evt.title} className="card-img" />
                  <div className="card-gradient" />
                  <span className={`badge ${evt.badgeColor}`}>{evt.badge}</span>
                  <div className="card-content-absolute">
                    <p className="card-title">{evt.title}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* QUER SABER? */}
      <section id="quer-saber" className="section-py bg-muted">
        <div className="container">
          <div className="text-center">
            <h2 className="section-title">Quer saber?</h2>
            <p className="section-desc">
              Aqui reunimos informações que ajudam a desmistificar conceitos, ampliar o conhecimento e despertar a
              curiosidade sobre como nossa mente funciona.
            </p>
          </div>

          <div className="grid-cards">
            {knowledgeItems.map((item, idx) => (
              <div key={idx} className="card">
                <div className="card-image-box">
                  <img src={item.image} alt={item.title} className="card-img" />
                  <div className="card-gradient" />
                  {item.badge && <span className={`badge ${item.badgeColor}`}>{item.badge}</span>}
                  <div className="card-content-absolute">
                    <p className="card-title">{item.title}</p>
                    {item.subtitle && <p className="card-sub">{item.subtitle}</p>}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CALL TO ACTION */}
      <section className="cta-section">
        <div className="cta-texture" />
        <div className="container">
          <h2 className="cta-text">VOCÊ NÃO ESTÁ SOZINHO!</h2>
        </div>
      </section>

      {/* CONSULTATION */}
      <section id="agendar" className="section-py">
        <div className="container">
          <div className="consult-box">
            <div className="consult-border-title">
              <h2 className="consult-h2">Agendar Consulta</h2>
            </div>
            <p style={{fontWeight:500, marginBottom:'0.5rem'}}>Você não está sozinho(a)!</p>
            <p className="consult-text">
              A nossa instituição, UFERSA, oferece atendimento gratuito a todos os estudantes para orientação,
              acompanhamento terapêutico e apoio em crises.
            </p>
            <button 
                className="btn-login" 
                style={{marginTop:'2rem', padding:'0.8rem 2.5rem', fontSize:'1rem'}}
                onClick={() => navigate('/escolha-perfil')}
            >
                Acessar Portal do Aluno
            </button>
          </div>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="container">
          <div className="footer-grid">
            <div>
              <h3>UFERSA</h3>
              <p style={{color:'rgba(255,255,255,0.8)', fontSize:'0.9rem', lineHeight:1.6}}>
                Universidade Federal Rural do Semi-Árido<br/>Campus Mossoró
              </p>
            </div>
            <div>
              <h3>Links Úteis</h3>
              <ul>
                <li><a href="#">Site UFERSA</a></li>
                <li><a href="#">Portal do Estudante</a></li>
                <li><a href="#">Ministério da Saúde</a></li>
              </ul>
            </div>
            <div>
              <h3>Recursos</h3>
              <ul>
                <li><a href="#">Política de Privacidade</a></li>
                <li><a href="#">Termos de Uso</a></li>
                <li><a href="#">Contato</a></li>
              </ul>
            </div>
          </div>
          <div className="footer-bottom">
            <p>© 2025 - UFERSA - Portal de Apoio à Saúde Mental.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}