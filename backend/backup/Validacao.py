# Validacoes.py
from datetime import datetime
import phonenumbers
from email_validator import validate_email, EmailNotValidError

def validar_nome(nome, nome_campo="Nome"):
    if not nome or not nome.strip():
        raise ValueError(f"O {nome_campo} não pode estar vazio")
    if any(char.isdigit() for char in nome):
        raise ValueError(f"O {nome_campo} não pode conter números")
    return nome.strip()

def validar_email_func(email, nome_campo="Email"):
    if not email or not email.strip():
        raise ValueError(f"O {nome_campo} não pode estar vazio")
    try:
        v = validate_email(email, check_deliverability=False)
        return v.normalized
    except EmailNotValidError as e:
        raise ValueError(f"{nome_campo} inválido: {str(e)}")

def validar_telefone(telefone, nome_campo="Telefone"):
    if not telefone or not telefone.strip():
        raise ValueError(f"O {nome_campo} não pode estar vazio")
    try:
        num_telefone = phonenumbers.parse(telefone, "BR")
        if not phonenumbers.is_valid_number(num_telefone):
            raise ValueError(f"Número de {nome_campo} inválido")
        return phonenumbers.format_number(num_telefone, phonenumbers.PhoneNumberFormat.E164)
    except Exception as e:
        raise ValueError(f"{nome_campo} inválido: {str(e)}")

def validar_data_hora(data, horario):
    try:
        datetime.strptime(f'{data} {horario}', '%d/%m/%Y %H:%M')
        return data, horario
    except (ValueError, TypeError):
        raise ValueError("Formato de data ou hora inválido")

def validar_id(id_val):
    try:
        return int(id_val)
    except (ValueError, TypeError):
        raise ValueError("ID inválido")

def validar_duracao(duracao):
    if not duracao: return None
    try:
        d = int(duracao)
        if d < 20 or d > 90:
            raise ValueError("A duração deve ser entre 20 e 90 minutos")
        return d
    except (ValueError, TypeError):
        raise ValueError("A duração deve ser um número inteiro válido")

def validar_causa(causa):
    if not causa: return ''
    if any(char.isdigit() for char in causa):
        raise ValueError("A causa não pode conter números")
    return causa.strip()