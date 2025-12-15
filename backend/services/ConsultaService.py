from repositories.ConsultaRepository import ConsultaRepository

class ConsultaService:
    def __init__(self):
        self.repo = ConsultaRepository()

    def adicionar_horario(self, dados):
        # Cria horário LIVRE
        if 'idPsicologo' not in dados or 'data' not in dados or 'hora' not in dados:
            raise ValueError("Dados incompletos para adicionar horário.")

        nova_consulta = {
            'id': self._gerar_id(),
            'idPsicologo': str(dados['idPsicologo']),
            'data': dados['data'],
            'hora': dados['hora'],
            'duracao': int(dados.get('duracao', 50)), # Garante que é número
            'status': 'livre',
            'idAluno': None,
            'nomeAluno': None
        }
        return self.repo.create(nova_consulta)

    def marcar_consulta_psi(self, dados):
        # Cria consulta MANUAL
        if 'nomePaciente' not in dados:
            raise ValueError("Nome do paciente é obrigatório.")

        nova_consulta = {
            'id': self._gerar_id(),
            'idPsicologo': str(dados['idPsicologo']),
            'data': dados['data'],
            'hora': dados['hora'],
            'duracao': int(dados.get('duracao', 50)), # Garante que é número
            'status': 'confirmado',
            'idAluno': 'manual',
            'nomeAluno': dados['nomePaciente']
        }
        return self.repo.create(nova_consulta)

    def _gerar_id(self):
        todos = self.repo.get_all()
        if not todos: return "1"
        # Garante que pega o maior ID numérico
        ids = [int(c.get('id', 0)) for c in todos]
        return str(max(ids) + 1)
        
    def confirmar_agendamento(self, dados):
        consulta = self.repo.get_by_id(dados['id'])
        if not consulta: return 404
        consulta['status'] = 'confirmado'
        self.repo.update(consulta)
        return 200

    def cancelar_reserva(self, dados):
        consulta = self.repo.get_by_id(dados['id'])
        if not consulta: return 404
        # Se for manual, deleta. Se for aluno, libera a vaga.
        if consulta.get('idAluno') == 'manual':
            self.repo.delete(dados['id'])
        else:
            consulta['status'] = 'livre'
            consulta['idAluno'] = None
            consulta['nomeAluno'] = None
            self.repo.update(consulta)
        return 200

    def remover_fisicamente(self, dados):
        self.repo.delete(dados['id'])

    # ... (métodos anteriores mantidos) ...

    def listar_por_aluno(self, id_aluno):
        todos = self.repo.get_all()
        # Retorna tudo onde o aluno é o dono da consulta
        return [c for c in todos if str(c.get('idAluno')) == str(id_aluno)]

    def solicitar_agendamento(self, dados):
        # Busca a consulta pelo ID (o horário livre)
        consulta = self.repo.get_by_id(dados['idConsulta'])
        if not consulta: return 404
        
        # Verifica se ainda está livre
        if consulta['status'] != 'livre':
            raise ValueError("Este horário não está mais disponível.")

        # Atualiza status e vincula ao aluno
        consulta['status'] = 'pendente'
        consulta['idAluno'] = str(dados['idAluno'])
        consulta['nomeAluno'] = dados['nomeAluno']
        
        self.repo.update(consulta)
        return consulta
    
    # ... métodos anteriores ...

    def remarcar_consulta(self, dados):
        # dados = { 'idAntiga': '...', 'idNova': '...' }
        
        # 1. Busca as duas consultas
        consulta_antiga = self.repo.get_by_id(dados['idAntiga'])
        consulta_nova = self.repo.get_by_id(dados['idNova'])

        if not consulta_antiga or not consulta_nova:
            raise ValueError("Horário não encontrado.")
        
        if consulta_nova['status'] != 'livre':
            raise ValueError("O novo horário escolhido não está mais disponível.")

        # 2. Copia os dados do paciente para a nova
        consulta_nova['idAluno'] = consulta_antiga.get('idAluno')
        consulta_nova['nomeAluno'] = consulta_antiga.get('nomeAluno')
        
        # Mantém o status que a antiga tinha (se era confirmado, continua confirmado. Se pendente, continua pendente)
        # Exception: Se for remarcação pelo aluno, volta pra 'pendente' pra o psicólogo aprovar de novo?
        # Vamos assumir que se o psicólogo remarca, fica confirmado. Se o aluno remarca, vira pendente.
        
        origem = dados.get('solicitante', 'aluno') # 'aluno' ou 'psicologo'
        
        if origem == 'psicologo':
            consulta_nova['status'] = 'confirmado'
        else:
            consulta_nova['status'] = 'pendente'

        # 3. Limpa a consulta antiga (vira horário livre novamente)
        consulta_antiga['idAluno'] = None
        consulta_antiga['nomeAluno'] = None
        consulta_antiga['status'] = 'livre'

        # 4. Salva ambas
        self.repo.update(consulta_antiga)
        self.repo.update(consulta_nova)
        
        return consulta_nova