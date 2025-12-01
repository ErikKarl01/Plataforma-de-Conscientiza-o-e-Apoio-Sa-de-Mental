from flask import request, jsonify
import json
from functools import wraps
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados
from .Psicologo import Psicologo, CONSULTAS_DB, pesquisaDataHorario, chaveDeOrdenacao
from .Validacao import (
    validar_nome, 
    validar_email_func, 
    validar_telefone, 
    validar_data_hora, 
    validar_id,
    validar_causa
)

# Caminhos ajustados para o seu ambiente local (data/...)
ESTUDANTE_DB = 'data/estudante.json'
PSICOLOGO_DB = 'data/psicologos.json'

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

def pesquisarPsicologoPorNomeEmail(dadosBanco, nome, email):
    nome_norm = nome.strip().lower()
    email_norm = email.strip().lower()
    for dado in dadosBanco:
        if dado['nome'].strip().lower() == nome_norm and \
           dado['email'].strip().lower() == email_norm:
            return dado
    return None

def pesquisaEstudante(dados, id):
    for index, estudante in enumerate(dados):
        if estudante.get('id') == id:
            return index, estudante
    return (None, None)

def pesquisaDataHorarioPorData(dados, data):
    return [u for u in dados if u.get('data') == data]

def pesquisaDataHorarioPorHorario(dados, horario):
    return [u for u in dados if u.get('horario') == horario]

