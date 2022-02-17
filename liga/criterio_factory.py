def definir_criterio(opcao):
    return criterios[opcao]


def pontos_vitorias_saldo_gols(time1, time2):
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


def pontos_saldo_gols(time1, time2):
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


def pontos_saldo_gols_vitorias(time1, time2):
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


def pontos_saldo_vitorias_gols(time1, time2):
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


criterios = [
    pontos_vitorias_saldo_gols,
    pontos_saldo_gols,
    pontos_saldo_gols_vitorias,
    pontos_saldo_vitorias_gols
]
