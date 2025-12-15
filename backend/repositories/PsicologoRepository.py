import json
import os

FILE_PATH = 'data/psicologos.json'

class PsicologoRepository:
    def __init__(self):
        self._load()

    def _load(self):
        if not os.path.exists('data'): os.makedirs('data')
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w') as f: json.dump([], f)
    
    def get_all(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return []

    def create(self, psi):
        lista = self.get_all()
        lista.append(psi)
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)
        return psi