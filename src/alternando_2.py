from tkinter import *


class FirstWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        # Configuração da janela principal
        self.title('Primeira Janela')
        self.configure(background='green')
        self.geometry('480x240')


class SecondWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        # Configuração da janela principal
        self.title('Segunda Janela')
        self.configure(background='darkgray')
        self.geometry('480x240')


class ThirdWindow(Toplevel):
    def __init__(self, master=None):
        Toplevel.__init__(self, master=master)

        # Configuração da janela principal
        self.title('Terceira Janela')
        self.configure(background='yellow')
        self.geometry('480x240')


class MainWindow(Frame):
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, master=None)

        # Configuração da janela principal
        self.master.title('Janela Principal')
        self.master.geometry('480x240')
        self.configure(borderwidth=4)
        self.configure(background='white')

        for name in ("button1", "button2", "button3"):
            self.button = Button(self, text=name)
            self.button.bind("<Button-1>", self.handle_event)
            self.button.pack(side='left', fill='x', expand=True)

        # Empacotamos o frame principal
        self.pack(fill='both', expand=True)

    def handle_event(self, event):
        btn_name = event.widget.cget('text')
        if btn_name.endswith('1'):
            window = FirstWindow()
        if btn_name.endswith('2'):
            window = SecondWindow()
        if btn_name.endswith('3'):
            window = ThirdWindow()

        window.mainloop()


if __name__ == '__main__':
    mainWindow = MainWindow()
    mainWindow.mainloop()