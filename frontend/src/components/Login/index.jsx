import { Link } from "react-router-dom";
import style from "./Login.module.css";

function Login() {
    return (
        <section className={style.ContainerPai}>
            <h1 className={style.titulo}>
                Portal de Atendimento
            </h1>
            <p className={style.p}>
                Gerenciamento dos atendimento
            </p>

            <div className={style.card_Login}>
                <h2>Entrar</h2>
                <p className={style.subtitle}>Digite suas credenciais para acessar</p>

                <form>
                    <label htmlFor="email">Email</label>
                    <div className={style.inputBox}>
                        <span className={style.icon}>📧</span>
                        <input
                            type="email"
                            id="email"
                            placeholder="seuemail@gmail.com"
                            required
                        />
                    </div>

                    <label htmlFor="senha">Senha</label>
                    <div className={style.inputBox}>
                        <span className={style.icon}>🔒</span>
                        <input
                            type="password"
                            id="senha"
                            placeholder="••••••••"
                            required
                        />
                    </div>

                    <div className={style.container_btn}>
                        <button type="submit" className={style.btn}>Entrar</button>
                    </div>
                </form>
            </div>

            <p className={style.p}>
                Ainda não tem cadastro? <Link to={"selecao-de-cadastro"}>Cadastre-se</Link>
            </p>
        </section>
    );
}

export default Login;
