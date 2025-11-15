from flask import request, jsonify
import json
from .CarregarDados import carregar_dados
from werkzeug.security import generate_password_hash
from .Psicologo import Psicologo, PSICOLOGO_DB, CONSULTAS_DB, pesquisaDataHorario, chaveDeOrdenacao

ESTUDANTE_DB = 'backend/data/estudante.json'

def pesquisarPsicologoPorNomeEmail(dadosBanco, nome, email):
    for dado in dadosBanco:
        if dado['nome'] == nome and dado['email'] == email:
            return dado
    return None

def pesquisaEstudante(dados, id):
    for index, estudante in enumerate(dados):
        if estudante.get('id') == id:
            return index, estudante
    return (None, None)

def pesquisaDataHorarioPorHorario(dados, horario):
    return [u for u in dados if u.get('horario') == horario]

def pesquisaDataHorarioPorData(dados, data):
    return [u for u in dados if u.get('data') == data]


class Estudante:
    @staticmethod
    def cadastrar():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        senha = dados_do_front.get('senha')
        telefone = dados_do_front.get('telefone')
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone}
        novo_usuario['senha'] = generate_password_hash(senha) 
        
        dados = carregar_dados(ESTUDANTE_DB)
            
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id 
        dados.append(novo_usuario)
        
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})
    
    @staticmethod
    def editarEstudante():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        telefone = dados_do_front.get('telefone')
        
        if not dados_do_front or 'id' not in dados_do_front:
            return jsonify({'erro': 'Id não fornecido no corpo'}), 400
        
        try:
            id = int(dados_do_front['id'])
        except: 
            return jsonify({'erro': 'ID inválido'}), 400
        
        dados = carregar_dados(ESTUDANTE_DB)
        index, estudante = pesquisaEstudante(dados, id)
        
        if not estudante:
            return jsonify({'erro': 'Estudante não encontrado'}), 400
        
        estudante['nome'] = nome
        estudante['email'] = email
        estudante['telefone'] = telefone
        
        dados[index] = estudante
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Estudante modificado com sucesso', 'estudante': estudante})
    
    @staticmethod
    def excluirEstudante():
        dados_do_front = request.get_json()
        
        if not dados_do_front or 'id' not in dados_do_front:
            return jsonify({'erro': 'Id não fornecido no corpo'}), 400
        
        try:
            id = int(dados_do_front['id'])
        except: 
            return jsonify({'erro': 'ID inválido'}), 400
        
        dados = carregar_dados(ESTUDANTE_DB)
        index, estudante = pesquisaEstudante(dados, id)
        
        if not estudante:
            return jsonify({'erro': 'Estudante não encontrado'}), 400
        
        dados.pop(index)
        
        with open(ESTUDANTE_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Estudante excluído com sucesso', 'estudante': estudante})
    
    @staticmethod
    def pesquisarPorNome():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        
        dados_psicologos = carregar_dados(PSICOLOGO_DB)
        psicologo = pesquisarPsicologoPorNomeEmail(dados_psicologos, nome, email)
        
        if not psicologo:
            return jsonify({'mensagem': 'Psicólogo não encontrado'}) 
        
        # CORREÇÃO 5: Chamando o método 'privado' (que assumimos que você tornará público 
        # ou renomeará para 'get_consultas_do_psicologo' em Psicologo.py)
        # Se o método ainda for '_get_consultas...' em Psicologo.py, esta é a forma correta
        todos_horarios = Psicologo._get_consultas_do_psicologo(psicologo['id'])
        
        # Lógica de filtrar por 'livres' restaurada
        horariosLivres = []
        for horario in todos_horarios:
            if not horario.get('reservado'):
                horariosLivres.append(horario)
        
        return jsonify(horariosLivres)
    
    @staticmethod
    def reservarDataHorario():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        telefone = dados_do_front.get('telefone')
        data = dados_do_front.get('data')
        horario = dados_do_front.get('horario')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        index, dataHorarioEscolhido = pesquisaDataHorario(dados, data, horario)
        
        if not dataHorarioEscolhido:
            return jsonify({'mensagem': 'Data/Horário não encontrados'})
        
        dados[index]['reservado'] = True 
        dados[index]['nomePaciente'] = nome
        dados[index]['telPaciente'] = telefone
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        
        return jsonify({'mensagem': 'Data/Horário reservados com sucesso'})
    
    @staticmethod
    def pesquisaPorData():
        dados_do_front = request.get_json()
        data = dados_do_front.get('data')
        
        dadosPsi = carregar_dados(PSICOLOGO_DB)
        dadosCon = carregar_dados(CONSULTAS_DB)
        
        mapa_psicologos = {psi['id']: psi['nome'] for psi in dadosPsi}
        
        lista_retornar = []
        
        # Usa a função 'pesquisaDataHorarioPorData' (que corrigimos)
        filtroData = pesquisaDataHorarioPorData(dadosCon, data)
        
        for consulta in filtroData:
            id_psi = consulta.get('idPsicologo')
            # Busca o nome do psicólogo no mapa
            nome_psi = mapa_psicologos.get(id_psi)
            
            if nome_psi:
                # Cria uma cópia da consulta para não modificar a original
                consulta_com_nome = consulta.copy() 
                consulta_com_nome['nomePsi'] = nome_psi
                lista_retornar.append(consulta_com_nome)
                
        # CORREÇÃO 2: 'chaveDeOrdenacao' agora está importada e pode ser usada
        ordenada = sorted(lista_retornar, key=chaveDeOrdenacao)
                
        return jsonify(ordenada)

    # NOVO MÉTODO ADICIONADO
    @staticmethod
    def pesquisaPorHorario():
        dados_do_front = request.get_json()
        horario = dados_do_front.get('horario')
        
        dadosPsi = carregar_dados(PSICOLOGO_DB)
        dadosCon = carregar_dados(CONSULTAS_DB)
        
        mapa_psicologos = {psi['id']: psi['nome'] for psi in dadosPsi}
        
        lista_retornar = []
        
        filtroHorario = pesquisaDataHorarioPorHorario(dadosCon, horario)
        
        for consulta in filtroHorario:
            id_psi = consulta.get('idPsicologo')
            nome_psi = mapa_psicologos.get(id_psi)
            
            if nome_psi:
                consulta_com_nome = consulta.copy() 
                consulta_com_nome['nomePsi'] = nome_psi
                lista_retornar.append(consulta_com_nome)
                
        ordenada = sorted(lista_retornar, key=chaveDeOrdenacao)
                
        return jsonify(ordenada)