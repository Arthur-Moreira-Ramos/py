"""Telas de apresentação; dados ilustrativos e nenhuma persistência."""
import tkinter as tk
import math
from .styles import *
from .components import lbl, card, stat, section_header, progress, data_table, field, dropdown, ActionButton, Icon
from .data_demo import SUMMARY, TRANSACTIONS, INCOME, EXPENSES, CATEGORIES, GOALS, RULES, CONTRIBUTIONS, money


def columns(parent, count=2, weights=None):
    area = tk.Frame(parent, bg=BG)
    area.pack(fill='x', pady=(0, 15))
    cols = []
    for i in range(count):
        area.grid_columnconfigure(i, weight=(weights or [1]*count)[i], uniform='equal' if weights is None else '')
        holder = tk.Frame(area, bg=BG)
        holder.grid(row=0, column=i, sticky='nsew', padx=(0, 10) if i < count-1 else 0)
        cols.append(holder)
    return cols


def information(parent, title, description, color=GREEN):
    panel = tk.Frame(parent, bg=GREEN_SOFT if color == GREEN else CARD, padx=16, pady=13)
    panel.pack(fill='x', pady=(3, 17))
    row = tk.Frame(panel, bg=panel.cget('bg'))
    row.pack(anchor='w')
    Icon(row, 'alert' if color == GREEN else 'check', 14, color, panel.cget('bg')).pack(side='left', padx=(0, 8), pady=1)
    lbl(row, title, 11, color, True, bg=panel.cget('bg')).pack(side='left')
    lbl(panel, description, 10, TEXT, wraplength=780, bg=panel.cget('bg')).pack(anchor='w', pady=(6, 0))


def panel_title(parent, title, hint=None):
    heading = tk.Frame(parent, bg=CARD)
    heading.pack(fill='x', pady=(0, 15))
    lbl(heading, title, 13, WHITE, True).pack(side='left')
    if hint: lbl(heading, hint, 9, DIM).pack(side='right')


def line_chart(parent):
    canvas = tk.Canvas(parent, height=150, bg=CARD, highlightthickness=0)
    canvas.pack(fill='x', pady=(4, 0))
    values = [2400, 2900, 2700, 3300, 3150, 3500]
    labels = ['JUN', 'JUL', 'AGO', 'SET', 'OUT', 'NOV']
    def redraw(_=None):
        canvas.delete('all'); w = max(canvas.winfo_width(), 100); h = 150
        for k in (0.25, 0.5, 0.75):
            y = 12+(h-42)*k
            canvas.create_line(10, y, w-10, y, fill=BORDER, dash=(3, 6))
        coords = []
        for i, v in enumerate(values):
            x = 14+i*(w-28)/5; y = 9+(h-52)*(1-(v-2200)/1600)
            coords.extend((x,y))
            canvas.create_text(x, h-12, text=labels[i], fill=DIM, font=font(9))
        if len(coords) >= 4:
            canvas.create_line(*coords, fill=GREEN, width=3, smooth=True)
            for i in range(0, len(coords), 2):
                x,y=coords[i:i+2]; canvas.create_oval(x-4,y-4,x+4,y+4,fill=GREEN,outline=CARD,width=2)
    canvas.bind('<Configure>', redraw)


def donut(parent):
    can = tk.Canvas(parent, width=160, height=145, bg=CARD, highlightthickness=0)
    can.pack(side='left', padx=(0, 18))
    parts = [(1200, BLUE), (350, AMBER), (150, PURPLE)]
    start = 90
    for amount, col in parts:
        sweep = amount/1700*360
        can.create_arc(10, 4, 142, 136, start=start, extent=-sweep, style='arc', outline=col, width=18)
        start -= sweep
    can.create_text(76, 60, text='R$ 1,7 mil', fill=WHITE, font=font(14,'bold'))
    can.create_text(76, 79, text='despesas', fill=MUTED, font=font(9))
    legend = tk.Frame(parent, bg=CARD)
    legend.pack(side='left', fill='both', expand=True)
    for item, amount, col in [('Moradia',1200,BLUE), ('Alimentação',350,AMBER), ('Mobilidade',150,PURPLE)]:
        r=tk.Frame(legend,bg=CARD);r.pack(fill='x',pady=9)
        Icon(r, 'dot', 10, col, CARD).pack(side='left', padx=(0, 6), pady=1);lbl(r,item,10,MUTED).pack(side='left')
        lbl(r,money(amount),10,WHITE,True).pack(side='right')


