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
    section_header(root, 'Painel geral', 'Seu dinheiro, suas escolhas. Tudo em um só lugar.')
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
    """Listagem interativa CustomTkinter: busca, filtros, ordem e paginação.

    Nenhuma ação altera o banco diretamente; edição/exclusão usam os
    formulários e controllers originais do projeto.
    """
    import customtkinter as ctk

    ctk.set_appearance_mode('dark')
    outer, inner = card(root, 16)
    outer.pack(fill='x', pady=(0, 18))

    title_bar = tk.Frame(inner, bg=CARD)
    title_bar.pack(fill='x', pady=(0, 15))
    lbl(title_bar, 'Registros cadastrados', 14, WHITE, True, bg=CARD).pack(side='left')
    count_label = lbl(title_bar, '', 9, MUTED, bg=CARD)
    count_label.pack(side='right')

    toolbar = ctk.CTkFrame(inner, fg_color='transparent', corner_radius=0)
    toolbar.pack(fill='x', pady=(0, 14))
    search = ctk.StringVar(value='')
    search_entry = ctk.CTkEntry(
        toolbar, textvariable=search, placeholder_text='Pesquisar registros...',
        fg_color=BG, border_color=BORDER, text_color=TEXT,
        placeholder_text_color=MUTED, height=38, corner_radius=8,
        font=(FONT, 12))
    search_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))

    order_values = ['Mais recentes', 'Mais antigos', 'Nome (A–Z)', 'Nome (Z–A)']
    if table_name in ('Rendas', 'Despesas', 'Aportes'):
        order_values.extend(['Maior valor', 'Menor valor'])
    ordering = ctk.StringVar(value='Mais recentes')
    order_menu = ctk.CTkOptionMenu(
        toolbar, values=order_values, variable=ordering, width=160, height=38,
        fg_color=BORDER, button_color='#475569', button_hover_color='#52647A',
        dropdown_fg_color=CARD, dropdown_hover_color=GREEN_DARK,
        text_color=WHITE, dropdown_text_color=WHITE, corner_radius=8,
        font=(FONT, 11), dropdown_font=(FONT, 11))
    order_menu.pack(side='right')

    filters = {'Rendas': ['Todas', 'Ativas', 'Inativas'],
               'Despesas': ['Todas', 'Pagas', 'Pendentes', 'Fixas', 'Variáveis']}
    selection = ctk.StringVar(value='Todas')
    if table_name in filters:
        filter_menu = ctk.CTkOptionMenu(
            toolbar, values=filters[table_name], variable=selection,
            width=130, height=38, fg_color=BORDER, button_color='#475569',
            button_hover_color='#52647A', dropdown_fg_color=CARD,
            dropdown_hover_color=GREEN_DARK, text_color=WHITE,
            dropdown_text_color=WHITE, corner_radius=8,
            font=(FONT, 11), dropdown_font=(FONT, 11))
        filter_menu.pack(side='right', padx=(0, 10))

    results = ctk.CTkFrame(inner, fg_color='transparent', corner_radius=0)
    results.pack(fill='x')
    footer = ctk.CTkFrame(inner, fg_color='transparent', corner_radius=0)
    footer.pack(fill='x', pady=(14, 0))

    categories = {}
    goals = {}
    if table_name == 'Despesas':
        categories = {int(c['id']): c['nome'] for c in controller.listar('categoria_despesa')}
    if table_name == 'Aportes':
        goals = {int(g['id']): g['descricao'] for g in controller.metas()}

    page = [0]
    page_size = 8

    def label(parent, text, size=11, color=TEXT, bold=False, **kwargs):
        return ctk.CTkLabel(
            parent, text=str(text), text_color=color, font=(FONT, size, 'bold' if bold else 'normal'),
            anchor='w', **kwargs)

    def badge(parent, text, color=GREEN, background=GREEN_SOFT):
        return ctk.CTkLabel(parent, text=text, text_color=color,
                            fg_color=background, corner_radius=6, height=25,
                            font=(FONT, 10, 'bold'), padx=10)

    def name_of(record):
        return str(record.get('nome') or record.get('descricao') or
                   goals.get(record.get('objetivo_id'), 'Registro'))

    def item_data(record):
        if table_name == 'Rendas':
            active = bool(record.get('ativa'))
            cadence = {'DIARIA': 'Diária', 'SEMANAL': 'Semanal', 'MENSAL': 'Mensal'}
            return (name_of(record), f"{cadence.get(record.get('periodicidade'), 'Não definida')}  ·  Fonte recorrente",
                    money(record.get('valor') or 0), 'Ativa' if active else 'Inativa',
                    GREEN if active else MUTED, GREEN_SOFT if active else BORDER)
        if table_name == 'Categorias':
            return (name_of(record), str(record.get('descricao') or 'Sem descrição'),
                    '', 'Categoria', BLUE, BG)
        if table_name == 'Despesas':
            paid = bool(record.get('pago'))
            category = categories.get(record.get('categoria_id'), 'Sem categoria')
            kind = 'Fixa' if record.get('tipo') == 'FIXA' else 'Variável'
            return (name_of(record), f"{category}  ·  {kind}  ·  {fmt(record.get('data_despesa'))}",
                    money(record.get('valor') or 0), 'Paga' if paid else 'Pendente',
                    GREEN if paid else AMBER, GREEN_SOFT if paid else '#45391F')
        if table_name == 'Aportes':
            return (goals.get(record.get('objetivo_id'), 'Objetivo não encontrado'),
                    f"Aporte em {fmt(record.get('data_aporte'))}",
                    money(record.get('valor') or 0), 'Aporte', BLUE, BG)
        return (name_of(record), '', '', 'Registro', MUTED, BG)

    def matching():
        import unicodedata
        def normalize(value):
            return ''.join(char for char in unicodedata.normalize('NFKD', str(value).lower())
                           if not unicodedata.combining(char))
        query = normalize(search.get().strip())
        filt = selection.get()
        found = []
        for record in items:
            main, subtitle, amount, status, *_ = item_data(record)
            haystack = normalize(' '.join([str(record['id']), main, subtitle, amount, status]))
            if query and query not in haystack:
                continue
            if table_name == 'Rendas' and filt != 'Todas':
                if bool(record.get('ativa')) != (filt == 'Ativas'):
                    continue
            if table_name == 'Despesas' and filt != 'Todas':
                if filt in ('Pagas', 'Pendentes') and bool(record.get('pago')) != (filt == 'Pagas'):
                    continue
                if filt in ('Fixas', 'Variáveis') and record.get('tipo') != ('FIXA' if filt == 'Fixas' else 'VARIAVEL'):
                    continue
            found.append(record)
        order = ordering.get()
        if order == 'Mais recentes':
            found.sort(key=lambda r: int(r['id']), reverse=True)
        elif order == 'Mais antigos':
            found.sort(key=lambda r: int(r['id']))
        elif order in ('Nome (A–Z)', 'Nome (Z–A)'):
            found.sort(key=lambda r: normalize(name_of(r)), reverse=order == 'Nome (Z–A)')
        elif order in ('Maior valor', 'Menor valor'):
            found.sort(key=lambda r: r.get('valor') or 0, reverse=order == 'Maior valor')
        return found

    def redraw(*_):
        for child in results.winfo_children():
            child.destroy()
        for child in footer.winfo_children():
            child.destroy()
        filtered = matching()
        total = len(filtered)
        maximum_page = max(0, (total-1)//page_size)
        page[0] = min(page[0], maximum_page)
        count_label.configure(text=f'{total} de {len(items)} registro(s)')
        if not filtered:
            empty = ctk.CTkFrame(results, fg_color=BG, corner_radius=8, height=100)
            empty.pack(fill='x')
            label(empty, 'Nenhum registro encontrado', 12, WHITE, True).pack(anchor='center', pady=(23, 2))
            label(empty, 'Altere a pesquisa ou os filtros para visualizar outros registros.', 10, MUTED).pack(anchor='center')
            return

        for record in filtered[page[0]*page_size:(page[0]+1)*page_size]:
            title, detail, amount, status, status_color, status_bg = item_data(record)
            block = ctk.CTkFrame(results, fg_color=BG, corner_radius=9,
                                 border_width=1, border_color=BORDER)
            block.pack(fill='x', pady=(0, 8))
            block.grid_columnconfigure(0, weight=1)
            block.grid_columnconfigure(1, weight=0)
            block.grid_columnconfigure(2, weight=0)

            info = ctk.CTkFrame(block, fg_color='transparent')
            info.grid(row=0, column=0, sticky='ew', padx=(14, 8), pady=12)
            name_line = ctk.CTkFrame(info, fg_color='transparent')
            name_line.pack(fill='x')
            label(name_line, title, 12, WHITE, True, wraplength=520).pack(side='left')
            label(name_line, f"  #{record['id']}", 9, DIM).pack(side='left', padx=(4, 0))
            if detail:
                label(info, detail, 10, MUTED, wraplength=610).pack(anchor='w', pady=(4, 0))

            metrics = ctk.CTkFrame(block, fg_color='transparent')
            metrics.grid(row=0, column=1, sticky='e', padx=(0, 16), pady=10)
            if amount:
                label(metrics, amount, 12, WHITE, True).pack(anchor='e', pady=(0, 5))
            badge(metrics, status, status_color, status_bg).pack(anchor='e')

            actions = ctk.CTkFrame(block, fg_color='transparent')
            actions.grid(row=0, column=2, sticky='e', padx=(0, 14), pady=10)
            ctk.CTkButton(actions, text='Editar', width=69, height=33,
                          fg_color=BORDER, hover_color='#475569', corner_radius=7,
                          font=(FONT, 11, 'bold'), command=lambda r=record: open_form((table_name, r))).pack(side='left', padx=(0, 7))
            ctk.CTkButton(actions, text='Excluir', width=69, height=33,
                          fg_color='transparent', border_color='#9B3946', border_width=1,
                          hover_color=RED_SOFT, text_color='#FDA4AF', corner_radius=7,
                          font=(FONT, 11, 'bold'), command=lambda r=record: delete_record(table_name, r, navigate)).pack(side='left')

        label(footer, f'Exibindo {page[0]*page_size+1}–{min((page[0]+1)*page_size,total)} de {total}', 10, MUTED).pack(side='left')
        if total > page_size:
            pagination = ctk.CTkFrame(footer, fg_color='transparent')
            pagination.pack(side='right')
            def shift(delta):
                page[0] += delta
                redraw()
            ctk.CTkButton(pagination, text='Anterior', width=75, height=29,
                          fg_color=BORDER, hover_color='#475569',
                          state='normal' if page[0] else 'disabled',
                          command=lambda: shift(-1)).pack(side='left', padx=(0, 8))
            label(pagination, f'{page[0]+1} / {maximum_page+1}', 10, MUTED).pack(side='left', padx=6)
            ctk.CTkButton(pagination, text='Próxima', width=75, height=29,
                          fg_color=BORDER, hover_color='#475569',
                          state='normal' if page[0] < maximum_page else 'disabled',
                          command=lambda: shift(1)).pack(side='left', padx=(8, 0))

    def reset(*_):
        page[0] = 0
        redraw()

    search.trace_add('write', reset)
    ordering.trace_add('write', reset)
    selection.trace_add('write', reset)
    redraw()



def rules_cards(root, records, navigate, open_form):
    """Cards interativos de regras, mantendo os controllers de edição/exclusão."""
    import customtkinter as ctk
    import unicodedata

    ctk.set_appearance_mode('dark')
    suggestions = {int(r['objetivo_id']): r for r in controller.sugestoes()
                   if r.get('objetivo_id') is not None}
    goals = {int(g['id']): g['descricao'] for g in controller.metas()}

    outer, inner = card(root, 16)
    outer.pack(fill='x', pady=(0, 18))
    header = ctk.CTkFrame(inner, fg_color='transparent')
    header.pack(fill='x', pady=(0, 12))
    ctk.CTkLabel(header, text='Regras cadastradas', text_color=WHITE,
                 font=(FONT, 14, 'bold')).pack(side='left')
    total = sum((Decimal(str(record['porcentagem'])) for record in records), Decimal('0'))
    ctk.CTkLabel(header, text=f'{len(records)} regra(s)  ·  {str(total).replace(".", ",")}% distribuído',
                 text_color=MUTED, font=(FONT, 10)).pack(side='right')

    toolbar = ctk.CTkFrame(inner, fg_color='transparent')
    toolbar.pack(fill='x', pady=(0, 12))
    search = ctk.StringVar(value='')
    ctk.CTkEntry(toolbar, textvariable=search, height=38, corner_radius=8,
                 placeholder_text='Pesquisar objetivo...', fg_color=BG,
                 border_color=BORDER, text_color=TEXT,
                 placeholder_text_color=MUTED, font=(FONT, 12)).pack(
                     side='left', fill='x', expand=True, padx=(0, 10))
    order = ctk.StringVar(value='Maior porcentagem')
    ctk.CTkOptionMenu(toolbar, variable=order, height=38, width=174,
                      values=['Maior porcentagem', 'Menor porcentagem', 'Nome (A–Z)', 'Nome (Z–A)'],
                      fg_color=BORDER, button_color='#475569',
                      button_hover_color='#52647A', dropdown_fg_color=CARD,
                      dropdown_hover_color=GREEN_DARK, text_color=WHITE,
                      dropdown_text_color=WHITE, font=(FONT, 11),
                      dropdown_font=(FONT, 11)).pack(side='right')
    results = ctk.CTkFrame(inner, fg_color='transparent')
    results.pack(fill='x')
    empty_label = ctk.CTkLabel(inner, text='', text_color=MUTED, font=(FONT, 10))
    empty_label.pack(anchor='w', pady=(8, 0))

    def name_of(record):
        goal_id = int(record['objetivo_id'])
        suggestion = suggestions.get(goal_id) or {}
        return suggestion.get('descricao') or goals.get(goal_id, 'Objetivo não encontrado')

    def normalized(value):
        return ''.join(ch for ch in unicodedata.normalize('NFKD', str(value).casefold())
                       if not unicodedata.combining(ch))

    def redraw(*_):
        for widget in results.winfo_children():
            widget.destroy()
        query = normalized(search.get().strip())
        filtered = [record for record in records if query in normalized(name_of(record))
                    or query in str(record['id'])]
        sort_mode = order.get()
        if sort_mode == 'Maior porcentagem':
            filtered.sort(key=lambda item: Decimal(str(item['porcentagem'])), reverse=True)
        elif sort_mode == 'Menor porcentagem':
            filtered.sort(key=lambda item: Decimal(str(item['porcentagem'])))
        else:
            filtered.sort(key=lambda item: normalized(name_of(item)),
                          reverse=sort_mode == 'Nome (Z–A)')

        empty_label.configure(text=(f'{len(filtered)} de {len(records)} regra(s) exibida(s)'
                                   if filtered else 'Nenhuma regra encontrada.'))
        for record in filtered:
            goal_id = int(record['objetivo_id'])
            suggestion = suggestions.get(goal_id)
            percentage = Decimal(str(record['porcentagem']))
            percent_display = f'{percentage:.2f}'.replace('.', ',') + '%'
            block = ctk.CTkFrame(results, fg_color=BG, border_width=1,
                                 border_color=BORDER, corner_radius=9)
            block.pack(fill='x', pady=(0, 8))
            block.grid_columnconfigure(0, weight=1)

            info = ctk.CTkFrame(block, fg_color='transparent')
            info.grid(row=0, column=0, sticky='ew', padx=(15, 12), pady=(12, 12))
            ctk.CTkLabel(info, text=name_of(record), text_color=WHITE,
                         font=(FONT, 12, 'bold'), anchor='w').pack(anchor='w')
            ctk.CTkLabel(info, text=(f'Valor sugerido: {money(suggestion["sugerido"])}'
                                          if suggestion is not None else 'Valor sugerido indisponível'),
                         text_color=MUTED, font=(FONT, 10), anchor='w').pack(
                             anchor='w', pady=(3, 9))
            bar = ctk.CTkProgressBar(info, height=8, corner_radius=4,
                                     fg_color=BORDER, progress_color=GREEN)
            bar.pack(fill='x')
            bar.set(max(0.0, min(float(percentage) / 100, 1.0)))

            pct = ctk.CTkFrame(block, fg_color='transparent')
            pct.grid(row=0, column=1, padx=(4, 20), pady=12, sticky='e')
            ctk.CTkLabel(pct, text=percent_display, text_color=GREEN,
                         font=(FONT, 15, 'bold')).pack(anchor='e')
            ctk.CTkLabel(pct, text='do saldo', text_color=MUTED,
                         font=(FONT, 10)).pack(anchor='e')

            actions = ctk.CTkFrame(block, fg_color='transparent')
            actions.grid(row=0, column=2, padx=(0, 14), pady=12, sticky='e')
            ctk.CTkButton(actions, text='Editar', width=70, height=34,
                          fg_color=BORDER, hover_color='#475569', corner_radius=7,
                          font=(FONT, 11, 'bold'),
                          command=lambda r=record: open_form(('Regras', r))).pack(
                              side='left', padx=(0, 8))
            ctk.CTkButton(actions, text='Excluir', width=70, height=34,
                          fg_color='transparent', border_width=1,
                          border_color='#9B3946', hover_color=RED_SOFT,
                          text_color='#FDA4AF', corner_radius=7,
                          font=(FONT, 11, 'bold'),
                          command=lambda r=record: delete_record('Regras', r, navigate)).pack(
                              side='left')

    search.trace_add('write', redraw)
    order.trace_add('write', redraw)
    redraw()


def delete_record(section, record, navigate):
    aviso = ("\n\nATENÇÃO: excluir este objetivo também apagará seus aportes e sua regra de distribuição."
             if section == 'Objetivos' else '')
    if not messagebox.askyesno('Confirmar exclusão',
            f"Excluir registro #{record['id']}? Esta ação não pode ser desfeita.{aviso}"):
        return
    try:
        controller.excluir(CONFIG[section][0], record['id'])
        navigate(section)
    except Exception as exc:
        messagebox.showerror('Não foi possível excluir', str(exc))


def record_actions(parent, section, record, navigate, open_form):
    actions = tk.Frame(parent, bg=CARD)
    actions.pack(side='right', padx=(14, 0))
    ActionButton(actions, 'Editar', lambda r=record: open_form((section, r)),
                 primary=False, small=True).pack(side='right', padx=(8, 0))
    ActionButton(actions, 'Excluir', lambda r=record: delete_record(section, r, navigate),
                 primary=False, small=True).pack(side='right')


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
            rules_cards(root, controller.listar(table), navigate, open_form)
            return
        elif section == 'Objetivos':
            goals = controller.metas()
            records = {int(r['id']): r for r in controller.listar(table)}
            if not goals:
                c, inner = card(root)
                c.pack(fill='x', pady=(0, 8))
                lbl(inner, 'Nenhum objetivo cadastrado.', 11, MUTED, bg=CARD).pack(anchor='w')
            for goal in goals:
                record = records.get(int(goal['id']), goal)
                c, inner = card(root, 14)
                c.pack(fill='x', pady=(0, 8))
                record_actions(inner, section, record, navigate, open_form)
                content = tk.Frame(inner, bg=CARD)
                content.pack(side='left', fill='x', expand=True)
                total = goal['valor_meta']
                ratio = max(0.0, float(goal['acumulado'] / total)) if total else 0.0
                lbl(content,
                    f"{goal['descricao']}  ·  {money(goal['acumulado'])} de {money(total)}  ({ratio:.0%})",
                    11, WHITE, True, bg=CARD, wraplength=900).pack(anchor='w')
                progress(content, min(ratio, 1.0), GREEN, height=8, animate=False).pack(
                    fill='x', pady=(9, 2))
            return
        table_rows(root, controller.listar(table), spec, open_form, section, navigate)
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
