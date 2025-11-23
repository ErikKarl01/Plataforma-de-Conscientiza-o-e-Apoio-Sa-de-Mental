from flask import request, jsonify
import json
import os
from datetime import datetime
from werkzeug.security import generate_password_hash
from .CarregarDados import carregar_dados
import phonenumbers
from email_validator import validate_email, EmailNotValidError


PSICOLOGO_DB = 'data/psicologos.json'
CONSULTAS_DB = 'data/consultas.json'

def pesquisaDataHorario(dados, data, horarioDoFront, id_sessao=None):
    for indice, consulta in enumerate(dados):
        if consulta['data'] == data and consulta['horario'] == horarioDoFront:
            if id_sessao is None:
                return indice, consulta
            elif consulta.get('idPsicologo') == id_sessao:
                return indice, consulta
    return (None, None)  


def horarioJaExiste(data, horario, idPsicologo):
    dados = carregar_dados(CONSULTAS_DB)
    _indice, consulta_encontrada = pesquisaDataHorario(dados, data, horario, idPsicologo)
    return consulta_encontrada is not None


def chaveDeOrdenacao(consulta):
    string_completa = consulta['data'] + ' ' + consulta['horario']
    return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')


class Psicologo:

    # ----------------------------------------------------------------------
    # CADASTRAR PSICÓLOGO
    # ----------------------------------------------------------------------
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
        
        novo_usuario = {
            'nome': nome,
            'email': email,
            'telefone': telefone,
            'crp': crp,
            'senha': generate_password_hash(senha),
        }
        
        dados = carregar_dados(PSICOLOGO_DB)
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_usuario['id'] = novo_id  
        dados.append(novo_usuario)
        
        with open(PSICOLOGO_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Usuário salvo com sucesso', 'usuario': novo_usuario})


    # ----------------------------------------------------------------------
    # ADICIONAR HORÁRIO COM DURAÇÃO
    # ----------------------------------------------------------------------
    @staticmethod
    def adicionarHorario():
        dados_do_front = request.get_json()
        
        dataConsulta = dados_do_front.get('data')
        horarioConsulta = dados_do_front.get('horario')
        idPsicologo = dados_do_front.get('idPsicologo')

        # NOVO: duração com fallback para 50
        duracao = dados_do_front.get('duracao', '50')

        novaConsulta = {
            'nomePaciente': '',
            'telPaciente': '',
            'data': dataConsulta,
            'horario': horarioConsulta,
            'idPsicologo': idPsicologo,
            'reservado': False,
            'duracao': duracao     # <--- ALTERAÇÃO FINAL
        }
        
        dados = carregar_dados(CONSULTAS_DB)
        
        idConsulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        novaConsulta['id'] = idConsulta
        dados.append(novaConsulta)
        
        with open(CONSULTAS_DB, 'w') as f:
            json.dump(dados, f)
            
        return jsonify({'mensagem': 'Consulta cadastrada com sucesso', 'consulta': novaConsulta})



    # ----------------------------------------------------------------------
    # EDITAR HORÁRIO
    # ----------------------------------------------------------------------
    @staticmethod
    def editarHorario():
        dados_do_front = request.get_json()
        
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id da sessão não informado no corpo'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id informado inválido'})
            
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

            return jsonify({'mensagem': 'Horário editado com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    # ----------------------------------------------------------------------
    # EXCLUIR HORÁRIO
    # ----------------------------------------------------------------------
    @staticmethod
    def excluirHorario():
        dados_do_front = request.get_json()
        
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id não informado'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Formato de id inválido'})
        
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
        except:
            return jsonify({'mensagem': 'Formato de data/horário inválidos'})
        
        dados = carregar_dados(CONSULTAS_DB)
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:
            dados.pop(indice)
            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)
            return jsonify({'mensagem': 'Horário excluído com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados para este psicólogo'})


    # ----------------------------------------------------------------------
    # ALTERAR RESERVA
    # ----------------------------------------------------------------------
    @staticmethod
    def editarReserva():
        dados_do_front = request.get_json()
        
        reserva = dados_do_front.get('reserva')
        id_front = dados_do_front.get('id')
        
        if not id_front:
            return jsonify({'mensagem': 'Id não informado'})
            
        try:
            id_sessao = int(id_front)
        except:
            return jsonify({'mensagem': 'Id inválido'})
        
        try:
            data = dados_do_front.get('data')
            horarioDoFront = dados_do_front.get('horario')
            datetime.strptime(f'{data} {horarioDoFront}', '%d/%m/%Y %H:%M')
        except:
            return jsonify({'mensagem': 'Formato inválido'})
            
        dados = carregar_dados(CONSULTAS_DB)                    
        
        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, id_sessao)
        
        if consulta:                    
            dados[indice]['reservado'] = reserva
            if not reserva:
                consulta['nomePaciente'] = ''
                consulta['telPaciente'] = ''
            dados[indice] = consulta

            with open(CONSULTAS_DB, 'w') as f:
                json.dump(dados, f)

            return jsonify({'mensagem': 'Reserva modificada com sucesso', 'consulta': consulta}) 
                    
        return jsonify({'mensagem': 'Data/horário não encontrados'})


    # ----------------------------------------------------------------------
    # LISTAR CONSULTAS DO PSICÓLOGO
    # ----------------------------------------------------------------------
    @staticmethod
    def get_consultas_do_psicologo(id_psicologo):
        dados_completos = carregar_dados(CONSULTAS_DB)
        
        dados_filtrados = []
        for consulta in dados_completos:
            if consulta.get('idPsicologo') == id_psicologo:
                try:
                    datetime.strptime(consulta['data'] + ' ' + consulta['horario'], '%d/%m/%Y %H:%M')
                    dados_filtrados.append(consulta)
                except:
                    print(f"Aviso: Consulta com formato inválido. ID: {consulta.get('id')}")
                
        return sorted(dados_filtrados, key=chaveDeOrdenacao)


    # ----------------------------------------------------------------------
    # LISTAR CONSULTAS RESERVADAS
    # ----------------------------------------------------------------------
    @staticmethod
    def listarConsultas():
        dados_do_front = request.get_json()

        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400

        id_psicologo = dados_do_front['idPsicologo']

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)

        horariosReservados = [h for h in todosOsHorarios if h.get('reservado')]

        return jsonify(horariosReservados), 200


    # ----------------------------------------------------------------------
    # LISTAR HORÁRIOS LIVRES
    # ----------------------------------------------------------------------
    @staticmethod
    def listarHorariosLivres():
        dados_do_front = request.get_json()

        if not dados_do_front or 'idPsicologo' not in dados_do_front:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400

        id_psicologo = dados_do_front['idPsicologo']

        todosOsHorarios = Psicologo.get_consultas_do_psicologo(id_psicologo)

        horariosLivres = [h for h in todosOsHorarios if not h.get('reservado')]

        return jsonify(horariosLivres)


    # ----------------------------------------------------------------------
    # MARCAR CONSULTA
    # ----------------------------------------------------------------------
    @staticmethod
    def marcarConsulta():
        dados_do_front = request.get_json()

        if not dados_do_front:
            return jsonify({"erro": "Nenhum dado enviado"}), 400

        data = dados_do_front.get("data")
        horarioDoFront = dados_do_front.get("horario")
        idPsicologo = dados_do_front.get("idPsicologo")
        nomePaciente = dados_do_front.get("nomePaciente", "")
        telPaciente = dados_do_front.get("telPaciente", "")

        if not idPsicologo:
            return jsonify({"erro": "idPsicologo não fornecido"}), 400

        if not data or not horarioDoFront:
            return jsonify({"erro": "Data e horário são obrigatórios"}), 400

        dados = carregar_dados(CONSULTAS_DB)

        indice, consulta = pesquisaDataHorario(dados, data, horarioDoFront, idPsicologo)

        if consulta is None:
            return jsonify({"erro": "Consulta não encontrada"}), 404

        if consulta.get("reservado"):
            return jsonify({"erro": "Horário já reservado"}), 409

        consulta["reservado"] = True
        consulta["nomePaciente"] = nomePaciente
        consulta["telPaciente"] = telPaciente

        dados[indice] = consulta

        with open(CONSULTAS_DB, "w") as f:
            json.dump(dados, f)

        return jsonify({
            "sucesso": True,
            "mensagem": "Consulta marcada com sucesso!",
            "consulta": consulta
        }), 200