def dashboard(root, open_page, open_form):
    section_header(root,'Painel geral','Seu dinheiro, suas escolhas. Tudo em um só lugar.', '+ Nova movimentação', lambda: open_form('Nova movimentação'))
    information(root,'◉  Modo de demonstração','Os valores mostrados são exemplos de interface. Nenhuma informação é enviada ou gravada.')
    boxes=columns(root,4)
    for container, (t,v,d,c,b) in zip(boxes,[
        ('Saldo disponível',money(3500),'Resultado deste mês',WHITE,'wallet'),
        ('Rendas do mês',money(5200),'2 fontes de renda',GREEN,'up'),
        ('Despesas do mês',money(1700),'3 movimentações',RED,'down'),
        ('Separado para metas',money(900),'Economia planejada',BLUE,'goal')]):
        stat(container,t,v,d,c,b,True).pack(fill='both',expand=True)
    left,right=columns(root,2)
    a,ai=card(left);a.pack(fill='both',expand=True)
    panel_title(ai,'Evolução do saldo','Últimos 6 meses');line_chart(ai)
    b,bi=card(right);b.pack(fill='both',expand=True)
    panel_title(bi,'Despesas por categoria','Novembro');donut(bi)
    left,right=columns(root,2)
    a,ai=card(left);a.pack(fill='both',expand=True)
    panel_title(ai,'Últimas movimentações','Visão recente')
    for name,category,date,amount,status in TRANSACTIONS[:4]:
        r=tk.Frame(ai,bg=CARD);r.pack(fill='x',pady=10)
        lbl(r,name,11,WHITE,True).pack(anchor='w',side='left')
        lbl(r, ('+' if amount>0 else '−')+money(abs(amount)),11,GREEN if amount>0 else RED,True).pack(side='right')
    b,bi=card(right);b.pack(fill='both',expand=True)
    panel_title(bi,'Progresso dos seus objetivos','3 metas')
    for name, saved, target, color in [(g[0],g[2],g[3],g[5]) for g in GOALS]:
        r=tk.Frame(bi,bg=CARD);r.pack(fill='x',pady=(5,3))
        lbl(r,name,10,TEXT).pack(side='left');lbl(r,f'{round(saved/target*100)}%',10,MUTED).pack(side='right')
        progress(bi,saved/target,color,height=7).pack(fill='x',pady=(0,13))


def make_form(root, title, fields, options=None, note='Visualização de formulário. O salvamento será integrado na etapa de controllers.'):
    outer, inside = card(root, 24)
    outer.pack(fill='x')
    panel_title(inside,title,'PROTÓTIPO')
    for name,placeholder in fields:
        field(inside,name,placeholder)
    for name,values in options or []:
        dropdown(inside,name,values)
    lbl(inside,note,10,DIM,wraplength=670).pack(anchor='w',pady=(16,12))
    ActionButton(inside,'Salvar  ·  em breve',None).pack(anchor='w')
    return outer


def incomes(root,open_page,open_form):
    section_header(root,'Minhas rendas','Acompanhe suas fontes e frequências de recebimento.', '+ Adicionar renda', lambda:open_form('Nova renda'))
    tiles=columns(root,3)
    for p,(t,v,d,c) in zip(tiles,[('Total do mês',money(5200),'Renda de referência',GREEN),('Renda recorrente',money(4500),'Mensal',WHITE),('Renda variável',money(700),'Trabalhos extras',BLUE)]):
        stat(p,t,v,d,c).pack(fill='x')
    outer,inside=card(root);outer.pack(fill='x',pady=(0,16))
    panel_title(inside,'Fontes de renda','Dados de exemplo')
    data_table(inside,['Fonte','Frequência','Valor','Último recebimento','Situação'],INCOME,[3,2,2,2,1]).pack(fill='x')
    information(root,'Como as rendas serão utilizadas','Na implementação dos controllers, o sistema poderá normalizar recebimentos diários, semanais e mensais para uma referência mensal.')


