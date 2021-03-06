import tkinter as tk
import os
from tkinter import messagebox
from tkinter.ttk import Combobox, Spinbox
from liga.liga import Liga
import database as db
from liga.team import Time


class Menu:

    def __init__(self, x=None, y=None):

        self.root = tk.Tk()
        self.root.title('Menu Principal')

        self.label_nome = tk.Label(self.root, height=5)

        self.botao_novo = tk.Button(self.root, text='NOVO', width=20, command=self.nova_liga, pady=4,
                                    font='arial 10 bold', bg='white', fg='#078745', bd=1, cursor='hand2')
        self.botao_carregar = tk.Button(self.root, text='CARREGAR', width=20, command=self.carregar_liga, pady=4,
                                        font='arial 10 bold', bg='white', bd=1, fg='#078745', cursor='hand2')
        self.botao_sair = tk.Button(self.root, text='SAIR', width=20, command=self.root.destroy, pady=4,
                                    font='arial 10 bold', bg='white', fg='red', bd=1, cursor='hand2',
                                    highlightcolor='red')

        self.botao_novo.focus_force()
        self.botao_novo.bind('<FocusIn>', lambda event: self.botao_novo.config(bg='#078745', fg='white'))
        self.botao_novo.bind('<FocusOut>', lambda event: self.botao_novo.config(bg='white', fg='#078745'))
        self.botao_carregar.bind('<FocusIn>', lambda event: self.botao_carregar.config(bg='#078745', fg='white'))
        self.botao_carregar.bind('<FocusOut>', lambda event: self.botao_carregar.config(bg='white', fg='#078745'))
        self.botao_sair.bind('<FocusIn>', lambda event: self.botao_sair.config(bg='red', fg='white'))
        self.botao_sair.bind('<FocusOut>', lambda event: self.botao_sair.config(bg='white', fg='red'))

        if len(os.listdir('data')) == 0 or db.get_ligas() is None:
            self.botao_carregar.config(state='disabled', cursor='arrow')
        else:
            self.botao_carregar.config(state='normal', cursor='hand2')

        self.label_nome.pack(side=tk.TOP)
        self.botao_novo.pack(pady=3)
        self.botao_carregar.pack(pady=3)
        self.botao_sair.pack(pady=3)

        self.botao_novo.bind('<Return>', lambda event: self.botao_novo.invoke())
        self.botao_novo.bind('<Up>', lambda event: self.botao_sair.focus())
        self.botao_novo.bind('<Down>', lambda event: self.botao_carregar.focus())

        self.botao_carregar.bind('<Return>', lambda event: self.botao_carregar.invoke())
        self.botao_carregar.bind('<Up>', lambda event: self.botao_novo.focus())
        self.botao_carregar.bind('<Down>', lambda event: self.botao_sair.focus())

        self.botao_sair.bind('<Return>', lambda event: self.botao_sair.invoke())
        self.botao_sair.bind('<Up>', lambda event: self.botao_carregar.focus())
        self.botao_sair.bind('<Down>', lambda event: self.botao_novo.focus())

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

    def carregar_liga(self):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.destroy()
        CarregaLiga(x, y)


class NovaLiga:

    def __init__(self, x=None, y=None):

        self.root = tk.Tk()
        self.root.title('Nova Liga')

        self.header = tk.Label(self.root, text='NOVA LIGA', bg='#078745', fg='white', font='arial 12 bold', pady=3)
        self.header.pack(fill=tk.X)

        self.frame0 = tk.Frame(self.root)
        self.frame0.pack(pady=20)

        self.frame_nome = tk.Frame(self.root)
        self.frame_nome.pack()

        self.label_nome = tk.Label(self.frame_nome, text='NOME:', font='arial 10 bold')
        self.label_nome.grid(row=0, column=0, sticky=tk.E)

        self.entry = tk.Entry(self.frame_nome, width=30, font='arial 12 bold', fg='#078745')
        self.entry.bind('<Return>', self.confirmar)
        self.entry.focus_force()
        self.entry.grid(row=0, column=1, padx=5, pady=5)
        self.entry.focus_force()

        self.frame_opcoes = tk.Frame(self.root, pady=20)
        self.frame_botoes = tk.Frame(self.root, pady=0)

        self.frame_opcoes.pack()
        self.frame_botoes.pack()

        self.label_turnos = tk.Label(self.frame_opcoes, text='TURNOS:', font='arial 10 bold')
        self.label_criterios = tk.Label(self.frame_opcoes, text='CRIT??RIOS:', font='arial 10 bold')

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

    def confirmar(self, event=None):
        nome_da_liga = self.entry.get().strip()

        if self.liga_existe(nome_da_liga):
            messagebox.showerror(message='J?? existe uma liga com esse nome!')
        elif nome_da_liga != '':
            numero_de_turnos = int(self.spinbox_turnos.get())
            criterio_de_classificacao = self.combobox_criterios.current()
            self.root.destroy()
            liga = Liga(nome_da_liga, numero_de_turnos, criterio_de_classificacao)
            AdicionaTimes(liga)
        else:
            messagebox.showerror(message='Entrada inv??lida!')

    @staticmethod
    def liga_existe(nome):
        if len(os.listdir('data')) == 0 or db.get_ligas() is None:
            return False
        ligas_existentes = db.get_ligas()
        for liga in ligas_existentes:
            if nome.upper() == liga.upper():
                return True
        return False


