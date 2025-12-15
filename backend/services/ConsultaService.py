from datetime import datetime
from repositories.ConsultaRepository import ConsultaRepository
from services.PsicologoService import PsicologoService
from services.EstudanteService import EstudanteService
from utils.Validacao import validar_data_hora, validar_id

print("--- SERVICE CONSULTA CARREGADO (FINAL) ---")

def chaveDeOrdenacao(consulta): 
    try: return datetime.strptime(consulta['data'] + ' ' + consulta['horario'], '%d/%m/%Y %H:%M')
    except: return datetime.min

class ConsultaService:
    def __init__(self):
        self.repo = ConsultaRepository()
        self.psi_service = PsicologoService()
        self.est_service = EstudanteService()

    def adicionar_horario(self, dados):
        id_psi = str(dados.get('idPsicologo'))
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        
        idx, existe = self.repo.find_by_data_horario_psi(data, horario, id_psi)
        if existe: raise ValueError('Horário já existe')

        nova = {
            'nomePaciente': '', 'telPaciente': '', 'emailPaciente': '',
            'data': data, 'horario': horario, 'idPsicologo': id_psi,
            'reservado': False, 'reservadoPorEstudante': False, 'idEstudante': '',
            'duracao': dados.get('duracao', '50'), 'causa': '',
            'status': 'livre'
        }
        return self.repo.create(nova)

    def marcar_consulta_psi(self, dados):
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        id_psi = str(dados.get('idPsicologo'))
        
        index, consulta = self.repo.find_by_data_horario_psi(data, horario, id_psi)
        
        # Se existe horário livre, ocupa ele
        if consulta:
            consulta.update({
                'nomePaciente': dados.get('nomePaciente'),
                'telPaciente': dados.get('telPaciente'),
                'reservado': True,
                'reservadoPorEstudante': False,
                'status': 'confirmado'
            })
            return self.repo.update(index, consulta)
        
        # Se não existe, cria novo já ocupado
        nova = {
            'nomePaciente': dados.get('nomePaciente'),
            'telPaciente': dados.get('telPaciente'),
            'emailPaciente': '',
            'data': data, 'horario': horario, 'idPsicologo': id_psi,
            'reservado': True, 'reservadoPorEstudante': False, 'idEstudante': '',
            'duracao': '50', 'causa': 'Agendamento Manual',
            'status': 'confirmado'
        }
        return self.repo.create(nova)

    def reservar_por_estudante(self, dados):
        print(f"DEBUG SERVICE: Tentando reservar. Dados: {dados}")
        data, horario = validar_data_hora(dados.get('data'), dados.get('horario'))
        
        # MODIFICAÇÃO PRINCIPAL: Usa o ID direto se vier do frontend
        id_psi = dados.get('idPsicologo')
        
        # Se não vier ID (fallback antigo), tenta achar pelo nome
        if not id_psi:
            nome_psi = dados.get('nome')
            mapa = self.psi_service.get_mapa_nomes()
            for pid, pnome in mapa.items():
                if pnome == nome_psi:
                    id_psi = pid
                    break
        
        if not id_psi:
            print(f"ERRO: ID Psicólogo não identificado.")
            raise ValueError(f"Psicólogo não identificado para este horário.")

        id_psi = str(id_psi) # Garante string

        index, consulta = self.repo.find_by_data_horario_psi(data, horario, id_psi)
        
        if not consulta: return 404
        if consulta.get('reservado'): return 409

        consulta.update({
            'nomePaciente': dados.get('nomePaci'),
            'telPaciente': dados.get('telefonePaci'),
            'emailPaciente': dados.get('emailPaci'),
            'idEstudante': str(dados.get('idEstudante')),
            'reservado': True,
            'reservadoPorEstudante': True,
            'causa': dados.get('causa'),
            'status': 'pendente'
        })
        return self.repo.update(index, consulta)

    def confirmar_agendamento(self, dados):
        id_psi = str(dados.get('idPsicologo'))
        index, consulta = self.repo.find_by_data_horario_psi(dados.get('data'), dados.get('horario'), id_psi)
        if not consulta: return 404
        consulta['status'] = 'confirmado'
        return self.repo.update(index, consulta)

    def cancelar_reserva(self, dados):
        nome_psi = dados.get('nome')
        id_psi = str(dados.get('idPsicologo')) if 'idPsicologo' in dados else None
        
        if not id_psi and nome_psi:
            mapa = self.psi_service.get_mapa_nomes()
            for pid, pnome in mapa.items():
                if pnome == nome_psi: id_psi = pid; break
        
        index, consulta = self.repo.find_by_data_horario_psi(dados.get('data'), dados.get('horario'), id_psi)
        if not consulta: return 404

        # Se for remover fisicamente (Lixeira do Psicólogo)
        if dados.get('acao') == 'remover_fisicamente':
             return self.repo.delete(index)

        # Se for apenas cancelar (Aluno ou Rejeitar) -> Vira Livre
        consulta.update({
            'nomePaciente': '', 'telPaciente': '', 'emailPaciente': '',
            'reservado': False, 'reservadoPorEstudante': False, 'idEstudante': '', 'causa': '',
            'status': 'livre'
        })
        return self.repo.update(index, consulta)

    def remover_fisicamente(self, dados):
        id_psi = str(dados.get('idPsicologo'))
        index, consulta = self.repo.find_by_data_horario_psi(dados.get('data'), dados.get('horario'), id_psi)
        if consulta:
            return self.repo.delete(index)
        return False

    def listar_todos_livres(self):
        todas = self.repo.get_all()
        todos_psis = self.psi_service.repo.get_all()
        psi_dict = {str(p['id']): p for p in todos_psis}

        livres = []
        for c in todas:
            if not c.get('reservado'):
                c_copy = c.copy()
                psi_data = psi_dict.get(str(c.get('idPsicologo')))
                if psi_data:
                    c_copy['nomePsi'] = psi_data.get('nome')
                    c_copy['emailPsi'] = psi_data.get('email')
                else:
                    c_copy['nomePsi'] = 'Psicólogo' # Nome Genérico
                    c_copy['emailPsi'] = ''
                livres.append(c_copy)
        return sorted(livres, key=chaveDeOrdenacao)

    def listar_solicitacoes_estudante(self, id_est):
        todas = self.repo.get_all()
        mapa = self.psi_service.get_mapa_nomes()
        retorno = []
        id_est = str(id_est)
        
        for c in todas:
            if c.get('reservadoPorEstudante') and str(c.get('idEstudante')) == id_est:
                c_copy = c.copy()
                c_copy['nomePsi'] = mapa.get(c.get('idPsicologo'), 'Psicólogo')
                c_copy['status_desc'] = 'Pendente' if c.get('status') == 'pendente' else 'Confirmada'
                retorno.append(c_copy)
        return sorted(retorno, key=chaveDeOrdenacao)
    
    # Stubs
    def listar_livres_por_psi_nome(self, n, e): return []
    def buscar_generico(self, t, v): return []
    def recuperar_consulta(self, d): return 404
    def consultar_historico_estudante(self, i): return []
    def consultar_historico_psicologo(self, i): return []