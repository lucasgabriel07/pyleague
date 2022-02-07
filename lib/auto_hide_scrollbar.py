from tkinter import *


class AutoHideScrollbar(Scrollbar):

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.pack_forget()
            self.place_forget()
        elif self.cget('orient') == VERTICAL:
            self.pack(side=RIGHT, fill=Y, anchor=E)
        else:
            self.place(relx=0, rely=1, relwidth=0.97, anchor=S+W)
        Scrollbar.set(self, lo, hi)