class AdicionaTimes:

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

        self.entry_nome.bind('<Return>', lambda event: self.entry_sigla_focus())
        self.entry_nome.bind('<Tab>', lambda event: self.entry_sigla_focus())
        self.entry_sigla.bind('<Return>', self.adicionar_time)

        self.label_nome.grid(row=0, column=0, sticky='e', padx=3)
        self.entry_nome.grid(row=0, column=1, padx=3)
        self.label_sigla.grid(row=1, column=0, sticky='e', pady=10)
        self.entry_sigla.grid(row=1, column=1, padx=3, pady=3, sticky='w')
        self.botao_add.grid(row=0, column=3, padx=3)

        self.botao_importar = tk.Button(self.frame, bg='white', bd=1, text='Importar', width=8, cursor='hand2',
                                        command=self.chamar_janela_importar_times)
        self.botao_importar.grid(row=2, column=0, columnspan=3, pady=10)

        if len(os.listdir('data')) == 0 or db.get_ligas() is None:
            self.botao_importar.config(state='disabled', cursor='arrow')
        else:
            self.botao_importar.config(state='normal', cursor='hand2')

        self.listbox_times = tk.Listbox(self.frame, bg='white', font='arial 12', selectbackground='#078745',
                                        cursor='hand2')
        self.scrollbar = tk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox_times.yview)
        self.listbox_times.configure(yscrollcommand=self.scrollbar.set)
        self.listbox_times.bind('<Delete>', self.remover_time)
        self.listbox_times.focus_force()

        self.listbox_times.grid(row=3, column=0, columnspan=4, sticky='WE')
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

    def entry_sigla_focus(self, event=None):
        sigla_padrao = self.entry_nome.get()[:3].upper()
        self.entry_sigla.delete(0, 'end')
        self.entry_sigla.insert(0, sigla_padrao)
        self.entry_sigla.focus()
        self.entry_sigla.selection_range(0, 3)

    def voltar(self, event=None):
        self.root.destroy()
        NovaLiga()

    def adicionar_time(self, event=None):
        nome = self.entry_nome.get().strip()
        sigla = self.entry_sigla.get().strip()

        if nome == '' or sigla == '':
            messagebox.showerror(title='Erro!', message='Entrada inv??lida!')
        elif nome in [item['nome'] for item in self.lista_de_times]:
            messagebox.showerror(title='Erro!', message=f'J?? existe um time cadastrado com esse nome!')
        elif sigla in [item['sigla'] for item in self.lista_de_times]:
            messagebox.showerror(title='Erro!', message=f'J?? existe um time cadastrado com essa sigla!')
        else:
            self.lista_de_times.append({
                'nome': self.entry_nome.get(),
                'sigla': self.entry_sigla.get()[:3],
                'emblema': None
            })
            i = len(self.lista_de_times)
            self.listbox_times.insert('end', f'Time {i}: {nome} ({sigla})')
            self.listbox_times.yview('end')
            self.entry_nome.delete(0, 'end')
            self.entry_sigla.delete(0, 'end')
            self.entry_nome.focus()

    def remover_time(self, event=None):
        index = self.listbox_times.curselection()[0]
        del self.lista_de_times[index]
        self.listbox_times.delete(0, 'end')

        for i, item in enumerate(self.lista_de_times):
            nome = item['nome']
            sigla = item['sigla']
            self.listbox_times.insert('end', f'TIME {i + 1}: {nome} ({sigla})')
        self.listbox_times.yview(index)

    def chamar_janela_importar_times(self, event=None):
        window = tk.Tk()
        window.title('Importar times')

        frame0 = tk.Frame(window)
        frame0.pack(pady=15)

        listbox_ligas = tk.Listbox(frame0, bg='white', font='arial 12', selectbackground='#078745', height=7,
                                   width=37, cursor='hand2')
        scrollbar = tk.Scrollbar(frame0, orient=tk.VERTICAL, command=listbox_ligas.yview)
        listbox_ligas.configure(yscrollcommand=scrollbar.set)
        listbox_ligas.bind('<Double-Button-1>', lambda e: self.importar_times(listbox_ligas, window))
        listbox_ligas.bind('<Return>', lambda e: self.importar_times(listbox_ligas, window))

        listbox_ligas.grid(row=0, column=0, sticky='WE')
        scrollbar.grid(row=0, column=1, sticky='NS')

        frame_botoes = tk.Frame(window)
        frame_botoes.pack()

        botao_cancelar = tk.Button(frame_botoes, bg='white', bd=1, text='Cancelar', width=8, cursor='hand2',
                                   command=window.destroy)
        botao_confirmar = tk.Button(frame_botoes, bg='white', bd=1, text='Confirmar', width=8, cursor='hand2',
                                    command=lambda: self.importar_times(listbox_ligas, window))
        botao_cancelar.pack(side=tk.LEFT, padx=5)
        botao_confirmar.pack(side=tk.LEFT, padx=5)

        lista_de_ligas = db.get_ligas()

        for nome in lista_de_ligas:
            listbox_ligas.insert('end', nome)

        x = (window.winfo_screenwidth() - 420) // 2
        y = (window.winfo_screenheight() - 350) // 2
        window.geometry(f'420x215+{x}+{y}')
        window.mainloop()

    def importar_times(self, listbox_ligas, window, event=None):
        nome_da_liga = listbox_ligas.selection_get()
        times_importados = db.get_times(nome_da_liga)
        times_atuais = [item['nome'] for item in self.lista_de_times]

        times_repetidos = []
        for nome, sigla, emblema in times_importados:
            if nome not in times_atuais:
                self.lista_de_times.append({
                    'nome': nome,
                    'sigla': sigla,
                    'emblema': emblema
                })
                i = len(self.lista_de_times)
                self.listbox_times.insert('end', f'Time {i}: {nome} ({sigla})')
                self.listbox_times.yview('end')
            else:
                times_repetidos.append(nome)

        if len(times_repetidos) > 0:
            text = 'Os seguintes times j?? estavam cadastrados:\n'
            for team in times_repetidos:
                text += f'\n    - {team}'
            messagebox.showerror('Times repetidos', text)

        window.destroy()

    def confirmar(self, event=None):
        if len(self.lista_de_times) > 1:
            for item in self.lista_de_times:
                nome = item['nome']
                sigla = item['sigla']
                emblema = item['emblema']
                time = Time(nome, sigla, emblema)
                self.liga.adicionar_time(time)
            self.root.destroy()
            self.liga.iniciar_liga()
        else:
            messagebox.showerror('Erro!', 'Adicione pelo menos 2 times!')


