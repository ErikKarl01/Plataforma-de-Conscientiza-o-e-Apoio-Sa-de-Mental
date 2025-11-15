import style from "./Container1.module.css";

function Container1( {children} ){
    return(
        <section className={style.Container1}>
            { children }
        </section>
    );
}

export default Container1;