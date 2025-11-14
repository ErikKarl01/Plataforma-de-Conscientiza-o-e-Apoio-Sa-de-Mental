from flask import request, jsonify
import json
# CORREÇÃO 1: Importação relativa (com o '.') para funcionar com o app.py
from .CarregarDados import carregar_dados
from werkzeug.security import generate_password_hash
from .Psicologo import pesquisaDataHorario, Psicologo

ESTUDANTE_DB = 'backend/data/estudante.json'
CONSULTAS_DB = 'backend/data/consultas.json'
PSICOLOGO_DB = 'backend/data/psicologos.json'

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
    def pesquisarDataHorarioLivres():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        
        dados = carregar_dados(PSICOLOGO_DB)
        psicologo = pesquisarPsicologoPorNomeEmail(dados, nome, email)
        
        if not psicologo:
            return jsonify({'mensagem': 'Psicólogo não encontrado'}) 
        
        horariosLivres = Psicologo.get_consultas_do_psicologo(psicologo['id'])
        
        return jsonify(horariosLivres)
    
    @staticmethod
    def selecionarDataHorario():
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
    