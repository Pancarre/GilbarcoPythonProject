import sqlite3

def create_table(cursor):
    # Creating the TEST table if it does not exist
    with open("SQLtxt/testSQL.txt", "r", encoding="utf-8") as testSQL:
        sql_queries = testSQL.read()
        cursor.execute(sql_queries)

    # Creating the EVENT-test table if it does not exist
    with open("SQLtxt/eventiSQL.txt", "r", encoding="utf-8") as eventiSQL:
        sql_queries = eventiSQL.read()
        cursor.execute(sql_queries)


def create_database(database_name):
    # Connection or creation of the SQLite database
    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    print(f"connected with database {database_name}.")
    # Table creation if it does not exist
    create_table(cursor)