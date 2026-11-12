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


class Icon(tk.Canvas):
    def __init__(self, master, name='dot', size=18, color=MUTED, bg=None):
        bg = bg or master.cget('bg')
        super().__init__(master, width=size, height=size, bg=bg, highlightthickness=0)
        self.name = name
        self.size = size
        self.color = color
        self.bg_color = bg
        self.draw()

    def recolor(self, color=None, bg=None):
        if color is not None:
            self.color = color
        if bg is not None:
            self.bg_color = bg
            self.configure(bg=bg)
        self.draw()

    def draw(self):
        self.delete('all')
        s = self.size
        c = self.color
        p = max(2, s // 10)
        m = max(3, s // 5)
        name = self.name
        if name == 'brand':
            self.create_rectangle(m, m, s - m, s - m, outline=c, width=2)
            self.create_rectangle(m + 4, m + 4, s - m - 4, s - m - 4, outline=c, width=1)
        elif name == 'dashboard':
            w = (s - 2*m - p) / 2
            h = (s - 2*m - p) / 2
            for r in range(2):
                for col in range(2):
                    x1 = m + col * (w + p)
                    y1 = m + r * (h + p)
                    self.create_rectangle(x1, y1, x1 + w, y1 + h, outline=c, width=2)
        elif name == 'income':
            self.create_line(s*0.25, s*0.75, s*0.72, s*0.28, fill=c, width=2)
            self.create_line(s*0.55, s*0.28, s*0.72, s*0.28, fill=c, width=2)
            self.create_line(s*0.72, s*0.28, s*0.72, s*0.45, fill=c, width=2)
        elif name == 'category':
            pts = [s*0.5, m, s-m, s*0.5, s*0.5, s-m, m, s*0.5]
            self.create_polygon(pts, outline=c, fill='', width=2)
            self.create_oval(s*0.45, s*0.45, s*0.55, s*0.55, outline=c, fill=c)
        elif name == 'expense':
            self.create_line(s*0.25, s*0.25, s*0.72, s*0.72, fill=c, width=2)
            self.create_line(s*0.55, s*0.72, s*0.72, s*0.72, fill=c, width=2)
            self.create_line(s*0.72, s*0.55, s*0.72, s*0.72, fill=c, width=2)
        elif name == 'goal':
            self.create_oval(m, m, s-m, s-m, outline=c, width=2)
            self.create_oval(s*0.35, s*0.35, s*0.65, s*0.65, outline=c, width=2)
            self.create_oval(s*0.47, s*0.47, s*0.53, s*0.53, outline=c, fill=c)
        elif name == 'rules':
            for y in (s*0.3, s*0.5, s*0.7):
                self.create_line(m, y, s-m, y, fill=c, width=2)
            for x in (s*0.35, s*0.65):
                self.create_line(x, s*0.22, x, s*0.78, fill=c, width=2)
        elif name == 'contributions':
            self.create_oval(m, m, s-m, s-m, outline=c, width=2)
            self.create_line(s*0.5, s*0.27, s*0.5, s*0.73, fill=c, width=2)
            self.create_line(s*0.27, s*0.5, s*0.73, s*0.5, fill=c, width=2)
        elif name == 'plus':
            self.create_line(s*0.5, s*0.2, s*0.5, s*0.8, fill=c, width=2)
            self.create_line(s*0.2, s*0.5, s*0.8, s*0.5, fill=c, width=2)
        elif name == 'wallet':
            self.create_rectangle(m, s*0.28, s-m, s*0.78, outline=c, width=2)
            self.create_rectangle(s*0.56, s*0.4, s-m+1, s*0.63, outline=c, width=2)
            self.create_oval(s*0.66, s*0.49, s*0.71, s*0.54, outline=c, fill=c)
        elif name == 'alert':
            self.create_oval(s*0.16, s*0.16, s*0.84, s*0.84, outline=c, width=2)
            self.create_line(s*0.5, s*0.34, s*0.5, s*0.57, fill=c, width=2)
            self.create_oval(s*0.47, s*0.67, s*0.53, s*0.73, outline=c, fill=c)
        elif name == 'check':
            self.create_oval(s*0.16, s*0.16, s*0.84, s*0.84, outline=c, width=2)
            self.create_line(s*0.32, s*0.52, s*0.45, s*0.65, s*0.7, s*0.38, fill=c, width=2, smooth=True)
        elif name == 'down':
            self.create_line(s*0.22, s*0.32, s*0.5, s*0.68, s*0.78, s*0.32, fill=c, width=2, smooth=True)
        elif name == 'up':
            self.create_line(s*0.22, s*0.68, s*0.5, s*0.32, s*0.78, s*0.68, fill=c, width=2, smooth=True)
        else:
            self.create_oval(s*0.35, s*0.35, s*0.65, s*0.65, outline=c, fill=c)


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
