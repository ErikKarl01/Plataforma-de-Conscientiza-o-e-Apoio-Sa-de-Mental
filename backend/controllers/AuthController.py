from flask import Blueprint, request, jsonify
from services.AuthService import AuthService

# Define o grupo de rotas de Autenticação
auth_bp = Blueprint('auth_bp', __name__)
service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        d = request.get_json()
        resultado = service.autenticar(d.get('email'), d.get('senha'))
        
        if resultado:
            return jsonify(resultado), 200
        else:
            return jsonify({'mensagem': 'Email ou senha inválidos'}), 401
            
    except ValueError as e:
        return jsonify({'erro': str(e)}), 400
    except Exception as e:
        return jsonify({'erro': 'Erro interno do servidor'}), 500