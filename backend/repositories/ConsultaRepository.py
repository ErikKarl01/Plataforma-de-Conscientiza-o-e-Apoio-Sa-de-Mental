import json
import os

FILE_PATH = 'data/consultas.json'

class ConsultaRepository:
    def __init__(self):
        self.consultas = self._load()

    def _load(self):
        if not os.path.exists('data'):
            os.makedirs('data')
        if not os.path.exists(FILE_PATH):
            with open(FILE_PATH, 'w') as f:
                json.dump([], f)
            return []
        try:
            with open(FILE_PATH, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def _save(self):
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump(self.consultas, f, indent=4, ensure_ascii=False)

    def create(self, consulta):
        self.consultas.append(consulta)
        self._save() # <--- OBRIGATÓRIO PARA NÃO PERDER DADOS
        return consulta

    def update(self, index, dados_novos):
        if 0 <= index < len(self.consultas):
            self.consultas[index] = dados_novos
            self._save() # <--- SALVA A EDIÇÃO
            return self.consultas[index]
        return None

    def delete(self, index):
        if 0 <= index < len(self.consultas):
            removido = self.consultas.pop(index)
            self._save() # <--- SALVA A REMOÇÃO
            return removido
        return None

    def get_all(self):
        return self.consultas

    def find_by_data_horario_psi(self, data, horario, id_psi=None):
        # Busca exata. O ID é convertido para string para garantir
        id_psi = str(id_psi) if id_psi else None
        
        for i, c in enumerate(self.consultas):
            # Compara Data, Hora e (se fornecido) o ID do Psicólogo
            if c['data'] == data and c['horario'] == horario:
                if id_psi:
                    if str(c.get('idPsicologo')) == id_psi:
                        return i, c
                else:
                    return i, c
        return None, None

    def find_by_psicologo(self, id_psi):
        return [c for c in self.consultas if str(c.get('idPsicologo')) == str(id_psi)]

    def _get_historico(self):
        # Apenas para compatibilidade, se usar histórico separado
        return []
    
    def adicionar_historico(self, consulta):
        # Opcional: Salvar em outro arquivo
        pass