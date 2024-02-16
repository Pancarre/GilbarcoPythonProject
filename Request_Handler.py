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
            # Decode the JSON data.
            data = json.loads(post_data.decode('utf-8'))
            # Add to the SQLite database.
            name = data['command']['name']
            test_id = addTest.handle_request(data, database_name)
            json_replay = responce.to_json(name, test_id, version_protocol, "ok", None)

            # send response
            self.response_json(200, json_replay)

        except json.JSONDecodeError as e:

            # Send a 400 Bad Request response if the request body is not a valid JSON.
            print("JSON decoding error with:" + str(self.client_address))

            json_replay = responce.to_json("Bad Request", None, version_protocol, "ko", str(e))
            self.response_json(400, json_replay)


        except KeyError as e:
            json_replay = responce.to_json("Key Error", None, version_protocol, "ko", str(e))
            self.response_json(400, json_replay)

        except Exception as e:
            json_replay = responce.to_json("Unknown Error", None, version_protocol, "ko", str(e) )
            self.response_json(400, json_replay)

    def response_json(self, status, json_replay):
        # Set up the response headers, status is status code of HTTP protocol
        self.send_response(status)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()

        # Send the body of the response.
        response_message = json.dumps(json_replay, indent=4, sort_keys=True)
        self.wfile.write(response_message.encode('utf-8'))

    def do_GET(self):
        # Not implemented.
        # Set up the response header.
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Send the response body.
        self.wfile.write("Hello, this is the HTTP API server!".encode('utf-8'))

# Main function for the server.
def main():
    # Configure the server.
    server_host = '127.0.0.1'
    server_port = 12345


    try:
        # Start the HTTP server.
        http_server = HTTPServer((server_host, server_port), MyHTTPRequestHandler)
        print(f"Server API HTTP in esecuzione su {server_host}:{server_port}...")

        # Start a thread for the HTTP server.
        server_thread = threading.Thread(target=http_server.serve_forever)
        server_thread.start()

        # Wait for the HTTP server thread to finish (which will never happen).
        server_thread.join()


    except ConnectionError as e:
        print("Connection error with: " + str(MyHTTPRequestHandler.client_address))

    except Exception as e:
        print("unknown error of the server")

if __name__ == "__main__":
    main()
