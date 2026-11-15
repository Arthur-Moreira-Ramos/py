"""Telas conectadas aos controllers PostgreSQL do MeuBolso."""
from datetime import date
from decimal import Decimal
import tkinter as tk
from tkinter import ttk, messagebox
from .styles import *
from .components import lbl, card, stat, section_header, progress, ActionButton, Icon
from .data_demo import money

# Instância definida pelo MainView após selecionar o usuário.
controller = None

CONFIG = {
    'Rendas': ('renda', 'Minhas rendas', [
        ('descricao', 'Descrição', 'text'), ('valor', 'Valor (R$)', 'money'),
        ('periodicidade', 'Periodicidade', ['DIARIA', 'SEMANAL', 'MENSAL']),
        ('ativa', 'Ativa', ['Sim', 'Não'])]),
    'Categorias': ('categoria_despesa', 'Categorias', [
        ('nome', 'Nome da categoria', 'text'), ('descricao', 'Descrição', 'text')]),
    'Despesas': ('despesa', 'Minhas despesas', [
        ('descricao', 'Descrição', 'text'), ('valor', 'Valor (R$)', 'money'),
        ('categoria_id', 'Categoria', 'category'), ('tipo',
                                                    'Tipo', ['FIXA', 'VARIAVEL']),
        ('data_despesa', 'Data da despesa', 'date'), ('pago', 'Paga', ['Sim', 'Não'])]),
    'Objetivos': ('objetivo_financeiro', 'Objetivos financeiros', [
        ('descricao', 'Objetivo', 'text'), ('valor_meta',
                                            'Valor da meta (R$)', 'money'),
        ('data_inicio', 'Início', 'date'), ('data_limite', 'Prazo', 'date')]),
    'Regras': ('regra_distribuicao', 'Regras de distribuição', [
        ('objetivo_id', 'Objetivo', 'goal'), ('porcentagem', 'Porcentagem (%)', 'money')]),
    'Aportes': ('aporte_objetivo', 'Aportes para objetivos', [
        ('objetivo_id', 'Objetivo', 'goal'), ('valor', 'Valor (R$)', 'money'),
        ('data_aporte', 'Data do aporte', 'date')]),
}
ACCENTS = [GREEN, BLUE, AMBER, PURPLE, RED]


def cols(parent, n=2):
    frame = tk.Frame(parent, bg=BG)
    frame.pack(fill='x', pady=(0, 14))
    out = []
    for i in range(n):
        frame.grid_columnconfigure(i, weight=1, uniform='col')
        box = tk.Frame(frame, bg=BG)
        box.grid(row=0, column=i, sticky='nsew',
                 padx=(0, 10) if i < n-1 else 0)
        out.append(box)
    return out


def panel_title(parent, title, hint=''):
    line = tk.Frame(parent, bg=CARD)
    line.pack(fill='x', pady=(0, 12))
    lbl(line, title, 13, WHITE, True, bg=CARD).pack(side='left')
    if hint:
        lbl(line, hint, 9, DIM, bg=CARD).pack(side='right')


def note(parent, title, description):
    area = tk.Frame(parent, bg=GREEN_SOFT, padx=16, pady=12)
    area.pack(fill='x', pady=(2, 16))
    lbl(area, title, 11, GREEN, True, bg=GREEN_SOFT).pack(anchor='w')
    lbl(area, description, 10, TEXT, bg=GREEN_SOFT,
        wraplength=950).pack(anchor='w', pady=(4, 0))


def fmt(v):
    if isinstance(v, bool):
        return 'Sim' if v else 'Não'
    if isinstance(v, date):
        return v.strftime('%d/%m/%Y')
    if isinstance(v, Decimal):
        return money(v)
    return str(v or '')


