from liga import Liga
from team import Time
from random import randint
from gui.gui_liga import GUILiga


if __name__ == '__main__':
    times = ['CORDINO', 'IAPE', 'JUVENTUDE', 'TUNTUM', 'MOTO CLUB', 'PINHEIRO', 'SAMPAIO CORRÊA', 'SÃO JOSÉ']

    liga = Liga("Campeonato Maranhense 2022", 1, 1)

    for nome in times:
        time = Time(nome, nome[:3])
        time.emblema = f'../assets/emblemas/{nome}.png'
        liga.adicionar_time(time)

    liga.iniciar_liga()

    for rodada in liga.rodadas:
        # print(f'{rodada.numero}ª Rodada:')
        for jogo in rodada.jogos:
            jogo.definir_placar(randint(0, 5), randint(0, 5))
            # print(jogo)
        liga.atualizar_classificacao()
        # print()
        # for time in liga.classificacao:
            # print(time)
        # print()

    GUILiga(liga)