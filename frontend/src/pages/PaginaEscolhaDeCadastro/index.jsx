import Container1 from "../../components/Container1";
import ContainerGeral from "../../components/ContainerGeral";
import ContainerInterno from "../../components/ContainerInterno";
import EscolhaDeCadastro from "../../components/EscolhaDeCadastro";
import Header2 from "../../components/Header2";


function PaginaEscolhaDeCadastro(){
    return(
        <>
            <ContainerGeral>
                <ContainerInterno>
                    <Header2 />
                    <Container1>
                        <EscolhaDeCadastro />
                    </Container1>
                </ContainerInterno>
            </ContainerGeral>
        </>
    );
}

export default PaginaEscolhaDeCadastro;