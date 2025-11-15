import { Link } from "react-router-dom";
import aluno from "./imagens/aluno.png";
import psicologo from "./imagens/psicologo.png";
import style from "./EscolhaDeCadastro.module.css";

function EscolhaDeCadastro(){
    return(
        <section className={style.ContainerPai}>
            <h1 className={style.titulo}>
                Cadastro
            </h1>
            <p className={style.p}>
                Gerenciamento dos atendimento
            </p>

            <div className={style.card_Login}>
                <Link to={"#"} className={style.link}>
                    <div className={style.container_logo}>
                        <img className={style.logoUsuario} src={aluno} alt="Logo do site" />
                        <span>Aluno</span>
                    </div>
                </Link>

                <Link to={"cadastro-psicologo"} className={style.link}>
                    <div className={style.container_logo}>
                        <img className={style.logoPsicologo} src={psicologo} alt="Logo do site" />
                        <span>Psícologo</span>
                    </div>
                </Link>
            </div>
        </section>
    );
}

export default EscolhaDeCadastro;