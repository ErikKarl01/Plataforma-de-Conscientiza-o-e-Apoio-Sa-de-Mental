import json
from datetime import datetime, timedelta
from backend.utils.CarregarDados import carregar_dados

DB_PATH = 'backend/data/consultas.json'
DB_HIST = 'backend/data/historico.json'

class ConsultaRepository:
    
    def _salvar_arquivo_generico(self, dados, caminho):
        with open(caminho, 'w') as f:
            json.dump(dados, f, indent=4)

    def _get_historico(self):
        return carregar_dados(DB_HIST)

    def _save_historico(self, dados):
        self._salvar_arquivo_generico(dados, DB_HIST)

    def _limpar_historico_antigo(self):
        historico = self._get_historico()
        agora = datetime.now()
        historico_atualizado = []
        alterado = False

        for item in historico:
            if 'dataExclusao' in item:
                try:
                    dt_exclusao = datetime.strptime(item['dataExclusao'], '%d/%m/%Y %H:%M:%S')
                    if (agora - dt_exclusao).days <= 5:
                        historico_atualizado.append(item)
                    else:
                        alterado = True
                except:
                    historico_atualizado.append(item)
            else:
                historico_atualizado.append(item)
        
        if alterado:
            self._save_historico(historico_atualizado)

    def get_all(self):
        return carregar_dados(DB_PATH)

    def save_all(self, dados):
        self._salvar_arquivo_generico(dados, DB_PATH)

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
        self._limpar_historico_antigo()
        
        dados = self.get_all()
        historico = self._get_historico()
        
        removido = dados.pop(index)
        removido['dataExclusao'] = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        
        historico.append(removido)
        
        self.save_all(dados)
        self._save_historico(historico)
        
        return removido

    def adicionar_historico(self, dados):
        self._limpar_historico_antigo()
        
        historico = self._get_historico()
        historico.append(dados)
        self._save_historico(historico)

    def recuperar_do_historico(self, data, horario, id_psi):
        self._limpar_historico_antigo()

        historico = self._get_historico()
        item_retorno = None
        idx_remover = -1
        
        for i, item in enumerate(historico):
            if item.get('data') == data and item.get('horario') == horario and item.get('idPsicologo') == id_psi:
                item_retorno = item
                idx_remover = i
                break
        
        if idx_remover != -1:
            historico.pop(idx_remover)
            self._save_historico(historico)
        
        return item_retorno