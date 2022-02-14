import os
import tkinter as tk
from random import randint
from tkinter import messagebox
from lib.table import Table
from lib.auto_hide_scrollbar import AutoHideScrollbar
from PIL import Image, ImageTk
from lib.tooltip import create_tool_tip
from tkinter.ttk import Combobox, Style
from src.gui.configuracoes import Configuracoes
import src.database as db


class GuiLiga:

    def __init__(self, liga):

        self.liga = liga
        self.root = tk.Tk()
        self.root.title(self.liga.nome)

        self.frame_header = tk.Frame(self.root, bg='#078745')
        self.frame_header.pack(fill=tk.X)

        self.icone_menu = tk.PhotoImage(file='assets/icones/menu.png')
        self.icone_editar = tk.PhotoImage(file='assets/icones/edit.png')
        self.icone_voltar = tk.PhotoImage(file='assets/icones/back.png')
        self.icone_sair = tk.PhotoImage(file='assets/icones/exit.png')
        self.icone_deletar = tk.PhotoImage(file='assets/icones/delete.png')
        self.icone_setas = tk.PhotoImage(file='assets/icones/arrows.png')
        self.icone_copa = tk.PhotoImage(file='assets/icones/cup.png')
        self.icone_time = tk.PhotoImage(file='assets/icones/team.png')
        self.icone_reset = tk.PhotoImage(file='assets/icones/reset.png')
        self.emblema_padrao = ImageTk.PhotoImage(Image.open('assets/emblemas/emblema_padrao.png').resize((30, 30),
                                                                                                         Image.BILINEAR))

        # Menus

        self.botao_menu = tk.Menubutton(self.frame_header, image=self.icone_menu, bg='#078745', bd=0,
                                        activebackground='#078745', cursor='hand2')
        self.botao_menu.pack(side=tk.LEFT, fill=tk.Y, padx=10)

        self.menu = tk.Menu(self.botao_menu, tearoff=0, bg='white', activebackground='#078745')
        self.botao_menu.config(menu=self.menu)

        self.menu_times = tk.Menu(self.menu, tearoff=0, bg='white', activebackground='#078745')

        for i, team in enumerate(self.liga.times):
            self.menu_times.add_command(label=team.nome, compound='left', font='arial 10', command=None)

        self.config = Configuracoes(self.liga, self)

        self.menu_editar = tk.Menu(self.menu, tearoff=0, bg='white', activebackground='#078745')
        self.menu_editar.add_command(label='Renomear Liga', image=self.icone_copa, compound='left', font='arial 10',
                                     command=self.config.abrir_janela_renomear_liga)
        self.menu_editar.add_command(label='Promoção/Rebaixamento', image=self.icone_setas, compound='left',
                                     font='arial 10', command=None)
        self.menu_editar.add_command(label='Resetar Liga', image=self.icone_reset, compound='left', font='arial 10',
                                     command=self.resetar_liga)
        self.menu_editar.add_command(label='Excluir Liga', image=self.icone_deletar, compound='left', font='arial 10',
                                     command=self.excluir_liga)

        self.menu.add_command(label='Tabela de Jogos', image=self.icone_copa, compound='left', font='arial 10',
                              command=None)
        self.menu.add_cascade(label='Times', image=self.icone_time, compound='left', font='arial 10',
                              menu=self.menu_times)
        self.menu.add_cascade(label='Editar', image=self.icone_editar, compound='left', font='arial 10',
                              menu=self.menu_editar)
        self.menu.add_command(label='Voltar ao Menu', image=self.icone_voltar, compound='left', font='arial 10',
                              command=self.voltar_ao_menu)
        self.menu.add_command(label='Sair', image=self.icone_sair, compound='left', font='arial 10',
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

        self.root.bind('<MouseWheel>', self.scroll)

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
        self.rodada_atual = self.definir_rodada_atual()
        self.tabela_de_jogos, self.combobox_rodada, self.label_msg = self.carregar_tabela_de_jogos()
        self.mostrar_rodada()

        w = self.root.winfo_screenwidth()
        h = self.root.winfo_screenheight()
        self.root.geometry(f'{w}x{h}+0+0')
        self.root.minsize(width=int(w / 2), height=int(h - 75))
        self.root.state('zoomed')

        self.root.mainloop()

    def carregar_tabela_de_classificacao(self):
        label_classificacao = tk.Label(self.frame_principal, text='CLASSIFICAÇÃO',
                                       height=3, font='rockwell 15 bold', fg='#078745')
        label_classificacao.grid(row=1, column=1)

        frame_classificacao = tk.Frame(self.frame_principal)
        frame_classificacao.grid(row=2, column=1, sticky='N', padx=65)

        header = ['#', 'TIME', 'PG', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']
        rows = self.liga.numero_de_times + 1
        columns = len(header)

        tabela_de_classificacao = Table(frame_classificacao, rows=rows, columns=columns,
                                        bg='gray99', font='arial 11', width=3, relief='flat', border_x=0, border_y=1)

        tabela_de_classificacao.config(column=1, width=30, anchor=tk.W, padx=5)
        tabela_de_classificacao.config(row=0, column=1, anchor=tk.CENTER)

        for i in range(2, 9, 2):
            tabela_de_classificacao.config(column=i, bg='gray95')

        tabela_de_classificacao.config(row=0, bg='gray91', font='arial 11 bold')
        tabela_de_classificacao.pack()

        footer = tk.Label(frame_classificacao, height=5)
        footer.pack()

        for c in range(columns):
            tabela_de_classificacao.insert(0, c, header[c])

        for i in range(self.liga.numero_de_times):
            frame_time = tk.Frame(tabela_de_classificacao.get_cell(i+1, 1))
            frame_time.pack(side=tk.LEFT, fill=tk.X)
            label_emblema = tk.Label(frame_time, bg='gray99')
            label_nome = tk.Label(frame_time, bg='gray99', font='arial 11')
            label_emblema.pack(side=tk.LEFT, fill=tk.BOTH)
            label_nome.pack(side=tk.LEFT, fill=tk.BOTH)

        return tabela_de_classificacao

    def carregar_tabela_de_jogos(self):
        label_jogos = tk.Label(self.frame_principal, text='JOGOS', height=3,
                               font='rockwell 15 bold', fg='#078745')

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
                                font='arial 11', border_x=0, pady=3)
        tabela_de_jogos.config(column=2, text='x', width=2, fg='grey')
        tabela_de_jogos.config(column=0)
        tabela_de_jogos.config(column=4)
        tabela_de_jogos.pack()

        label_msg = tk.Label(frame_jogos, font='arial 12 bold')
        label_msg.pack(pady=30)

        for i in range(self.liga.jogos_por_rodada):
            frame_time_mandante = tk.Frame(tabela_de_jogos.get_cell(i, 0), bg='gray99', pady=5, padx=10)
            frame_time_visitante = tk.Frame(tabela_de_jogos.get_cell(i, 4), bg='gray99', pady=5, padx=10)
            frame_time_mandante.pack(fill=tk.Y)
            frame_time_visitante.pack(fill=tk.Y)

            label_emblema_mandante = tk.Label(frame_time_mandante, bg='gray99')
            label_time_mandante = tk.Label(frame_time_mandante, bg='gray99', font='arial 12', width=3, padx=10)
            label_emblema_mandante.pack(side=tk.RIGHT)
            label_time_mandante.pack(fill=tk.Y, expand=True)

            label_emblema_visitante = tk.Label(frame_time_visitante, bg='gray99')
            label_time_visitante = tk.Label(frame_time_visitante, bg='gray99', font='arial 12', width=3, padx=10)
            label_emblema_visitante.pack(side=tk.LEFT)
            label_time_visitante.pack(fill=tk.Y, expand=True)

            frame_placar_mandante = tk.Frame(tabela_de_jogos.get_cell(i, 1), bg='gray99')
            frame_placar_visitante = tk.Frame(tabela_de_jogos.get_cell(i, 3), bg='gray99')
            frame_placar_mandante.pack(fill=tk.Y)
            frame_placar_visitante.pack(fill=tk.Y)

        return tabela_de_jogos, combobox_rodada, label_msg

    def scroll(self, event):
        if self.yscrollbar.winfo_ismapped():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

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

            celula = self.tabela_de_classificacao.get_cell(i+1, 1)
            frame_time = celula.winfo_children()[0]

            if time.emblema is not None:
                emblema = ImageTk.PhotoImage(Image.open(time.emblema).resize((20, 20), Image.BILINEAR))
            else:
                emblema = self.emblema_padrao

            label_emblema = frame_time.winfo_children()[0]
            label_emblema.config(image=emblema)
            label_emblema.img = emblema
            label_nome = frame_time.winfo_children()[1]
            label_nome.config(text=time.nome)

    def proxima_rodada(self):
        index = self.rodada_atual.numero
        if index < self.liga.numero_de_rodadas:
            self.rodada_atual = self.liga.get_rodada(index)
            self.mostrar_rodada()

    def rodada_anterior(self):
        index = self.rodada_atual.numero - 2
        if index >= 0:
            self.rodada_atual = self.liga.get_rodada(index)
            self.mostrar_rodada()

    def selecionar_rodada(self, event):
        index = self.combobox_rodada.current()
        self.rodada_atual = self.liga.get_rodada(index)
        self.mostrar_rodada()
        self.root.focus()

    def mostrar_rodada(self):
        self.combobox_rodada.current(self.rodada_atual.numero - 1)

        for i, jogo in enumerate(self.rodada_atual.jogos):
            frame_time_mandante = self.tabela_de_jogos.get_cell(i, 0).winfo_children()[0]
            frame_placar_mandante = self.tabela_de_jogos.get_cell(i, 1).winfo_children()[0]
            frame_placar_visitante = self.tabela_de_jogos.get_cell(i, 3).winfo_children()[0]
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

            try:
                entry_placar_mandante = frame_placar_mandante.winfo_children()[0]
                entry_placar_visitante = frame_placar_visitante.winfo_children()[0]
            except IndexError:
                pass
            else:
                entry_placar_mandante.destroy()
                entry_placar_visitante.destroy()

            entry_placar_mandante = tk.Entry(frame_placar_mandante, width=3, font='arial 19 bold', fg='#078745',
                                             justify=tk.CENTER, bd=2)
            entry_placar_visitante = tk.Entry(frame_placar_visitante, width=3, font='arial 19 bold', fg='#078745',
                                              justify=tk.CENTER, bd=2)
            entry_placar_mandante.pack(anchor=tk.CENTER, pady=5)
            entry_placar_visitante.pack(anchor=tk.CENTER, pady=5)

            sv_mandante = tk.StringVar()
            sv_visitante = tk.StringVar()
            sv_mandante.set(jogo.gols_time_mandante)
            sv_visitante.set(jogo.gols_time_visitante)

            for sv in (sv_mandante, sv_visitante):
                sv.trace('w', lambda name, index, mode, sv1=sv_mandante, sv2=sv_visitante,
                                     index_jogo=i: self.editar_placar(sv1.get(), sv2.get(), index_jogo))

            entry_placar_mandante.config(textvariable=sv_mandante)
            entry_placar_visitante.config(textvariable=sv_visitante)

    def definir_rodada_atual(self):
        for rodada in self.liga.rodadas:
            for jogo in rodada.jogos:
                if jogo.gols_time_mandante == '':
                    return rodada
        return self.liga.get_rodada(0)

    def editar_placar(self, gols_mandante, gols_visitante, index):
        jogo = self.rodada_atual.get_jogo(index)
        jogo.resetar()
        try:
            gols_mandante = int(gols_mandante)
            gols_visitante = int(gols_visitante)
        except ValueError:
            pass
        else:
            jogo.definir_placar(gols_mandante, gols_visitante)

        self.label_msg.config(text='Salvando... ⌛', fg='gray')
        self.liga.atualizar_classificacao()
        self.atualizar_tabela()
        db.update_resultado(self.liga.nome, self.rodada_atual.numero, jogo)
        self.label_msg.after(500, lambda: self.label_msg.config(text='Salvo automaticamente ✔️', fg='green'))
        self.label_msg.after(2500, lambda: self.label_msg.config(text=''))

    def renomear_liga(self, event=None):
        nome_antigo = self.liga.nome
        nome_novo = self.config.entry_nome.get()
        if nome_novo == self.liga.nome or f'{nome_novo}.db' not in os.listdir('data'):
            self.liga.nome = nome_novo
            self.root.title(self.liga.nome)
            self.header.config(text=self.liga.nome.upper())
            self.config.window_renomear_liga.destroy()
            db.update_nome_liga(nome_antigo, nome_novo)
        else:
            messagebox.showerror(title='Erro!', message='Já existe um campeonato com esse nome!')

    def excluir_liga(self):
        from src.gui.menu import Menu
        if messagebox.askyesno('Excluir Campeonato', f'Tem certeza que deseja excluir "{self.liga.nome}"?'):
            db.deletar_liga(self.liga.nome)
            messagebox.showinfo('Concluído!', f'"{self.liga.nome}" foi excluído com sucesso!')
            self.root.destroy()
            Menu()

    def resetar_liga(self):
        for rodada in self.liga.rodadas:
            rodada.resetar()
        self.atualizar_tabela()
        self.rodada_atual = self.liga.get_rodada(0)
        self.mostrar_rodada()
        db.resetar_liga(self.liga.nome)

    def voltar_ao_menu(self):
        from src.gui.menu import Menu
        self.root.destroy()
        Menu()

    def gerar_placares(self):
        # Para testes
        for rodada in self.liga.rodadas:
            for jogo in rodada.jogos:
                jogo.definir_placar(randint(0, 5), randint(0, 5))
        self.liga.atualizar_classificacao()
        self.atualizar_tabela()
        self.rodada_atual = self.liga.get_rodada(0)
        self.mostrar_rodada()
