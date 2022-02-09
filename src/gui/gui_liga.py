import tkinter as tk
from lib.table import Table
from lib.auto_hide_scrollbar import AutoHideScrollbar
from PIL import Image, ImageTk
from lib.tooltip import create_tool_tip
from tkinter.ttk import Combobox, Style


class GUILiga:

    def __init__(self, liga):

        self.liga = liga
        self.root = tk.Tk()
        self.root.title(self.liga.nome)

        self.frame_header = tk.Frame(self.root, bg='#078745')
        self.frame_header.pack(fill=tk.X)

        self.menu_icon = tk.PhotoImage(file='assets/menu.png')
        self.edit_icon = tk.PhotoImage(file='assets/edit.png')
        self.back_icon = tk.PhotoImage(file='assets/back.png')
        self.exit_icon = tk.PhotoImage(file='assets/exit.png')
        self.delete_icon = tk.PhotoImage(file='assets/delete.png')
        self.arrows_icon = tk.PhotoImage(file='assets/arrows.png')
        self.cup_icon = tk.PhotoImage(file='assets/cup.png')
        self.team_icon = tk.PhotoImage(file='assets/team.png')
        self.reset_icon = tk.PhotoImage(file='assets/reset.png')
        self.emblema_padrao = ImageTk.PhotoImage(Image.open('assets/emblemas/emblema.png').resize((30, 30),
                                                 Image.BILINEAR))

        self.menu_button = tk.Menubutton(self.frame_header, image=self.menu_icon, bg='#078745', bd=0,
                                         activebackground='#078745', cursor='hand2')
        self.menu_button.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.menu = tk.Menu(self.menu_button, tearoff=0, bg='white', activebackground='#078745')
        self.menu_button.config(menu=self.menu)

        self.teams_menu = tk.Menu(self.menu, tearoff=0, bg='white', activebackground='#078745')

        for i, team in enumerate(self.liga.times):
            self.teams_menu.add_command(label=team.nome, compound='left', font='arial 10', command=None)

        self.edit_menu = tk.Menu(self.menu, tearoff=0, bg='white', activebackground='#078745')
        self.edit_menu.add_command(label='Renomear Campeonato', image=self.cup_icon, compound='left', font='arial 10',
                                   command=None)
        self.edit_menu.add_command(label='Renomear Times', image=self.team_icon, compound='left', font='arial 10',
                                   command=None)
        self.edit_menu.add_command(label='Promoção/Rebaixamento', image=self.arrows_icon, compound='left',
                                   font='arial 10',
                                   command=None)
        self.edit_menu.add_command(label='Resetar Campeonato', image=self.reset_icon, compound='left', font='arial 10',
                                   command=None)
        self.edit_menu.add_command(label='Excluir Campeonato', image=self.delete_icon, compound='left', font='arial 10',
                                   command=None)

        self.menu.add_command(label='Tabela de Jogos', image=self.cup_icon, compound='left', font='arial 10',
                              command=None)
        self.menu.add_cascade(label='Times', image=self.team_icon, compound='left', font='arial 10',
                              menu=self.teams_menu)
        self.menu.add_cascade(label='Editar', image=self.edit_icon, compound='left', font='arial 10',
                              menu=self.edit_menu)
        self.menu.add_command(label='Voltar ao Menu', image=self.back_icon, compound='left', font='arial 10',
                              command=None)
        self.menu.add_command(label='Sair', image=self.exit_icon, compound='left', font='arial 10',
                              command=self.root.destroy)

        self.menu.insert_separator(4)

        self.header = tk.Label(self.frame_header, text=self.liga.nome.upper(), bg='#078745',
                               fg='white', font='rockwell 20 bold', pady=5)
        self.header.pack()

        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.yscrollbar = AutoHideScrollbar(self.root, orient=tk.VERTICAL, command=self.canvas.yview)
        self.xscrollbar = AutoHideScrollbar(self.root, orient=tk.HORIZONTAL, command=self.canvas.xview)
        self.canvas.configure(xscrollcommand=self.xscrollbar.set, yscrollcommand=self.yscrollbar.set)

        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.frame_principal = tk.Frame(self.canvas)
        self.frame_principal.bind('<Configure>',
                                  lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.create_window((0, 0), window=self.frame_principal, anchor=tk.N)
        self.canvas.bind('<Configure>', lambda event:  self.frame_principal.config(
            padx=(event.width - self.frame_principal.winfo_width() - 4) // 2
        ))

        # Tabela de classificação
        self.tabela_de_classificacao = self.carregar_tabela_de_classificacao()
        self.atualizar_tabela()

        # Tabela de jogos
        self.rodada_atual = self.liga.rodadas[0]
        self.tabela_de_jogos, self.combobox_rodada = self.carregar_tabela_de_jogos()
        self.mostrar_rodada()

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f'{w}x{h}+0+0')
        self.root.minsize(width=int(w / 2), height=int(h - 75))
        self.root.state('zoomed')

        self.root.mainloop()

    def carregar_menus(self):
        pass

    def carregar_tabela_de_classificacao(self):
        label_classificacao = tk.Label(self.frame_principal, text='CLASSIFICAÇÃO',
                                       height=3, font='rockwell 13 bold', fg='#078745')
        label_classificacao.grid(row=1, column=1)

        frame_classificacao = tk.Frame(self.frame_principal)
        frame_classificacao.grid(row=2, column=1, sticky='N', padx=65)

        header = ['#', 'TIME', 'PG', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']
        rows = self.liga.numero_de_times + 1
        columns = len(header)

        tabela_de_classificacao = Table(frame_classificacao, rows=rows, columns=columns,
                                        bg='gray99', font='arial 11', width=3, relief='flat', pady=4)

        tabela_de_classificacao.config(column=1, width=25, anchor=tk.W, padx=5)
        tabela_de_classificacao.config(row=0, bg='lightgrey', font='arial 11 bold')
        tabela_de_classificacao.config(row=0, column=1, anchor=tk.CENTER)
        tabela_de_classificacao.pack()

        for c in range(columns):
            tabela_de_classificacao.insert(0, c, header[c])

        return tabela_de_classificacao

    def carregar_tabela_de_jogos(self):
        label_jogos = tk.Label(self.frame_principal, text='JOGOS', height=3,
                               font='rockwell 13 bold', fg='#078745')

        label_jogos.grid(row=1, column=4)

        frame_jogos = tk.Frame(self.frame_principal)
        frame_jogos.grid(row=2, column=4, sticky='N', padx=65)

        frame_header_rodada = tk.Frame(frame_jogos, bg='gray91')
        frame_header_rodada.pack(fill=tk.X)

        botao_rodada_anterior = tk.Button(frame_header_rodada, text='<', fg='#078745', command=self.rodada_anterior,
                                          relief='flat', cursor='hand2', bg='gray91', font='arial 12 bold')

        botao_rodada_seguinte = tk.Button(frame_header_rodada, text='>', fg='#078745', command=self.proxima_rodada,
                                          relief='flat', cursor='hand2', bg='gray91', font='arial 12 bold')

        botao_rodada_anterior.grid(row=0, column=0)
        botao_rodada_seguinte.grid(row=0, column=2)

        style = Style()
        values = [f'{rodada.numero}ª RODADA' for rodada in self.liga.rodadas]
        combobox_rodada = Combobox(frame_header_rodada, values=values, font='arial 11 bold', cursor='hand2',
                                   width=34)
        style.map('TCombobox', foreground=[('readonly', 'black')])
        combobox_rodada.config(justify=tk.CENTER, state='readonly')
        combobox_rodada.bind('<<ComboboxSelected>>', self.selecionar_rodada)
        combobox_rodada.current(0)
        combobox_rodada.grid(row=0, column=1, sticky='NSWE')
        frame_jogos.option_add('*TCombobox*Listbox.selectBackground', '#078745')

        tabela_de_jogos = Table(frame_jogos, rows=self.liga.jogos_por_rodada, columns=5, bg='gray99',
                                font='arial 11', border_x=0, pady=3, cursor='hand2')
        tabela_de_jogos.config(column=2, text='x', width=2, fg='grey')
        tabela_de_jogos.config(column=0)
        tabela_de_jogos.config(column=4)
        tabela_de_jogos.config(column=1, width=3, font='arial 18 bold')
        tabela_de_jogos.config(column=3, width=3, font='arial 18 bold')
        tabela_de_jogos.pack()

        for i in range(self.liga.jogos_por_rodada):
            frame_time_mandante = tk.Frame(tabela_de_jogos.get_cell(i, 0), bg='gray99', pady=5, padx=35)
            frame_time_visitante = tk.Frame(tabela_de_jogos.get_cell(i, 4), bg='gray99', pady=5, padx=35)
            frame_time_mandante.pack()
            frame_time_visitante.pack()

            label_emblema_mandante = tk.Label(frame_time_mandante, bg='gray99')
            label_time_mandante = tk.Label(frame_time_mandante, bg='gray99', font='arial 12', width=3)
            label_emblema_mandante.pack()
            label_time_mandante.pack()

            label_emblema_visitante = tk.Label(frame_time_visitante, bg='gray99')
            label_time_visitante = tk.Label(frame_time_visitante, bg='gray99', font='arial 12', width=3)
            label_emblema_visitante.pack()
            label_time_visitante.pack()

        return tabela_de_jogos, combobox_rodada

    def atualizar_tabela(self):
        for i, time in enumerate(self.liga.classificacao):
            self.tabela_de_classificacao.insert(i+1, 0, i+1)
            self.tabela_de_classificacao.insert(i + 1, 2, time.pontos)
            self.tabela_de_classificacao.insert(i + 1, 3, time.jogos)
            self.tabela_de_classificacao.insert(i + 1, 4, time.vitorias)
            self.tabela_de_classificacao.insert(i + 1, 5, time.empates)
            self.tabela_de_classificacao.insert(i + 1, 6, time.derrotas)
            self.tabela_de_classificacao.insert(i + 1, 7, time.gols_feitos)
            self.tabela_de_classificacao.insert(i + 1, 8, time.gols_sofridos)
            self.tabela_de_classificacao.insert(i + 1, 9, time.saldo_de_gols)

            frame_time = tk.Frame(self.tabela_de_classificacao.get_cell(i+1, 1))
            frame_time.pack(side=tk.LEFT, fill=tk.X)

            if time.emblema is not None:
                emblema = ImageTk.PhotoImage(Image.open(time.emblema).resize((20, 20), Image.BILINEAR))
            else:
                emblema = self.emblema_padrao

            label_emblema = tk.Label(frame_time, image=emblema, bg='gray99')
            label_emblema.img = emblema
            label_nome = tk.Label(frame_time, text=time.nome, bg='gray99', font='arial 11')
            label_emblema.pack(side=tk.LEFT, fill=tk.BOTH)
            label_nome.pack(side=tk.LEFT, fill=tk.BOTH)

    def proxima_rodada(self):
        index = self.rodada_atual.numero
        if index < self.liga.numero_de_rodadas:
            self.rodada_atual = self.liga.rodadas[index]
            self.mostrar_rodada()

    def rodada_anterior(self):
        index = self.rodada_atual.numero - 2
        if index >= 0:
            self.rodada_atual = self.liga.rodadas[index]
            self.mostrar_rodada()

    def selecionar_rodada(self, event):
        index = self.combobox_rodada.current()
        self.rodada_atual = self.liga.rodadas[index]
        self.mostrar_rodada()
        self.root.focus()

    def mostrar_rodada(self):
        self.combobox_rodada.current(self.rodada_atual.numero - 1)

        for i, jogo in enumerate(self.rodada_atual.jogos):

            frame_time_mandante = self.tabela_de_jogos.get_cell(i, 0).winfo_children()[0]
            frame_time_visitante = self.tabela_de_jogos.get_cell(i, 4).winfo_children()[0]

            label_emblema_mandante = frame_time_mandante.winfo_children()[0]
            label_time_mandante = frame_time_mandante.winfo_children()[1]

            label_emblema_visitante = frame_time_visitante.winfo_children()[0]
            label_time_visitante = frame_time_visitante.winfo_children()[1]

            create_tool_tip(frame_time_mandante, jogo.time_mandante)
            create_tool_tip(frame_time_visitante, jogo.time_visitante)

            if jogo.time_mandante.emblema is not None:
                emblema_time_mandante = ImageTk.PhotoImage(
                    Image.open(jogo.time_mandante.emblema).resize((30, 30), Image.BILINEAR))
            else:
                emblema_time_mandante = self.emblema_padrao

            if jogo.time_visitante.emblema is not None:
                emblema_time_visitante = ImageTk.PhotoImage(
                    Image.open(jogo.time_visitante.emblema).resize((30, 30), Image.BILINEAR))
            else:
                emblema_time_visitante = self.emblema_padrao

            label_emblema_mandante.config(image=emblema_time_mandante)
            label_emblema_mandante.img = emblema_time_mandante
            label_emblema_visitante.config(image=emblema_time_visitante)
            label_emblema_visitante.img = emblema_time_visitante
            label_time_mandante.config(text=jogo.time_mandante.sigla)
            label_time_visitante.config(text=jogo.time_visitante.sigla)

            self.tabela_de_jogos.insert(i, 1, jogo.gols_time_mandante)
            self.tabela_de_jogos.insert(i, 3, jogo.gols_time_visitante)
