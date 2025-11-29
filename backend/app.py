from flask import Flask
import os

# 1. Importa as CLASSES dos seus arquivos de models
from models.Psicologo import Psicologo
from models.Estudante import Estudante
from models.Login import Login

# --- Configuração Central ---
app = Flask(__name__)

# 2. Garante que TODOS os diretórios de dados existam
os.makedirs('backend/data', exist_ok=True)

# --- Rotas de Login ---
@app.route('/login', methods=['POST'])
def fazer_login():
    return Login.fazerLogin()

# --- Rotas de Estudante ---
@app.route('/cadastrar_estudante', methods=['POST'])
def cadastrar_estudante():
    return Estudante.cadastrar()

@app.route('/editar_estudante', methods=['POST'])
def editar_estudante():
    return Estudante.editarEstudante()
        
@app.route('/excluir_estudante', methods=['POST'])
def excluir_estudante():
    return Estudante.excluirEstudante()

@app.route('/pesquisar_por_nome', methods=['POST'])
def pesquisa_horarioData_por_nome_do_psi():
    return Estudante.pesquisarPorNome()

@app.route('/pesquisar_por_data', methods=['POST'])
def pesquisa_horarioData_por_data():
    return Estudante.pesquisarPorData()

@app.route('/pesquisar_por_horario', methods=['POST'])
def pesquisa_horarioData_por_horario():
    return Estudante.pesquisarPorHorario()

@app.route('/reservar_data_horario', methods=['POST'])
def reservar_horarioData_por():
    return Estudante.reservarDataHorario()

@app.route('/cancelar_reserva', methods=['POST'])
def cancelar_reserva():
    return Estudante.cancelarReserva()

@app.route('/listar_horarios_livres', methods=['POST'])
def listar_horarios_livres():
    return Estudante.listarHorariosLivres()

@app.route('/listar_minhas_solicitacoes', methods=['POST'])
def listar_minhas_solicitacoes():
    return Estudante.listarMinhasSolicitacoes()

# --- Rotas de Psicólogo ---
@app.route('/cadastrar', methods=['POST'])
def cadastrar_psicologo():
    return Psicologo.cadastrarPsicologo()

@app.route('/adicionarHorario', methods=['POST'])
def adicionar_horario(): 
    return Psicologo.adicionarHorario()

@app.route('/marcarConsulta', methods=['POST'])
def marcar_consulta(): 
    return Psicologo.marcarConsulta()

@app.route('/modificarConsulta', methods=['POST'])
def editar_horario():
    return Psicologo.editarHorario()

@app.route('/removerConsulta', methods=['POST'])
def excluir_horario():
    return Psicologo.excluirHorario()

@app.route('/editarReserva', methods=['POST'])
def editar_reserva():
    return Psicologo.editarReserva()

@app.route('/listarConsultas', methods=['POST'])
def listar_consultas():
    return Psicologo.listarConsultas()

@app.route('/listarHorariosLivres', methods=['POST'])
def listar_horarios_livres():
    return Psicologo.listarHorariosLivres()

@app.route('/listar_solicitacoes_atendimento', methods=['POST'])
def listar_solicitacoes_atendimento():
    return Psicologo.listarSolicitacoesAtendimento()

if __name__ == '__main__':
    app.run(debug=True)