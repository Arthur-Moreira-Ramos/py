"""Dados totalmente fictícios, exclusivamente para visualização; não há persistência."""
SUMMARY = {'saldo': 3500, 'rendas': 5200, 'despesas': 1700, 'poupado': 900}
TRANSACTIONS = [
    ('Aluguel', 'Moradia', '05 nov 2026', -1200, 'Pago'),
    ('Freelance de design', 'Trabalho extra', '04 nov 2026', 700, 'Recebido'),
    ('Supermercado', 'Alimentação', '03 nov 2026', -350, 'Pago'),
    ('Transporte', 'Mobilidade', '02 nov 2026', -150, 'Pago'),
    ('Salário', 'Trabalho', '01 nov 2026', 4500, 'Recebido'),
]
INCOME = [
    ('Salário principal', 'Mensal', 4500, '01 nov 2026', 'Ativa'),
    ('Freelance de design', 'Variável', 700, '04 nov 2026', 'Ativa'),
]
EXPENSES = [
    ('Aluguel', 'Moradia', 1200, '05 nov 2026', 'Paga'),
    ('Supermercado', 'Alimentação', 350, '03 nov 2026', 'Paga'),
    ('Transporte', 'Mobilidade', 150, '02 nov 2026', 'Paga'),
]
CATEGORIES = [
    ('Moradia', 'Despesas fixas', 1200, '#60A5FA'),
    ('Alimentação', 'Despesas variáveis', 350, '#FBBF24'),
    ('Mobilidade', 'Despesas variáveis', 150, '#A78BFA'),
    ('Saúde', 'Despesas variáveis', 0, '#34D399'),
    ('Lazer', 'Despesas variáveis', 0, '#FB7185'),
]
GOALS = [
    ('Reserva de emergência', 'Segurança financeira', 3000, 5000, 'Dez 2027', '#10B981'),
    ('Viagem de férias', 'Experiências', 850, 2500, 'Jul 2027', '#60A5FA'),
    ('Notebook novo', 'Tecnologia', 400, 4000, 'Mar 2028', '#A78BFA'),
]
RULES = [('Reserva de emergência', 50, '#10B981'), ('Viagem de férias', 30, '#60A5FA'), ('Notebook novo', 20, '#A78BFA')]
CONTRIBUTIONS = [('Reserva de emergência', 400, '06 nov 2026'), ('Viagem de férias', 250, '06 nov 2026'), ('Notebook novo', 100, '06 nov 2026')]

def money(value):
    return f'R$ {value:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
