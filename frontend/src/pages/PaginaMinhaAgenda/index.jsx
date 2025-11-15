import Container2 from "../../components/Container2";
import ContainerGeral from "../../components/ContainerGeral";
import ContainerInterno from "../../components/ContainerInterno";
import Header3 from "../../components/Header3";
import PsicoMinhaAgenda from "../../components/PsicoMinhaAgenda";


function PaginaMinhaAgenda(){
    return(
        <>
            <ContainerGeral>
                <ContainerInterno>
                    <Header3 />
                    <Container2>
                        <PsicoMinhaAgenda />
                    </Container2>
                </ContainerInterno>
            </ContainerGeral>
        </>
    );
}

export default PaginaMinhaAgenda;
