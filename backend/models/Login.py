from flask import Flask, request, jsonify
import json
import os
from Psicologo import carregar_dados

app = Flask(__name__)

USUARIOS_DB = 'backend/data/psicologos.json'

class Estudante:
    def cadastrar():
        dados_do_front = request.get_json()
        
        n 