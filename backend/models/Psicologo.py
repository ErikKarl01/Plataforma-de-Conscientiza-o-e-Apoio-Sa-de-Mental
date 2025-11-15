from flask import request, jsonify
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados


PSICOLOGO_DB = 'data/psicologos.json'
CONSULTAS_DB = 'data/consultas.json'

def pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo):
    for indice, consulta in enumerate(dados):
        if (consulta['data'] == data 
            and consulta['horario'] == horarioDoFront
            and consulta['idPsicologo'] == idPsicologo):
            return indice, consulta
    return (None, None)


def chaveDeOrdenacao(consulta): 
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')


class Psicologo:

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
    

    @staticmethod
    def adicionarHorario():
        dados_do_front = request.get_json()
        
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')

        novaConsulta = {
            'nomePaciente': '',
            'telPaciente': '',
            'data': dataConsulta,
            'horario': horarioConsulta,
            'idPsicologo': idPsicologo,
            'reservado': False
        }
        
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
        idPsicologo = dados_do_front.get('idPsicologo')

        nomePaciente = dados_do_front.get('nomePaciente')
        telPaciente = dados_do_front.get('telPaciente')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo)
        
        if consulta:
            consulta['nomePaciente'] = nomePaciente
            consulta['telPaciente'] = telPaciente
            consulta['reservado'] = True 
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário reservado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')

        dataModificada = dados_do_front.get('dataModificada')
        horarioModificado = dados_do_front.get('horarioModificado')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo)
        
        if consulta:
            consulta['horario'] = horarioModificado
            consulta['data'] = dataModificada
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário editado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')

        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluído com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    @staticmethod
    def editarReserva():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        reserva = dados_do_front.get('reserva')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo)
        
        if consulta:
            consulta['reservado'] = reserva
            if not reserva:
                consulta['nomePaciente'] = ''
                consulta['telPaciente'] = ''
            dados[indice] = consulta

            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)

            return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        
        dados_filtrados = [
            consulta for consulta in dados_completos
            if str(consulta.get('idPsicologo')) == str(id_psicologo)
        ]
                
        return sorted(dados_filtrados, key=chaveDeOrdenacao)



    @staticmethod
    def listarConsultas():
        dados_do_front = request.get_json()

        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400

        id_psicologo = str(dados_do_front.get('idPsicologo'))

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosReservados = [
            h for h in todosOsHorarios if h.get('reservado')
        ]
                
        return jsonify(horariosReservados)



    @staticmethod
    def listarHorariosLivres():
        dados_do_front = request.get_json()

        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400

        id_psicologo = int(dados_do_front.get('idPsicologo'))

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosLivres = [
            h for h in todosOsHorarios if not h.get('reservado')
        ]
                
        return jsonify(horariosLivres)
