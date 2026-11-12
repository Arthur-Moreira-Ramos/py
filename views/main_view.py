# views/main_view.py
import tkinter as tk
from tkinter import ttk
from views.styles import BG_COLOR, CARD_BG, TEXT_TABLE, SEPARATOR_COLOR, TEXT_SUB
from views.sidebar import Sidebar
from views.dashboard import Dashboard

class MainView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MeuBolso - Controle Financeiro")
        self.geometry("1100x650")
        self.configure(bg=BG_COLOR)
        
        self._configurar_estilos()
        self._montar_layout()

    def _configurar_estilos(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        style.configure(
            "Treeview", background=CARD_BG, foreground=TEXT_TABLE, fieldbackground=CARD_BG, 
            font=("Inter", 10), borderwidth=0, rowheight=30
        )
        style.map("Treeview", background=[("selected", SEPARATOR_COLOR)])
        
        style.configure(
            "Treeview.Heading", background=CARD_BG, foreground=TEXT_SUB, 
            font=("Inter", 10, "bold"), borderwidth=0
        )

    def _montar_layout(self):
        # Instancia e empacota o Menu Lateral
        self.sidebar = Sidebar(self)
        self.sidebar.pack(side="left", fill="y")
        
        # Instancia e empacota o Conteúdo Principal
        self.dashboard = Dashboard(self)
        self.dashboard.pack(side="left", fill="both", expand=True, padx=20, pady=20)