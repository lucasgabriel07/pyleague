import os
from gui.menu import Menu

if __name__ == '__main__':
    if not os.path.isdir('data'):
        os.mkdir('./data')
    Menu()
