"""Shell da aplicação: transições e navegação; sem controllers ou banco."""
import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
from .styles import *
from .sidebar import Sidebar
from .components import ScrollPage, lbl, Icon
from .pages import PAGES, form_page
from . import pages
from controllers.financeiro import FinanceiroController


class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        # Preserva a escala real de DPI calculada pelo Tk no monitor.
        # Não usar tk scaling=1.0: isso reduz fontes e provoca blur no Windows.
        self.title('MeuBolso • Planejamento financeiro')
        self.geometry('1180x740')  # Dimensão de reserva para sistemas sem maximização.
        self.minsize(1024, 680)
        self.configure(bg=BG)
        self._maximizar_janela()
        self._init_styles()
        self.financeiro = self._select_user()
        if self.financeiro is None:
            self.destroy()
            return
        # Diálogos modais podem modificar o estado da janela principal no Windows.
        # Recupera a janela antes de construir a interface e novamente no próximo ciclo.
        self._restaurar_apos_selecao()
        pages.controller = self.financeiro
        self.sidebar = Sidebar(self, self.navigate)
        self.sidebar.pack(side='left', fill='y')
        self.shell = tk.Frame(self, bg=BG)
        self.shell.pack(side='left', fill='both', expand=True)
        self._build_topbar()
        self.stage = tk.Frame(self.shell, bg=BG, padx=22, pady=16)
        self.stage.pack(fill='both', expand=True)
        self.current = None
        self.after(75, lambda: self.navigate('Dashboard'))

    def _maximizar_janela(self):
        """Maximiza sem entrar no modo fullscreen (mantém barra do Windows)."""
        try:
            self.state('zoomed')  # Windows
        except tk.TclError:
            try:
                self.attributes('-zoomed', True)  # Alguns gerenciadores Linux
            except tk.TclError:
                self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0')

    def _restaurar_apos_selecao(self):
        """Evita que o diálogo de escolha deixe a aplicação minimizada."""
        self.deiconify()
        self._maximizar_janela()
        self.lift()
        self.after_idle(self._recuperar_foco_inicial)
        self.after(180, self._recuperar_foco_inicial)

    def _recuperar_foco_inicial(self):
        if not self.winfo_exists():
            return
        if self.state() == 'iconic' or self.state() == 'withdrawn':
            self.deiconify()
        self._maximizar_janela()
        self.lift()
        self.focus_set()

    def _select_user(self):
        try:
            users = FinanceiroController.usuarios()
            if not users:
                messagebox.showinfo('Primeiro acesso', 'Nenhum usuário cadastrado. Crie uma conta local para começar.')
                name = simpledialog.askstring('Novo usuário', 'Nome:', parent=self)
                if not name:
                    return None
                email = simpledialog.askstring('Novo usuário', 'E-mail:', parent=self)
                if not email:
                    return None
                user_id = FinanceiroController.criar_usuario(name, email)
                self.account_label = name
            elif len(users) == 1:
                user_id = users[0]['id']
                self.account_label = users[0]['nome']
            else:
                choices = '\n'.join(f"#{u['id']} — {u['nome']} ({u['email']})" for u in users)
                user_id = simpledialog.askinteger('Selecionar usuário',
                    'Digite o ID do usuário:\n' + choices, parent=self)
                if user_id is None:
                    return None
                matched = next((u for u in users if u['id'] == user_id), None)
                if not matched:
                    raise ValueError('Identificador de usuário inválido.')
                self.account_label = matched['nome']
            return FinanceiroController(user_id)
        except Exception as exc:
            messagebox.showerror('Erro de conexão ou configuração',
                f'{exc}\n\nVerifique o banco, schema.sql e as variáveis DB_*.', parent=self)
            return None

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
        lbl(avatar, self.account_label, 10, TEXT, True, bg=CARD).pack(side='left')
        tk.Frame(self.shell, bg=BORDER, height=1).pack(fill='x')

    def navigate(self, name):
        if name not in PAGES:
            return
        self.current = name
        self.sidebar.select(name)
        self.breadcrumb.configure(text='MEUBOLSO   /   ' + name.upper())
        self._render(lambda body: PAGES[name](body, self.navigate, self.open_form))

    def open_form(self, title):
        section = title[0] if isinstance(title, tuple) else title
        action = 'EDITAR' if isinstance(title, tuple) else 'CADASTRAR'
        self.breadcrumb.configure(text=f'MEUBOLSO   /   FORMULÁRIOS   /   {action}   /   {section.upper()}')
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
