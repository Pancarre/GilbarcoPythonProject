import json

import requests


# This is the client that connects to the server to verify the functionalities.

# HTTP server address
server_host = 'http://127.0.0.1'
server_port = 12345

# The complete URL for the POST request to the server.
url = f"{server_host}:{server_port}"

# Data to be sent in the POST request.

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

# Execute a POST request to the server.
response = requests.post(url, json=command_json)

# Print the response received from the server.
print("Response from the server in case of a new-test:")
print(response.text)

# Convert the response into a dictionary and send other request if acknowledge == ok.
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
    # Make a POST request to the server.
    response = requests.post(url, json=command_json)

    # Print the response received from the server.
    print("Response from the server in case of a update-test:")
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
    # Make a POST request to the server.
    response = requests.post(url, json=command_json)

    # Print the response received from the server.
    print("Response from the server in case of a end-test:")
    print(response.text)

    # send a post with no_json.

    response = requests.post(url, "not_json")
    print("Response from the server in case of a bad request:")
    print(response.text)

else:
    print("error")
