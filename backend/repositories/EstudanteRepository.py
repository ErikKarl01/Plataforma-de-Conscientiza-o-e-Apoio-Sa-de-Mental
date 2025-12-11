import json
from utils.CarregarDados import carregar_dados

DB_PATH = 'data/estudante.json'

class EstudanteRepository:
    def get_all(self):
        return carregar_dados(DB_PATH)

    def save_all(self, dados):
        with open(DB_PATH, 'w') as f:
            json.dump(dados, f)

    def find_by_id(self, id):
        dados = self.get_all()
        for index, estudante in enumerate(dados):
            if estudante.get('id') == id:
                return index, estudante
        return None, None
    
    def find_by_nome_telefone(self, nome_norm, telefone):
        dados = self.get_all()
        for index, estudante in enumerate(dados):
            if estudante.get('nome', '').strip().lower() == nome_norm and \
               estudante.get('telefone', '') == telefone:
                return index, estudante
        return None, None

    def create(self, novo_estudante_dict):
        dados = self.get_all()
        # Gera ID
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_estudante_dict['id'] = novo_id
        dados.append(novo_estudante_dict)
        self.save_all(dados)
        return novo_estudante_dict

    def update(self, index, dados_atualizados):
        dados = self.get_all()
        dados[index] = dados_atualizados
        self.save_all(dados)
        return dados_atualizados

    def delete(self, index):
        dados = self.get_all()
        removido = dados.pop(index)
        self.save_all(dados)
        return removido