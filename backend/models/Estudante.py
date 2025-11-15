from flask import request, jsonify
import json
import phonenumbers
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
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
        
        try:
            nome = dados_do_front.get('nome')
            email = dados_do_front.get('email')
            senha = dados_do_front.get('senha')
            telefone = dados_do_front.get('telefone')

            if not nome or not nome.strip():
                return jsonify({"erro": "O nome não pode estar vazio"}), 400
            if any(char.isdigit() for char in nome):
                return jsonify({"erro": "O nome não pode conter números"}), 400
            nome = nome.strip()

            if not email:
                return jsonify({"erro": "O email não pode estar vazio"}), 400
            v = validate_email(email, check_deliverability=False)
            email = v.normalized
            
            if not senha:
                return jsonify({"erro": "A senha não pode estar vazia"}), 400
            
            num_telefone = phonenumbers.parse(telefone, "BR")
            if not phonenumbers.is_valid_number(num_telefone):
                raise ValueError("Número de telefone inválido")
            telefone = phonenumbers.format_number(
                num_telefone, phonenumbers.PhoneNumberFormat.E164
            )

        except EmailNotValidError as e:
            return jsonify({"erro": f"Email inválido: {e}"}), 400
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as e:
            return jsonify({'erro': f'Telefone inválido: {e}'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro nos dados fornecidos: {e}'}), 400
        
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
        
        try:
            nome = dados_do_front.get('nome')
            email = dados_do_front.get('email')
            telefone = dados_do_front.get('telefone')

            if not nome or not nome.strip():
                return jsonify({"erro": "O nome não pode estar vazio"}), 400
            if any(char.isdigit() for char in nome):
                return jsonify({"erro": "O nome não pode conter números"}), 400
            nome = nome.strip()

            if not email:
                return jsonify({"erro": "O email não pode estar vazio"}), 400
            v = validate_email(email, check_deliverability=False)
            email = v.normalized
            
            num_telefone = phonenumbers.parse(telefone, "BR")
            if not phonenumbers.is_valid_number(num_telefone):
                raise ValueError("Número de telefone inválido")
            telefone = phonenumbers.format_number(
                num_telefone, phonenumbers.PhoneNumberFormat.E164
            )

        except EmailNotValidError as e:
            return jsonify({"erro": f"Email inválido: {e}"}), 400
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as e:
            return jsonify({'erro': f'Telefone inválido: {e}'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro nos dados fornecidos: {e}'}), 400
        
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
        
        
        todos_horarios = Psicologo.get_consultas_do_psicologo(psicologo['id'])
        
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
        try:
            idPsicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID do psicólogo inválido ou não fornecido"}), 400

        dados = carregar_dados(CONSULTAS_DB)
        
        index, dataHorarioEscolhido = pesquisaDataHorario(dados, data, horario, idPsicologo)
        
        if not dataHorarioEscolhido:
            return jsonify({'mensagem': 'Data/Horário não encontrados para este psicólogo'}), 404
        
        if dataHorarioEscolhido.get('reservado'):
            return jsonify({'mensagem': 'Este horário já está reservado'}), 409
        
        dados[index]['reservado'] = True 
        dados[index]['nomePaciente'] = nome
        dados[index]['telPaciente'] = telefone
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
        
        return jsonify({'mensagem': 'Data/Horário reservados com sucesso'})
    
    @staticmethod
    def pesquisarPorData():
        dados_do_front = request.get_json()
        data = dados_do_front.get('data')
        
        dadosPsi = carregar_dados(PSICOLOGO_DB)
        dadosCon = carregar_dados(CONSULTAS_DB)
        
        mapa_psicologos = {psi['id']: psi['nome'] for psi in dadosPsi}
        
        lista_retornar = []
        
        filtroData = pesquisaDataHorarioPorData(dadosCon, data)
        
        for consulta in filtroData:
            id_psi = consulta.get('idPsicologo')
            nome_psi = mapa_psicologos.get(id_psi)
            
            if nome_psi:
                try:
                    string_completa = consulta['data'] + ' ' + consulta['horario']
                    datetime.strptime(string_completa, '%d/%m/%Y %H:%M')
                    
                    consulta_com_nome = consulta.copy() 
                    consulta_com_nome['nomePsi'] = nome_psi
                    lista_retornar.append(consulta_com_nome)
                
                except (ValueError, TypeError, KeyError):
                    pass
                    
        ordenada = sorted(lista_retornar, key=chaveDeOrdenacao)
                
        return jsonify(ordenada)
    
    @staticmethod
    def pesquisarPorHorario():
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
                try:
                    string_completa = consulta['data'] + ' ' + consulta['horario']
                    datetime.strptime(string_completa, '%d/%m/%Y %H:%M')
                    
                    consulta_com_nome = consulta.copy() 
                    consulta_com_nome['nomePsi'] = nome_psi
                    lista_retornar.append(consulta_com_nome)

                except (ValueError, TypeError, KeyError):
                    pass
                    
        ordenada = sorted(lista_retornar, key=chaveDeOrdenacao)
                
        return jsonify(ordenada)