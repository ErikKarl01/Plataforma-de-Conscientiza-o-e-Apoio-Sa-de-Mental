from repositories.EstudanteRepository import EstudanteRepository

class EstudanteService:
    def __init__(self):
        self.repo = EstudanteRepository()

    def cadastrar(self, dados):
        # Validação simples para evitar erro 400 misterioso
        if not dados.get('email') or '@' not in dados.get('email'):
            raise ValueError("Email inválido")
        if not dados.get('senha') or len(dados.get('senha')) < 3:
            raise ValueError("Senha muito curta")
        
        # Verifica se já existe
        todos = self.repo.get_all()
        for a in todos:
            if a['email'] == dados['email']:
                raise ValueError("Email já cadastrado")

        novo_aluno = {
            'id': str(len(todos) + 1),
            'nome': dados['nome'],
            'email': dados['email'],
            'senha': dados['senha'],
            'telefone': dados.get('telefone', '')
        }
        
        return self.repo.create(novo_aluno)