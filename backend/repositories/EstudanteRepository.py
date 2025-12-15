import json
import os

# NOME CORRETO: Plural e com ponto
FILE_PATH = 'data/estudantes.json'

class EstudanteRepository:
    def __init__(self):
        self._load()

    def _load(self):
        # Garante que a pasta existe
        if not os.path.exists('data'):
            os.makedirs('data')
        
        # Se o arquivo não existir, cria um array vazio []
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                json.dump([], f)
    
    def get_all(self):
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se der erro de leitura ou arquivo vazio, retorna lista vazia
            return []

    def create(self, aluno):
        lista = self.get_all()
        lista.append(aluno)
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)
        return aluno