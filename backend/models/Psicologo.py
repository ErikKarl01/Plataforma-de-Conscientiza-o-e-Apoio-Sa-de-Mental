from flask import request, jsonify
import json
from functools import wraps
from datetime import datetime
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados
from .Validacao import (
    validar_nome, 
    validar_email_func, 
    validar_telefone, 
    validar_data_hora, 
    validar_id, 
    validar_duracao, 
    validar_causa
)

PSICOLOGO_DB = 'data/psicologos.json'
CONSULTAS_DB = 'data/consultas.json'
ESTUDANTE_DB = 'data/estudante.json'

def tratar_erros(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except ValueError as e:
            return jsonify({'erro': str(e)}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro interno: {str(e)}'}), 500
    return wrapper

def pesquisaPaciente(dadosEstudante, nome_buscado, telefone_formatado_buscado):
    nome_normalizado = nome_buscado.strip().lower()

    for indice, estudante in enumerate(dadosEstudante):
        estudante_nome_normalizado = estudante.get('nome', '').strip().lower()
        estudante_telefone = estudante.get('telefone', '') 

        if estudante_nome_normalizado == nome_normalizado and \
           estudante_telefone == telefone_formatado_buscado:
            return indice, estudante
    
    return (None, None)

def pesquisaDataHorario(dados, data, horarioDoFront, id_sessao=None):
    for indice, consulta in enumerate(dados):
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                if id_sessao is None:
                    return indice, consulta
                elif consulta.get('idPsicologo') == id_sessao:
                    return indice, consulta
    return (None, None) 

def horarioJaExiste(data, horario, idPsicologo):
    dados = carregar_dados(CONSULTAS_DB)
    _indice, consulta_encontrada = pesquisaDataHorario(dados, data, horario, idPsicologo)
    return consulta_encontrada is not None

def chaveDeOrdenacao(consulta):
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')

class Psicologo:

    # ----------------------------------------------------------------------
    # CADASTRAR PSICÓLOGO
    # ----------------------------------------------------------------------
    @staticmethod 
    @tratar_erros
    def cadastrarPsicologo():
        dados_do_front = request.get_json()
        
        nome = validar_nome(dados_do_front.get('nome'))
        email = validar_email_func(dados_do_front.get('email'))
        telefone = validar_telefone(dados_do_front.get('telefone'))
        
        crp = dados_do_front.get('crp')
        if not crp or not crp.strip():
            raise ValueError("O CRP não pode estar vazio")
        crp = crp.strip()
        
        senha = dados_do_front.get('senha')
        if not senha or not senha.strip():
            raise ValueError("A senha não pode estar vazia")
        senha_limpa = senha.strip()
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone, 'crp': crp}
        novo_usuario['senha'] = generate_password_hash(senha_limpa)
        
        dados = carregar_dados(PSICOLOGO_DB)
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id 
        dados.append(novo_usuario)
        
        with open(PSICOLOGO_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})

    # ----------------------------------------------------------------------
    # ADICIONAR HORÁRIO COM DURAÇÃO (SUA VERSÃO MANTIDA)
    # ----------------------------------------------------------------------
    @staticmethod
    def adicionarHorario():
        dados_do_front = request.get_json()
        
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')

        # NOVO: duração com fallback para 50 (Mantendo sua lógica)
        duracao = dados_do_front.get('duracao', '50')

        novaConsulta = {
            'nomePaciente': '',
            'telPaciente': '',
            'data': dataConsulta,
            'horario': horarioConsulta,
            'idPsicologo': idPsicologo,
            'reservado': False,
            'duracao': duracao     # <--- CAMPO IMPORTANTE MANTIDO
        }
        
        dados = carregar_dados(CONSULTAS_DB)
        
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})

    # ----------------------------------------------------------------------
    # MARCAR CONSULTA
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def marcarConsulta():
        dados_do_front = request.get_json()
        
        data, horarioDoFront = validar_data_hora(dados_do_front.get('data'), dados_do_front.get('horario'))
        nomePaciente_limpo = validar_nome(dados_do_front.get('nomePaciente'), "Nome do Paciente")
        
        telPaciente = dados_do_front.get('telPaciente')
        if not telPaciente:
            raise ValueError("O Telefone do Paciente não pode estar vazio")
        telefone_formatado = validar_telefone(telPaciente, "Telefone do Paciente")
        
        duracao = validar_duracao(dados_do_front.get('duracao'))
        causa = validar_causa(dados_do_front.get('causa'))
        
        emailPaciente = dados_do_front.get('emailPaciente')
        email_formatado = validar_email_func(emailPaciente, "Email do Paciente") if emailPaciente and emailPaciente.strip() else ''
        
        dados = carregar_dados(CONSULTAS_DB)
        dadosEst = carregar_dados(ESTUDANTE_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        _indexEst, estudante = pesquisaPaciente(dadosEst, nomePaciente_limpo, telefone_formatado)
        
        if not consulta:
            return jsonify({'mensagem': 'Data e horário não encontrados'}), 404

        id_estudante = ''
        reservado_por_estudante = False
        email_para_consulta = email_formatado

        if estudante:
            id_estudante = estudante.get('id')
            reservado_por_estudante = True
            email_para_consulta = estudante.get('email', email_formatado)

        consulta['nomePaciente'] = nomePaciente_limpo
        consulta['telPaciente'] = telefone_formatado
        consulta['emailPaciente'] = email_para_consulta 
        consulta['reservado'] = True
        consulta['reservadoPorEstudante'] = reservado_por_estudante 
        consulta['idEstudante'] = id_estudante
        
        if duracao is not None:
            consulta['duracao'] = duracao
        if causa is not None:
            consulta['causa'] = causa
        
        dados[indice] = consulta
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 

    # ----------------------------------------------------------------------
    # EDITAR HORÁRIO
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def editarHorario():
        dados_do_front = request.get_json()
        
        id_sessao = validar_id(dados_do_front.get('id'))
        
        data, horarioDoFront = validar_data_hora(dados_do_front.get('data'), dados_do_front.get('horario'))
        
        dataModificada, horarioModificado = validar_data_hora(dados_do_front.get('dataModificada'), dados_do_front.get('horarioModificado'))
        
        duracao = validar_duracao(dados_do_front.get('duracao'))
        causa = validar_causa(dados_do_front.get('causa'))
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if not consulta:
            return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
        
        consulta['horario'] = horarioModificado
        consulta['data'] = dataModificada
        
        if duracao is not None:
            consulta['duracao'] = duracao
        if causa is not None:
            consulta['causa'] = causa

        dados[indice] = consulta
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        return jsonify({'mensagem': 'Horário modificado com sucesso', 'consulta': consulta}) 

    # ----------------------------------------------------------------------
    # EXCLUIR HORÁRIO
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def excluirHorario():
        dados_do_front = request.get_json()
        
        id_sessao = validar_id(dados_do_front.get('id'))
        data, horarioDoFront = validar_data_hora(dados_do_front.get('data'), dados_do_front.get('horario'))
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluído com sucesso', 'consulta': consulta}) 
            
        return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
    
    # ----------------------------------------------------------------------
    # ALTERAR RESERVA
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def editarReserva():
        dados_do_front = request.get_json()
        
        id_sessao = validar_id(dados_do_front.get('id'))
        data, horarioDoFront = validar_data_hora(dados_do_front.get('data'), dados_do_front.get('horario'))
        duracao = validar_duracao(dados_do_front.get('duracao'))
        causa = validar_causa(dados_do_front.get('causa'))
        
        reserva = dados_do_front.get('reserva')
        if reserva is None:
            raise ValueError("O campo 'reserva' não foi fornecido")
        if not isinstance(reserva, bool):
            raise ValueError("O campo 'reserva' deve ser booleano")
            
        dados = carregar_dados(CONSULTAS_DB) 
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if not consulta:
             return jsonify({'mensagem': 'Data e horário não encontrados'}), 404
             
        dados[indice]['reservado'] = reserva
        
        if duracao is not None:
            dados[indice]['duracao'] = duracao
        
        if reserva:
            if causa is not None:
                dados[indice]['causa'] = causa
        else:
            dados[indice]['nomePaciente'] = ''
            dados[indice]['telPaciente'] = ''
            dados[indice]['emailPaciente'] = '' 
            dados[indice]['reservadoPorEstudante'] = False
            dados[indice]['idEstudante'] = ''
            dados[indice]['causa'] = ''
                
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
            
    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                try:
                    validar_data_hora(consulta.get('data'), consulta.get('horario'))
                    dados_filtrados.append(consulta)
                except (ValueError, TypeError, KeyError):
                    pass
                
        return sorted(dados_filtrados, key=chaveDeOrdenacao)

    # ----------------------------------------------------------------------
    # LISTAR CONSULTAS RESERVADAS
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def listarConsultas():
        dados_do_front = request.get_json()
        
        id_psicologo = validar_id(dados_do_front.get('idPsicologo'))

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosReservados = [horario for horario in todosOsHorarios if horario.get('reservado')]
            
        return jsonify(horariosReservados)
    
    # ----------------------------------------------------------------------
    # LISTAR HORÁRIOS LIVRES
    # ----------------------------------------------------------------------
    @staticmethod
    @tratar_erros
    def listarHorariosLivresPsi():
        dados_do_front = request.get_json()
        
        id_psicologo = validar_id(dados_do_front.get('idPsicologo'))

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosLivres = [horario for horario in todosOsHorarios if not horario.get('reservado')]
            
        return jsonify(horariosLivres)
    
    @staticmethod
    @tratar_erros
    def listarSolicitacoesAtendimento():
        """método deve pegar dados do front e listar as data horários que tem o 
        id do psicólogo e ao mesmo tempo tem o campo 'reservadoPorEstudante' true
        """
        dados_do_front = request.get_json()
        idSessao = validar_id(dados_do_front.get('idPsicologo'))
        if idSessao is None:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo da requisição'}), 404
        
        dadosConsultas = carregar_dados(CONSULTAS_DB)
        
        listaSolicitacoes = [dado for dado in dadosConsultas if dado['idPsicologo'] == idSessao and dado.get('reservadoPorEstudante')]
        
        if not listaSolicitacoes:
            return jsonify({'mensagem': 'Nenhuma solicitação encontrada'}), 404
        
        return jsonify(listaSolicitacoes)