class PsicologoModel:
    def __init__(self, id, nome, email, telefone, crp, senha):
        self.id = id
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.crp = crp
        self.senha = senha

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'email': self.email,
            'telefone': self.telefone,
            'crp': self.crp,
            'senha': self.senha
        }