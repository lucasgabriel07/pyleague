import tkinter as tk
from tkinter import colorchooser, messagebox
from src.highlight import Highlight
import src.database as db


class Configuracoes:

    def __init__(self, liga, gui_liga):
        self.liga = liga
        self.gui_liga = gui_liga

        self.window_renomear_liga = None
        self.label_nome = None
        self.entry_nome = None
        self.botao_renomear_liga = None

    def abrir_janela_renomear_liga(self):
        self.window_renomear_liga = tk.Tk()
        self.window_renomear_liga.title('Renomear Liga')

        self.label_nome = tk.Label(self.window_renomear_liga, text='NOME:', font='arial 15 bold')
        self.label_nome.grid(row=0, column=0, sticky='e', padx=10, pady=20)

        self.entry_nome = tk.Entry(self.window_renomear_liga, width=50, font='arial 20 bold', fg='#078745')
        self.entry_nome.bind('<Return>', self.gui_liga.renomear_liga)
        self.entry_nome.insert(0, self.liga.nome)
        self.entry_nome.grid(row=0, column=1, padx=3, pady=30)

        self.botao_renomear_liga = tk.Button(self.window_renomear_liga, bg='white', bd=1, text='Ok',
                                             command=self.gui_liga.renomear_liga, font='arial 12', width=2,
                                             cursor='hand2')
        self.botao_renomear_liga.grid(row=0, column=2, padx=10)

        self.window_renomear_liga.geometry('+180+270')
        self.window_renomear_liga.resizable(width=False, height=False)
        self.window_renomear_liga.mainloop()


