import style from "./NotificacaoNovaConsultaModal.module.css";

function NotificacaoNovaConsultaModal({ notificacaoOpen, notificacaoClose }){
    if(notificacaoOpen == true){
        return(
            <section className={style.card_notificacao}>
                
            </section>
        );
    }
    else{
        <></>
    }
}

export default NotificacaoNovaConsultaModal;