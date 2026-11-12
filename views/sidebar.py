# views/sidebar.py
import tkinter as tk
from views.styles import *

class Sidebar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg=SIDEBAR_BG, width=220)
        self.pack_propagate(False)
        self._criar_widgets()

    def _criar_widgets(self):
        # Logo / Título do App
        tk.Label(
            self, text="MeuBolso", fg=ACCENT_GREEN, bg=SIDEBAR_BG, 
            font=("Inter", 18, "bold")
        ).pack(pady=20, padx=20, anchor="w")
        
        # Linha separadora
        tk.Frame(self, bg=SEPARATOR_COLOR, height=1).pack(fill="x", padx=10, pady=(0, 10))
        
        # Itens de Navegação
        menus = ["Dashboard", "Rendas",'Categoria' , "Despesas", "Objetivos", "Regras", "Aportes"]
        for menu in menus:
            btn = tk.Button(
                self, text=f"  {menu}", bg=SIDEBAR_BG, fg=TEXT_SUB, 
                bd=0, font=FONT_MENU, anchor="w", 
                activebackground=SEPARATOR_COLOR, activeforeground=TEXT_TITLE,
                cursor="hand2"
            )
            btn.pack(fill="x", pady=2, padx=10, ipady=5)