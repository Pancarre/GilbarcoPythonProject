import sqlite3

def create_table(cursor):
    # Creazione di tabella test se non esiste
    with open("SQLtxt/testSQL.txt", "r", encoding="utf-8") as testSQL:
        sql_queries = testSQL.read()
        cursor.execute(sql_queries)

    # Creazione di tabella eventi-test se non esiste
    with open("SQLtxt/eventiSQL.txt", "r", encoding="utf-8") as eventiSQL:
        sql_queries = eventiSQL.read()
        cursor.execute(sql_queries)


def create_database(database_name):
    # Connessione o creazione del database SQLite
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    print(f"Collegato con il database {database_name}.")
    # Creazione delle tabelle se non esiste
    create_table(cursor)