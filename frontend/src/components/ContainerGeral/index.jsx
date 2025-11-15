import style from "./ContainerGeral.module.css";

function ContainerGeral( {children} ){
    return(
        <section className={style.ContainerGeral}>
            { children }
        </section>
    );
}

export default ContainerGeral;