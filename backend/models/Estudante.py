from flask import request, jsonify
import json
# CORREÇÃO 1: Importação relativa (com o '.') para funcionar com o app.py
from .Psicologo import carregar_dados 
from werkzeug.security import generate_password_hash

ESTUDANTE_DB = 'backend/data/estudante.json'

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