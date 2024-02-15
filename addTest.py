import json
import sqlite3
import threading
def is_test_id_valid(test_id, cursor):
     #funzione per verificare se id soddisfa le condizioni
    cursor.execute("SELECT id FROM TEST WHERE id = ?", (test_id,))
    result = cursor.fetchone()
    if result is None:
        raise Exception("id non valido")
    return True

def handle_request(json_data, database_name, version_protocol):

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Definizione di un blocco per garantire l'accesso sequenziale al database
    insert_lock = threading.Lock()

    # Esegui l'azione in base al tipo di richiesta
    #try
    if json_data['command']['name'] == 'new-test-in-progress':
            with insert_lock:
                cursor.execute("""INSERT INTO TEST (env_id, test_name,start_time)
                                        VALUES (?, ?, CURRENT_TIMESTAMP)""",
                            (json_data['command']['fields']['env-id'], json_data['command']['fields']['test-name']))
                conn.commit()
                # Ottenere l'ID assegnato all'ultima riga inserita
                cursor.execute("SELECT last_insert_rowid()")
                assigned_id = cursor.fetchone()[0]
            return assigned_id

    elif json_data['command']['name'] == 'update-test-in-progress':
        if is_test_id_valid(json_data['command']['fields']['test-id'], cursor):
            cursor.execute("""INSERT INTO EVENTI_test (test_id, test_update, time_stamp, other_info)
                                    VALUES (?, ?, ?, ?)""",
                           (json_data['command']['fields']['test-id'], json_data['command']['fields']['test-update'],
                                        json_data['command']['fields']['time-stamp'],json_data['command']['fields']['other-info']))
            conn.commit()

            return None

    elif json_data['command']['name'] == 'end-test-in-progress':
        if is_test_id_valid(json_data['command']['fields']['test-id'], cursor):
            cursor.execute("""UPDATE TEST
                                    SET end_time = CURRENT_TIMESTAMP, result = ?
                                    WHERE id = ?;""",
                           (json_data['command']['fields']['result'],
                                        json_data['command']['fields']['test-id']))
            conn.commit()


    else:
        raise Exception("errore di name")