class EstudanteModel:
    def __init__(self, id, nome, email, telefone, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.senha = senha

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'senha': self.senha
        }