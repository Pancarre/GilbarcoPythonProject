from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import json
import addTest
import createDatabase
import responce

#variabili globali
database_name = 'mydatabase.db'
version_protocol = 00.01

createDatabase.create_database(database_name)

class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        #riceve richiesta con JSON
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)

        try:
            # Decodifica i dati JSON
            data = json.loads(post_data.decode('utf-8'))
            # agigungere nel SQLite database
            name = data['command']['name']

            test_id = addTest.handle_request(data, database_name, version_protocol)

            json_replay = responce.to_json(name, test_id, version_protocol, "ok", None)

            self.response_json(200, json_replay)

        except json.JSONDecodeError as e:

            # Invia una risposta 400 Bad Request se il corpo della richiesta non è un JSON valido
            print("errore di decodifica JSON con:" + str(self.client_address))

            json_replay = responce.to_json("Bad Request", None, version_protocol, "ko", str(e))
            self.response_json(400, json_replay)


        except KeyError as e:

            json_replay = responce.to_json("Key Error", None, version_protocol, "ko", str(e))
            self.response_json(400, json_replay)

        except Exception as e:
            json_replay = responce.to_json("Unknown Erroe", None, version_protocol, "ko", str(e) )

        # Configura l'intestazione della risposta

    def response_json(self, status, json_replay):

        self.send_response(status)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Invia il corpo della risposta
        response_message = json.dumps(json_replay, indent=4, sort_keys=True)
        self.wfile.write(response_message.encode('utf-8'))

    def do_GET(self):
        # Configura l'intestazione della risposta
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Invia il corpo della risposta
        self.wfile.write("Ciao, questo è il server API HTTP!".encode('utf-8'))

# Funzione principale per il server
def main():
    # Configura il server
    server_host = '127.0.0.1'
    server_port = 12345

    # Avvia il server HTTP
    http_server = HTTPServer((server_host, server_port), MyHTTPRequestHandler)
    print(f"Server API HTTP in esecuzione su {server_host}:{server_port}...")

    # Avvia un thread per il server HTTP
    server_thread = threading.Thread(target=http_server.serve_forever)
    server_thread.start()

    # Attendi che il thread del server HTTP termini (non succederà mai)
    server_thread.join()

if __name__ == "__main__":
    main()