def expenses(root,open_page,open_form):
    section_header(root,'Minhas despesas','Visualize seus gastos e organize seu orçamento.', '+ Adicionar despesa',lambda:open_form('Nova despesa'))
    tiles=columns(root,3)
    for p,(t,v,d,c) in zip(tiles,[('Total em despesas',money(1700),'Novembro de 2026',RED),('Contas fixas',money(1200),'70,6% das despesas',WHITE),('Despesas variáveis',money(500),'29,4% das despesas',AMBER)]):
        stat(p,t,v,d,c).pack(fill='x')
    outer,inside=card(root);outer.pack(fill='x',pady=(0,17))
    panel_title(inside,'Histórico de despesas','Novembro de 2026')
    data_table(inside,['Descrição','Categoria','Valor','Vencimento','Status'],EXPENSES,[3,2,2,2,1]).pack(fill='x')
    information(root,'Organização financeira','Diferenciar contas fixas e variáveis facilita a compreensão de quanto do orçamento já está comprometido.')


def categories(root,open_page,open_form):
    section_header(root,'Categorias','Identifique onde seu dinheiro está sendo utilizado.', '+ Nova categoria',lambda:open_form('Nova categoria'))
    slots=columns(root,3)
    for i,(name,kind,amount,col) in enumerate(CATEGORIES):
        p=slots[i%3];outer,inside=card(p,20);outer.pack(fill='x',pady=(0,12))
        lbl(inside,'●',17,col).pack(anchor='w',pady=(0,7))
        lbl(inside,name,14,WHITE,True).pack(anchor='w')
        lbl(inside,kind,10,MUTED).pack(anchor='w',pady=5)
        lbl(inside,money(amount),17,col,True).pack(anchor='w',pady=(8,0))
    information(root,'Categorias personalizadas','Os cards são demonstrativos. Futuramente, o usuário poderá criar, editar e excluir categorias por meio dos controllers.')


def goals(root,open_page,open_form):
    section_header(root,'Meus objetivos','Transforme planos em conquistas com metas financeiras.', '+ Novo objetivo',lambda:open_form('Novo objetivo'))
    cols=columns(root,3)
    for slot,(name,description,saved,target,date,col) in zip(cols,GOALS):
        outer,inside=card(slot,21);outer.pack(fill='both',expand=True)
        head = tk.Frame(inside, bg=CARD)
        head.pack(anchor='w', pady=(0, 13))
        Icon(head, 'goal', 12, col, CARD).pack(side='left', padx=(0, 6), pady=1)
        lbl(head,'OBJETIVO FINANCEIRO',8,col,True,bg=CARD).pack(side='left')
        lbl(inside,name,15,WHITE,True,wraplength=235).pack(anchor='w')
        lbl(inside,description,10,MUTED).pack(anchor='w',pady=(5,16))
        lbl(inside,money(saved),22,WHITE,True).pack(anchor='w')
        lbl(inside,f'de {money(target)}',11,MUTED).pack(anchor='w',pady=(2,13))
        r=tk.Frame(inside,bg=CARD);r.pack(fill='x')
        lbl(r,'Progresso',10,MUTED).pack(side='left')
        lbl(r,f'{round(saved/target*100)}%',10,col,True).pack(side='right')
        progress(inside,saved/target,col,height=8).pack(fill='x',pady=(8,17))
        foot = tk.Frame(inside, bg=CARD)
        foot.pack(anchor='w')
        Icon(foot, 'dot', 8, MUTED, CARD).pack(side='left', padx=(0, 6), pady=2)
        lbl(foot,'Prazo: '+date,9,MUTED,bg=CARD).pack(side='left')
    information(root,'Planejamento por objetivos','Os aportes efetivos e os cálculos de tempo até a meta serão conectados na etapa final do projeto.')