class AdicionaHighlights:

    def __init__(self, liga, gui_liga):
        self.liga = liga
        self.gui_liga = gui_liga

        self.root = tk.Tk()
        self.root.title('Classificação/Rebaixamento')

        self.label_titulo = tk.Label(self.root, text='CLASSIFICAÇÃO/REBAIXAMENTO', bg='#078745', fg='white',
                                     font='arial 12 bold', pady=3)
        self.label_titulo.pack(fill='x')

        self.frame_botao = tk.Frame(self.root)
        self.frame_botao.pack(pady=15, padx=50)

        self.botao_adicionar = tk.Button(self.frame_botao, text='+', font='arial 12 bold', bg='white', fg='#078745',
                                         width=3, command=self.abrir_janela_adicionar_highlights)
        self.botao_adicionar.pack()

        self.frame_principal = tk.Frame(self.root)
        self.frame_principal.pack()

        self.icone_editar = tk.PhotoImage(file='assets/icones/edit.png', master=self.frame_principal)
        self.icone_deletar = tk.PhotoImage(file='assets/icones/delete.png', master=self.frame_principal)

        self.atualizar_janela()

        # Janela de adição de highlights
        self.window_add_highlights = None
        self.frame_add_highlights = None
        self.entry = None
        self.botao_bg = None
        self.botao_fg = None

        self.root.geometry('400x250+450+200')
        self.root.resizable(0, 1)
        self.root.mainloop()

    def abrir_janela_adicionar_highlights(self, edicao=False, index=None, texto='', bg='#078745', fg='white'):
        self.window_add_highlights = tk.Tk()
        self.window_add_highlights.title('')
        self.frame_add_highlights = tk.Frame(self.window_add_highlights)
        self.frame_add_highlights.pack(pady=10, padx=10)
        self.entry = tk.Entry(self.frame_add_highlights, width=7, justify=tk.CENTER)
        self.entry.bind('<Return>', lambda e: self.confirmar(edicao, index))
        self.entry.insert(0, texto)
        self.entry.focus_force()
        self.entry.selection_range(0, 'end')

        label1 = tk.Label(self.frame_add_highlights, text='Times*:', font='arial 10 bold')
        label2 = tk.Label(self.frame_add_highlights, text='* Ex: 1 - 4', fg='gray', font='arial 10')
        label3 = tk.Label(self.frame_add_highlights, text='Cor de Fundo:', font='arial 10 bold')
        label4 = tk.Label(self.frame_add_highlights, text='Cor da Fonte:', font='arial 10 bold')

        self.botao_bg = tk.Button(self.frame_add_highlights, width=3, bg=bg)
        self.botao_fg = tk.Button(self.frame_add_highlights, width=3, bg=fg)
        botao_confirmar = tk.Button(self.frame_add_highlights, text='Ok', bg='white', bd=1,
                                    command=lambda: self.confirmar(edicao, index))

        self.botao_bg.bind('<1>', lambda e: self.escolher_cor(e))
        self.botao_fg.bind('<1>', lambda e: self.escolher_cor(e))

        label1.grid(row=0, column=0)
        self.entry.grid(row=0, column=1, padx=5)
        label2.grid(row=1, column=0, padx=5, columnspan=2, sticky='W')
        label3.grid(row=0, column=2, padx=5)
        self.botao_bg.grid(row=0, column=3, padx=5)
        label4.grid(row=0, column=4, padx=5)
        self.botao_fg.grid(row=0, column=5, padx=5)
        botao_confirmar.grid(row=2, column=0, columnspan=6, padx=5)

        self.window_add_highlights.geometry('+447+270')
        self.window_add_highlights.resizable(0, 0)
        self.window_add_highlights.mainloop()

    def atualizar_janela(self):
        for w in self.frame_principal.winfo_children():
            w.grid_forget()

        if len(self.liga.highlights_tabela) == 0:
            label_msg = tk.Label(self.frame_principal, text='Não há classificações ou rebaixamentos cadastrados.',
                                 fg='#078745', font='arial 10 bold', pady=50)
            label_msg.grid()
        else:
            label_times = tk.Label(self.frame_principal, text='Times', bg='gray91', font='arial 10 bold', width=12)
            label_cor_fundo = tk.Label(self.frame_principal, text='Cor do Fundo', bg='gray91', font='arial 10 bold',
                                       width=12)
            label_cor_fonte = tk.Label(self.frame_principal, text='Cor da Fonte', bg='gray91', font='arial 10 bold',
                                       width=12)
            label_times.grid(row=0, column=0, pady=1, padx=1)
            label_cor_fundo.grid(row=0, column=1, pady=1, padx=1)
            label_cor_fonte.grid(row=0, column=2, pady=1, padx=1)

            for i, highlight in enumerate(self.liga.highlights_tabela):

                label_posicoes = tk.Label(self.frame_principal, bg='white', font='arial 10')
                label_bg = tk.Label(self.frame_principal, bg=highlight.bg, font='arial 10')
                label_fg = tk.Label(self.frame_principal, bg=highlight.fg, font='arial 10')

                if highlight.inicio == highlight.fim:
                    label_posicoes.config(text=highlight.inicio)
                else:
                    label_posicoes.config(text=f'{highlight.inicio} - {highlight.fim}')

                botao_editar = tk.Button(self.frame_principal, image=self.icone_editar, bd=0,
                                         command=lambda index=i: self.editar_highlight(index))
                botao_deletar = tk.Button(self.frame_principal, image=self.icone_deletar, bd=0,
                                          command=lambda index=i: self.remover_highlight(index))

                label_posicoes.grid(row=i + 1, column=0, pady=1, padx=1, sticky='WE')
                label_bg.grid(row=i + 1, column=1, pady=1, padx=1, sticky='WE')
                label_fg.grid(row=i + 1, column=2, pady=1, padx=1, sticky='WE')
                botao_editar.grid(row=i + 1, column=3, padx=3)
                botao_deletar.grid(row=i + 1, column=4)

    def escolher_cor(self, event):
        cor = colorchooser.askcolor(parent=self.window_add_highlights)[1]
        event.widget.config(bg=cor)

    def confirmar(self, edicao=False, index=None):
        entrada = self.entry.get()
        bg = self.botao_bg['bg']
        fg = self.botao_fg['bg']

        itens = [item.split('-') for item in entrada.split(',')]
        if self.valida_entrada(itens):
            if edicao is True and index is not None:
                self.remover_highlight(index)
            for item in itens:
                if len(item) == 1:
                    posicao = int(item[0])
                    highlight = Highlight(bg, fg, posicao)
                    self.adicionar_highlight(highlight)
                elif len(item) == 2:
                    inicio, fim = map(int, item)
                    highlight = Highlight(bg, fg, inicio, fim)
                    self.adicionar_highlight(highlight)
            self.gui_liga.atualizar_highlights()
            self.atualizar_janela()
            self.window_add_highlights.destroy()
        else:
            messagebox.showerror(title=None, message='Entrada inválida!', parent=self.window_add_highlights)

    def editar_highlight(self, index):
        hl = self.liga.highlights_tabela[index]
        inicio = hl.inicio
        fim = hl.fim
        bg = hl.bg
        fg = hl.fg

        if inicio == fim:
            texto = inicio
        else:
            texto = f'{inicio} - {fim}'

        self.abrir_janela_adicionar_highlights(edicao=True, index=index, texto=texto, bg=bg, fg=fg)

    def adicionar_highlight(self, highlight):
        self.liga.adicionar_highlight(highlight)
        db.adicionar_highlight(self.liga.nome, highlight)

    def remover_highlight(self, index):
        hl = self.liga.get_highlight(index)
        self.gui_liga.remover_highlight(hl.inicio, hl.fim)
        db.remover_highlight(self.liga.nome, self.liga.get_highlight(index))
        self.liga.remover_highlight(index)
        self.atualizar_janela()

    def valida_entrada(self, itens):
        for item in itens:
            if len(item) == 1:
                try:
                    posicao = int(item[0])
                except ValueError:
                    return False
                else:
                    if posicao not in range(1, self.liga.numero_de_rodadas):
                        return False
            elif len(item) == 2:
                try:
                    inicio, fim = map(int, item)
                except ValueError:
                    return False
                else:
                    if inicio > fim:
                        return False
                    elif inicio < 1 or fim > self.liga.numero_de_rodadas:
                        return False
            else:
                return False

        return True
