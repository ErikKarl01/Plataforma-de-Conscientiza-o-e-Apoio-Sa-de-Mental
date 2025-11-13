from flask import Flask, request, jsonify
import json
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Garante que o arquivo banco.json exista
if not os.path.exists('backend/banco.json'):
    with open('backend/banco.json', 'w') as f:
        json.dump([], f)


class Usuario:
    def __init__(self, nome: str, email: str, senha: str, telefone: str, crp: str):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.crp = crp

    def salvar(self):
        # Lê os dados existentes
        with open('backend/banco.json', 'r') as f:
            dados = json.load(f)

        # Gera novo ID
        novo_id = len(dados) + 1
        usuario_dict = {
            'id': novo_id,
            'nome': self.nome,
            'email': self.email,
            'senha': self.senha,
            'telefone': self.telefone,
            'crp': self.crp
        }

        # Adiciona o novo usuário e salva no arquivo
        dados.append(usuario_dict)
        with open('backend/banco.json', 'w') as f:
            json.dump(dados, f, indent=4)

        return usuario_dict


@app.route('/cadastrar', methods=['POST'])
def cadastrar_usuario():
    dados_do_front = request.get_json()

    nome = dados_do_front.get('nome')
    email = dados_do_front.get('email')
    senha = dados_do_front.get('senha')
    telefone = dados_do_front.get('telefone')
    crp = dados_do_front.get('crp')

    usuario = Usuario(nome, email, senha, telefone, crp)
    usuario_salvo = usuario.salvar()

    return jsonify({'mensagem': 'Usuário salvo com sucesso!', 'usuario': usuario_salvo})


if __name__ == '__main__':
    app.run(debug=True)
