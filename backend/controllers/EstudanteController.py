from flask import Blueprint, request, jsonify
from services.EstudanteService import EstudanteService
from services.ConsultaService import ConsultaService
from utils.Validacao import validar_data_hora

estudante_bp = Blueprint('estudante_bp', __name__)

service_estudante = EstudanteService()
service_consulta = ConsultaService()

@estudante_bp.route('/cadastrar_estudante', methods=['POST'])
def cadastrar():
    try:
        d = request.get_json()
        resultado = service_estudante.cadastrar(d)
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': resultado}), 201
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/editar_estudante', methods=['POST'])
def editar():
    try:
        d = request.get_json()
        resultado = service_estudante.editar(d)
        if not resultado:
            return jsonify({'erro': 'Estudante não encontrado'}), 404
        return jsonify({'mensagem': 'Estudante modificado', 'estudante': resultado})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/excluir_estudante', methods=['POST'])
def excluir():
    try:
        d = request.get_json()
        resultado = service_estudante.excluir(d)
        if not resultado:
            return jsonify({'erro': 'Estudante não encontrado'}), 404
        return jsonify({'mensagem': 'Estudante excluído', 'estudante': resultado})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/pesquisar_por_nome', methods=['POST'])
def pesquisar_por_nome():
    try:
        d = request.get_json()
        livres = service_consulta.listar_livres_por_psi_nome(d.get('nome'), d.get('email'))
        if livres is None:
            return jsonify({'mensagem': 'Psicólogo não encontrado'}), 404
        return jsonify(livres)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/pesquisar_por_data', methods=['POST'])
def pesquisar_por_data():
    try:
        d = request.get_json() or {}
        dataValida, _ = validar_data_hora(d.get('data'), '00:00')
        resultado = service_consulta.buscar_generico('data', dataValida)
        return jsonify(resultado)
    except ValueError:
        return jsonify({'erro': 'Data inválida'}), 400

@estudante_bp.route('/pesquisar_por_horario', methods=['POST'])
def pesquisar_por_horario():
    try:
        d = request.get_json() or {}
        validar_data_hora('01/01/2000', d.get('horario'))
        resultado = service_consulta.buscar_generico('horario', d.get('horario'))
        return jsonify(resultado)
    except ValueError:
        return jsonify({'erro': 'Horário inválido'}), 400

@estudante_bp.route('/reservar_data_horario', methods=['POST'])
def reservar_horario():
    try:
        d = request.get_json()
        res = service_consulta.reservar_por_estudante(d)
        if res == 404: return jsonify({'mensagem': 'Data/Horário não encontrados'}), 404
        if res == 409: return jsonify({'mensagem': 'Este horário já está reservado'}), 409
        return jsonify({'mensagem': 'Reservado com sucesso', 'consulta': res})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/cancelar_reserva', methods=['POST'])
def cancelar_reserva():
    try:
        d = request.get_json()
        # Chama a função que cancela e salva no histórico (com regra de 5 dias)
        res = service_consulta.cancelar_reserva(d)
        if res == 404: return jsonify({'mensagem': 'Agendamento não encontrado'}), 404
        if res == 409: return jsonify({'mensagem': 'Horário não está reservado'}), 409
        return jsonify({'mensagem': 'Cancelado com sucesso', 'consulta': res})
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/listar_horarios_livres', methods=['POST'])
def listar_livres():
    try:
        d = request.get_json()
        livres = service_consulta.listar_livres_por_psi_nome(d.get('nome'), d.get('email'))
        if livres is None:
            return jsonify({"erro": "Psicologo não encontrado"}), 404
        return jsonify(livres)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400

@estudante_bp.route('/listar_minhas_solicitacoes', methods=['POST'])
def listar_solicitacoes():
    try:
        d = request.get_json()
        if not d or 'id' not in d: raise ValueError('Id do estudante não fornecido')
        resultado = service_consulta.listar_solicitacoes_estudante(d.get('id'))
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    
@estudante_bp.route('/listar_historico_estudante', methods=['POST'])
def listar_historico():
    try:
        d = request.get_json()
        if not d or 'id' not in d:
            raise ValueError('Id do estudante não fornecido')
            
        resultado = service_consulta.consultar_historico_estudante(d.get('id'))
        return jsonify(resultado)
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno'}), 500