class CarregaLiga:

    def __init__(self, x=None, y=None):
        self.root = tk.Tk()
        self.root.title('Carregar Liga')

        self.header = tk.Label(self.root, text='CARREGAR LIGA', bg='#078745', fg='white', font='arial 12 bold', pady=3)
        self.header.pack(fill=tk.X)

        self.frame_listbox = tk.Frame(self.root)
        self.frame_listbox.pack(pady=15)

        self.listbox = tk.Listbox(self.frame_listbox, bg='white', font='arial 12', selectbackground='#078745',
                                  height=10, width=45, cursor='hand2')
        self.scrollbar = tk.Scrollbar(self.frame_listbox, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<Return>', self.confirmar)
        self.listbox.bind('<Double-Button-1>', self.confirmar)

        self.listbox.grid(row=0, column=0, sticky='WE')
        self.scrollbar.grid(row=0, column=1, sticky='NS')

        self.frame_botoes = tk.Frame(self.root)
        self.frame_botoes.pack()

        self.botao_voltar = tk.Button(self.frame_botoes, bg='white', bd=1, text='Voltar', command=self.voltar, width=8,
                                      cursor='hand2')
        self.botao_confirmar = tk.Button(self.frame_botoes, bg='white', bd=1, text='Confirmar', command=self.confirmar,
                                         width=8, cursor='hand2')
        self.botao_voltar.pack(side=tk.LEFT, padx=5)
        self.botao_confirmar.pack(side=tk.LEFT, padx=5)

        lista_de_ligas = db.get_ligas()

        for nome in lista_de_ligas:
            self.listbox.insert('end', nome)

        self.listbox.selection_set(0)
        self.listbox.focus_force()

        if x is None:
            x = (self.root.winfo_screenwidth() - 500) // 2

        if y is None:
            y = (self.root.winfo_screenheight() - 350) // 2

        width = 500
        height = 300

        self.root.geometry(f'{width}x{height}+{x}+{y}')
        self.root.resizable(0, 0)
        self.root.mainloop()

    def confirmar(self, event=None):
        try:
            nome_liga = self.listbox.get(self.listbox.curselection()[0])
            self.root.destroy()
            liga = db.carregar_liga(nome_liga)
            liga.carregar_liga()
        except IndexError:
            messagebox.showerror(message='Selecione um campeonato')

    def voltar(self, event=None):
        x = self.root.winfo_x()
        y = self.root.winfo_y()
        self.root.destroy()
        Menu(x, y)
