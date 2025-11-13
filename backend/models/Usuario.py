from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

if not os.path.exists('backend/data/usuarios.json'):
    with open('backend/data/usuarios.json', 'w') as f:
        json.dump([], f)
        

class Usuario:
    id: str
    nome: str
    email: str
    senha: str
    telefone: str
    
    def __init__(self, nome: str, email: str, senha: str, telefone: str):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método cadastra um usuário 
    @staticmethod 
    def cadastrar(self):
        dados_do_front = request.get_json()
        
        self.nome = dados_do_front.get('nome')
        self.email = dados_do_front.get('email')
        self.senha = dados_do_front.get('senha')
        self.telefone = dados_do_front.get('telefone')
        self.crp = dados_do_front.get('crp')
        
        novo_usuario = {'nome': self.nome, 'email': self.email, 'senha': self.senha, 'telefone': self.telefone, 'crp': self.crp}
        
        with open('backend/data/usuarios.json', 'r') as f:
            dados = json.load(f)
            
        self.id = len(dados) + 1
        novo_usuario['id'] = self.id    
        dados.append(novo_usuario)
        
        with open('backend/data/usuarios.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo comsucesso', 'usuario': novo_usuario})
    
    
@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    usuario = Usuario()
    return usuario.cadastrar()


if __name__ == '__main__':
    app.run(debug=True)