import json
from backend.utils.CarregarDados import carregar_dados

DB_PATH = 'data/consultas.json'

class ConsultaRepository:
    def get_all(self):
        return carregar_dados(DB_PATH)

    def save_all(self, dados):
        with open(DB_PATH, 'w') as f:
            json.dump(dados, f)

    def find_by_data_horario_psi(self, data, horario, id_psi=None):
        dados = self.get_all()
        for index, consulta in enumerate(dados):
            if consulta['data'] == data and consulta['horario'] == horario:
                if id_psi is None:
                    return index, consulta
                elif consulta.get('idPsicologo') == id_psi:
                    return index, consulta
        return None, None
    
    def find_by_psicologo(self, id_psi):
        dados = self.get_all()
        return [c for c in dados if c.get('idPsicologo') == id_psi]

    def create(self, nova_consulta_dict):
        dados = self.get_all()
        id_consulta = (max((c.get('id', -1) for c in dados), default=-1) + 1)
        nova_consulta_dict['id'] = id_consulta
        dados.append(nova_consulta_dict)
        self.save_all(dados)
        return nova_consulta_dict

    def update(self, index, consulta_dict):
        dados = self.get_all()
        dados[index] = consulta_dict
        self.save_all(dados)
        return consulta_dict

    def delete(self, index):
        dados = self.get_all()
        removido = dados.pop(index)
        self.save_all(dados)
        return removido