import tkinter as tk
from tkinter import ttk, messagebox
import os


class Menu:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Menu Principal')

        self.label1 = tk.Label(self.root, height=3)

        self.button1 = tk.Button(self.root, text='NOVO', width=20, command=self.new, pady=4,
                              font='arial 10 bold', bg='white', fg='#078745', bd=1, cursor='hand2')
        self.button2 = tk.Button(self.root, text='CARREGAR', width=20, command=self.load, pady=4,
                              font='arial 10 bold', bg='white', bd=1, fg='#078745', cursor='hand2')
        self.button3 = tk.Button(self.root, text='SAIR', width=20, command=self.root.destroy, pady=4,
                              font='arial 10 bold', bg='white', fg='red', bd=1, cursor='hand2')

        if len(os.listdir('../../data')) == 0:
            self.button2.config(state='disabled')
        else:
            self.button2.config(state='normal')

        self.label1.pack(side=tk.TOP)
        self.button1.pack(pady=3)
        self.button2.pack(pady=3)
        self.button3.pack(pady=3)

        try:
            self.root.geometry(f'420x215+{self.x}+{self.y}')

        except AttributeError:
            self.x = (self.root.winfo_screenwidth() - 420) // 2
            self.y = (self.root.winfo_screenheight() - 350) // 2
            self.root.geometry(f'420x215+{self.x}+{self.y}')

        self.root.resizable(0, 0)
        self.root.mainloop()

    def new(self):
        New.x = self.root.winfo_x()
        New.y = self.root.winfo_y()
        self.root.destroy()
        New()

    def load(self):
        Load.x = self.root.winfo_x()
        Load.y = self.root.winfo_y()
        self.root.destroy()
        Load()


class New:

    def __init__(self):

        self.name = None
        self.shifts = None

        self.root = tk.Tk()
        self.root.title('Novo Campeonato')

        self.label1 = tk.Label(self.root, text='NOVO CAMPEONATO', bg='#078745', fg='white', font='arial 12 bold', pady=3)
        self.label1.pack(fill=tk.X)

        self.frame1 = tk.Frame(self.root)
        self.frame2 = tk.Frame(self.root)

        self.frame1.pack(pady=15)
        self.frame2.pack(pady=5)

        self.label2 = tk.Label(self.frame1, text='NOME:', font='arial 10 bold')
        self.label3 = tk.Label(self.frame1, text='FORMATO:', font='arial 10 bold')
        self.label2.grid(row=0, column=0, sticky=tk.E)
        self.label3.grid(row=1, column=0, sticky=tk.E)

        self.entry = tk.Entry(self.frame1, width=30, font='arial 12 bold', fg='#078745')
        self.entry.bind('<Return>', self.confirm)
        self.entry.focus_force()
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        self.combobox = ttk.Combobox(self.frame1, values=['Pontos Corridos', 'Mata-Mata', 'Grupos + Mata-Mata'],
                                 font='arial 10 bold', justify=tk.CENTER, state='readonly', width=36, cursor='hand2')
        self.combobox.current(0)
        self.frame1.option_add('*Ttk.Combobox*tk.Listbox.selectBackground', '#078745')
        self.combobox.grid(row=1, column=1, padx=5, pady=5)

        self.button1 = tk.Button(self.frame2, bg='white', bd=1, text='Voltar', command=self.back, width=8, cursor='hand2')
        self.button2 = tk.Button(self.frame2, bg='white', bd=1, text='Confirmar', command=self.confirm, width=8, cursor='hand2')
        self.button1.pack(side=tk.LEFT, padx=5, pady=10)
        self.button2.pack(side=tk.LEFT, padx=5, pady=10)

        try:
            self.root.geometry(f'420x215+{self.x}+{self.y}')
        except AttributeError:
            self.x = (self.root.winfo_screenwidth() - 420) // 2
            self.y = (self.root.winfo_screenheight() - 350) // 2
            self.root.geometry(f'420x215+{self.x}+{self.y}')

        self.root.resizable(0, 0)
        self.root.mainloop()

    def confirm(self, event=None):
        name = self.entry.get()

        file_exists = False
        for file in os.listdir('data'):
            if f'{name}.db'.upper() == file.upper():
                file_exists = True

        if file_exists:
            tk.messagebox.showerror(message='Já existe um campeonato com esse nome!')

        elif name != '' and name.isspace() is False:
            """
            if self.combobox.current() == 0:
                League.name = name
                NewLeague.x = self.root.winfo_x()
                NewLeague.y = self.root.winfo_y()
                self.root.destroy()
                NewLeague()

            elif self.combobox.current() == 1:
                Playoff.name = name
                Playoff.x = self.root.winfo_x()
                Playoff.y = self.root.winfo_y()
                self.root.destroy()
                NewPlayoff()
    
            else:
                # Cup.name = name
                # Cup.x = self.root.winfo_x()
                # Cup.y = self.root.winfo_y()
                self.root.destroy()
                # NewCup()
            """

        else:
            tk.messagebox.showerror(message='Entrada inválida!')

    def back(self):
        Menu.x = self.root.winfo_x()
        Menu.y = self.root.winfo_y()
        self.root.destroy()
        Menu()


