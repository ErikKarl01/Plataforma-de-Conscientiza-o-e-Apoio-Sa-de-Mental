import re
from datetime import datetime

def validar_id(valor):
    if valor is None or valor == '':
        return None
    return str(valor)

def validar_nome(nome, campo="Nome"):
    if not nome or len(nome.strip()) < 2:
        raise ValueError(f"{campo} deve ter pelo menos 2 caracteres.")
    return nome.strip()

def validar_email_func(email, campo="Email"):
    if not email or '@' not in email:
        raise ValueError(f"{campo} inválido.")
    return email.strip()

def validar_telefone(telefone, campo="Telefone"):
    if not telefone or len(telefone.strip()) < 8:
        raise ValueError(f"{campo} inválido (mínimo 8 dígitos).")
    return telefone.strip()

def validar_data_hora(data, horario):
    if not data or not horario:
        raise ValueError("Data e Horário são obrigatórios.")
    # Opcional: Validar formato DD/MM/AAAA e HH:MM
    return data, horario

def validar_duracao(duracao):
    if not duracao:
        return '50'
    return str(duracao)

def validar_causa(causa):
    if not causa:
        return ''
    return causa.strip()

# --- AS FUNÇÕES QUE FALTAVAM E CAUSARAM O ERRO ---

def validar_crp(crp):
    if not crp or len(crp.strip()) < 4:
        raise ValueError("CRP inválido. Deve conter identificação do conselho.")
    return crp.strip()

def validar_senha(senha):
    if not senha or len(senha) < 4:
        raise ValueError("A senha deve ter pelo menos 4 caracteres.")
    return senha.strip()