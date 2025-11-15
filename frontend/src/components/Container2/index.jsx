import style from "./Container2.module.css";

function Container2( {children} ){
    return(
        <section className={style.Container1}>
            { children }
        </section>
    );
}

export default Container2;
