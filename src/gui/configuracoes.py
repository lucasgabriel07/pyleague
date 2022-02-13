import tkinter as tk


class Configuracoes:

    def __init__(self, liga, gui_liga):
        self.liga = liga
        self.gui_liga = gui_liga

        # Renomear Liga
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
