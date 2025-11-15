import style from "./ContainerInterno.module.css";

function ContainerInterno({ children }){
    return(
        <section className={style.ContainerInterno}>
            { children }
        </section>
    );
}

export default ContainerInterno;