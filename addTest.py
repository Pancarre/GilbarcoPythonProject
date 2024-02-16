import json
import sqlite3
import threading
def is_test_id_valid(test_id, cursor):
     # Function to check if the ID meets the conditions
    cursor.execute("SELECT id FROM TEST WHERE id = ?", (test_id,))
    result = cursor.fetchone()
    if result is None:
        raise Exception("Invalid id")
    return True

def handle_request(json_data, database_name):

    conn = sqlite3.connect(database_name)
    cursor = conn.cursor()

    # Definition of a block to ensure sequential access to the database
    insert_lock = threading.Lock()

    # Perform the action based on the type of request

    if json_data['command']['name'] == 'new-test-in-progress':
            with insert_lock:
                cursor.execute("""INSERT INTO TEST (env_id, test_name,start_time)
                                        VALUES (?, ?, CURRENT_TIMESTAMP)""",
                            (json_data['command']['fields']['env-id'], json_data['command']['fields']['test-name']))
                conn.commit()
                # Get the ID assigned to the last inserted row.
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
        raise Exception("name error")