def dashboard(root, navigate, open_form):
    d = controller.resumo()
    section_header(root, 'Painel geral', 'Seu dinheiro, suas escolhas. Tudo em um só lugar.',
                   'Nova movimentação', lambda: open_form('Nova movimentação'))
    note(root, 'Dados conectados ao PostgreSQL',
         'Renda é uma projeção mensal (diária × 30; semanal × 52/12). Despesas e aportes usam registros de 1º até hoje no mês atual.')
    info = [('Saldo projetado', d['saldo'], 'Após despesas e aportes', WHITE, 'wallet'),
            ('Rendas previstas', d['receita'],
             f"{d['fontes']} fonte(s) ativa(s)", GREEN, 'up'),
            ('Despesas registradas',
             d['despesas'], f"{d['quantidade_despesas']} despesa(s) no mês", RED, 'down'),
            ('Aportes registrados', d['aportes'], 'Valores efetivamente reservados', BLUE, 'goal')]
    for slot, (title, value, desc, col, badge) in zip(cols(root, 4), info):
        stat(slot, title, money(value), desc, col,
             badge, True).pack(fill='both', expand=True)
    left, right = cols(root)
    a, ai = card(left)
    a.pack(fill='both', expand=True)
    panel_title(ai, 'Despesas por categoria', 'Mês até hoje')
    categories = [c for c in d['categorias'] if c['total'] > 0]
    if not categories:
        lbl(ai, 'Nenhuma despesa registrada neste mês.',
            11, MUTED, bg=CARD).pack(anchor='w', pady=12)
    else:
        total = sum(c['total'] for c in categories)
        for i, c in enumerate(categories):
            row = tk.Frame(ai, bg=CARD)
            row.pack(fill='x', pady=6)
            lbl(row, c['nome'], 10, TEXT, bg=CARD).pack(side='left')
            lbl(row, money(c['total']), 10, WHITE,
                True, bg=CARD).pack(side='right')
            progress(ai, float(c['total']/total), ACCENTS[i % len(ACCENTS)],
                     height=7, animate=False).pack(fill='x', pady=(0, 5))
    b, bi = card(right)
    b.pack(fill='both', expand=True)
    panel_title(bi, 'Progresso dos objetivos',
                f"{len(controller.metas())} metas")
    goals = controller.metas()
    if not goals:
        lbl(bi, 'Cadastre um objetivo para acompanhar o progresso.',
            11, MUTED, bg=CARD).pack(anchor='w', pady=12)
    for i, g in enumerate(goals[:5]):
        ratio = float(g['acumulado']/g['valor_meta'])
        r = tk.Frame(bi, bg=CARD)
        r.pack(fill='x', pady=(4, 3))
        lbl(r, g['descricao'], 10, TEXT, bg=CARD).pack(side='left')
        lbl(r, f'{ratio:.0%}', 10, MUTED, bg=CARD).pack(side='right')
        progress(bi, ratio, ACCENTS[i % len(ACCENTS)], height=7, animate=False).pack(
            fill='x', pady=(0, 11))
    a, ai = card(root)
    a.pack(fill='x', pady=(0, 12))
    panel_title(ai, 'Últimas despesas registradas')
    if not d['ultimas']:
        lbl(ai, 'Nenhum lançamento ainda.', 10, MUTED, bg=CARD).pack(anchor='w')
    for v in d['ultimas']:
        row = tk.Frame(ai, bg=CARD)
        row.pack(fill='x', pady=6)
        lbl(row, f"{v['descricao']}   ·   {fmt(v['data_despesa'])}",
            10, TEXT, bg=CARD).pack(side='left')
        lbl(row, '−'+money(v['valor']), 11, RED,
            True, bg=CARD).pack(side='right')


def reference_options(kind):
    if kind == 'category':
        items = controller.listar('categoria_despesa')
        return [(c['id'], c['nome']) for c in items]
    if kind == 'goal':
        items = controller.metas()
        return [(c['id'], c['descricao']) for c in items]
    return []


def table_rows(root, items, specs, open_form, table_name, navigate):
    outer, inner = card(root)
    outer.pack(fill='x', pady=(0, 18))
    panel_title(inner, 'Registros cadastrados', f'{len(items)} encontrado(s)')
    if not items:
        lbl(inner, 'Nenhum registro cadastrado.', 11,
            MUTED, bg=CARD).pack(anchor='w', pady=12)
        return
    shown = [s for s in specs if s[0] not in (
        'usuario_id', 'categoria_id', 'objetivo_id')]
    for item in items:
        row = tk.Frame(inner, bg=CARD, pady=10)
        row.pack(fill='x')
        lbl(row, f"#{item['id']}   " + '  |  '.join(f'{label}: {fmt(item.get(key))}' for key, label,
            _ in shown), 10, TEXT, bg=CARD, wraplength=800).pack(side='left', fill='x', expand=True)
        ActionButton(row, 'Editar', lambda r=item: open_form(
            (table_name, r)), primary=False, small=True).pack(side='right', padx=(8, 0))

        def delete(r=item):
            if not messagebox.askyesno('Confirmar exclusão', f"Excluir registro #{r['id']}? Esta ação não pode ser desfeita."):
                return
            try:
                controller.excluir(CONFIG[table_name][0], r['id'])
                navigate(table_name)
            except Exception as e:
                messagebox.showerror('Não foi possível excluir', str(e))
        ActionButton(row, 'Excluir', delete, primary=False,
                     small=True).pack(side='right')
        tk.Frame(inner, bg=BORDER, height=1).pack(fill='x')


