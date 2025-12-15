import json
from utils.CarregarDados import carregar_dados

DB_PATH = 'data/psicologos.json'

class PsicologoRepository:
    def get_all(self):
        return carregar_dados(DB_PATH)

    def save_all(self, dados):
        with open(DB_PATH, 'w') as f:
            json.dump(dados, f)

    def find_by_id(self, id):
        dados = self.get_all()
        for psi in dados:
            if psi.get('id') == id:
                return psi
        return None

    def find_by_nome_email(self, nome, email):
        dados = self.get_all()
        nome_norm = nome.strip().lower()
        email_norm = email.strip().lower()
        for psi in dados:
            if psi['nome'].strip().lower() == nome_norm and \
               psi['email'].strip().lower() == email_norm:
                return psi
        return None

    def create(self, novo_psi_dict):
        dados = self.get_all()
        novo_id = (max((u.get('id', -1) for u in dados), default=-1) + 1)
        novo_psi_dict['id'] = novo_id
        dados.append(novo_psi_dict)
        self.save_all(dados)
        return novo_psi_dict