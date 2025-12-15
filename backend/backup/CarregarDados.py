import os
import json

USUARIOS_DB = 'data/psicologos.json'
CONSULTAS_DB = 'data/consultas.json'
ESTUDANTE_DB = 'data/estudante.json'

def carregar_dados(caminho_arquivo):
    """
    Função auxiliar para carregar dados de um arquivo JSON com segurança.
    Cria o arquivo se não existir e trata arquivos vazios ou corrompidos.
    """
    if not os.path.exists(caminho_arquivo) or os.path.getsize(caminho_arquivo) == 0:
        with open(caminho_arquivo, 'w') as f:
            json.dump([], f)
        return []
    
    try:
        with open(caminho_arquivo, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"AVISO: O arquivo {caminho_arquivo} estava corrompido. Iniciando com dados limpos.")
        return []