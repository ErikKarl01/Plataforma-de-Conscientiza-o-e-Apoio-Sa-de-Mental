import style from "./AdicionarNovaConsultaModal.module.css";

function AdicionarNovaConsultaModal({ consultaopen, consultaclose }) {
    if (consultaopen == true) {
        return (
            <section className={style.card_Login}>
                <h2>Adicionar nova consulta</h2>
                <p className={style.subtitle}>Preencha os dados da consulta</p>

                <form className={style.form}>

                    {/* Nome do paciente */}
                    <div className={style.inputGroupFull}>
                        <label>Nome do paciente</label>
                        <input type="text" placeholder="ex. jose fernando da silva" required />
                    </div>

                    {/* Data */}
                    <div className={style.inputGroup}>
                        <label>Data</label>
                        <input type="text" placeholder="01/11/1111" required />
                    </div>

                    {/* Horário */}
                    <div className={style.inputGroup}>
                        <label>Horário</label>
                        <input type="text" placeholder="00:00" required />
                    </div>

                </form>

                <div className={style.buttons}>
                    <button type="submit" className={style.btnConfirm}>Adicionar Consulta</button>
                    <button className={style.btnCancel} onClick={()=> consultaclose(!consultaopen)}>Cancelar</button>
                </div>
            </section>
        );
    }
    else {
        <></>
    }


}

export default AdicionarNovaConsultaModal;