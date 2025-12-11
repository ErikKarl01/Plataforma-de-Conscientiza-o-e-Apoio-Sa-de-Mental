from datetime import datetime
from repositories.ConsultaRepository import ConsultaRepository
from services.PsicologoService import PsicologoService
from services.EstudanteService import EstudanteService
from utils.Validacao import (validar_data_hora, validar_duracao, validar_causa, 
                                     validar_nome, validar_email_func, validar_telefone, validar_id)

def chaveDeOrdenacao(consulta): 
    try:
        string_completa = consulta['data'] + ' ' + consulta['horario']
        return datetime.strptime(string_completa, '%d/%m/%Y %H:%M')
    except:
        return datetime.min

class ConsultaService:
    def __init__(self):
        self.repo = ConsultaRepository()
        self.psi_service = PsicologoService()
        self.est_service = EstudanteService()

    def adicionar_horario(self, dados):
        id_psi = validar_id(dados.get('idPsicologo'))
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        duracao = validar_duracao(dados.get('duracao'))
        causa = validar_causa(dados.get('causa'))

        idx, existe = self.repo.find_by_data_horario_psi(data, horario, id_psi)
        if existe:
            raise ValueError('Data/horário já cadastrados')

        nova_consulta = {
            'nomePaciente': '', 'telPaciente': '', 'emailPaciente': '',
            'data': data, 'horario': horario, 'idPsicologo': id_psi,
            'reservado': False, 'reservadoPorEstudante': False, 'idEstudante': '',
            'duracao': duracao, 'causa': causa
        }
        return self.repo.create(nova_consulta)

    def marcar_consulta_psi(self, dados):
        # Lógica usada pelo Psicólogo para marcar manualmente
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        nome_paci = validar_nome(dados.get('nomePaciente'), "Nome Paciente")
        tel_paci = validar_telefone(dados.get('telPaciente'), "Telefone Paciente")
        duracao = validar_duracao(dados.get('duracao'))
        causa = validar_causa(dados.get('causa'))
        email_paci = dados.get('emailPaciente', '')
        if email_paci.strip():
            email_paci = validar_email_func(email_paci)

        index, consulta = self.repo.find_by_data_horario_psi(data, horario)
        if not consulta: return None

        # Verifica se é estudante
        _, estudante = self.est_service.buscar_por_nome_telefone(nome_paci, tel_paci)
        
        id_est = estudante['id'] if estudante else ''
        res_por_est = True if estudante else False
        email_final = estudante['email'] if estudante else email_paci

        consulta.update({
            'nomePaciente': nome_paci, 'telPaciente': tel_paci, 'emailPaciente': email_final,
            'reservado': True, 'reservadoPorEstudante': res_por_est, 'idEstudante': id_est
        })
        if duracao: consulta['duracao'] = duracao
        if causa: consulta['causa'] = causa

        return self.repo.update(index, consulta)

    def reservar_por_estudante(self, dados):
        nome_paci = validar_nome(dados.get('nomePaci'), "Nome Paciente")
        email_paci = validar_email_func(dados.get('emailPaci'), "Email Paciente")
        tel_paci = validar_telefone(dados.get('telefonePaci'), "Telefone Paciente")
        nome_psi = validar_nome(dados.get('nome'), "Nome Psicólogo")
        email_psi = validar_email_func(dados.get('email'), "Email Psicólogo")
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        causa = validar_causa(dados.get('causa'))

        psi = self.psi_service.buscar_por_nome_email(nome_psi, email_psi)
        if not psi: raise ValueError('Psicólogo não encontrado')

        index, consulta = self.repo.find_by_data_horario_psi(data, horario, psi['id'])
        
        if not consulta: return 404 # Not found
        if consulta.get('reservado'): return 409 # Conflict

        consulta.update({
            'nomePaciente': nome_paci, 'telPaciente': tel_paci, 'emailPaciente': email_paci,
            'reservado': True, 'reservadoPorEstudante': True, 'causa': causa
        })
        return self.repo.update(index, consulta)

    def cancelar_reserva(self, dados):
        nome_psi = validar_nome(dados.get('nome'), "Nome Psicólogo")
        email_psi = validar_email_func(dados.get('email'), "Email Psicólogo")
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))

        psi = self.psi_service.buscar_por_nome_email(nome_psi, email_psi)
        if not psi: raise ValueError('Psicólogo não encontrado')

        index, consulta = self.repo.find_by_data_horario_psi(data, horario, psi['id'])
        if not consulta: return 404
        if not consulta.get('reservado'): return 409

        consulta.update({
            'nomePaciente': '', 'telPaciente': '', 'emailPaciente': '',
            'reservado': False, 'reservadoPorEstudante': False, 'idEstudante': '', 'causa': ''
        })
        return self.repo.update(index, consulta)

    def listar_livres_por_psi_nome(self, nome_psi, email_psi):
        psi = self.psi_service.buscar_por_nome_email(nome_psi, email_psi)
        if not psi: return None
        consultas = self.repo.find_by_psicologo(psi['id'])
        return [c for c in consultas if not c.get('reservado')]

    def listar_solicitacoes_estudante(self, id_est):
        id_est = validar_id(id_est)
        todas = self.repo.get_all()
        mapa_psi = self.psi_service.get_mapa_nomes()
        
        retorno = []
        for c in todas:
            if c.get('reservadoPorEstudante') and c.get('idEstudante') == id_est:
                c_copy = c.copy()
                c_copy['nomePsi'] = mapa_psi.get(c.get('idPsicologo'), 'N/A')
                retorno.append(c_copy)
        return sorted(retorno, key=chaveDeOrdenacao)

    def buscar_generico(self, tipo, valor):
        # tipo: 'data' ou 'horario'
        todas = self.repo.get_all()
        filtradas = [c for c in todas if c.get(tipo) == valor]
        mapa_psi = self.psi_service.get_mapa_nomes()
        
        retorno = []
        for c in filtradas:
            if c.get('idPsicologo') in mapa_psi:
                c_copy = c.copy()
                c_copy['nomePsi'] = mapa_psi[c['idPsicologo']]
                retorno.append(c_copy)
        return sorted(retorno, key=chaveDeOrdenacao)