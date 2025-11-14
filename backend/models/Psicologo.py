from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

app = Flask(__name__)

USUARIOS_DB = 'backend/data/psicologos.json'
CONSULTAS_DB = 'backend/data/consultas.json'

os.makedirs(os.path.dirname(USUARIOS_DB), exist_ok=True)

def carregar_dados(caminho_arquivo):
    """
    Função auxiliar para carregar dados de um arquivo JSON com segurança.
    Cria o arquivo se não existir e trata arquivos vazios ou corrompidos.
    """
    if not os.path.exists(caminho_arquivo) or os.path.getsize(caminho_arquivo) == 0:
        with open(caminho_arquivo, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(caminho_arquivo, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"AVISO: O arquivo {caminho_arquivo} estava corrompido. Iniciando com dados limpos.")
        return []
        
def pesquisaDataHorario(dados, data, horarioDoFront):
    for indice, consulta in enumerate(dados):
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                return indice, consulta
    return (None, None) 

def chaveDeOrdenacao(consulta): 
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')


class Psicologo:
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método cadastra um usuário 
    @staticmethod 
    def cadastrarPsicologo():
        dados_do_front = request.get_json()
        
        nome = dados_do_front.get('nome')
        email = dados_do_front.get('email')
        senha = dados_do_front.get('senha')
        telefone = dados_do_front.get('telefone')
        crp = dados_do_front.get('crp')
        
        novo_usuario = {'nome': nome, 'email': email, 'senha': senha, 'telefone': telefone, 'crp': crp}
        
        dados = carregar_dados(USUARIOS_DB)
            
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id  
        dados.append(novo_usuario)
        
        with open(USUARIOS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método permite o psicólogo marcar uma consulta
    @staticmethod
    def adicionarConsulta ():
        dados_do_front = request.get_json()
        
        nomeDoPaciente = dados_do_front.get('nomePaciente')
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')
        reservado = False
        
        novaConsulta = {'nomePaciente': nomeDoPaciente, 'data': dataConsulta, 'horario': horarioConsulta,
        'idPsicologo': idPsicologo, 'reservado': reservado}
        
        dados = carregar_dados(CONSULTAS_DB)
        
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})
    
    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        dataModificada = dados_do_front.get('dataModificada')
        horarioModificado = dados_do_front.get('horarioModificado')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            consulta['horario'] = horarioModificado
            consulta['data'] = dataModificada
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluido com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    @staticmethod
    def editarReserva():
        dados_do_front = request.get_json()
        
        data = dados_do_front.get('data')
        horarioDoFront = dados_do_front.get('horario')
        reserva = dados_do_front.get('reserva')
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            dados[indice]['reservado'] = reserva
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'}) 
    
    @staticmethod
    def listarConsultas():
        dados_do_front = request.get_json()

        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido no corpo"}), 400
            
        try:
            id_psicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID inválido"}), 400

        dados_completos = carregar_dados(CONSULTAS_DB)
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                dados_filtrados.append(consulta)
                
        dados_ordenados = sorted(dados_filtrados, key=chaveDeOrdenacao)
        return jsonify(dados_ordenados)
            

@app.route('/cadastrar', methods=['POST'])
def cadastrar_psicologo():
    return Psicologo.cadastrarPsicologo()

@app.route('/adicionarConsulta', methods=['POST'])
def marcar_consulta():
    return Psicologo.adicionarConsulta()

@app.route('/modificarConsulta', methods=['POST'])
def editar_horario():
    return Psicologo.editarHorario()

@app.route('/removerConsulta', methods=['POST'])
def excluir_horario():
    return Psicologo.excluirHorario()

@app.route('/editarReserva', methods=['POST'])
def editar_reserva():
    return Psicologo.editarReserva()

@app.route('/listarConsultas', methods=['POST'])
def listar_consultas():
    return Psicologo.listarConsultas()


if __name__ == '__main__':
    app.run(debug=True)