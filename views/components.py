"""Componentes visuais em Tkinter puro; sem lógica de domínio."""
import tkinter as tk
from tkinter import ttk
from .styles import *
from .data_demo import money


def lbl(parent, text, size=13, color=TEXT, bold=False, bg=None, **kw):
    return tk.Label(
        parent,
        text=text,
        font=font(size, 'bold' if bold else 'normal'),
        bg=bg or parent.cget('bg'),
        fg=color,
        anchor='w',
        **kw,
    )


def card(parent, pad=18, bg=CARD):
    outer = tk.Frame(parent, bg=bg, highlightbackground=BORDER, highlightthickness=1)
    inner = tk.Frame(outer, bg=bg, padx=pad, pady=pad)
    inner.pack(fill='both', expand=True)
    return outer, inner


class Icon(tk.Label):
    """Ícone antialiasado com assets PNG e recoloração em memória.

    A imagem é renderizada no tamanho final com Lanczos, em vez de
    desenhar linhas fracionárias num Canvas minúsculo.
    """
    _cache = {}

    def __init__(self, master, name='dot', size=18, color=MUTED, bg=None):
        from pathlib import Path
        self.name = name
        self.size = int(size)
        self.color = color
        self.bg_color = bg or master.cget('bg')
        super().__init__(master, bg=self.bg_color, borderwidth=0,
                         highlightthickness=0, padx=0, pady=0)
        self.recolor(color, self.bg_color)

    def recolor(self, color=None, bg=None):
        from pathlib import Path
        from PIL import Image, ImageTk, ImageColor
        if color is not None:
            self.color = color
        if bg is not None:
            self.bg_color = bg
        key = (self.name, self.size, self.color)
        image = self._cache.get(key)
        if image is None:
            file = Path(__file__).resolve().parent / 'assets' / 'icons' / (self.name + '.png')
            if not file.exists():
                file = file.with_name('dot.png')
            with Image.open(file) as src:
                rgba = src.convert('RGBA').resize((self.size, self.size), Image.Resampling.LANCZOS)
            alpha = rgba.getchannel('A')
            image = Image.new('RGBA', rgba.size, ImageColor.getrgb(self.color) + (0,))
            image.putalpha(alpha)
            self._cache[key] = image
        self._photo = ImageTk.PhotoImage(image, master=self)
        self.configure(image=self._photo, bg=self.bg_color)


def icon_button(parent, text, command=None, primary=True, small=False, bg=None, icon_name=None):
    return ActionButton(parent, text=text, command=command, primary=primary, small=small, bg=bg, icon_name=icon_name)


class ActionButton(tk.Frame):
    def __init__(self, master, text, command=None, primary=True, small=False, bg=None, icon_name=None):
        super().__init__(master, bg=bg or master.cget('bg'))
        self.primary = primary
        self.base = GREEN if primary else BORDER
        self.hover = '#0DA574' if primary else '#475569'
        self.content = tk.Frame(self, bg=self.base, cursor='hand2', padx=12 if small else 14, pady=7 if small else 9)
        self.content.pack(fill='both', expand=True)
        self.icon = None
        if icon_name:
            self.icon = Icon(self.content, icon_name, size=14 if small else 16, color=WHITE, bg=self.base)
            self.icon.pack(side='left', padx=(0, 7))
        self.label = tk.Label(
            self.content,
            text=text,
            bg=self.base,
            fg=WHITE,
            cursor='hand2',
            font=font(10 if small else 11, 'bold'),
        )
        self.label.pack(side='left')
        self._bind_widget(self)
        self._bind_widget(self.content)
        self._bind_widget(self.label)
        if self.icon is not None:
            self._bind_widget(self.icon)
        if command:
            for widget in (self, self.content, self.label, self.icon):
                if widget is not None:
                    widget.bind('<Button-1>', lambda event=None: command())

    def _bind_widget(self, widget):
        widget.bind('<Enter>', lambda event=None: self._apply(self.hover))
        widget.bind('<Leave>', lambda event=None: self._apply(self.base))

    def _apply(self, color):
        self.content.configure(bg=color)
        self.label.configure(bg=color)
        if self.icon is not None:
            self.icon.recolor(WHITE, color)


def field(parent, name, placeholder='', width=26):
    lbl(parent, name, 10, MUTED).pack(fill='x', pady=(8, 5))
    entry = tk.Entry(
        parent,
        bg=BG,
        fg=TEXT,
        insertbackground=WHITE,
        relief='flat',
        highlightthickness=1,
        highlightbackground=BORDER,
        highlightcolor=GREEN,
        font=font(11),
        width=width,
    )
    entry.pack(fill='x', ipady=10)
    if placeholder:
        entry.insert(0, placeholder)
        entry.configure(fg=DIM)

        def focus_in(_):
            if entry.get() == placeholder:
                entry.delete(0, 'end')
                entry.configure(fg=TEXT)

        def focus_out(_):
            if not entry.get():
                entry.insert(0, placeholder)
                entry.configure(fg=DIM)

        entry.bind('<FocusIn>', focus_in)
        entry.bind('<FocusOut>', focus_out)
    return entry


