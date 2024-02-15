import json
import sqlite3
import threading

def handle_request(json_data, database_name, version_protocol):

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Decodifica la richiesta JSON
    request = json.loads(json_data.decode('utf-8'))


        # Definizione di un blocco per garantire l'accesso sequenziale al database
    insert_lock = threading.Lock()

    # Esegui l'azione in base al tipo di richiesta
    #try
    if request['command']['name'] == 'new-test-in-progress':
            with insert_lock:
                cursor.execute("""INSERT INTO TEST (protocol_version, env_id, test_name)
                                  VALUES (?, ?, ?)""",
                               (request['command']['protocol-version'], request['command']['fields']['env-id'], request['command']['fields']['test-name']))
                conn.commit()
                # Ottenere l'ID assegnato all'ultima riga inserita
                cursor.execute("SELECT last_insert_rowid()")
                assigned_id = cursor.fetchone()[0]
            return "new-test-in-progress", assigned_id

    elif request['command']['name'] == 'update-test-in-progress':

        cursor.execute("""INSERT INTO EVENTI_test (test_id, test_update, time_stamp, other_info)
                              VALUES (?, ?, ?, ?)""",
                           (request['command']['fields']['test-id'], request['command']['fields']['test-update'], request['command']['fields']['time-stamp'],
                            request['command']['fields']['other-info']))
        conn.commit()

        return "update-test-in-progress", None


