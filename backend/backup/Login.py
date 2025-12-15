from flask import request, jsonify
from .CarregarDados import carregar_dados
from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError

PSICOLOGO_DB = 'data/psicologos.json'
ESTUDANTE_DB = 'data/estudante.json'

def busca_usuario(dadosDosUsuario, email, senha):
    for usuario in dadosDosUsuario:
        email_db = usuario.get('email')
        hash_senha_db = usuario.get('senha')
        
        if not email_db or not hash_senha_db:
            continue
        
        if email_db == email and check_password_hash(hash_senha_db, senha):
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
        try:
            dados_do_front = request.get_json()
            if not dados_do_front:
                raise ValueError("Corpo da requisição está vazio ou não é JSON")

            email = dados_do_front.get('email')
            senha = dados_do_front.get('senha')
            
            if not email or not email.strip():
                return jsonify({"erro": "O email não pode estar vazio"}), 400
            
            if not senha:
                return jsonify({"erro": "A senha não pode estar vazia"}), 400
            
            v = validate_email(email, check_deliverability=False)
            email = v.normalized.strip()

        except (ValueError, EmailNotValidError) as e:
            return jsonify({'erro': f'Dados de login inválidos: {e}'}), 400
        except Exception as e:
            return jsonify({'erro': f'Erro ao processar requisição: {e}'}), 400
        
        dados_estudante = carregar_dados(ESTUDANTE_DB)
        dados_psicologo = carregar_dados(PSICOLOGO_DB)
        
        sessao = busca_usuario(dados_estudante, email, senha)
        
        if sessao:
            return jsonify({'usuario': sessao, 'tipo': 'estudante'}) 
        
        sessao = busca_usuario(dados_psicologo, email, senha)
        
        if sessao:
            return jsonify({'usuario': sessao, 'tipo': 'psicologo'})
            
        return jsonify({'mensagem': 'Email ou senha inválidos'}), 401