class Rodada:

    def __init__(self, numero):
        self.numero = numero
        self.jogos = []

    def adicionar_jogo(self, jogo):
        self.jogos.append(jogo)
