import { BrowserRouter, Route, Routes } from "react-router-dom";
import PaginaLogin from "./pages/PaginaLogin";
import PaginaCadastroPsicologo from "./pages/PaginaCadastroPsicologo";
import PaginaMinhaAgenda from "./pages/PaginaMinhaAgenda";
import PaginaEscolhaDeCadastro from "./pages/PaginaEscolhaDeCadastro";

function AppRoutes() {
    return (
        <BrowserRouter>
            <Routes>
                <Route path="/" element={<PaginaLogin />}></Route>
                <Route path="selecao-de-cadastro" element={<PaginaEscolhaDeCadastro />}></Route>
                <Route path="selecao-de-cadastro/cadastro-psicologo" element={<PaginaCadastroPsicologo />}></Route>
                <Route path="minha-agenda" element={<PaginaMinhaAgenda />}></Route>
            </Routes>
        </BrowserRouter>
    );
}

export default AppRoutes;
