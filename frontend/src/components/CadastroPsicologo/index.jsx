import { Link } from "react-router-dom";
import style from "./CadastroPsicologo.module.css";

function CadastroPsicologo() {
    return (
        <section className={style.ContainerPai}>
            <h1 className={style.titulo}>
                Cadastro de Psícologo
            </h1>
            <p className={style.p}>
                Preencha seus dados para começar a gerenciar sua agenda
            </p>

            <div className={style.card_Login}>
                <h2>Criar Conta</h2>
                <p className={style.subtitle}>
                    Preencha o formulário abaixo para criar sua conta
                </p>

                <form className={style.form}>

                    {/* Nome Completo */}
                    <div className={style.inputGroup}>
                        <label>Nome completo</label>
                        <input type="text" placeholder="ex. maria da silva" required/>
                    </div>

                    {/* CRP */}
                    <div className={style.inputGroup}>
                        <label>CRP</label>
                        <input type="text" placeholder="00/0000" required/>
                    </div>

                    {/* Email */}
                    <div className={style.inputGroup}>
                        <label>E-mail</label>
                        <input type="email" placeholder="email@gmail.com" required/>
                    </div>

                    {/* Telefone */}
                    <div className={style.inputGroup}>
                        <label>Telefone</label>
                        <input type="text" placeholder="(88) 9 9999-9999" required/>
                    </div>

                    {/* Senha */}
                    <div className={style.inputGroup}>
                        <label>Senha</label>
                        <input type="password" placeholder="••••••••" required/>
                    </div>

                    {/* Confirmar senha */}
                    <div className={style.inputGroup}>
                        <label>Confirmar senha</label>
                        <input type="password" placeholder="••••••••" required/>
                    </div>
                </form>

                <div className={style.container_btn}>
                    <button type="submit" className={style.btn}>Criar conta</button>
                </div>
            </div>
        </section>
    );
}

export default CadastroPsicologo;