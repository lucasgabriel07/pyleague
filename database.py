import sqlite3

from liga.highlight import Highlight
from liga.jogo import Jogo
from liga.rodada import Rodada


database = 'data/database.db'


def create_database(liga):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Ligas('
                   'nome TEXT PRIMARY_KEY NOT NULL,'
                   'numero_de_turnos INTEGER NOT NULL,'
                   'index_criterio INTEGER NOT NULL'
                   ')')

    cursor.execute('INSERT INTO Ligas (nome, numero_de_turnos, index_criterio) VALUES (?,?,?)',
                   (liga.nome, liga.numero_de_turnos, liga.index_criterio))

    cursor.execute('CREATE TABLE IF NOT EXISTS Times('
                   'nome_liga TEXT NOT NULL,'
                   'nome TEXT NOT NULL,'
                   'sigla TEXT NOT NULL,'
                   'emblema TEXT'
                   ')')

    for time in liga.times:
        cursor.execute('INSERT INTO Times (nome_liga, nome, sigla, emblema) VALUES (?,?,?,?)',
                       (liga.nome, time.nome, time.sigla, time.emblema))

    cursor.execute('CREATE TABLE IF NOT EXISTS Rodadas('
                   'nome_liga TEXT NOT NULL,'
                   'numero INTEGER NOT NULL'
                   ')')

    cursor.execute('CREATE TABLE IF NOT EXISTS Jogos('
                   'nome_liga TEXT NOT NULL,'
                   'numero_rodada INTEGER NOT NULL,'
                   'numero_jogo INTEGER NOT NULL,'
                   'nome_time_mandante TEXT NOT NULL,'
                   'nome_time_visitante TEXT NOT NULL,'
                   'gols_time_mandante INTEGER,'
                   'gols_time_visitante INTEGER'
                   ')')

    for rodada in liga.rodadas:
        cursor.execute('INSERT INTO Rodadas (nome_liga, numero) VALUES (?,?)', (liga.nome, rodada.numero))
        for jogo in rodada.jogos:
            cursor.execute('INSERT INTO Jogos (numero_rodada, nome_liga, numero_jogo, nome_time_mandante, '
                           'nome_time_visitante, gols_time_mandante, gols_time_visitante) VALUES (?,?,?,?,?,?,?)',
                           (rodada.numero, liga.nome, jogo.numero, jogo.time_mandante.nome, jogo.time_visitante.nome,
                            jogo.gols_time_mandante, jogo.gols_time_visitante))

    cursor.execute('CREATE TABLE IF NOT EXISTS Highlights('
                   'nome_liga TEXT NOT NULL,'
                   'bg TEXT NOT NULL,'
                   'fg TEXT NOT NULL,'
                   'inicio INTEGER NOT NULL,'
                   'fim INTEGER NOT NULL'
                   ')')

    conn.commit()
    conn.close()