class Load:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title('Carregar Campeonato')

        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(pady=15)

        self.listbox = tk.Listbox(self.frame1, bg='white', font='arial 12', selectbackground='#078745', height=7, width=37,
                               cursor='hand2')
        self.scrollbar = tk.Scrollbar(self.frame1, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=self.scrollbar.set)
        self.listbox.bind('<Delete>', self.delete_championship)
        self.listbox.bind('<F2>', self.edit_championship)
        self.listbox.bind('<Return>', self.confirm)
        self.listbox.bind('<Double-tk.Button-1>', self.confirm)
        self.listbox.bind('<tk.Button-3>', self.call_menu)

        self.listbox.grid(row=0, column=0, sticky='WE')
        self.scrollbar.grid(row=0, column=1, sticky='NS')

        self.frame2 = tk.Frame(self.root)
        self.frame2.pack()

        self.button2 = tk.Button(self.frame2, bg='white', bd=1, text='Voltar', command=self.back, width=8,
                              cursor='hand2')
        self.button3 = tk.Button(self.frame2, bg='white', bd=1, text='Confirmar', command=self.confirm, width=8,
                              cursor='hand2')
        self.button2.pack(side=tk.LEFT, padx=5)
        self.button3.pack(side=tk.LEFT, padx=5)

        files = os.listdir('data')
        for file in files:
            self.listbox.insert(tk.END, str(file[:-3]))

        try:
            self.root.geometry(f'420x215+{self.x}+{self.y}')
        except AttributeError:
            self.x = (self.root.winfo_screenwidth() - 420) // 2
            self.y = (self.root.winfo_screenheight() - 350) // 2
            self.root.geometry(f'420x215+{self.x}+{self.y}')

        self.root.mainloop()

    def delete_championship(self, event=None):
        file = self.listbox.get(self.listbox.curselection()[0])
        if tk.messagebox.askyesno('Excluir Campeonato', f'Tem certeza que deseja excluir "{file}"?'):
            os.remove(f'data/{file}.db')
            tk.messagebox.showinfo('Concluído!', f'"{file}" foi excluído com sucesso!')
            self.listbox.delete(0, 'end')
            files = os.listdir('data')
            for file in files:
                self.listbox.insert(tk.END, str(file[:-3]))

    def edit_championship(self, event=None):

        def edit(event=None):
            new_name = f'{entry.get()}.db'

            if new_name == old_name or new_name not in os.listdir('data'):

                os.rename(f'data/{old_name}', f'data/{new_name}')
                edit_window.destroy()
                self.listbox.delete(0, 'end')
                files = os.listdir('data')
                for file in files:
                    self.listbox.insert(tk.END, str(file[:-3]))

            else:
                tk.messagebox.showerror(title='Erro!', message='Já existe um campeonato com esse nome!')
                edit_window.destroy()

        if len(self.listbox.curselection()) != 0:

            old_name = f'{self.listbox.get(self.listbox.curselection()[0])}.db'

            edit_window = tk.Tk()
            edit_window.title('Editar Campeonato')

            frame = tk.Frame(edit_window)
            frame.pack()

            label1 = tk.Label(frame, text='NOME:', font='arial 10 bold')
            label1.grid(row=0, column=0, sticky='e', padx=3, pady=20)

            entry = tk.Entry(frame, width=40, font='arial 12 bold', fg='#078745')
            entry.bind('<Return>', edit)
            entry.insert(0, old_name[:-3])
            entry.grid(row=0, column=1, padx=3)

            button1 = tk.Button(frame, bg='white', bd=1, text='Ok', command=edit, width=2, cursor='hand2')
            button1.grid(row=0, column=2, padx=3)

            edit_window.geometry('500x80+430+270')
            edit_window.resizable(width=False, height=False)
            edit_window.mainloop()

    def back(self):
        Menu.x = self.root.winfo_x()
        Menu.y = self.root.winfo_y()
        self.root.destroy()
        Menu()

    def call_menu(self, event):

        def call_edit():
            self.menu.destroy()
            self.edit_championship()
            self.listbox.unbind('<tk.Button-1>', f1)
            self.root.unbind('<tk.Button-1>', f2)

        def call_del():
            self.menu.destroy()
            self.delete_championship()
            self.listbox.unbind('<tk.Button-1>', f1)
            self.root.unbind('<tk.Button-1>', f2)

        f1 = self.listbox.bind('<tk.Button-1>', lambda e: self.menu.destroy())
        f2 = self.root.bind('<tk.Button-1>', lambda e: self.menu.destroy())

        try:
            self.menu.destroy()
        except AttributeError:
            pass

        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.listbox.nearest(event.y))
        self.listbox.activate(self.listbox.nearest(event.y))

        self.menu = tk.Toplevel()
        self.menu.overrideredirect(1)
        edit_button = tk.tk.Button(self.menu, text='Editar', width=15, command=call_edit, font='arial 8', bd=0)
        del_button = tk.Button(self.menu, text='Excluir', width=15, command=call_del, font='arial 8', bd=0)
        edit_button.pack(fill=tk.X)
        del_button.pack(fill=tk.X)

        self.menu.geometry(f'+{event.x+530}+{event.y+260}')
        self.menu.mainloop()

    """
    @staticmethod
    def define_current_round():
        for rd in range(1, len(League.rounds) + 1):
            for match in League.rounds[rd]:
                team1_score, team2_score = match[2], match[3]
                if team1_score == '' or team2_score == '':
                    return rd
        return len(League.rounds)

    def confirm(self, event=None):
        try:
            file = self.listbox.get(self.listbox.curselection()[0])
            connection = sqlite3.connect(f'data/{file}.db')
            cursor = connection.cursor()

            cursor.execute('select * from data')

            data = cursor.fetchone()
            League.name = file
            League.team_list = eval(data[0])
            League.team_dict = eval(data[1])
            League.updated_ranking = eval(data[2])
            League.rounds = eval(data[3])
            League.classification_criteria = data[4]
            League.highlight_list = eval(data[5])

            connection.close()

            League.new = False
            League.current_round = self.define_current_round()
            League.number_of_teams = len(League.team_dict)
            League.number_of_rounds = League.number_of_teams - 1 + League.number_of_teams % 2
            League.matches_by_round = League.number_of_teams // 2

            self.root.destroy()
            League()

        except IndexError:
            tk.messagebox.showerror(message='Selecione um campeonato')
        """


if __name__ == '__main__':
    Menu()