def listing(section):
    def render(root, navigate, open_form):
        table, title, spec = CONFIG[section]
        section_header(root, title, 'Gerencie seus registros no banco de dados.',
                       'Novo registro', lambda: open_form(section))
        if section == 'Rendas':
            d = controller.resumo()
            note(root, 'Previsão mensal de rendimentos',
                 f"Total estimado das fontes ativas: {money(d['receita'])}. As fontes são recorrentes; ainda não representam entradas individuais confirmadas.")
        elif section == 'Regras':
            note(root, 'Distribuição do saldo',
                 'As porcentagens são sugestões. Não geram aportes automaticamente; a soma das regras não pode exceder 100%.')
            for r in controller.sugestoes():
                c, i = card(root, 10)
                c.pack(fill='x', pady=3)
                lbl(i, f"{r['descricao']} — {r['porcentagem']}%: {money(r['sugerido'])}",
                    11, TEXT, bg=CARD).pack(anchor='w')
        elif section == 'Objetivos':
            for g in controller.metas():
                c, i = card(root, 12)
                c.pack(fill='x', pady=(0, 7))
                ratio = float(g['acumulado']/g['valor_meta'])
                lbl(i, f"{g['descricao']}  ·  {money(g['acumulado'])} de {money(g['valor_meta'])}  ({ratio:.0%})",
                    11, WHITE, True, bg=CARD).pack(anchor='w')
                progress(i, ratio, GREEN, height=8, animate=False).pack(
                    fill='x', pady=(6, 0))
        table_rows(root, controller.listar(table),
                   spec, open_form, section, navigate)
    return render


def form_page(root, request, navigate, open_form):
    if isinstance(request, tuple):
        section, record = request
    else:
        section, record = request, None
    if section == 'Nova movimentação':
        section_header(root, 'Nova movimentação',
                       'Selecione o tipo de registro que deseja criar.')
        note(root, 'Tipos de movimentação',
             'A renda cadastra uma fonte recorrente. A despesa registra um gasto com data e categoria.')
        ActionButton(root, 'Registrar despesa', lambda: open_form(
            'Despesas')).pack(anchor='w', pady=10)
        ActionButton(root, 'Cadastrar fonte de renda', lambda: open_form(
            'Rendas'), primary=False).pack(anchor='w', pady=10)
        return
    table, title, spec = CONFIG[section]
    section_header(root, ('Editar' if record else 'Cadastrar')+' — ' +
                   title, 'Preencha os campos e confirme para gravar no PostgreSQL.')
    outer, inner = card(root, 24)
    outer.pack(fill='x')
    values = {}
    selected = {}
    for key, label, kind in spec:
        lbl(inner, label, 10, MUTED, bg=CARD).pack(anchor='w', pady=(12, 4))
        value = record.get(key) if record else None
        if isinstance(kind, list) or kind in ('category', 'goal'):
            entries = reference_options(kind) if isinstance(
                kind, str) else [(name, name) for name in kind]
            if not entries:
                lbl(inner, 'Cadastre primeiro o registro relacionado.',
                    10, RED, bg=CARD).pack(anchor='w')
                values[key] = None
                continue
            mapping = {f'{label} (#{id})' if kind in (
                'category', 'goal') else str(label): id for id, label in entries}
            choices = list(mapping)
            if isinstance(value, bool):
                value = 'Sim' if value else 'Não'
            sel = next((name for name, raw in mapping.items()
                       if str(raw) == str(value)), choices[0])
            variable = tk.StringVar(value=sel)
            combo = ttk.Combobox(inner, textvariable=variable,
                                 values=choices, state='readonly', font=font(11))
            combo.pack(fill='x', ipady=5)
            values[key] = variable
            selected[key] = mapping
        else:
            default = (date.today().strftime('%d/%m/%Y') if kind ==
                       'date' else '') if value is None else fmt(value)
            entry = tk.Entry(inner, bg=BG, fg=TEXT, insertbackground=WHITE, relief='flat',
                             highlightthickness=1, highlightbackground=BORDER, highlightcolor=GREEN, font=font(11))
            entry.pack(fill='x', ipady=9)
            entry.insert(0, default)
            values[key] = entry

    def save():
        try:
            data = {}
            for key, label, kind in spec:
                widget = values.get(key)
                if widget is None:
                    raise ValueError(
                        f'Preencha os dados relacionados: {label}.')
                raw = widget.get()
                data[key] = selected[key][raw] if key in selected else raw
            controller.salvar(table, data, record['id'] if record else None)
            messagebox.showinfo(
                'Registro salvo', 'Dados gravados no PostgreSQL.')
            navigate(section)
        except Exception as e:
            messagebox.showerror('Erro ao salvar', str(e))
    ActionButton(inner, 'Salvar alterações' if record else 'Cadastrar', save).pack(
        anchor='w', pady=(18, 8))
    ActionButton(root, 'Voltar', lambda: navigate(section),
                 primary=False).pack(anchor='w', pady=15)


PAGES = {'Dashboard': dashboard, **{name: listing(name) for name in CONFIG}}
