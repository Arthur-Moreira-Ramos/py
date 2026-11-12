# views/dashboard.py
import tkinter as tk
from tkinter import ttk
from views.styles import *

class Dashboard(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=BG_COLOR)
        self._criar_widgets()

    def _criar_widgets(self):
        # Título da Seção
        tk.Label(
            self, text="Painel Geral", fg=TEXT_TITLE, bg=BG_COLOR, font=FONT_TITLE 
        ).pack(anchor="w", pady=(0, 20))

        # Cards de Resumo
        cards_frame = tk.Frame(self, bg=BG_COLOR)
        cards_frame.pack(fill="x", pady=(0, 20))
        
        self._criar_card(cards_frame, "Saldo Total", "R$ 3.500,00", TEXT_TITLE)
        self._criar_card(cards_frame, "Minhas Rendas", "R$ 5.200,00", ACCENT_GREEN)
        self._criar_card(cards_frame, "Minhas Despesas", "R$ 1.700,00", ACCENT_RED)

        # Container inferior (Tabela à esquerda, Formulário à direita)
        lower_frame = tk.Frame(self, bg=BG_COLOR)
        lower_frame.pack(fill="both", expand=True)

        self._criar_tabela(lower_frame)
        self._criar_formulario(lower_frame)

    def _criar_card(self, parent, titulo, valor, cor_valor):
        card = tk.Frame(parent, bg=CARD_BG, padx=20, pady=15)
        card.pack(side="left", fill="x", expand=True, padx=(0, 15))
        
        tk.Label(card, text=titulo, fg=TEXT_SUB, bg=CARD_BG, font=FONT_SUBTITLE).pack(anchor="w")
        tk.Label(card, text=valor, fg=cor_valor, bg=CARD_BG, font=FONT_VALUE).pack(anchor="w", pady=(5, 0))

    def _criar_tabela(self, parent):
        table_frame = tk.Frame(parent, bg=CARD_BG, padx=15, pady=15)
        table_frame.pack(side="left", fill="both", expand=True, padx=(0, 15))
        
        tk.Label(
            table_frame, text="Últimas Transações", fg=TEXT_TITLE, bg=CARD_BG, font=("Inter", 14, "bold")
        ).pack(anchor="w", pady=(0, 10))
        
        colunas = ("descricao", "categoria", "valor")
        tree = ttk.Treeview(table_frame, columns=colunas, show="headings", height=10)
        tree.heading("descricao", text="Descrição")
        tree.heading("categoria", text="Categoria")
        tree.heading("valor", text="Valor")
        
        tree.column("descricao", width=150)
        tree.column("categoria", width=100)
        tree.column("valor", width=100, anchor="e")
        
        # Dados estáticos para o protótipo
        tree.insert("", "end", values=("Mensalidade Faculdade", "Educação", "R$ 800,00"))
        tree.insert("", "end", values=("Supermercado", "Alimentação", "R$ 450,00"))
        
        tree.pack(fill="both", expand=True)

    def _criar_formulario(self, parent):
        form_frame = tk.Frame(parent, bg=CARD_BG, padx=20, pady=20, width=300)
        form_frame.pack(side="right", fill="y")
        form_frame.pack_propagate(False)
        
        tk.Label(
            form_frame, text="Nova Despesa", fg=TEXT_TITLE, bg=CARD_BG, font=("Inter", 14, "bold")
        ).pack(anchor="w", pady=(0, 15))
        
        self._criar_input(form_frame, "Descrição")
        self._criar_input(form_frame, "Valor (R$)")
        self._criar_input(form_frame, "Categoria")
        
        btn_frame = tk.Frame(form_frame, bg=CARD_BG)
        btn_frame.pack(fill="x", pady=25)
        
        tk.Button(
            btn_frame, text="Salvar", bg=ACCENT_GREEN, fg=TEXT_TITLE, 
            bd=0, font=("Inter", 10, "bold"), padx=15, pady=8, cursor="hand2"
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))
        
        tk.Button(
            btn_frame, text="Cancelar", bg=SEPARATOR_COLOR, fg=TEXT_TITLE, 
            bd=0, font=("Inter", 10, "bold"), padx=15, pady=8, cursor="hand2"
        ).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def _criar_input(self, parent, label):
        tk.Label(parent, text=label, fg=TEXT_SUB, bg=CARD_BG, font=FONT_LABEL).pack(anchor="w", pady=(10, 2))
        entry = tk.Entry(
            parent, bg=BG_COLOR, fg=TEXT_TABLE, insertbackground=TEXT_TITLE, 
            bd=0, font=("Inter", 11), highlightthickness=1, highlightbackground=SEPARATOR_COLOR,
            highlightcolor=ACCENT_GREEN
        )
        entry.pack(fill="x", ipady=6)