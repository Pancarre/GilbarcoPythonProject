import json

import requests

# Indirizzo del server HTTP
server_host = 'http://127.0.0.1'
server_port = 12345

# URL completo per la richiesta POST al server
url = f"{server_host}:{server_port}"

# Dati da inviare nella richiesta POST

command_json = {
    "command": {
        "protocol-version": "00.01",
        "name": "new-test-in-progress",
        "fields": {
            "env-id": "$ENV-ID",
            "test-name": "$TEST-NAME"
        }
    }
}


# Esegui una richiesta POST al server
response = requests.post(url, json=command_json)

# Stampa la risposta ricevuta dal server
print("Risposta dal server:")
print(response.text)

# Converti la risposta in un dizionario
response_data = json.loads(response.text)

if response_data["answer"]["fields"]["acknowledge"] == "ok":

    test_id = response_data["answer"]["fields"]["new-test-id"]

    command_json = {
        "command": {
            "protocol-version": "00.01",
            "name": "update-test-in-progress",
            "fields": {
                "test-id": test_id,
                "test-update": "$NEW-STATUS",
                "time-stamp": "$TIME-STAMP",
                "other-info": "$INFO"
            }
        }
    }
    # Esegui una richiesta POST al server
    response = requests.post(url, json=command_json)

    # Stampa la risposta ricevuta dal server
    print("Risposta dal server:")
    print(response.text)

    command_json = {
        "command": {
            "protocol-version": "00.01",
            "name": "end-test-in-progress",
            "fields": {
                "test-id": test_id,
                "result": "terminato"

            }
        }
    }
    # Esegui una richiesta POST al server
    response = requests.post(url, json=command_json)

    # Stampa la risposta ricevuta dal server
    print("Risposta dal server:")
    print(response.text)









else:
    print("errore")
