import socket
from ttypes import Node

class BootstrapServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.nodes = []

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print(f"Bootstrap server started on {self.host}:{self.port}")
            while True:
                conn, addr = server_socket.accept()
                with conn:
                    data = conn.recv(1024).decode()
                    print(f"Received request: {data}")
                    response = self.handle_request(data)
                    print(f"Sending response: {response}")
                    conn.send(response.encode())

    def handle_request(self, request):
        print(f"Handling request: {request}")
        tokens = request.split()
        if tokens[0] == "REG":
            return self.register_node(tokens)
        elif tokens[0] == "UNREG":
            return self.unregister_node(tokens)
        else:
            return "Invalid request"

    def register_node(self, tokens):
        print(f"Registering node with tokens: {tokens}")
        ip, port, name = tokens[1], int(tokens[2]), tokens[3]
        new_node = Node(ip, port, name)
        self.nodes.append(new_node)
        node_count = len(self.nodes)
        response = f"REGOK {node_count}"
        for node in self.nodes:
            response += f" {node.ip} {node.port} {node.name}"
        return response

    def unregister_node(self, tokens):
        print(f"Unregistering node with tokens: {tokens}")
        ip, port, name = tokens[1], int(tokens[2]), tokens[3]
        self.nodes = [node for node in self.nodes if not (node.ip == ip and node.port == port and node.name == name)]
        return "UNROK 0"

if __name__ == "__main__":
    server = BootstrapServer("0.0.0.0", 5001)  # Use port 5001
    server.start()
