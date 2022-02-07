class Jogo:

    def __init__(self, time_mandante, time_visitante):
        self.time_mandante = time_mandante
        self.time_visitante = time_visitante
        self.gols_time_mandante = ""
        self.gols_time_visitante = ""

    def __str__(self):
        return f'{self.time_mandante.nome} {self.gols_time_mandante} x ' \
               f'{self.gols_time_visitante} {self.time_visitante.nome}'

    def definir_placar(self, gols_time_mandante, gols_time_visitante):
        self.gols_time_mandante = gols_time_mandante
        self.gols_time_visitante = gols_time_visitante
        self.definir_vencendor()

    def definir_vencendor(self):
        if self.gols_time_mandante is not None and self.gols_time_visitante is not None:
            if self.gols_time_mandante > self.gols_time_visitante:
                self.time_mandante.vitoria()
                self.time_visitante.derrota()
            elif self.gols_time_mandante < self.gols_time_visitante:
                self.time_mandante.derrota()
                self.time_visitante.vitoria()
            else:
                self.time_mandante.empate()
                self.time_visitante.empate()
            self.time_mandante.atualizar_gols(self.gols_time_mandante, self.gols_time_visitante)
            self.time_visitante.atualizar_gols(self.gols_time_visitante, self.gols_time_mandante)
        else:
            print("Impossível definir o vencedor, pois o placar é inválido")
