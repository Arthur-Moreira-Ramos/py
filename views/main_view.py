"""Shell da aplicação: transições e navegação; sem controllers ou banco."""
import tkinter as tk
from tkinter import ttk
from .styles import *
from .sidebar import Sidebar
from .components import ScrollPage, lbl, Icon
from .pages import PAGES, form_page


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        try:
            self.tk.call('tk', 'scaling', 1.0)
        except Exception:
            pass
        self.title('MeuBolso • Planejamento financeiro')
        self.geometry('1180x740')
        self.minsize(1024, 680)
        self.configure(bg=BG)
        self._init_styles()
        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.pack(side='left', fill='y')
        self.shell = tk.Frame(self, bg=BG)
        self.shell.pack(side='left', fill='both', expand=True)
        self._build_topbar()
        self.stage = tk.Frame(self.shell, bg=BG, padx=22, pady=16)
        self.stage.pack(fill='both', expand=True)
        self.current = None
        self.after(75, lambda: self.navigate('Dashboard'))

    def _init_styles(self):
        theme = ttk.Style(self)
        theme.theme_use('clam')
        theme.configure(
            'TCombobox',
            fieldbackground=BG,
            background=CARD,
            foreground=WHITE,
            arrowcolor=GREEN,
            bordercolor=BORDER,
            lightcolor=BORDER,
            darkcolor=BORDER,
            selectbackground=BG,
            selectforeground=WHITE,
        )
        theme.map('TCombobox', fieldbackground=[('readonly', BG)], foreground=[('readonly', WHITE)])
        theme.configure(
            'Vertical.TScrollbar',
            background=BORDER,
            troughcolor=BG,
            arrowcolor=MUTED,
            bordercolor=BORDER,
            darkcolor=BORDER,
            lightcolor=BORDER,
            arrowsize=12,
        )
        self.option_add('*TCombobox*Listbox.background', CARD)
        self.option_add('*TCombobox*Listbox.foreground', WHITE)
        self.option_add('*TCombobox*Listbox.selectBackground', GREEN_DARK)

    def _build_topbar(self):
        top = tk.Frame(self.shell, bg=BG, height=64)
        top.pack(fill='x', padx=26)
        top.pack_propagate(False)
        self.breadcrumb = lbl(top, 'VISÃO GERAL   /   DASHBOARD', 8, DIM, True)
        self.breadcrumb.pack(side='left', pady=24)
        avatar = tk.Frame(top, bg=CARD, padx=12, pady=8)
        avatar.pack(side='right', pady=12)
        Icon(avatar, 'check', 14, GREEN, CARD).pack(side='left', padx=(0, 8))
        lbl(avatar, 'Conta demonstrativa', 10, TEXT, True, bg=CARD).pack(side='left')
        tk.Frame(self.shell, bg=BORDER, height=1).pack(fill='x')

    def navigate(self, name):
        if name not in PAGES:
            return
        self.current = name
        self.sidebar.select(name)
        self.breadcrumb.configure(text='MEUBOLSO   /   ' + name.upper())
        self._render(lambda body: PAGES[name](body, self.navigate, self.open_form))

    def open_form(self, title):
        self.breadcrumb.configure(text='MEUBOLSO   /   FORMULÁRIOS   /   ' + title.upper())
        self._render(lambda body: form_page(body, title, self.navigate, self.open_form))

    def _render(self, renderer):
        for widget in self.stage.winfo_children():
            widget.destroy()
        page = ScrollPage(self.stage)
        page.pack(fill='both', expand=True)
        renderer(page.body)
        widget = page.canvas

        def move(step=0):
            if not widget.winfo_exists():
                return
            offset = max(0, 10 - step * 2)
            widget.coords(page.window, 0, offset)
            if step < 5:
                widget.after(18, lambda: move(step + 1))

        widget.after(20, move)
