import tkinter as tk
from .styles import *
from .components import lbl, Icon

MENU = [
    ('Dashboard', 'dashboard'),
    ('Rendas', 'income'),
    ('Categorias', 'category'),
    ('Despesas', 'expense'),
    ('Objetivos', 'goal'),
    ('Regras', 'rules'),
    ('Aportes', 'contributions'),
]


class Sidebar(tk.Frame):
    def __init__(self, master, on_navigate):
        super().__init__(master, bg=SIDEBAR, width=220, highlightbackground=BORDER, highlightthickness=1)
        self.pack_propagate(False)
        self.on_navigate = on_navigate
        self.buttons = {}

        brand = tk.Frame(self, bg=SIDEBAR)
        brand.pack(fill='x', padx=20, pady=(24, 6))
        Icon(brand, 'brand', 18, GREEN, SIDEBAR).pack(side='left', pady=1)
        lbl(brand, ' MeuBolso', 17, WHITE, True).pack(side='left')
        lbl(self, 'SEU DINHEIRO, SEM COMPLICAÇÃO', 8, DIM, True, bg=SIDEBAR).pack(anchor='w', padx=22, pady=(0, 28))
        tk.Frame(self, bg=BORDER, height=1).pack(fill='x', padx=18, pady=(0, 18))
        lbl(self, 'MENU PRINCIPAL', 8, DIM, True, bg=SIDEBAR).pack(anchor='w', padx=22, pady=(0, 10))

        for name, icon_name in MENU:
            row = tk.Frame(self, bg=SIDEBAR, height=42, cursor='hand2')
            row.pack(fill='x', padx=12, pady=3)
            row.pack_propagate(False)
            indicator = tk.Frame(row, bg=SIDEBAR, width=3)
            indicator.pack(side='left', fill='y')
            icon = Icon(row, icon_name, size=16, color=MUTED, bg=SIDEBAR)
            icon.pack(side='left', padx=(14, 12), pady=12)
            text = lbl(row, name, 11, MUTED, bg=SIDEBAR)
            text.pack(side='left')
            self.buttons[name] = (row, indicator, icon, text)
            for item in (row, icon, text, indicator):
                item.bind('<Button-1>', lambda _, n=name: self.on_navigate(n))
                item.bind('<Enter>', lambda _, n=name: self.hover(n, True))
                item.bind('<Leave>', lambda _, n=name: self.hover(n, False))

        tk.Frame(self, bg=SIDEBAR).pack(expand=True, fill='both')
        bottom = tk.Frame(self, bg=CARD, padx=14, pady=12)
        bottom.pack(fill='x', padx=12, pady=(0, 16))
        row = tk.Frame(bottom, bg=CARD)
        row.pack(anchor='w')
        Icon(row, 'check', size=14, color=GREEN, bg=CARD).pack(side='left', pady=1)
        lbl(row, '  Modo visual', 10, GREEN, True, bg=CARD).pack(side='left')
        lbl(bottom, 'Sem controllers ou banco', 9, MUTED, bg=CARD).pack(anchor='w', pady=(5, 0))
        self.active = None
        self.select('Dashboard')

    def hover(self, name, active):
        if name == self.active:
            return
        row, indicator, icon, text = self.buttons[name]
        bg = CARD_HOVER if active else SIDEBAR
        row.configure(bg=bg)
        indicator.configure(bg=bg)
        icon.recolor(MUTED, bg)
        text.configure(bg=bg)

    def select(self, name):
        if name not in self.buttons:
            return
        self.active = name
        for key, (row, ind, ico, txt) in self.buttons.items():
            selected = key == name
            bg = GREEN_SOFT if selected else SIDEBAR
            fg = WHITE if selected else MUTED
            row.configure(bg=bg)
            ind.configure(bg=GREEN if selected else bg)
            ico.recolor(GREEN if selected else MUTED, bg)
            txt.configure(bg=bg, fg=fg, font=font(11, 'bold' if selected else 'normal'))
