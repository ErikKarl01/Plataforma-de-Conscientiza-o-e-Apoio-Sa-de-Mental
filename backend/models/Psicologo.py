from Usuario import Usuario
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)
        
if not os.path.exists('backend/data/consultas.json'):
    with open('backend/data/consultas.json', 'w') as f:
        json.dump([], f)

class Psicologo(Usuario):
    crp: str
    
    def __init__(self, nome, email, senha, telefone, crp):
        super().__init__(nome, email, senha, telefone)
        self.crp = crp
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método permite o psicólogo marcar uma consulta
    @staticmethod
    def adicionarConsulta ():
        dados_do_front = request.get_json()
        
        nomeDoPaciente = dados_do_front.get('nomePaciente')
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        
        novaConsulta = {'nomePaciente': nomeDoPaciente, 'data': dataConsulta, 'horario': horarioConsulta, 'idPsicologo': idPsicologo}
        
        with open('backend/data/consultas.json', 'r') as f:
            dados = json.load(f)
        
        idConsulta = len(dados) + 1
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open('backend/data/consultas.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})
        

@app.route('/adicionarConsulta', methods=['POST'])
def marcar_consulta():
    consulta = Psicologo()
    return consulta.adicionarConsulta()


if __name__ == '__main__':
    app.run(debug=True)