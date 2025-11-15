import style from "./Header1.module.css";
import logo from "../../../public/imagens/img_header1.png";
import { GoArrowLeft } from "react-icons/go";
import { Link } from "react-router-dom";


function Header1(){
    return(
        <section className={style.container}>
            <div className={style.container_btn_voltar}>
                <Link to={"#"} className={style.link}>
                    <div className={style.btn_voltar}>
                        <span className={style.btn_icon}><GoArrowLeft /></span>
                        <span>Voltar para Home</span>
                    </div>
                </Link>
            </div>

            <div className={style.container_logo}>
                <img className={style.logo} src={logo} alt="Logo do site" />
            </div>
        </section>
    );
}

export default Header1;