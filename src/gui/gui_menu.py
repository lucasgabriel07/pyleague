import tkinter as tk
import os
from tkinter import messagebox
from tkinter.ttk import Combobox, Spinbox
from src.liga import Liga
from src.team import Time


class Menu:

    def __init__(self, x=None, y=None):

        self.root = tk.Tk()
        self.root.title('Menu Principal')

        self.label_nome = tk.Label(self.root, height=5)

        self.botao_novo = tk.Button(self.root, text='NOVO', width=20, command=self.nova_liga, pady=4,
                                    font='arial 10 bold', bg='white', fg='#078745', bd=1, cursor='hand2')
        self.botao_carregar = tk.Button(self.root, text='CARREGAR', width=20, command=None, pady=4,
                                        font='arial 10 bold', bg='white', bd=1, fg='#078745', cursor='hand2')
        self.botao_sair = tk.Button(self.root, text='SAIR', width=20, command=self.root.destroy, pady=4,
                                    font='arial 10 bold', bg='white', fg='red', bd=1, cursor='hand2')

        if len(os.listdir('data')) == 0:
            self.botao_carregar.config(state='disabled')
        else:
            self.botao_carregar.config(state='normal')

        self.label_nome.pack(side=tk.TOP)
        self.botao_novo.pack(pady=3)
        self.botao_carregar.pack(pady=3)
        self.botao_sair.pack(pady=3)

        if x is None:
            x = (self.root.winfo_screenwidth() - 500) // 2

        if y is None:
            y = (self.root.winfo_screenheight() - 350) // 2

        width = 500
        height = 300

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.resizable(0, 0)

        self.root.mainloop()

    def nova_liga(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.destroy()
        NovaLiga(x, y)


class NovaLiga:

    def __init__(self, x=None, y=None):

        self.name = None
        self.legs = None

        self.root = tk.Tk()
        self.root.title('Nova Liga')

        self.header = tk.Label(self.root, text='NOVA LIGA', bg='#078745', fg='white', font='arial 12 bold',
                               pady=3)
        self.header.pack(fill=tk.X)

        self.frame0 = tk.Frame(self.root)
        self.frame0.pack(pady=20)

        self.frame_nome = tk.Frame(self.root)
        self.frame_nome.pack()

        self.label_nome = tk.Label(self.frame_nome, text='NOME:', font='arial 10 bold')
        self.label_nome.grid(row=0, column=0, sticky=tk.E)

        self.entry = tk.Entry(self.frame_nome, width=30, font='arial 12 bold', fg='#078745')
        self.entry.bind('<Return>', None)
        self.entry.focus_force()
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        self.frame_opcoes = tk.Frame(self.root, pady=20)
        self.frame_botoes = tk.Frame(self.root, pady=0)

        self.frame_opcoes.pack()
        self.frame_botoes.pack()

        self.label_turnos = tk.Label(self.frame_opcoes, text='TURNOS:', font='arial 10 bold')
        self.label_criterios = tk.Label(self.frame_opcoes, text='CRITÉRIOS:', font='arial 10 bold')

        self.spinbox_turnos = Spinbox(self.frame_opcoes, values=(1, 2), font='arial 10 bold', justify=tk.CENTER,
                                      state='readonly')
        self.spinbox_turnos.set(1)

        self.combobox_criterios = Combobox(self.frame_opcoes, values=['P > V > SG > GP', 'P > SG > GP',
                                                                      'P > SG > GP > V', 'P > SG > V > GP'],
                                           font='arial 10 bold', justify=tk.CENTER, state='readonly', cursor='hand2')
        self.combobox_criterios.current(0)
        self.frame_opcoes.option_add('*TCombobox*Listbox.selectBackground', '#078745')

        self.label_turnos.grid(row=0, column=0, sticky=tk.E)
        self.label_criterios.grid(row=1, column=0, sticky=tk.E)
        self.spinbox_turnos.grid(row=0, column=1, padx=5, pady=5, sticky='WE')
        self.combobox_criterios.grid(row=1, column=1, padx=5, pady=5)

        self.botao_sair = tk.Button(self.frame_botoes, bg='white', bd=1, text='Voltar', command=self.voltar, width=8,
                                    cursor='hand2')
        self.botao_confirmar = tk.Button(self.frame_botoes, bg='white', bd=1, text='Confirmar', command=self.confirmar,
                                         width=8, cursor='hand2')
        self.botao_confirmar.focus_force()
        self.botao_confirmar.bind('<Return>', self.confirmar)
        self.botao_sair.pack(side=tk.LEFT, padx=5)
        self.botao_confirmar.pack(side=tk.LEFT, padx=5)

        if x is None:
            x = (self.root.winfo_screenwidth() - 500) // 2

        if y is None:
            y = (self.root.winfo_screenheight() - 350) // 2

        width = 500
        height = 300

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.resizable(0, 0)

        self.root.resizable(0, 0)
        self.root.mainloop()

    def voltar(self, event=None):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.destroy()
        Menu(x, y)

    def confirmar(self):
        nome_da_liga = self.entry.get()
        numero_de_turnos = int(self.spinbox_turnos.get())
        criterio_de_classificacao = self.combobox_criterios.current()
        self.root.destroy()
        liga = Liga(nome_da_liga, numero_de_turnos, criterio_de_classificacao)
        AdicionarTimes(liga)


class AdicionarTimes:

    def __init__(self, liga):

        self.liga = liga

        self.root = tk.Tk()
        self.root.title('Adicionar times')

        self.lista_de_times = []

        self.header = tk.Label(self.root, text='ADICIONAR TIMES', bg='#078745', fg='white', font='arial 12 bold',
                               pady=3)
        self.header.pack(fill=tk.X)

        self.frame = tk.Frame(self.root)
        self.frame.pack(pady=15)
        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()

        self.label_nome = tk.Label(self.frame, text='NOME DO TIME:', font='arial 10 bold')
        self.entry_nome = tk.Entry(self.frame, font='arial 12 bold', fg='#078745', width=25)
        self.entry_nome.focus_force()
        self.label_sigla = tk.Label(self.frame, text='SIGLA:', font='arial 10 bold')
        self.entry_sigla = tk.Entry(self.frame, font='arial 12 bold', fg='#078745', width=5)
        self.botao_add = tk.Button(self.frame, bg='white', bd=1, text='+', command=self.adicionar_time, cursor='hand2',
                                   font='arial 10 bold')

        self.entry_nome.bind('<Return>', self.entry_sigla_focus)
        self.entry_sigla.bind('<Return>', self.adicionar_time)

        self.label_nome.grid(row=0, column=0, sticky='e', padx=3)
        self.entry_nome.grid(row=0, column=1, padx=3)
        self.label_sigla.grid(row=1, column=0, sticky='e', pady=10)
        self.entry_sigla.grid(row=1, column=1, padx=3, pady=3, sticky='w')
        self.botao_add.grid(row=0, column=3, padx=3)

        self.botao_importar = tk.Button(self.frame, bg='white', bd=1, text='Importar', width=8, cursor='hand2',
                                        command=None)
        self.botao_importar.grid(row=2, column=0, columnspan=3, pady=10)

        self.listbox = tk.Listbox(self.frame, bg='white', font='arial 12', selectbackground='#078745',
                                  cursor='hand2')
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<Delete>', self.remover_time)
        self.listbox.bind('<F2>', None)
        self.listbox.bind('<Return>', None)
        self.listbox.bind('<Double-Button-1>', None)
        self.listbox.bind('<Button-3>', None)

        self.listbox.grid(row=3, column=0, columnspan=4, sticky='WE')
        self.scrollbar.grid(row=3, column=4, sticky='NS')

        self.botao_voltar = tk.Button(self.frame_botoes, bg='white', bd=1, text='Voltar', command=self.voltar, width=8,
                                      cursor='hand2')
        self.botao_confirmar = tk.Button(self.frame_botoes, bg='white', bd=1, text='Confirmar', command=self.confirmar,
                                         width=8, cursor='hand2')
        self.botao_voltar.pack(side=tk.LEFT, padx=5, pady=5)
        self.botao_confirmar.pack(side=tk.LEFT, padx=5, pady=5)

        x = (self.root.winfo_screenwidth() - 500) // 2
        y = (self.root.winfo_screenheight() - 450) // 2
        self.root.geometry(f'500x420+{x}+{y}')

        self.root.resizable(0, 0)
        self.root.mainloop()

    def entry_sigla_focus(self, event):
        self.entry_sigla.focus()

    def voltar(self, event=None):
        self.root.destroy()
        NovaLiga()

    def adicionar_time(self, event=None):
        nome = self.entry_nome.get().strip()
        sigla = self.entry_sigla.get().strip()

        if nome == '' or sigla == '':
            messagebox.showerror(title='Erro!', message='Entrada inválida!')
        elif nome in [item['nome'] for item in self.lista_de_times]:
            messagebox.showerror(title='Erro!', message=f'Já existe um time cadastrado com esse nome!')
        elif sigla in [item['sigla'] for item in self.lista_de_times]:
            messagebox.showerror(title='Erro!', message=f'Já existe um time cadastrado com essa sigla!')
        else:
            self.lista_de_times.append({
                'nome': self.entry_nome.get(),
                'sigla': self.entry_sigla.get()[:3]
            })
            i = len(self.lista_de_times)
            self.listbox.insert('end', f'TIME {i}: {nome} ({sigla})')
            self.listbox.yview('end')
            self.entry_nome.delete(0, 'end')
            self.entry_sigla.delete(0, 'end')
            self.entry_nome.focus()

    def remover_time(self, event=None):
        index = self.listbox.curselection()[0]
        del self.lista_de_times[index]
        self.listbox.delete(0, 'end')

        for i, item in enumerate(self.lista_de_times):
            nome = item['nome']
            sigla = item['sigla']
            self.listbox.insert('end', f'TIME {i+1}: {nome} ({sigla})')
        self.listbox.yview(index)

    def confirmar(self, event=None):
        for item in self.lista_de_times:
            nome = item['nome']
            sigla = item['sigla']
            time = Time(nome, sigla)
            self.liga.adicionar_time(time)

        self.root.destroy()
        self.liga.iniciar_liga()
