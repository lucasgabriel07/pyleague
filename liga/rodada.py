class Rodada:

    def __init__(self, numero):
        self.numero = numero
        self.jogos = []

    def adicionar_jogo(self, jogo):
        self.jogos.append(jogo)

    def get_jogo(self, index):
        return self.jogos[index]

    def resetar(self):
        for jogo in self.jogos:
            jogo.resetar()
