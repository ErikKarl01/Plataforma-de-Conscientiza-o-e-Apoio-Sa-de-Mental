import json
import os

# Define o caminho correto do arquivo
FILE_PATH = 'data/consultas.json'

class ConsultaRepository:
    def __init__(self):
        self._load()

    def _load(self):
        # Garante que a pasta data existe
        if not os.path.exists('data'):
            os.makedirs('data')
        # Garante que o arquivo existe com um array vazio []
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_all(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def get_by_id(self, id_consulta):
        todos = self.get_all()
        for c in todos:
            if str(c['id']) == str(id_consulta):
                return c
        return None

    def create(self, consulta):
        lista = self.get_all()
        lista.append(consulta)
        self._save(lista)
        return consulta

    def update(self, consulta_atualizada):
        lista = self.get_all()
        for i, c in enumerate(lista):
            if str(c['id']) == str(consulta_atualizada['id']):
                lista[i] = consulta_atualizada
                self._save(lista)
                return True
        return False

    def delete(self, id_consulta):
        lista = self.get_all()
        nova_lista = [c for c in lista if str(c['id']) != str(id_consulta)]
        self._save(nova_lista)

    def _save(self, lista):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)