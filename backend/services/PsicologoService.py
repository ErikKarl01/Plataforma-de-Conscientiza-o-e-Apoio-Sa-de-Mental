from werkzeug.security import generate_password_hash
from backend.repositories.PsicologoRepository import PsicologoRepository
from backend.utils.Validacao import validar_nome, validar_email_func, validar_telefone

class PsicologoService:
    def __init__(self):
        self.repo = PsicologoRepository()

    def cadastrar(self, dados):
        nome = validar_nome(dados.get('nome'))
        email = validar_email_func(dados.get('email'))
        telefone = validar_telefone(dados.get('telefone'))
        crp = dados.get('crp', '').strip()
        senha = dados.get('senha', '').strip()

        if not crp: raise ValueError("O CRP não pode estar vazio")
        if not senha: raise ValueError("A senha não pode estar vazia")

        novo_usuario = {
            'nome': nome, 'email': email, 'telefone': telefone, 'crp': crp,
            'senha': generate_password_hash(senha)
        }
        return self.repo.create(novo_usuario)

    def buscar_por_nome_email(self, nome, email):
        nome = validar_nome(nome)
        email = validar_email_func(email)
        return self.repo.find_by_nome_email(nome, email)

    def buscar_por_id(self, id):
        return self.repo.find_by_id(id)
        
    def get_mapa_nomes(self):
        # Retorna um dicionário {id: nome} para facilitar displays
        todos = self.repo.get_all()
        return {p['id']: p['nome'] for p in todos}