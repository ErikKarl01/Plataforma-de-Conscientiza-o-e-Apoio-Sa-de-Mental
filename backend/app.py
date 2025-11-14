from flask import Flask
import os

# 1. Importa as CLASSES dos seus arquivos de models
from models.Psicologo import Psicologo
from models.Estudante import Estudante
from models.Login import Login

# --- Configuração Central ---
app = Flask(__name__)

# 2. Garante que TODOS os diretórios de dados existam
# (Você não precisa das variáveis DB aqui, só do path)
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

if __name__ == '__main__':
    app.run(debug=True)