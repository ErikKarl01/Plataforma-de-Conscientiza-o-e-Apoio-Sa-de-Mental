from flask import Blueprint, request, jsonify
from backend.services.PsicologoService import PsicologoService
from backend.services.ConsultaService import ConsultaService
from backend.repositories.ConsultaRepository import ConsultaRepository
from backend.utils.Validacao import validar_id, validar_data_hora, validar_duracao, validar_causa

# Define o grupo de rotas de Psicólogo
psicologo_bp = Blueprint('psicologo_bp', __name__)

service_psi = PsicologoService()
service_consulta = ConsultaService()
repo_consulta = ConsultaRepository()

@psicologo_bp.route('/cadastrar', methods=['POST'])
def cadastrar():
    try:
        d = request.get_json()
        usuario = service_psi.cadastrar(d)
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': usuario}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/adicionar_horario', methods=['POST'])
def adicionar_horario():
    try:
        d = request.get_json()
        consulta = service_consulta.adicionar_horario(d)
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': consulta})
    except ValueError as e:
        status = 409 if str(e) == 'Data/horário já cadastrados' else 400
        return jsonify({'mensagem': str(e)}), status

@psicologo_bp.route('/marcar_consulta', methods=['POST'])
def marcar_consulta():
    try:
        d = request.get_json()
        consulta = service_consulta.marcar_consulta_psi(d)
        if not consulta:
             return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
        return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/modificar_consulta', methods=['POST'])
def editar_horario():
    try:
        d = request.get_json()
        id_sessao = validar_id(d.get('id'))
        data, horario = validar_data_hora(d.get('data'), d.get('horario'))
        dataMod, horarioMod = validar_data_hora(d.get('dataModificada'), d.get('horarioModificado'))
        duracao = validar_duracao(d.get('duracao'))
        causa = validar_causa(d.get('causa'))

        idx, consulta = repo_consulta.find_by_data_horario_psi(data, horario, id_sessao)
        if not consulta:
            return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
        
        consulta.update({'horario': horarioMod, 'data': dataMod})
        if duracao: consulta['duracao'] = duracao
        if causa: consulta['causa'] = causa
        
        repo_consulta.update(idx, consulta)
        return jsonify({'mensagem': 'Horário modificado com sucesso', 'consulta': consulta})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/remover_consulta', methods=['POST'])
def excluir_horario():
    try:
        d = request.get_json()
        id_sessao = validar_id(d.get('id'))
        data, horario = validar_data_hora(d.get('data'), d.get('horario'))
        
        idx, consulta = repo_consulta.find_by_data_horario_psi(data, horario, id_sessao)
        if consulta:
            repo_consulta.delete(idx)
            return jsonify({'mensagem': 'Horário excluído com sucesso', 'consulta': consulta})
        
        return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/editar_reserva', methods=['POST'])
def editar_reserva():
    try:
        d = request.get_json()
        id_sessao = validar_id(d.get('id'))
        data, horario = validar_data_hora(d.get('data'), d.get('horario'))
        reserva = d.get('reserva')
        duracao = validar_duracao(d.get('duracao'))
        causa = validar_causa(d.get('causa'))

        if not isinstance(reserva, bool): raise ValueError("Reserva deve ser booleano")

        idx, consulta = repo_consulta.find_by_data_horario_psi(data, horario, id_sessao)
        if not consulta:
            return jsonify({'mensagem': 'Data e horário não encontrados'}), 404

        consulta['reservado'] = reserva
        if duracao: consulta['duracao'] = duracao
        
        if reserva:
             if causa: consulta['causa'] = causa
        else:
             consulta.update({'nomePaciente':'', 'telPaciente':'', 'emailPaciente':'', 
                              'reservadoPorEstudante':False, 'idEstudante':'', 'causa':''})
        
        repo_consulta.update(idx, consulta)
        return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/listar_consultas', methods=['POST'])
def listar_consultas():
    try:
        d = request.get_json()
        id_psi = validar_id(d.get('idPsicologo'))
        consultas = repo_consulta.find_by_psicologo(id_psi)
        reservados = [c for c in consultas if c.get('reservado')]
        return jsonify(reservados)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/listar_horarios_livres_psi', methods=['POST'])
def listar_livres_psi():
    try:
        d = request.get_json()
        id_psi = validar_id(d.get('idPsicologo'))
        consultas = repo_consulta.find_by_psicologo(id_psi)
        livres = [c for c in consultas if not c.get('reservado')]
        return jsonify(livres)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@psicologo_bp.route('/listar_solicitacoes_atendimento', methods=['POST'])
def listar_solicitacoes():
    try:
        d = request.get_json()
        id_sessao = validar_id(d.get('idPsicologo'))
        consultas = repo_consulta.find_by_psicologo(id_sessao)
        solicitacoes = [c for c in consultas if c.get('reservadoPorEstudante')]
        
        if not solicitacoes:
            return jsonify({'mensagem': 'Nenhuma solicitação encontrada'}), 404
        return jsonify(solicitacoes)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400