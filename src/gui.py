import tkinter as tk
from lib.table import Table

class Menu:

    def __init__(self):
        self.window = tk.Tk()

        self.window.mainloop()


class NovaLiga:
    pass


class Liga:

    def __init__(self, liga):

        self.window = tk.Tk()
        self.liga = liga
        self.table = Table(master=self.window, rows=self.liga.numero_de_times+1, columns=10, bg="white", width=3,
                           relief='flat')
        self.table.pack()
        self.table.config(column=1, width=30)
        self.table.config(row=0, bg='lightgrey')

        header = ['#', 'TIME', 'PG', 'J', 'V', 'E', 'D', 'GP', 'GC', 'SG']

        for c in range(len(header)):
            self.table.insert(0, c, header[c])

        self.atualizar_tabela()
        self.window.mainloop()

    def atualizar_tabela(self):
        for i, time in enumerate(self.liga.classificacao):
            self.table.insert(i+1, 0, i+1)
            self.table.insert(i+1, 1, time.nome)
            self.table.insert(i+1, 2, time.pontos)
            self.table.insert(i+1, 3, time.jogos)
            self.table.insert(i+1, 4, time.vitorias)
            self.table.insert(i+1, 5, time.empates)
            self.table.insert(i+1, 6, time.derrotas)
            self.table.insert(i+1, 7, time.gols_feitos)
            self.table.insert(i+1, 8, time.gols_sofridos)
            self.table.insert(i+1, 9, time.saldo_de_gols)


class Configuracoes:
    pass