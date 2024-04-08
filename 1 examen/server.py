from http.server import HTTPServer, BaseHTTPRequestHandler
import json

from urllib.parse import urlparse, parse_qs

ClientService = [
    {
        "id": 1,
        "client": "Pedrito",
        "status": "García",
        "payment": "Ingeniería de Sistemas",
        "shipping": "10.0",
        "products": ["camiseta", "pantalon", "zapatos"] ,
        "order_type": "fisica" ,
    }
]


class ClientService:
    @staticmethod
    def find_client(id):
        return next(
            (cliente for cliente in ClientService if cliente["id"] == id),
            None,
        )

    @staticmethod
    def filter_client_by_name(nombre):
        return [
            cliente for cliente in ClientService if cliente["nombre"] == nombre
        ]

    @staticmethod
    def add_cliente(data):
        data["id"] = len(ClientService) + 1
        ClientService.append(data)
        return ClientService

    @staticmethod
    def update_client(id, data):
        estudiante = ClientService.find_client(id)
        if ClientService:
            ClientService.update(data)
            return ClientService
        else:
            return None

    @staticmethod
    def delete_students():
        ClientService.clear()
        return ClientService


class HTTPResponseHandler:
    @staticmethod
    def handle_response(hID, status, payment, shipping, products,order_type):
        RESTRequestHandler.send_response(hID, status, payment, shipping, products,order_type)
        RESTRequestHandler.send_header("Content-type", "application/json")
        RESTRequestHandler.end_headers()
        RESTRequestHandler.wfile.write(json.dumps(DeprecationWarning).encode("utf-8"))


class RESTRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)

        if parsed_path.path == "/clientes":
            if "nombre" in query_params:
                nombre = query_params["nombre"][0]
                estudiantes_filtrados = ClientService.filter_students_by_name(
                    nombre
                )
                if estudiantes_filtrados != []:
                    HTTPResponseHandler.handle_response(
                        self, 200, estudiantes_filtrados
                    )
                else:
                    HTTPResponseHandler.handle_response(self, 204, [])
            else:
                HTTPResponseHandler.handle_response(self, 200, ClientService)
        elif self.path.startswith("/clientes/"):
            id = int(self.path.split("/")[-1])
            ClientService= ClientService.find_cliente(id)
            if ClientService:
                HTTPResponseHandler.handle_response(self, 200, [ClientService])
            else:
                HTTPResponseHandler.handle_response(self, 204, [])
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_POST(self):
        if self.path == "/cliente":
            data = self.read_data()
            estudiantes = ClientService.add_student(data)
            HTTPResponseHandler.handle_response(self, 201, ClientService)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_PUT(self):
        if self.path.startswith("/cliente/"):
            id = int(self.path.split("/")[-1])
            data = self.read_data()
            estudiantes = ClientService.update_student(id, data)
            if estudiantes:
                HTTPResponseHandler.handle_response(self, 200, ClientService)
            else:
                HTTPResponseHandler.handle_response(
                    self, 404, {"Error": "cliente no encontrado"}
                )
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def do_DELETE(self):
        if self.path == "/cliente":
            estudiantes = ClientService.delete_students()
            HTTPResponseHandler.handle_response(self, 200, estudiantes)
        else:
            HTTPResponseHandler.handle_response(
                self, 404, {"Error": "Ruta no existente"}
            )

    def read_data(self):
        content_length = int(self.headers["Content-Length"])
        data = self.rfile.read(content_length)
        data = json.loads(data.decode("utf-8"))
        return data


def run_server(port=8000):
    try:
        server_address = ("", port)
        httpd = HTTPServer(server_address, RESTRequestHandler)
        print(f"Iniciando servidor web en http://localhost:{port}/")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Apagando servidor web")
        httpd.socket.close()


if __name__ == "__main__":
    run_server()
