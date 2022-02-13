class Jogo:

    def __init__(self, time_mandante, time_visitante, numero):
        self.numero = numero
        self.time_mandante = time_mandante
        self.time_visitante = time_visitante
        self.gols_time_mandante = ''
        self.gols_time_visitante = ''
        self.vencedor = None
        self.derrotado = None
        self.empate = False

    def definir_placar(self, gols_time_mandante, gols_time_visitante):
        if gols_time_visitante != '' and gols_time_visitante != '':
            self.gols_time_mandante = gols_time_mandante
            self.gols_time_visitante = gols_time_visitante
            self.definir_vencedor()

    def definir_vencedor(self):
        if self.gols_time_mandante != '' and self.gols_time_visitante != '':
            if self.gols_time_mandante > self.gols_time_visitante:
                self.time_mandante.vitoria()
                self.time_visitante.derrota()
                self.vencedor = self.time_mandante
                self.derrotado = self.time_visitante
                self.empate = False
            elif self.gols_time_mandante < self.gols_time_visitante:
                self.time_mandante.derrota()
                self.time_visitante.vitoria()
                self.vencedor = self.time_visitante
                self.derrotado = self.time_mandante
                self.empate = False
            else:
                self.time_mandante.empate()
                self.time_visitante.empate()
                self.vencedor = self.derrotado = None
                self.empate = True
            self.time_mandante.atualizar_gols(self.gols_time_mandante, self.gols_time_visitante)
            self.time_visitante.atualizar_gols(self.gols_time_visitante, self.gols_time_mandante)

    def resetar(self):
        if self.gols_time_mandante != '' and self.gols_time_visitante != '':
            if self.empate:
                self.time_mandante.resetar_empate()
                self.time_visitante.resetar_empate()
            else:
                self.vencedor.resetar_vitoria()
                self.derrotado.resetar_derrota()

            self.time_mandante.resetar_gols(self.gols_time_mandante, self.gols_time_visitante)
            self.time_visitante.resetar_gols(self.gols_time_visitante, self.gols_time_mandante)
            self.gols_time_mandante = ''
            self.gols_time_visitante = ''

    def __str__(self):
        return f'{self.time_mandante.nome} {self.gols_time_mandante} x ' \
               f'{self.gols_time_visitante} {self.time_visitante.nome}'
