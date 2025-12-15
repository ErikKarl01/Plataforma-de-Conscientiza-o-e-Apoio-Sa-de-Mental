from werkzeug.security import check_password_hash
from email_validator import validate_email, EmailNotValidError
from repositories.EstudanteRepository import EstudanteRepository
from repositories.PsicologoRepository import PsicologoRepository

class AuthService:
    def __init__(self):
        # Instancia os repositórios para poder buscar os dados
        self.repo_estudante = EstudanteRepository()
        self.repo_psicologo = PsicologoRepository()

    def _buscar_por_email(self, lista_usuarios, email):
        """Método auxiliar interno para achar usuário na lista pelo email"""
        for usuario in lista_usuarios:
            if usuario.get('email') == email:
                return usuario
        return None

    def autenticar(self, email, senha):
        # 1. Validação básica de entrada
        if not email or not email.strip():
            raise ValueError("O email não pode estar vazio")
        if not senha:
            raise ValueError("A senha não pode estar vazia")

        # 2. Normalização do email
        try:
            v = validate_email(email, check_deliverability=False)
            email_norm = v.normalized.strip()
        except EmailNotValidError:
            raise ValueError("Formato de email inválido")

        # 3. Tenta achar no banco de ESTUDANTES
        todos_estudantes = self.repo_estudante.get_all()
        estudante = self._buscar_por_email(todos_estudantes, email_norm)
        
        if estudante:
            hash_senha = estudante.get('senha')
            if hash_senha and check_password_hash(hash_senha, senha):
                return {'usuario': estudante, 'tipo': 'estudante'}

        # 4. Tenta achar no banco de PSICÓLOGOS (se não achou estudante)
        todos_psicologos = self.repo_psicologo.get_all()
        psicologo = self._buscar_por_email(todos_psicologos, email_norm)
        
        if psicologo:
            hash_senha = psicologo.get('senha')
            if hash_senha and check_password_hash(hash_senha, senha):
                return {'usuario': psicologo, 'tipo': 'psicologo'}

        # 5. Se não achou em nenhum ou senha errada
        return None