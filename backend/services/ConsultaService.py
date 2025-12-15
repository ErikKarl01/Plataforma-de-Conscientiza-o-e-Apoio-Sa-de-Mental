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