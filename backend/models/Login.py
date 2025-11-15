from flask import request, jsonify
from .CarregarDados import carregar_dados
from werkzeug.security import check_password_hash

PSICOLOGO_DB = 'data/psicologos.json'
ESTUDANTE_DB = 'data/estudante.json'

def busca_usuario(dadosDosUsuario, email, senha):
    for usuario in dadosDosUsuario:
        if usuario.get('email') == email and check_password_hash(usuario.get('senha'), senha):
            return usuario
    return None

class Login:
    @staticmethod
    def fazerLogin():
        """
        função que pega dados de dois arquivos json e verifica se o usuário está em pelo menos uma delas
        
        função recebe dados do front
        função procura dados nas duas listas e verifica se está em pelo menos uma delas
        função retorna os dados do usuário ou menságemd e erro caso usuário não exista
        """
        dados_do_front = request.get_json() 
        
        email = dados_do_front.get('email')
        senha = dados_do_front.get('senha')
        
        dados_estudante = carregar_dados(ESTUDANTE_DB)
        dados_psicologo = carregar_dados(PSICOLOGO_DB)
        
        sessao = busca_usuario(dados_estudante, email, senha)
        
        if sessao:
            return jsonify({'usuario': sessao, 'tipo': 'estudante'}) 
        
        sessao = busca_usuario(dados_psicologo, email, senha)
        
        if sessao:
            return jsonify({'usuario': sessao, 'tipo': 'psicologo'})
            
        return jsonify({'mensagem': 'Usuário não encontrado'}), 400