from flask import Blueprint, request, jsonify
from services.EstudanteService import EstudanteService
from services.PsicologoService import PsicologoService

login_bp = Blueprint('login_bp', __name__)

service_estudante = EstudanteService()
service_psicologo = PsicologoService()

@login_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    senha = data.get('senha')

    if not email or not senha:
        return jsonify({'erro': 'Email e senha são obrigatórios'}), 400

    # 1. Tenta achar nos Estudantes
    todos_alunos = service_estudante.repo.get_all()
    for aluno in todos_alunos:
        if aluno.get('email') == email and aluno.get('senha') == senha:
            # Remove a senha antes de enviar pro frontend por segurança
            aluno_safe = aluno.copy()
            aluno_safe.pop('senha', None)
            return jsonify({
                'mensagem': 'Login realizado com sucesso',
                'tipo': 'estudante',
                'usuario': aluno_safe
            }), 200

    # 2. Tenta achar nos Psicólogos
    todos_psis = service_psicologo.repo.get_all()
    for psi in todos_psis:
        if psi.get('email') == email and psi.get('senha') == senha:
            psi_safe = psi.copy()
            psi_safe.pop('senha', None)
            return jsonify({
                'mensagem': 'Login realizado com sucesso',
                'tipo': 'psicologo',
                'usuario': psi_safe
            }), 200

    # 3. Se não achou em nenhum
    return jsonify({'erro': 'Email ou senha incorretos'}), 401