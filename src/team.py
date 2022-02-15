class Time:

    def __init__(self, nome, sigla, emblema=None):
        self.nome = nome
        self.sigla = sigla
        self.jogadores = []
        self.pontos = 0
        self.jogos = 0
        self.vitorias = 0
        self.empates = 0
        self.derrotas = 0
        self.gols_feitos = 0
        self.gols_sofridos = 0
        self.saldo_de_gols = 0
        if emblema is not None:
            self.emblema = emblema
        else:
            self.emblema = 'assets/emblemas/emblema_padrao.png'

    def __str__(self):
        return self.nome

    def vitoria(self):
        self.pontos += 3
        self.vitorias += 1
        self.jogos += 1

    def empate(self):
        self.pontos += 1
        self.empates += 1
        self.jogos += 1

    def derrota(self):
        self.derrotas += 1
        self.jogos += 1

    def atualizar_gols(self, gols_feitos, gols_sofridos):
        self.gols_feitos += gols_feitos
        self.gols_sofridos += gols_sofridos
        self.saldo_de_gols = self.gols_feitos - self.gols_sofridos

    def adicionar_jogador(self, jogador):
        self.jogadores.append(jogador)

    def remover_jogador(self, jogador):
        self.jogadores.remove(jogador)

    def atualizar_nome(self, novo_nome):
        self.nome = novo_nome

    def atualizar_emblema(self, novo_emblema):
        self.emblema = novo_emblema

    def adicionar_punicao(self, pontos_perdidos):
        self.pontos -= pontos_perdidos

    def resetar_vitoria(self):
        self.pontos -= 3
        self.vitorias -= 1
        self.jogos -= 1

    def resetar_empate(self):
        self.pontos -= 1
        self.empates -= 1
        self.jogos -= 1

    def resetar_derrota(self):
        self.derrotas -= 1
        self.jogos -= 1

    def resetar_gols(self, gols_feitos, gols_sofridos):
        self.gols_feitos -= gols_feitos
        self.gols_sofridos -= gols_sofridos
        self.saldo_de_gols = self.gols_feitos - self.gols_sofridos

    def __eq__(self, other):
        return self.nome == other.nome

    def __lt__(self, other):
        return self.nome < other.nome
