from repositories.PsicologoRepository import PsicologoRepository
from utils.Validacao import validar_nome, validar_email_func, validar_telefone, validar_crp, validar_senha

class PsicologoService:
    def __init__(self):
        self.repo = PsicologoRepository()

    def cadastrar(self, dados):
        nome = validar_nome(dados.get('nome'))
        email = validar_email_func(dados.get('email'))
        senha = validar_senha(dados.get('senha'))
        telefone = validar_telefone(dados.get('telefone'))
        crp = validar_crp(dados.get('crp'))

        # Verifica duplicidade
        if self.buscar_por_email(email):
            raise ValueError("Email já cadastrado.")

        novo_psi = {
            'id': self._gerar_id(),
            'nome': nome,
            'email': email,
            'senha': senha,
            'telefone': telefone,
            'crp': crp
        }
        return self.repo.create(novo_psi)

    def buscar_por_email(self, email):
        todos = self.repo.get_all()
        for p in todos:
            if p['email'] == email:
                return p
        return None

    def buscar_por_nome_email(self, nome, email):
        todos = self.repo.get_all()
        for p in todos:
            if p['email'] == email and p['nome'] == nome:
                return p
        return None

    def get_mapa_nomes(self):
        # Retorna dicionário {id: nome} para facilitar busca
        todos = self.repo.get_all()
        return {str(p['id']): p['nome'] for p in todos}

    def _gerar_id(self):
        todos = self.repo.get_all()
        if not todos: return "1"
        ids = [int(p['id']) for p in todos]
        return str(max(ids) + 1)