from flask import Flask
from flask_cors import CORS
import os

from controllers.AuthController import auth_bp
from controllers.EstudanteController import estudante_bp
from controllers.PsicologoController import psicologo_bp

app = Flask(__name__)
CORS(app) 

os.makedirs('backend/data', exist_ok=True)

app.register_blueprint(auth_bp)
app.register_blueprint(estudante_bp)
app.register_blueprint(psicologo_bp)

if __name__ == '__main__':
    app.run(debug=True)