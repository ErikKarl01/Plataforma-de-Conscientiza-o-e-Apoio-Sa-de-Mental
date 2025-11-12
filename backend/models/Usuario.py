from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS # Importar o CORS

app = Flask(__name__)
CORS(app) # Habilitar o CORS

with open('backend/banco.json', 'w') as f:
    json.dump([], f)

class Usuario:
    nome: str
    email: str
    senha: str
    telefone: str
    crp: str
    
    def __init__(self, nome: str, email: str, senha: str, telefone: str, crp: str):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.crp = crp
        
    def cadastrar(self):
        dados_do_front = request.get_json()
        
        self.nome = dados_do_front.get('nome')
        self.email = dados_do_front.get('email')
        self.senha = dados_do_front.get('senha')
        self.telefone = dados_do_front.get('telefone')
        self.crp = dados_do_front.get('crp')
        
        novo_usuario = {'nome': self.nome, 'email': self.email, 'senha': self.senha, 'telefone': self.telefone, 'crp': self.crp}
        
        with open('backend/banco.json', 'r') as f:
            dados = json.load(f)
            
        dados.append(novo_usuario)
        
        with open('backend/banco.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo comsucesso', 'banco': novo_usuario})
    
    
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    usuario = Usuario('', '', '', '', '')
    return usuario.cadastrar()


if __name__ == '__main__':
    app.run(debug=True)