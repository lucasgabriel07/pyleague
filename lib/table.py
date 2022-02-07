import tkinter as tk


class Table(tk.Frame):

    def __init__(self, master, rows, columns, border_x=1, border_y=1, **kw):

        super().__init__(master)
        self.__rows = rows
        self.__columns = columns
        self.__cells = []

        for r in range(self.__rows):
            self.__cells.append(list())
            for c in range(self.__columns):
                cell = tk.Label(self, kw)
                cell.grid(row=r, column=c, pady=border_y, padx=border_x, sticky='NSEW')
                self.__cells[r].append(cell)

    def insert(self, row, column, text):
        cell = self.__cells[row][column]
        cell.config(text=text)

    def config(self, row=None, column=None, **kw):
        if row is not None and column is not None:
            cell = self.__cells[row][column]
            cell.config(kw)

        elif row is None and column is None:
            for r in range(self.__rows):
                for c in range(self.__columns):
                    cell = self.__cells[r][c]
                    cell.config(kw)

        elif row is None:
            for r in range(self.__rows):
                cell = self.__cells[r][column]
                cell.config(kw)

        elif column is None:
            for c in range(self.__columns):
                cell = self.__cells[row][c]
                cell.config(kw)

    def get_cell(self, row, column):
        return self.__cells[row][column]
