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
        if estudante_nome_normalizado == nome_normalizado and estudante_telefone == telefone_formatado_buscado:
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

    @staticmethod 
    @tratar_erros
    def cadastrarPsicologo():
        dados_do_front = request.get_json()
        nome = validar_nome(dados_do_front.get('nome'))
        email = validar_email_func(dados_do_front.get('email'))
        telefone = validar_telefone(dados_do_front.get('telefone'))
        crp = dados_do_front.get('crp')
        if not crp or not crp.strip(): raise ValueError("O CRP não pode estar vazio")
        crp = crp.strip()
        senha = dados_do_front.get('senha')
        if not senha or not senha.strip(): raise ValueError("A senha não pode estar vazia")
        senha_limpa = senha.strip()
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone, 'crp': crp}
        novo_usuario['senha'] = generate_password_hash(senha_limpa)
        
        dados = carregar_dados(PSICOLOGO_DB)
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id 
        dados.append(novo_usuario)
        
        with open(PSICOLOGO_DB, 'w') as f: json.dump(dados, f)
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})

    @staticmethod
    def adicionarHorario():
        dados_do_front = request.get_json()
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        duracao = dados_do_front.get('duracao', '50')

        novaConsulta = {
            'nomePaciente': '',
            'telPaciente': '',
            'data': dataConsulta,
            'horario': horarioConsulta,
            'idPsicologo': idPsicologo,
            'reservado': False,
            'duracao': duracao,
            'status': 'livre'  
        }
        
        dados = carregar_dados(CONSULTAS_DB)
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f: json.dump(dados, f)
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})

    @staticmethod
    @tratar_erros
    def marcarConsulta():
        dados_do_front = request.get_json()
        data, horarioDoFront = validar_data_hora(dados_do_front.get('data'), dados_do_front.get('horario'))
        nomePaciente_limpo = validar_nome(dados_do_front.get('nomePaciente'), "Nome do Paciente")
        telPaciente = dados_do_front.get('telPaciente')
        if not telPaciente: raise ValueError("O Telefone do Paciente não pode estar vazio")
        telefone_formatado = validar_telefone(telPaciente, "Telefone do Paciente")
        duracao = validar_duracao(dados_do_front.get('duracao'))
        causa = validar_causa(dados_do_front.get('causa'))
        emailPaciente = dados_do_front.get('emailPaciente')
        email_formatado = validar_email_func(emailPaciente, "Email do Paciente") if emailPaciente and emailPaciente.strip() else ''
        
        dados = carregar_dados(CONSULTAS_DB)
        dadosEst = carregar_dados(ESTUDANTE_DB)
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        _indexEst, estudante = pesquisaPaciente(dadosEst, nomePaciente_limpo, telefone_formatado)
        
        if not consulta: return jsonify({'mensagem': 'Data e horário não encontrados'}), 404

        id_estudante = ''
        reservado_por_estudante = False
        email_para_consulta = email_formatado
        if estudante:
            id_estudante = estudante.get('id')
            reservado_por_estudante = True
            email_para_consulta = estudante.get('email', email_formatado)

        consulta.update({
            'nomePaciente': nomePaciente_limpo,
            'telPaciente': telefone_formatado,
            'emailPaciente': email_para_consulta,
            'reservado': True,
            'reservadoPorEstudante': reservado_por_estudante,
            'idEstudante': id_estudante,
            'status': 'confirmada' 
        })
        if duracao: consulta['duracao'] = duracao
        if causa: consulta['causa'] = causa
        
        dados[indice] = consulta
        with open(CONSULTAS_DB, 'w') as f: json.dump(dados, f)
        return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta})

    @staticmethod
    @tratar_erros
    def editarHorario():
        # Implementação existente original
        return Psicologo._editarHorarioOriginal()

    @staticmethod
    @tratar_erros
    def excluirHorario():
        return Psicologo._excluirHorarioOriginal()

    @staticmethod
    @tratar_erros
    def editarReserva():
        return Psicologo._editarReservaOriginal()

    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                try:
                    validar_data_hora(consulta.get('data'), consulta.get('horario'))
                    dados_filtrados.append(consulta)
                except: pass
        return sorted(dados_filtrados, key=chaveDeOrdenacao)

    @staticmethod
    @tratar_erros
    def listarConsultas():
        dados_do_front = request.get_json()
        id_psicologo = validar_id(dados_do_front.get('idPsicologo'))
        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        horariosReservados = [h for h in todosOsHorarios if h.get('reservado')]
        return jsonify(horariosReservados)
    
    @staticmethod
    @tratar_erros
    def listarHorariosLivresPsi():
        dados_do_front = request.get_json()
        id_psicologo = validar_id(dados_do_front.get('idPsicologo'))
        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        horariosLivres = [h for h in todosOsHorarios if not h.get('reservado')]
        return jsonify(horariosLivres)
    
    @staticmethod
    @tratar_erros
    def listarSolicitacoesAtendimento():
        dados_do_front = request.get_json()
        idSessao = validar_id(dados_do_front.get('idPsicologo'))
        if idSessao is None: return jsonify({'mensagem': 'Id da sessão não informado'}), 404
        
        dadosConsultas = carregar_dados(CONSULTAS_DB)
        listaSolicitacoes = [
            dado for dado in dadosConsultas 
            if dado['idPsicologo'] == idSessao 
            and dado.get('reservadoPorEstudante')
            and (dado.get('status') == 'pendente' or 'status' not in dado)
        ]

        if not listaSolicitacoes:
            return jsonify({'mensagem': 'Nenhuma solicitação encontrada'}), 404
        
        return jsonify(listaSolicitacoes)

    @staticmethod
    @tratar_erros
    def atualizarStatusConsulta():
        dados_do_front = request.get_json()
        id_consulta = dados_do_front.get('idConsulta') or dados_do_front.get('id')
        try:
            id_consulta = int(id_consulta)
        except:
            return jsonify({'mensagem': 'ID da consulta inválido'}), 400

        novo_status = dados_do_front.get('status')
        if novo_status not in ['confirmada', 'rejeitada']:
            return jsonify({'mensagem': 'Status inválido'}), 400

        dados = carregar_dados(CONSULTAS_DB)
        consulta_encontrada = None
        indice_encontrado = -1

        for i, c in enumerate(dados):
            if c.get('id') == id_consulta:
                consulta_encontrada = c
                indice_encontrado = i
                break
        
        if not consulta_encontrada:
            return jsonify({'mensagem': 'Consulta não encontrada'}), 404

        consulta_encontrada['status'] = novo_status
        dados[indice_encontrado] = consulta_encontrada
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Status atualizado com sucesso', 'consulta': consulta_encontrada})

    # Métodos placeholders para manter compatibilidade com código anterior
    def _editarHorarioOriginal(): pass 
    def _excluirHorarioOriginal(): pass
    def _editarReservaOriginal(): pass
