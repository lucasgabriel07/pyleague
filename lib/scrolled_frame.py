from tkinter import *


class ScrolledFrame(Frame):

    def __init__(self, master):
        super().__init__(master)

        self.canvas = Canvas(self, highlightthickness=0)
        self.yscrollbar = Scrollbar(self, orient=VERTICAL, command=self.canvas.yview)
        self.xscrollbar = Scrollbar(self, orient=HORIZONTAL, command=self.canvas.xview)
        self.canvas.config(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.yscrollbar.pack(side=RIGHT, fill=Y)
        self.xscrollbar.pack(side=BOTTOM, fill=X)
        self.canvas.pack(fill=BOTH, expand=True)

        self.frame = Frame(self.canvas)
        self.window = self.canvas.create_window((4, 4), window=self.frame, anchor=N+W, tags='self.frame')

        self.frame.bind('<Configure>', lambda event: self.canvas.configure(scrollregion=self.canvas.bbox('all')))
        self.canvas.bind('<Configure>', lambda event: self.canvas.itemconfig(self.window, width=event.width))