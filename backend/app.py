from flask import Flask
from flask_cors import CORS # <--- 1. Importação necessária

# Importação dos Controllers (Blueprints)
from controllers.EstudanteController import estudante_bp
from controllers.PsicologoController import psicologo_bp
from controllers.LoginController import login_bp
# Se tiver outros controllers (como ConsultaController), importe aqui também
# from controllers.ConsultaController import consulta_bp 

app = Flask(__name__)

# <--- 2. Habilita CORS para todas as rotas e origens (*)
# Isso permite que o Frontend (localhost:5173) fale com o Backend
CORS(app, resources={r"/*": {"origins": "*"}})

# Registro dos Blueprints
app.register_blueprint(estudante_bp)
app.register_blueprint(psicologo_bp)
app.register_blueprint(login_bp)
# app.register_blueprint(consulta_bp) # Descomente se tiver

if __name__ == '__main__':
    app.run(debug=True)