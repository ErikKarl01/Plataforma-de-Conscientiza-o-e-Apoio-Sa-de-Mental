from flask import Blueprint, request, jsonify
from services.EstudanteService import EstudanteService
from services.ConsultaService import ConsultaService

estudante_bp = Blueprint('estudante_bp', __name__)

service_estudante = EstudanteService()
service_consulta = ConsultaService()

print("--- CONTROLLER ESTUDANTE CARREGADO ---")

@estudante_bp.route('/cadastrar_estudante', methods=['POST'])
def cadastrar():
    data = request.get_json()
    try:
        novo_aluno = service_estudante.cadastrar(data)
        return jsonify({'mensagem': 'Estudante cadastrado', 'id': novo_aluno['id']}), 201
    except ValueError as e: return jsonify({'erro': str(e)}), 400
    except Exception as e: return jsonify({'erro': 'Erro interno'}), 500

@estudante_bp.route('/listar_consultas_aluno', methods=['POST'])
def listar_consultas():
    data = request.get_json()
    id_aluno = data.get('idAluno')
    
    if not id_aluno:
        return jsonify({'erro': 'ID do aluno é obrigatório'}), 400

    try:
        consultas = service_consulta.listar_por_aluno(id_aluno)
        return jsonify(consultas), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@estudante_bp.route('/solicitar_agendamento', methods=['POST'])
def solicitar():
    data = request.get_json()
    try:
        service_consulta.solicitar_agendamento(data)
        return jsonify({'mensagem': 'Solicitação enviada'}), 200
    except ValueError as e: return jsonify({'erro': str(e)}), 400
    except Exception as e: return jsonify({'erro': str(e)}), 500

@estudante_bp.route('/listar_todos_horarios_livres', methods=['GET'])
def listar_todos_livres():
    try:
        todos = service_consulta.repo.get_all()
        # Filtra tudo que tem status 'livre'
        livres = [c for c in todos if c.get('status') == 'livre']
        
        # Opcional: Adicionar nome do psicólogo se não tiver no objeto consulta
        # (Isso exigiria buscar no service de psicólogo, mas vamos simplificar por enquanto)
        
        return jsonify(livres), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500