import socket
import threading
import tkinter as tk
from chat_interface import ChatInterface

def get_local_ip():
    """Obtiene la dirección IP local de la máquina."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # No es necesario que el servidor esté realmente conectado a internet.
        s.connect(('10.254.254.254', 1))
        local_ip = s.getsockname()[0]
    except Exception:
        local_ip = '127.0.0.1'
    finally:
        s.close()
    return local_ip

HOST = get_local_ip()
PORT = 12345
clients = []

def broadcast(message, current_client=None):
    for client in clients:
        if client != current_client:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def handle_client(client_socket, chat_interface):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            chat_interface.display_message(f"Cliente: {message}")
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            client_socket.close()
            break

def start_server(chat_interface):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    chat_interface.display_message(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        chat_interface.display_message(f"Conexión aceptada de {client_address}")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, chat_interface))
        client_thread.start()

def main():
    root = tk.Tk()
    chat_interface = ChatInterface(root, lambda msg: broadcast(f"Servidor: {msg}"))
    server_thread = threading.Thread(target=start_server, args=(chat_interface,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