class Estudante:
    @staticmethod
    @tratar_erros
    def cadastrar():
        d = request.get_json()
        
        nome = validar_nome(d.get('nome'))
        email = validar_email_func(d.get('email'))
        telefone = validar_telefone(d.get('telefone'))
        senha = d.get('senha')
        
        if not senha or not senha.strip():
            raise ValueError("A senha não pode estar vazia")
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone}
        novo_usuario['senha'] = generate_password_hash(senha.strip())
        
        dados = carregar_dados(ESTUDANTE_DB)
        novo_usuario['id'] = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        dados.append(novo_usuario)
        
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})

    @staticmethod
    @tratar_erros
    def editarEstudante():
        d = request.get_json()
        
        if not d or 'id' not in d:
            raise ValueError('Id não fornecido no corpo')
            
        id_est = validar_id(d['id'])
        nome = validar_nome(d.get('nome'))
        email = validar_email_func(d.get('email'))
        telefone = validar_telefone(d.get('telefone'))
        
        dados = carregar_dados(ESTUDANTE_DB)
        index, estudante = pesquisaEstudante(dados, id_est)
        
        if not estudante:
            return jsonify({'erro': 'Estudante não encontrado'}), 404
        
        estudante.update({'nome': nome, 'email': email, 'telefone': telefone})
        dados[index] = estudante
        
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Estudante modificado', 'estudante': estudante})

    @staticmethod
    @tratar_erros
    def excluirEstudante():
        d = request.get_json()
        if not d or 'id' not in d:
            raise ValueError('Id não fornecido no corpo')
            
        id_est = validar_id(d['id'])
        dados = carregar_dados(ESTUDANTE_DB)
        index, estudante = pesquisaEstudante(dados, id_est)
        
        if not estudante:
            return jsonify({'erro': 'Estudante não encontrado'}), 404
        
        dados.pop(index)
        
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Estudante excluído', 'estudante': estudante})

    @staticmethod
    @tratar_erros
    def pesquisarPorNome():
        d = request.get_json()
        nome = validar_nome(d.get('nome'))
        email = validar_email_func(d.get('email'))
        
        dados_psi = carregar_dados(PSICOLOGO_DB)
        psicologo = pesquisarPsicologoPorNomeEmail(dados_psi, nome, email)
        
        if not psicologo:
            return jsonify({'mensagem': 'Psicólogo não encontrado'}), 404
            
        todos = Psicologo.get_consultas_do_psicologo(psicologo['id'])
        livres = [h for h in todos if not h.get('reservado')]
        
        return jsonify(livres)

    @staticmethod
    @tratar_erros
    def reservarDataHorario():
        d = request.get_json()
        
        nomePaci = validar_nome(d.get('nomePaci'), "Nome do Paciente")
        emailPaci = validar_email_func(d.get('emailPaci'), "Email do Paciente")
        telPaci = validar_telefone(d.get('telefonePaci'), "Telefone do Paciente")
        
        nomePsi = validar_nome(d.get('nome'), "Nome do Psicólogo")
        emailPsi = validar_email_func(d.get('email'), "Email do Psicólogo")
        
        data, horario = validar_data_hora(d.get('data'), d.get('horario'))
        causa = validar_causa(d.get('causa'))
        
        dados = carregar_dados(CONSULTAS_DB)
        dados_psi = carregar_dados(PSICOLOGO_DB)
        
        psicologo = pesquisarPsicologoPorNomeEmail(dados_psi, nomePsi, emailPsi)
        if not psicologo:
             return jsonify({'mensagem': 'Psicólogo não encontrado'}), 404
             
        index, consulta = pesquisaDataHorario(dados, data, horario, psicologo['id'])
        
        if not consulta:
            return jsonify({'mensagem': 'Data/Horário não encontrados'}), 404
        
        if consulta.get('reservado'):
            return jsonify({'mensagem': 'Este horário já está reservado'}), 409
        
        consulta.update({
            'nomePaciente': nomePaci,
            'telPaciente': telPaci,
            'emailPaciente': emailPaci,
            'reservado': True,
            'reservadoPorEstudante': True,
            'causa': causa
        })
        dados[index] = consulta
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        
        return jsonify({'mensagem': 'Reservado com sucesso', 'consulta': consulta})

    @staticmethod
    @tratar_erros
    def cancelarReserva():
        d = request.get_json()
        
        nomePsi = validar_nome(d.get('nome'), "Nome do Psicólogo")
        emailPsi = validar_email_func(d.get('email'), "Email do Psicólogo")
        data, horario = validar_data_hora(d.get('data'), d.get('horario'))
        
        dados = carregar_dados(CONSULTAS_DB)
        dados_psi = carregar_dados(PSICOLOGO_DB)
        
        psicologo = pesquisarPsicologoPorNomeEmail(dados_psi, nomePsi, emailPsi)
        if not psicologo:
             return jsonify({'mensagem': 'Psicólogo não encontrado'}), 404
             
        index, consulta = pesquisaDataHorario(dados, data, horario, psicologo['id'])
        
        if not consulta:
            return jsonify({'mensagem': 'Agendamento não encontrado'}), 404
        
        if not consulta.get('reservado'):
             return jsonify({'mensagem': 'Horário não está reservado'}), 409
        
        consulta.update({
            'nomePaciente': '', 'telPaciente': '', 'emailPaciente': '',
            'reservado': False, 'reservadoPorEstudante': False, 'idEstudante': '', 'causa': ''
        })
        dados[index] = consulta
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        
        return jsonify({'mensagem': 'Cancelado com sucesso', 'consulta': consulta})

    @staticmethod
    def pesquisarPorData():
        d = request.get_json() or {}
        try:
            dataValida, hora = validar_data_hora(d.get('data'), '00:00') 
        except ValueError:
            return jsonify({'erro': 'Data inválida'}), 400
            
        return Estudante._pesquisar_generico(pesquisaDataHorarioPorData, dataValida)

    @staticmethod
    def pesquisarPorHorario():
        d = request.get_json() or {}
        try:
            validar_data_hora('01/01/2000', d.get('horario'))
        except ValueError:
            return jsonify({'erro': 'Horário inválido'}), 400
            
        return Estudante._pesquisar_generico(pesquisaDataHorarioPorHorario, d.get('horario'))

    @staticmethod
    def _pesquisar_generico(funcao_filtro, valor):
        dados_psi = carregar_dados(PSICOLOGO_DB)
        dados_con = carregar_dados(CONSULTAS_DB)
        mapa_psi = {psi['id']: psi['nome'] for psi in dados_psi}
        
        retorno = []
        for c in funcao_filtro(dados_con, valor):
            nome = mapa_psi.get(c.get('idPsicologo'))
            if nome:
                c_copy = c.copy()
                c_copy['nomePsi'] = nome
                retorno.append(c_copy)
                
        return jsonify(sorted(retorno, key=chaveDeOrdenacao))

    @staticmethod
    @tratar_erros
    def listarHorariosLivres():
        d = request.get_json()
        if not d: raise ValueError("Dados não fornecidos")
        
        nome = validar_nome(d.get('nome'))
        email = validar_email_func(d.get('email'))
        
        dados = carregar_dados(PSICOLOGO_DB)
        psi = pesquisarPsicologoPorNomeEmail(dados, nome, email) 
        
        if not psi:
            return jsonify({"erro": "Psicologo não encontrado"}), 404

        todos = Psicologo.get_consultas_do_psicologo(psi['id'])
        return jsonify([h for h in todos if not h.get('reservado')])

    @staticmethod
    @tratar_erros
    def listarMinhasSolicitacoes():
        d = request.get_json()
        if not d or 'id' not in d:
             raise ValueError('Id do estudante não fornecido')
        
        id_est = validar_id(d.get('id'))
        dados_con = carregar_dados(CONSULTAS_DB)
        dados_psi = carregar_dados(PSICOLOGO_DB)
        mapa_psi = {p['id']: p['nome'] for p in dados_psi}
        
        lista = []
        for c in dados_con:
            if c.get('reservadoPorEstudante') and c.get('idEstudante') == id_est:
                c_display = c.copy()
                c_display['nomePsi'] = mapa_psi.get(c.get('idPsicologo'), 'N/A')
                lista.append(c_display)
        
        return jsonify(sorted(lista, key=chaveDeOrdenacao))