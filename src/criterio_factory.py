class CriterioFactory:

    @staticmethod
    def definir_criterio(opcao):
        return CriterioFactory.criterios[opcao]

    @staticmethod
    def __criterio1(time1, time2):
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

    @staticmethod
    def __criterio2(time1, time2):
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

    @staticmethod
    def __criterio3(time1, time2):
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

    @staticmethod
    def __criterio4(time1, time2):
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

    criterios = [__criterio1, __criterio2, __criterio3, __criterio4]
