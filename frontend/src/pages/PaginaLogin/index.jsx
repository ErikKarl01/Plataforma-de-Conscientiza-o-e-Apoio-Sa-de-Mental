import Header1 from "../../components/Header1";
import ContainerGeral from "../../components/ContainerGeral";
import ContainerInterno from "../../components/ContainerInterno";
import Container1 from "../../components/Container1";
import Login from "../../components/Login";


function PaginaLogin(){
    return(
        <>
            <ContainerGeral>
                <ContainerInterno>
                    <Header1 />
                    <Container1>
                        <Login />
                    </Container1>
                </ContainerInterno>
            </ContainerGeral>
        </>
    );
}

export default PaginaLogin;
