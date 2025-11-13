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
    
    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        dataModificada = dados_do_front.get('dataModificada')
        horarioModificado = dados_do_front.get('horarioModificado')
        
        with open('backend/data/consultas.json', 'f') as f:
            dados = json.loads(f)
        
        for consulta in dados:
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                consulta['data'] == dataModificada
                consulta['horario'] == horarioModificado
                
                with open('backend/data/consultas.json', 'w') as f:
                    json.dump(dados, f)
                    
                return jsonify({'mensagem': 'Consulta modiicada com sucesso', 'consulta': consulta})
                    
        with open('backend/data/consultas.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        with open('backend/data/consultas.json', 'f') as f:
            dados = json.loads(f)
        
        for consulta in dados:
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                dados.remove(consulta)
                
                with open('backend/data/consultas.json', 'w') as f:
                    json.dump(dados, f)
                    
                return jsonify({'mensagem': 'Consulta modiicada com sucesso', 'consulta': consulta})
                    
        with open('backend/data/consultas.json', 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Data e horário não encontrados'})               
        

@app.route('/adicionarConsulta', methods=['POST'])
def marcar_consulta():
    consulta = Psicologo()
    return consulta.adicionarConsulta()

@app.route('/modificarConsulta', methods=['POST'])
def editar_horario():
    consulta = Psicologo()
    return consulta.editarHorario()

@app.route('/removerConsulta', methods=['POST'])
def excluir_horario():
    consulta = Psicologo()
    return consulta.excluirHorario()

if __name__ == '__main__':
    app.run(debug=True)