import style from "./PsicoMinhaAgenda.module.css";
import { FaPlus } from "react-icons/fa6";
import { IoNotifications } from "react-icons/io5";
import AdicionarNovaConsultaModal from "../AdicionarNovaConsultaModal";
import NotificacaoNovaConsultaModal from "../NotificacaoNovaConsultaModal";
import { useState } from "react";

function PsicoMinhaAgenda(){
    const [openConsulta, setOpenConsulta] = useState(false);
    const [openNoticacao, setOpenNoticacao] = useState(false);

    return(
        <section>
            <div className={style.containerPai}>
                <div className={style.containerFilho}>
                    <div className={style.titulo_subtitulo}>
                        <h1 className={style.titulo}>Minha Agenda</h1>
                        <h2 className={style.subtitulo}>Gerencie seus atendimento e consultas</h2>
                    </div>

                    <div className={style.botoes}>

                        <button className={style.btn_notificacao} onClick={()=>setOpenNoticacao(!openNoticacao)}>
                            <IoNotifications/>
                        </button>

                        <button className={style.btn_nova_consulta} onClick={()=>setOpenConsulta(!openConsulta)}>
                            <FaPlus/>
                            <span>Nova consulta</span>
                        </button>

                    </div>

                </div>

                <AdicionarNovaConsultaModal consultaopen={openConsulta} consultaclose={setOpenConsulta}/>
                <NotificacaoNovaConsultaModal notificacaoOpen={openNoticacao} notificacaoClose={setOpenNoticacao}/>
            </div>
        </section>
    );
}

export default PsicoMinhaAgenda;