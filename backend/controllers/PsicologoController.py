from flask import Blueprint, request, jsonify
from services.PsicologoService import PsicologoService
from services.ConsultaService import ConsultaService

psicologo_bp = Blueprint('psicologo_bp', __name__)
service_psi = PsicologoService()
service_consulta = ConsultaService()

print("--- CONTROLLER PSICOLOGO CARREGADO ---")

@psicologo_bp.route('/cadastrar_psicologo', methods=['POST'])
def cadastrar():
    data = request.get_json()
    try:
        novo_psi = service_psi.cadastrar(data)
        return jsonify({'mensagem': 'Psicólogo cadastrado com sucesso', 'id': novo_psi['id']}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno ao cadastrar'}), 500

@psicologo_bp.route('/listar_horarios_livres_psi', methods=['POST'])
def listar_horarios():
    data = request.get_json(silent=True) or {}
    try:
        # Pega horários livres deste psicólogo específico
        id_psi = data.get('idPsicologo')
        todos = service_consulta.repo.get_all()
        # Filtra apenas os meus horários que estão livres
        meus_livres = [c for c in todos if str(c.get('idPsicologo')) == str(id_psi) and c.get('status') == 'livre']
        return jsonify(meus_livres), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/listar_consultas', methods=['POST'])
def listar_consultas():
    # Lista consultas agendadas (confirmadas) para este psicólogo
    data = request.get_json(silent=True) or {}
    try:
        id_psi = data.get('idPsicologo')
        todos = service_consulta.repo.get_all()
        # Filtra confirmadas
        minhas = [c for c in todos if str(c.get('idPsicologo')) == str(id_psi) and c.get('status') == 'confirmado']
        return jsonify(minhas), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/listar_solicitacoes_atendimento', methods=['POST'])
def listar_solicitacoes():
    # Lista pendentes
    data = request.get_json(silent=True) or {}
    try:
        id_psi = data.get('idPsicologo')
        todos = service_consulta.repo.get_all()
        pendentes = [c for c in todos if str(c.get('idPsicologo')) == str(id_psi) and c.get('status') == 'pendente']
        return jsonify(pendentes), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/adicionar_horario', methods=['POST'])
def adicionar_horario():
    data = request.get_json()
    try:
        service_consulta.adicionar_horario(data)
        return jsonify({'mensagem': 'Horário criado'}), 201
    except Exception as e: return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/marcar_consulta', methods=['POST'])
def marcar_consulta():
    data = request.get_json()
    try:
        service_consulta.marcar_consulta_psi(data)
        return jsonify({'mensagem': 'Consulta marcada manual'}), 201
    except Exception as e: return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/confirmar_agendamento', methods=['POST'])
def confirmar_agendamento():
    data = request.get_json()
    res = service_consulta.confirmar_agendamento(data)
    if res == 404: return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'mensagem': 'Confirmado'}), 200

@psicologo_bp.route('/cancelar_reserva', methods=['POST'])
def cancelar_reserva():
    data = request.get_json()
    # Se vier do botão de lixeira (remover fisicamente)
    if data.get('acao') == 'remover_fisicamente':
        service_consulta.remover_fisicamente(data)
        return jsonify({'mensagem': 'Removido'}), 200
    
    # Se for apenas recusar/cancelar (liberar horário)
    res = service_consulta.cancelar_reserva(data)
    if res == 404: return jsonify({'erro': 'Não encontrado'}), 404
    return jsonify({'mensagem': 'Cancelado'}), 200

@psicologo_bp.route('/remover_consulta', methods=['POST'])
def remover_consulta():
    data = request.get_json(silent=True) or {}
    try:
        service_consulta.remover_fisicamente(data)
        return jsonify({'mensagem': 'Removido'}), 200
    except Exception as e: return jsonify({'erro': str(e)}), 400