from flask import request, jsonify
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados

PSICOLOGO_DB = 'backend/data/psicologos.json'
CONSULTAS_DB = 'backend/data/consultas.json'

def pesquisaDataHorario(dados, data, horarioDoFront):
    for indice, consulta in enumerate(dados):
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                return indice, consulta
    return (None, None) 

def chaveDeOrdenacao(consulta): 
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')


class Psicologo:
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método cadastra um usuário 
    @staticmethod 
    def cadastrarPsicologo():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        senha = dados_do_front.get('senha')
        telefone = dados_do_front.get('telefone')
        crp = dados_do_front.get('crp')
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone, 'crp': crp}
        novo_usuario['senha'] = generate_password_hash(senha)
        
        dados = carregar_dados(PSICOLOGO_DB)
            
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id  
        dados.append(novo_usuario)
        
        with open(PSICOLOGO_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método permite o psicólogo marcar uma consulta
    @staticmethod
    def adicionarHorario ():
        dados_do_front = request.get_json()
        
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        nome = ''
        numeroPaciente = ''
        reservado = False
        
        novaConsulta = {'nomePaciente': nome, 'telPaciente': numeroPaciente,  'data': dataConsulta, 'horario': horarioConsulta,
        'idPsicologo': idPsicologo, 'reservado': reservado}
        
        dados = carregar_dados(CONSULTAS_DB)
        
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})
    
    @staticmethod
    def marcarConsulta():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        nomePaciente = dados_do_front.get('nomePaciente')
        telPaciente = dados_do_front.get('telPaciente')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            consulta['nomePaciente'] = nomePaciente
            consulta['telPaciente'] = telPaciente
            consulta['reservado'] = True 
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
        
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método edita data e horário
    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        dataModificada = dados_do_front.get('dataModificada')
        horarioModificado = dados_do_front.get('horarioModificado')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            consulta['horario'] = horarioModificado
            consulta['data'] = dataModificada
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método excluir uma consulta
    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluido com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método muda a disponibilidade da reserva para um psicólogo
    @staticmethod
    def editarReserva():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        reserva = dados_do_front.get('reserva')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            dados[indice]['reservado'] = reserva
            if not reserva:
                dados[indice]['nomePaciente'] = ''
                dados[indice]['telPaciente'] = ''
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'}) 
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método adiciona um pacinente a um horário
    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                dados_filtrados.append(consulta)
                
        dados_ordenados = sorted(dados_filtrados, key=chaveDeOrdenacao)
        return dados_ordenados

    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método lista todas as consultas
    @staticmethod
    def listarConsultas():
        dados_do_front = request.get_json()
        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400
        try:
            id_psicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID inválido"}), 400

        todosOsHorarios = Psicologo._get_consultas_do_psicologo(id_psicologo)
        
        horariosReservados = []
        for horario in todosOsHorarios:
            if horario.get('reservado'):
                horariosReservados.append(horario)
                
        return jsonify(horariosReservados)
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método lista todos os horarios livres
    @staticmethod
    def listarHorariosLivres():
        dados_do_front = request.get_json()
        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400
        try:
            id_psicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID inválido"}), 400

        todosOsHorarios = Psicologo._get_consultas_do_psicologo(id_psicologo)
        
        horariosLivres = []
        for horario in todosOsHorarios:
            if not horario.get('reservado'):
                horariosLivres.append(horario)
                
        return jsonify(horariosLivres)