from flask import Blueprint, request, jsonify
from services.EstudanteService import EstudanteService
from services.ConsultaService import ConsultaService

# Blueprint configuration
estudante_bp = Blueprint('estudante_bp', __name__)
service_estudante = EstudanteService()
service_consulta = ConsultaService()

print("--- CONTROLLER ESTUDANTE CARREGADO (SILENT MODE) ---")

# AQUI ESTAVA O ERRO. AGORA ESTÁ CORRIGIDO PARA @estudante_bp
@estudante_bp.route('/listar_horarios_livres', methods=['POST'])
def listar_livres():
    data = request.get_json(silent=True) or {}
    print(f"DEBUG ALUNO (Listar): {data}")
    try:
        # Se não tiver filtros, lista tudo
        if not data.get('nome') and not data.get('email'):
            livres = service_consulta.listar_todos_livres()
            return jsonify(livres), 200
        
        livres = service_consulta.listar_livres_por_psi_nome(data.get('nome'), data.get('email'))
        if livres is None: return jsonify({"erro": "Psicologo não encontrado"}), 404
        return jsonify(livres)
    except Exception as e:
        print(f"ERRO ALUNO: {e}")
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/reservar_data_horario', methods=['POST'])
def reservar_horario():
    data = request.get_json(silent=True)
    
    print(f"DEBUG ALUNO (Reservar Payload Bruto): {data}")
    
    if data is None:
        print("ERRO: Payload vazio ou inválido recebido do frontend")
        return jsonify({'erro': 'JSON inválido ou vazio'}), 400

    try:
        res = service_consulta.reservar_por_estudante(data)
        
        if res == 404: return jsonify({'mensagem': 'Horário não encontrado'}), 404
        if res == 409: return jsonify({'mensagem': 'Horário já ocupado'}), 409
        
        return jsonify({'mensagem': 'Reservado', 'consulta': res}), 200
    except ValueError as e:
        print(f"ERRO DE VALIDAÇÃO: {e}")
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        print(f"ERRO GERAL SERVIDOR: {e}")
        return jsonify({'erro': str(e)}), 500

@estudante_bp.route('/listar_minhas_solicitacoes', methods=['POST'])
def listar_minhas_solicitacoes():
    data = request.get_json(silent=True) or {}
    try:
        res = service_consulta.listar_solicitacoes_estudante(data.get('id'))
        return jsonify(res), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/cancelar_reserva', methods=['POST'])
def cancelar_reserva():
    data = request.get_json(silent=True) or {}
    try:
        res = service_consulta.cancelar_reserva(data)
        return jsonify({'mensagem': 'Cancelado', 'consulta': res}), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400

# Rotas de cadastro
@estudante_bp.route('/cadastrar_estudante', methods=['POST'])
def cadastrar():
    try: return jsonify(service_estudante.cadastrar(request.get_json(silent=True))), 201
    except Exception as e: return jsonify({'erro': str(e)}), 400
@estudante_bp.route('/editar_estudante', methods=['POST'])
def editar():
    try: return jsonify(service_estudante.editar(request.get_json(silent=True))), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400
@estudante_bp.route('/excluir_estudante', methods=['POST'])
def excluir():
    try: return jsonify(service_estudante.excluir(request.get_json(silent=True))), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400
@estudante_bp.route('/pesquisar_por_nome', methods=['POST'])
def pesquisar(): return listar_livres()