def dropdown(parent, name, options):
    lbl(parent, name, 10, MUTED).pack(fill='x', pady=(8, 5))
    var = tk.StringVar(value=options[0])
    combo = ttk.Combobox(parent, textvariable=var, values=options, state='readonly', font=font(10))
    combo.pack(fill='x', ipady=6)
    return var


def section_header(parent, title, subtitle=None, button=None, callback=None):
    header = tk.Frame(parent, bg=BG)
    header.pack(fill='x', pady=(0, 18))
    left = tk.Frame(header, bg=BG)
    left.pack(side='left')
    lbl(left, title, 22, WHITE, True).pack(anchor='w')
    if subtitle:
        lbl(left, subtitle, 10, MUTED).pack(anchor='w', pady=(6, 0))
    if button:
        ActionButton(header, button, callback, small=True, icon_name='plus').pack(side='right', pady=4)
    return header


def stat(parent, title, value, detail, accent=WHITE, badge='dot', compact=False):
    outer, inside = card(parent, 16 if compact else 18)
    top = tk.Frame(inside, bg=CARD)
    top.pack(fill='x')
    lbl(top, title, 10, MUTED).pack(side='left')
    badge_icon = badge if badge in {'wallet', 'up', 'down', 'goal', 'check'} else 'dot'
    Icon(top, badge_icon, size=14, color=accent, bg=CARD).pack(side='right')
    lbl(inside, value, 18 if compact else 21, accent, True).pack(anchor='w', pady=(10, 7))
    lbl(inside, detail, 9, MUTED).pack(anchor='w')
    return outer


def progress(parent, ratio, color=GREEN, width=240, height=7, animate=True):
    c = tk.Canvas(parent, width=width, height=height, bg=parent.cget('bg'), highlightthickness=0)
    c.create_rectangle(0, 0, width, height, fill=BORDER, outline='')
    target = max(0, min(1, ratio)) * width
    bar = c.create_rectangle(0, 0, 0 if animate else target, height, fill=color, outline='')
    if animate:
        def step(current=0):
            if not c.winfo_exists():
                return
            nxt = min(target, current + max(3, target / 18))
            c.coords(bar, 0, 0, nxt, height)
            if nxt < target:
                c.after(16, lambda: step(nxt))
        c.after(120, step)
    return c


def data_table(parent, headers, rows, widths=None, formats=None):
    """Tabela visual sem callbacks de persistência."""
    frame = tk.Frame(parent, bg=CARD)
    weights = widths or [2] + [1] * (len(headers) - 1)
    for j, weight in enumerate(weights):
        frame.grid_columnconfigure(j, weight=weight, uniform='table')
    for j, header in enumerate(headers):
        lbl(frame, header.upper(), 8, MUTED, True, bg=CARD).grid(row=0, column=j, sticky='ew', pady=(2, 12), padx=6)
    for i, row in enumerate(rows, 1):
        sep = tk.Frame(frame, bg=BORDER, height=1)
        sep.grid(row=2 * i - 1, column=0, columnspan=len(headers), sticky='ew')
        for j, value in enumerate(row):
            color = TEXT if j == 0 else MUTED
            if isinstance(value, (float, int)):
                value = money(value)
            if isinstance(value, str) and value.startswith('+'):
                color = GREEN
            if isinstance(value, str) and value.startswith('-'):
                color = RED
            lbl(frame, str(value), 10, color, j == 0, bg=CARD).grid(
                row=2 * i,
                column=j,
                sticky='ew',
                padx=6,
                pady=12,
            )
    return frame


class ScrollPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg=BG)
        self.canvas = tk.Canvas(self, bg=BG, highlightthickness=0)
        self.scroll = ttk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scroll.set)
        self.scroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        self.body = tk.Frame(self.canvas, bg=BG, padx=4, pady=4)
        self.window = self.canvas.create_window((0, 0), window=self.body, anchor='nw')
        self.body.bind('<Configure>', lambda _: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda e: self.canvas.itemconfigure(self.window, width=e.width))
        self.canvas.bind('<Enter>', lambda _: self.canvas.bind_all('<MouseWheel>', self._wheel))
        self.canvas.bind('<Leave>', lambda _: self.canvas.unbind_all('<MouseWheel>'))

    def _wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), 'units')
