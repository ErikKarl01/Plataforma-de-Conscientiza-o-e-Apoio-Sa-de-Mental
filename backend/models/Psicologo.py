from flask import request, jsonify
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados
import phonenumbers
from email_validator import validate_email, EmailNotValidError

PSICOLOGO_DB = 'backend/data/psicologos.json'
CONSULTAS_DB = 'backend/data/consultas.json'

def pesquisaDataHorario(dados, data, horarioDoFront, id_sessao=None):
    for indice, consulta in enumerate(dados):
            if consulta['data'] == data and consulta['horario'] == horarioDoFront:
                if id_sessao is None:
                    return indice, consulta
                elif consulta.get('idPsicologo') == id_sessao:
                    return indice, consulta
    return (None, None)  

def horarioJaExiste(data, horario, idPsicologo):
    """
    Verifica se um horário específico já está cadastrado para um psicólogo.
    Retorna True se existir, False caso contrário.
    """
    dados = carregar_dados(CONSULTAS_DB)
    
    _indice, consulta_encontrada = pesquisaDataHorario(dados, data, horario, idPsicologo)
    
    if consulta_encontrada:
        return True
    
    return False

def chaveDeOrdenacao(consulta): 
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')


class Psicologo:
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método cadastra um usuário 
    @staticmethod 
    def cadastrarPsicologo():
        dados_do_front = request.get_json()
        
        try:
            nome = dados_do_front.get('nome')
            email = dados_do_front.get('email')
            senha = dados_do_front.get('senha')
            telefone = dados_do_front.get('telefone')
            crp = dados_do_front.get('crp')

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
            
            if not crp or not crp.strip():
                return jsonify({"erro": "O CRP não pode estar vazio"}), 400
            crp = crp.strip()

        except EmailNotValidError as e:
            return jsonify({"erro": f"Email inválido: {e}"}), 400
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError) as e:
            return jsonify({'erro': f'Telefone inválido: {e}'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro nos dados fornecidos: {e}'}), 400
        
        novo_usuario = {'nome': nome, 'email': email, 'telefone': telefone, 'crp': crp}
        novo_usuario['senha'] = generate_password_hash(senha)
        
        dados = carregar_dados(PSICOLOGO_DB)
            
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id  
        dados.append(novo_usuario)
        
        with open(PSICOLOGO_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método permite o psicólogo marcar uma consulta
    @staticmethod
    def adicionarHorario ():
        dados_do_front = request.get_json()
        
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id informado no cropo inválido'})
        
        try:
            dataConsulta = dados_do_front.get('data')
            horarioConsulta = dados_do_front.get('horario')
            # Valida o formato
            datetime.strptime(f'{dataConsulta} {horarioConsulta}', '%d/%m/%Y %H:%M')
        except (ValueError, TypeError):
            return jsonify({"erro": "Formato de data ou hora inválido"}), 400
        
        existe_data_horario = existe_data_horario(dataConsulta, horarioConsulta, id_sessao)
        if existe_data_horario:
            return jsonify({'mensagem': 'Data/horário já cadastrados'})

        try:
            idPsicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
             return jsonify({"erro": "ID do psicólogo inválido"}), 400
        
        nome = ''
        numeroPaciente = ''
        reservado = False
        
        novaConsulta = {'nomePaciente': nome, 'telPaciente': numeroPaciente,  'data': dataConsulta, 'horario': horarioConsulta,
        'idPsicologo': idPsicologo, 'reservado': reservado}
        
        dados = carregar_dados(CONSULTAS_DB)
        
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})
    
    @staticmethod
    def marcarConsulta():
        dados_do_front = request.get_json()
        
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
        except ValueError:
            return jsonify({'mensagem': 'Formato de data/horário inválidos'})
        except TypeError:
            return jsonify({'mensagem': 'Data/horário não fornecidos'})
        
        nomePaciente = dados_do_front.get('nomePaciente')
        if not nomePaciente or not nomePaciente.strip():
            return jsonify({"erro": "O nome não pode estar vazio"}), 400
        elif any(char.isdigit() for char in nomePaciente):
            return jsonify({"erro": "O nome não pode conter números"}), 400
        
        telPaciente = dados_do_front.get('telPaciente')
        
        try:
            numero_tel = phonenumbers.parse(telPaciente, "BR")
            
            if not phonenumbers.is_valid_number(numero_tel):
                return jsonify({'mensagem': 'Número inválido, tente outro'})
            telefone_formatado = phonenumbers.format_number(
            numero_tel, phonenumbers.PhoneNumberFormat.E164
            )
        except Exception as e:
            return jsonify({'erro': f'Telefone inválido {e}'})
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront)
        
        if consulta:
            consulta['nomePaciente'] = nomePaciente
            consulta['telPaciente'] = telefone_formatado
            consulta['reservado'] = True 
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
        
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método edita data e horário
    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id informado no cropo inválido'})
            
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
        
            dataModificada = dados_do_front.get('dataModificada')
            horarioModificado = dados_do_front.get('horarioModificado')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
            datetime.strptime(f'{dataModificada} {horarioModificado}', '%d/%m/%Y %H:%M')
        except ValueError:
            return jsonify({'mensagem': 'Formato de data/horário inválidos'})
        except TypeError:
            return jsonify({'mensagem': 'Data/horário não fornecidos'})
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:
            consulta['horario'] = horarioModificado
            consulta['data'] = dataModificada
            dados[indice] = consulta
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário cadastrado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método excluir uma consulta
    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id informado no cropo inválido'})
        
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
        except ValueError:
            return jsonify({'mensagem': 'Formato de data/horário inválidos'})
        except TypeError:
            return jsonify({'mensagem': 'Data/horário não fornecidos'})
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluido com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'})
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método muda a disponibilidade da reserva para um psicólogo
    @staticmethod
    def editarReserva():
        dados_do_front = request.get_json()
        
        reserva = dados_do_front.get('reserva')
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id informado no cropo inválido'})
        
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
        except ValueError:
            return jsonify({'mensagem': 'Formato de data/horário inválidos'})
        except TypeError:
            return jsonify({'mensagem': 'Data/horário não fornecidos'})
            
        dados = carregar_dados(CONSULTAS_DB)                    
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:                    
            dados[indice]['reservado'] = reserva
            if not reserva:
                dados[indice]['nomePaciente'] = ''
                dados[indice]['telPaciente'] = ''
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data e horário não encontrados'}) 
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método adiciona um pacinente a um horário
    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                try:
                    string_completa = consulta['data'] + ' ' + consulta['horario']
                    datetime.strptime(string_completa, '%d/%m/%Y %H:%M')
                    
                    dados_filtrados.append(consulta)
                    
                except (ValueError, TypeError, KeyError):
                    print(f"Aviso: Ignorando consulta com formato de data inválido. ID: {consulta.get('id')}")
                
        dados_ordenados = sorted(dados_filtrados, key=chaveDeOrdenacao)
        return dados_ordenados

    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método lista todas as consultas
    @staticmethod
    def listarConsultas():
        dados_do_front = request.get_json()
        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400
        try:
            id_psicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID inválido"}), 400

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosReservados = []
        for horario in todosOsHorarios:
            if horario.get('reservado'):
                horariosReservados.append(horario)
                
        return jsonify(horariosReservados)
    
    #Esse método permite pegar dados do front e adicionar a um arquivo json usado como banco de dados  
    #Esse método lista todos os horarios livres
    @staticmethod
    def listarHorariosLivres():
        dados_do_front = request.get_json()
        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400
        try:
            id_psicologo = int(dados_do_front.get('idPsicologo'))
        except (ValueError, TypeError):
            return jsonify({"erro": "ID inválido"}), 400

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)
        
        horariosLivres = []
        for horario in todosOsHorarios:
            if not horario.get('reservado'):
                horariosLivres.append(horario)
                
        return jsonify(horariosLivres)