from rodada import Rodada
from jogo import Jogo
from random import shuffle


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
        self.criterios_de_classificacao = [
            self.criterio1,
            self.criterio2,
            self.criterio3,
            self.criterio4
        ]
        self.criterio = self.criterios_de_classificacao[index_criterio]

    def adicionar_time(self, time):
        self.times.append(time)
        self.times.sort()
        self.numero_de_times += 1

    def iniciar_liga(self):
        self.classificacao = sorted(self.times, key=lambda time: time.nome)
        self.numero_de_rodadas = self.numero_de_times - 1 + self.numero_de_times % 2
        self.jogos_por_rodada = self.numero_de_times // 2
        self.gerar_rodadas()

    def gerar_rodadas(self):
        if self.numero_de_times > 1:
            shuffle(self.times)
            for i in range(self.numero_de_rodadas):
                rodada = Rodada(i+1)
                for j in range(self.jogos_por_rodada):
                    time_mandante = self.times[j]
                    time_visitante = self.times[-j-1]
                    jogo = Jogo(time_mandante, time_visitante)
                    rodada.adicionar_jogo(jogo)
                self.times.insert(1, self.times.pop())
                self.rodadas.append(rodada)

            for r, rodada in enumerate(self.rodadas):
                for j, jogo in enumerate(rodada.jogos):
                    if j % 2 == 0:
                        jogo.time_mandante, jogo.time_visitante = jogo.time_visitante, jogo.time_mandante

                if r % 2 == 0:
                    jogo = rodada.jogos[0]
                    jogo.time_mandante, jogo.time_visitante = jogo.time_visitante, jogo.time_mandante

        else:
            raise Exception("Não há times suficientes")

    def atualizar_classificacao(self):
        cmp = self.criterio
        for i in range(self.numero_de_times):
            for j in range(i+1, self.numero_de_times):
                if cmp(self.classificacao[i], self.classificacao[j]) < 0:
                    self.classificacao[i], self.classificacao[j] = self.classificacao[j], self.classificacao[i]

    def criterio1(self, time1, time2):
        """
        Critério de classificação: Pontos > Saldo de Gols > Gols Feitos
        :return: 1 se o time1 tiver mais bem colocado que o time2
                -1 se o time2 tiver mais bem colocado que o time1
                 0 se os dois times estiverem empatados na classificação
        """
        if time1.pontos > time2.pontos:
            return 1
        if time1.pontos < time2.pontos:
            return -1
        if time1.saldo_de_gols > time2.saldo_de_gols:
            return 1
        if time1.saldo_de_gols < time2.saldo_de_gols:
            return -1
        if time1.gols_feitos > time2.gols_feitos:
            return 1
        if time1.gols_feitos < time2.gols_feitos:
            return -1
        return 0

    def criterio2(self, time1, time2):
        """
        Critério de classificação: Pontos > Vitórias > Saldo de Gols > Gols Feitos
        :return: 1 se o time1 tiver mais bem colocado que o time2
                -1 se o time2 tiver mais bem colocado que o time1
                 0 se os dois times estiverem empatados na classificação
        """
        if time1.pontos > time2.pontos:
            return 1
        if time1.pontos < time2.pontos:
            return -1
        if time1.vitorias > time2.vitorias:
            return 1
        if time1.vitorias < time2.vitorias:
            return -1
        if time1.saldo_de_gols > time2.saldo_de_gols:
            return 1
        if time1.saldo_de_gols < time2.saldo_de_gols:
            return -1
        if time1.gols_feitos > time2.gols_feitos:
            return 1
        if time1.gols_feitos < time2.gols_feitos:
            return -1
        return 0

    def criterio3(self, time1, time2):
        """
        Critério de classificação: Pontos > Saldo de Gols > Gols Feitos > Vitórias
        :return: 1 se o time1 tiver mais bem colocado que o time2
                -1 se o time2 tiver mais bem colocado que o time1
                 0 se os dois times estiverem empatados na classificação
        """

        if time1.pontos > time2.pontos:
            return 1
        if time1.pontos < time2.pontos:
            return -1
        if time1.saldo_de_gols > time2.saldo_de_gols:
            return 1
        if time1.saldo_de_gols < time2.saldo_de_gols:
            return -1
        if time1.gols_feitos > time2.gols_feitos:
            return 1
        if time1.gols_feitos < time2.gols_feitos:
            return -1
        if time1.vitorias > time2.vitorias:
            return 1
        if time1.vitorias < time2.vitorias:
            return -1
        return 0

    def criterio4(self, time1, time2):
        """
        Critério de classificação: Pontos > Saldo de Gols > Vitórias > Gols Feitos
        :return: 1 se o time1 tiver mais bem colocado que o time2
                -1 se o time2 tiver mais bem colocado que o time1
                 0 se os dois times estiverem empatados na classificação
        """
        if time1.pontos > time2.pontos:
            return 1
        if time1.pontos < time2.pontos:
            return -1
        if time1.saldo_de_gols > time2.saldo_de_gols:
            return 1
        if time1.saldo_de_gols < time2.saldo_de_gols:
            return -1
        if time1.vitorias > time2.vitorias:
            return 1
        if time1.vitorias < time2.vitorias:
            return -1
        if time1.gols_feitos > time2.gols_feitos:
            return 1
        if time1.gols_feitos < time2.gols_feitos:
            return -1
        return 0
