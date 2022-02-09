from rodada import Rodada
from jogo import Jogo
from random import shuffle
from criterio_factory import CriterioFactory
from gui.gui_liga import GUILiga
from src.team import Time


class Liga:

    def __init__(self, nome, numero_de_turnos, index_criterio):
        self.nome = nome
        self.numero_de_turnos = numero_de_turnos
        self.times = []
        self.classificacao = None
        self.numero_de_times = 0
        self.rodadas = []
        self.numero_de_rodadas = 0
        self.rodadas_por_turno = 0
        self.jogos_por_rodada = 0
        self.criterio = CriterioFactory.definir_criterio(index_criterio)

    def adicionar_time(self, time):
        self.times.append(time)
        self.times.sort()
        self.numero_de_times += 1

    def iniciar_liga(self):
        self.classificacao = sorted(self.times, key=lambda time: time.nome)
        self.rodadas_por_turno = self.numero_de_times - 1 + self.numero_de_times % 2
        self.numero_de_rodadas = self.numero_de_turnos * self.rodadas_por_turno
        self.jogos_por_rodada = self.numero_de_times // 2
        self.gerar_rodadas()
        GUILiga(self)

    def gerar_rodadas(self):
        if self.numero_de_times > 1:
            """
            Em caso de um número ímpar de times, é adicionado um time 'fake' para auxiliar na geração dos jogos.
            O time que, pela geração dos jogos, enfrentaria o time auxiliar em uma determinada rodada, deverá folgar
            nessa rodada.
            """
            time_auxiliar = Time('', '')
            if self.numero_de_times % 2 == 1:
                self.times.append(time_auxiliar)

            shuffle(self.times)

            for i in range(self.rodadas_por_turno):
                rodada = Rodada(i + 1)
                for j in range(self.jogos_por_rodada + self.numero_de_times % 2):
                    time_mandante = self.times[j]
                    time_visitante = self.times[-j - 1]
                    if time_mandante != time_auxiliar and time_visitante != time_auxiliar:
                        jogo = Jogo(time_mandante, time_visitante)
                        rodada.adicionar_jogo(jogo)
                self.times.insert(1, self.times.pop())
                self.rodadas.append(rodada)

            # Ajustar mandos de campo
            for r, rodada in enumerate(self.rodadas):
                for j, jogo in enumerate(rodada.jogos):
                    if j % 2 == 0:
                        jogo.time_mandante, jogo.time_visitante = jogo.time_visitante, jogo.time_mandante

                if r % 2 == 0:
                    jogo = rodada.jogos[0]
                    jogo.time_mandante, jogo.time_visitante = jogo.time_visitante, jogo.time_mandante

            # Returno --> Inverte os mandos de campo
            if self.numero_de_turnos == 2:
                for r in range(self.rodadas_por_turno):
                    rodada_turno = self.rodadas[r]
                    rodada_returno = Rodada(self.rodadas_por_turno + r + 1)
                    for jogo_turno in rodada_turno.jogos:
                        jogo_returno = Jogo(jogo_turno.time_visitante, jogo_turno.time_mandante)
                        rodada_returno.adicionar_jogo(jogo_returno)
                    self.rodadas.append(rodada_returno)

            # Removendo o time auxiliar
            if time_auxiliar in self.times:
                self.times.remove(time_auxiliar)

        else:
            raise Exception("Não há times suficientes")

    def atualizar_classificacao(self):
        cmp = self.criterio
        for i in range(self.numero_de_times):
            for j in range(i + 1, self.numero_de_times):
                if cmp(self.classificacao[i], self.classificacao[j]) < 0:
                    self.classificacao[i], self.classificacao[j] = self.classificacao[j], self.classificacao[i]