def update_nome_liga(nome_antigo, nome_novo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('UPDATE Ligas SET nome=(?) WHERE nome=(?)', (nome_novo, nome_antigo))
    cursor.execute('UPDATE Times SET nome_liga=(?) WHERE nome_liga=(?)', (nome_novo, nome_antigo))
    cursor.execute('UPDATE Jogos SET nome_liga=(?) WHERE nome_liga=(?)', (nome_novo, nome_antigo))
    cursor.execute('UPDATE Rodadas SET nome_liga=(?) WHERE nome_liga=(?)', (nome_novo, nome_antigo))
    cursor.execute('UPDATE Highlights SET nome_liga=(?) WHERE nome_liga=(?)', (nome_novo, nome_antigo))
    conn.commit()
    conn.close()


def update_nome_time(nome_liga, nome_antigo, nome_novo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('UPDATE Times SET nome=(?) WHERE nome=(?) AND nome_liga=(?)',
                   (nome_novo, nome_antigo, nome_liga))
    cursor.execute('UPDATE Jogos SET nome_time_mandante=(?) WHERE nome_time_mandante=(?)',
                   (nome_novo, nome_antigo))
    cursor.execute('UPDATE Jogos SET nome_time_visitante=(?) WHERE nome_time_visitante=(?)',
                   (nome_novo, nome_antigo))
    conn.commit()
    conn.close()


def update_sigla_time(nome_liga, nome_time, nova_sigla):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('UPDATE Times SET sigla=(?) WHERE nome=(?) AND nome_liga=(?)',
                   (nova_sigla, nome_time, nome_liga))
    conn.commit()
    conn.close()


def update_emblema_time(nome_liga, nome_time, emblema_novo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('UPDATE Times SET emblema=(?) WHERE nome=(?) AND nome_liga=(?)',
                   (emblema_novo, nome_time, nome_liga))
    conn.commit()
    conn.close()


def update_resultado(nome_liga, numero_rodada, jogo):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('UPDATE Jogos SET gols_time_mandante=(?), gols_time_visitante=(?) WHERE nome_liga=(?) AND '
                   'numero_rodada=(?) AND numero_jogo=(?)',
                   (jogo.gols_time_mandante, jogo.gols_time_visitante, nome_liga, numero_rodada, jogo.numero))
    conn.commit()
    conn.close()


def adicionar_highlight(nome_da_liga, hl):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO Highlights (nome_liga, bg, fg, inicio, fim) VALUES(?,?,?,?,?)',
                   (nome_da_liga, hl.bg, hl.fg, hl.inicio, hl.fim))
    conn.commit()
    conn.close()


def remover_highlight(nome_da_liga, hl):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Highlights WHERE nome_liga=(?) AND bg=(?) AND fg=(?) AND inicio=(?) AND fim=(?)',
                   (nome_da_liga, hl.bg, hl.fg, hl.inicio, hl.fim))
    conn.commit()
    conn.close()


def resetar_liga(nome_liga):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute("UPDATE Jogos SET gols_time_mandante='', gols_time_visitante='' WHERE nome_liga=(?)",
                   (nome_liga,))
    conn.commit()
    conn.close()


def get_ligas():
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT nome FROM Ligas')
    except sqlite3.OperationalError:
        ligas = None
    else:
        data = cursor.fetchall()
        if len(data) > 0:
            ligas = [d[0] for d in data]
        else:
            ligas = None
    conn.close()
    return ligas


def get_times(nome_da_liga):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('SELECT nome, sigla, emblema FROM Times WHERE nome_liga=(?)', (nome_da_liga,))
    data = cursor.fetchall()
    conn.close()
    return data


def carregar_liga(nome_da_liga):
    from liga.liga import Liga
    from liga.team import Time

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM Ligas WHERE nome=(?)', (nome_da_liga,))
    nome, numero_de_turnos, index_criterio = cursor.fetchone()

    liga = Liga(nome, numero_de_turnos, index_criterio)

    cursor.execute('SELECT nome, sigla, emblema FROM Times WHERE nome_liga=(?)', (nome_da_liga,))
    data_times = cursor.fetchall()

    dict_times = {}

    for data_time in data_times:
        nome, sigla, emblema = data_time

        time = Time(nome, sigla, emblema)
        liga.adicionar_time(time)
        dict_times[nome] = time

    cursor.execute('SELECT * FROM Rodadas WHERE nome_liga=(?)', (nome_da_liga,))
    data_rodadas = cursor.fetchall()

    for data_rodada in data_rodadas:
        numero = data_rodada[1]
        rodada = Rodada(numero)
        liga.adicionar_rodada(rodada)

        cursor.execute('SELECT nome_time_mandante, nome_time_visitante, gols_time_mandante, gols_time_visitante '
                       'FROM Jogos WHERE nome_liga=(?) AND numero_rodada=(?)', (nome_da_liga, str(numero)))
        data_jogos = cursor.fetchall()

        for i, data_jogo in enumerate(data_jogos):
            nome_time_mandante, nome_time_visitante, gols_time_mandante, gols_time_visitante = data_jogo

            time_mandante = dict_times[nome_time_mandante]
            time_visitante = dict_times[nome_time_visitante]

            jogo = Jogo(time_mandante, time_visitante, i+1)
            jogo.definir_placar(gols_time_mandante, gols_time_visitante)
            rodada.adicionar_jogo(jogo)

    cursor.execute('SELECT bg, fg, inicio, fim FROM Highlights WHERE nome_liga=(?)', (nome_da_liga,))
    data_highlights = cursor.fetchall()

    for bg, fg, inicio, fim in data_highlights:
        hl = Highlight(bg, fg, inicio, fim)
        liga.adicionar_highlight(hl)

    conn.close()
    return liga


def deletar_liga(nome_da_liga):
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM Ligas WHERE nome=(?)', (nome_da_liga,))
    cursor.execute('DELETE FROM Times WHERE nome_liga=(?)', (nome_da_liga,))
    cursor.execute('DELETE FROM Jogos WHERE nome_liga=(?)', (nome_da_liga,))
    cursor.execute('DELETE FROM Rodadas WHERE nome_liga=(?)', (nome_da_liga,))
    conn.commit()
    conn.close()
