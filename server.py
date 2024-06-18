import socket
import threading
import tkinter as tk
import os
from chat_interface import ChatInterface

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
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
                client.send(b'TEXT' + len(message).to_bytes(4, 'big') + message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def send_file_to_clients(file_path, current_client=None):
    with open(file_path, 'rb') as file:
        data = file.read()
        for client in clients:
            if client != current_client:
                try:
                    client.send(b'FILE')
                    client.send(len(os.path.basename(file_path)).to_bytes(4, 'big') + os.path.basename(file_path).encode('utf-8'))
                    client.send(len(data).to_bytes(8, 'big') + data)
                except:
                    client.close()
                    clients.remove(client)

def handle_client(client_socket, chat_interface):
    while True:
        try:
            data_type = client_socket.recv(4)
            if data_type == b'TEXT':
                msg_len = int.from_bytes(client_socket.recv(4), 'big')
                message = client_socket.recv(msg_len).decode('utf-8')
                if not message:
                    break
                chat_interface.display_message(f"Cliente: {message}")
                broadcast(message, client_socket)
            elif data_type == b'FILE':
                filename_len = int.from_bytes(client_socket.recv(4), 'big')
                filename = client_socket.recv(filename_len).decode('utf-8')
                file_size = int.from_bytes(client_socket.recv(8), 'big')
                file_data = b''
                while len(file_data) < file_size:
                    file_data += client_socket.recv(1024)
                with open(f"received_{filename}", 'wb') as file:
                    file.write(file_data)
                chat_interface.display_message(f"Archivo {filename} recibido")
                broadcast(f"Archivo {filename} recibido", client_socket)
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
    chat_interface = ChatInterface(root, lambda msg: broadcast(f"Servidor: {msg}"), send_file_to_clients)
    server_thread = threading.Thread(target=start_server, args=(chat_interface,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
