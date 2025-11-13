from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

if not os.path.exists('backend/data/usuarios.json'):
    with open('backend/data/usuarios.json', 'w') as f:
        json.dump([], f)
        
if not os.path.exists('backend/data/consultas.json'):
    with open('backend/data/consultas.json', 'w') as f:
        json.dump([], f)

class Psicologo:
    id: str
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
        
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método cadastra um usuário  
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
            
        self.id = len(dados) - 1
        novo_usuario['id'] = self.id    
        dados.append(novo_usuario)
        
        with open('backend/data/usuarios.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo comsucesso', 'usuario': novo_usuario})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método permite o psicólogo marcar uma consulta
    def adicionarConsulta ():
        dados_do_front = request.get_json()
        
        nomeDoPaciente = dados_do_front.get('nomePaciente')
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        
        novaConsulta = {'nomePaciente': nomeDoPaciente, 'data': dataConsulta, 'horario': horarioConsulta, 'idPsicologo': idPsicologo}
        
        with open('backend/data/consultas.json', 'r') as f:
            dados = json.load(f)
        
        idConsulta = len(dados) - 1
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open('backend/data/consultas.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})
        
        
        
        
    
    
@app.route('/cadastrarPsicologo', methods=['POST'])
def cadastrar_usuario():
    usuario = Psicologo('', '', '', '', '')
    return usuario.cadastrar()

@app.route('/adicionarConsulta', methods=['POST'])
def marcar_consulta():
    consulta = Psicologo()
    return consulta.adicionarConsulta()


if __name__ == '__main__':
    app.run(debug=True)