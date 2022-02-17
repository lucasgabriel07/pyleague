class Highlight:

    def __init__(self, bg, fg, inicio, fim=None):
        self.bg = bg
        self.fg = fg
        self.inicio = inicio
        if fim is None:
            self.fim = inicio
        else:
            self.fim = fim
