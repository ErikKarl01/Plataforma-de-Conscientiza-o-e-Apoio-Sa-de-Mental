from werkzeug.security import generate_password_hash
from backend.repositories.EstudanteRepository import EstudanteRepository
from backend.utils.Validacao import validar_nome, validar_email_func, validar_telefone, validar_id

class EstudanteService:
    def __init__(self):
        self.repo = EstudanteRepository()

    def cadastrar(self, dados):
        nome = validar_nome(dados.get('nome'))
        email = validar_email_func(dados.get('email'))
        telefone = validar_telefone(dados.get('telefone'))
        senha = dados.get('senha')
        
        if not senha or not senha.strip():
            raise ValueError("A senha não pode estar vazia")

        novo_usuario = {
            'nome': nome, 
            'email': email, 
            'telefone': telefone,
            'senha': generate_password_hash(senha.strip())
        }
        return self.repo.create(novo_usuario)

    def editar(self, dados):
        if not dados or 'id' not in dados:
            raise ValueError('Id não fornecido')
            
        id_est = validar_id(dados['id'])
        index, estudante = self.repo.find_by_id(id_est)
        
        if not estudante:
            return None
        
        estudante.update({
            'nome': validar_nome(dados.get('nome')),
            'email': validar_email_func(dados.get('email')),
            'telefone': validar_telefone(dados.get('telefone'))
        })
        
        return self.repo.update(index, estudante)

    def excluir(self, dados):
        if not dados or 'id' not in dados:
            raise ValueError('Id não fornecido')
            
        id_est = validar_id(dados['id'])
        index, estudante = self.repo.find_by_id(id_est)
        
        if not estudante:
            return None
            
        return self.repo.delete(index)
    
    def buscar_por_nome_telefone(self, nome, telefone):
        return self.repo.find_by_nome_telefone(nome.strip().lower(), telefone)