def rules(root,open_page,open_form):
    section_header(root,'Regras de distribuição','Defina como distribuir o dinheiro que sobrar ao fim do mês.', 'Editar regras',lambda:open_form('Editar distribuição'))
    information(root,'Como funciona a distribuição','Uma porcentagem do saldo positivo pode ser direcionada a cada objetivo. Esta tela demonstra o conceito; não executa os cálculos.')
    left,right=columns(root,2)
    outer,inside=card(left);outer.pack(fill='both',expand=True)
    panel_title(inside,'Distribuição planejada','100% do valor destinado às metas')
    for name,percent,col in RULES:
        row=tk.Frame(inside,bg=CARD);row.pack(fill='x',pady=(7,5))
        lbl(row,name,11,WHITE).pack(side='left');lbl(row,f'{percent}%',12,col,True).pack(side='right')
        progress(inside,percent/100,col,height=10).pack(fill='x',pady=(1,13))
    outer2,ins2=card(right);outer2.pack(fill='both',expand=True)
    panel_title(ins2,'Simulação ilustrativa','Saldo disponível: R$ 3.500,00')
    lbl(ins2,'Exemplo de divisão para objetivos',11,MUTED).pack(anchor='w',pady=(2,17))
    for name,percent,col in RULES:
        row=tk.Frame(ins2,bg=CARD);row.pack(fill='x',pady=14)
        lbl(row,name,11,TEXT).pack(side='left')
        lbl(row,money(3500*percent/100),13,col,True).pack(side='right')
    lbl(ins2,'Valores fictícios; não representam aportes realizados.',10,DIM,wraplength=300).pack(anchor='w',pady=(22,0))


def contributions(root,open_page,open_form):
    section_header(root,'Meus aportes','Acompanhe o dinheiro reservado para cada conquista.', '+ Registrar aporte',lambda:open_form('Novo aporte'))
    slots=columns(root,3)
    for slot,(t,v,d,c) in zip(slots,[('Aportes registrados',money(750),'Exemplo no mês',GREEN),('Metas com aportes','3','Objetivos ativos',BLUE),('Próximo passo','Continuar','Evolução consistente',WHITE)]):
        stat(slot,t,v,d,c).pack(fill='x')
    outer,inside=card(root);outer.pack(fill='x',pady=(0,17))
    panel_title(inside,'Histórico de aportes','Novembro de 2026')
    data_table(inside,['Objetivo','Valor reservado','Data'],CONTRIBUTIONS,[3,2,2]).pack(fill='x')
    information(root,'Aporte x distribuição','A distribuição indica uma sugestão de orçamento. O aporte representa o valor que o usuário realmente separou para a meta.')


PAGES = {'Dashboard': dashboard, 'Rendas': incomes, 'Categorias': categories,
         'Despesas': expenses, 'Objetivos': goals, 'Regras': rules, 'Aportes': contributions}
FORM_CONFIG = {
    'Nova movimentação': ([('Descrição','Ex.: Compra no mercado'),('Valor (R$)','0,00')],[('Tipo',['Despesa','Renda']),('Categoria',['Alimentação','Moradia','Trabalho','Outros'])]),
    'Nova renda': ([('Nome da fonte','Ex.: Salário'),('Valor (R$)','0,00')],[('Frequência',['Mensal','Semanal','Diária','Variável'])]),
    'Nova despesa': ([('Descrição','Ex.: Conta de luz'),('Valor (R$)','0,00'),('Data de vencimento','DD/MM/AAAA')],[('Categoria',['Moradia','Alimentação','Mobilidade','Outras']),('Tipo',['Fixa','Variável'])]),
    'Nova categoria': ([('Nome da categoria','Ex.: Educação')],[('Classificação',['Fixa','Variável'])]),
    'Novo objetivo': ([('Nome do objetivo','Ex.: Comprar um notebook'),('Valor da meta (R$)','0,00'),('Prazo desejado','MM/AAAA')],[]),
    'Editar distribuição': ([('Reserva de emergência (%)','50'),('Viagem de férias (%)','30'),('Notebook novo (%)','20')],[]),
    'Novo aporte': ([('Valor (R$)','0,00'),('Data','DD/MM/AAAA')],[('Objetivo',[item[0] for item in GOALS])]),
}


def form_page(root,title,open_page,open_form):
    section_header(root,title,'Prévia do formulário — etapa de interface')
    fields,options=FORM_CONFIG[title]
    make_form(root,'Dados do registro',fields,options)
    ActionButton(root,'Voltar para o dashboard',lambda:open_page('Dashboard'),primary=False).pack(anchor='w',pady=18)
