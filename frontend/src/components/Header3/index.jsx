import style from "./Header3.module.css";
import logo from "../../../public/imagens/img_header1.png";
import { RxExit } from "react-icons/rx";
import { Link } from "react-router-dom";

function Header3(){
    return(
        <section className={style.container}>
            <div className={style.container_logo_legenda}>
                <div className={style.container_logo}>
                    <img className={style.logo} src={logo} alt="Logo do site" />
                </div>
                <div className={style.legendas}>
                    <div className={style.legenda1}>
                        <span>Portal do Psícologo</span>
                    </div>
                    <div className={style.legenda2}>
                        <span>Gerenciamento de agenda</span>
                    </div>
                </div>
            </div>

            <Link to={"/"} className={style.link}>
                <div className={style.btn_sair}>
                    <span className={style.btn_icon}><RxExit /></span>
                    <span>Sair</span>
                </div>
            </Link>
        </section>
    );
}

export default Header3;