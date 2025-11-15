import Header2 from "../../components/Header2";
import ContainerGeral from "../../components/ContainerGeral";
import ContainerInterno from "../../components/ContainerInterno";
import Container1 from "../../components/Container1";
import CadastroPsicologo from "../../components/CadastroPsicologo";

function PaginaCadastroPsicologo(){
    return(
        <>
            <ContainerGeral>
                <ContainerInterno>
                    <Header2 />
                    <Container1>
                        <CadastroPsicologo />
                    </Container1>
                </ContainerInterno>
            </ContainerGeral>
        </>
    );
}

export default PaginaCadastroPsicologo;