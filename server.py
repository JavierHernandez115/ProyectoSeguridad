import socket
import threading
import tkinter as tk
from chat_interface import ChatInterface
import os

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
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def send_file(client_socket, filename):
    with open(filename, 'rb') as f:
        while True:
            bytes_read = f.read(1024)
            if not bytes_read:
                break
            client_socket.sendall(bytes_read)
    client_socket.sendall(b'FILETRANSFERCOMPLETE')

def handle_client(client_socket, chat_interface):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message.startswith('FILE:'):
                filename = message.split(':', 1)[1]
                chat_interface.display_message(f"Cliente enviando archivo: {filename}")
                receive_file(client_socket, filename)
            elif not message:
                break
            else:
                chat_interface.display_message(f"Cliente: {message}")
                broadcast(message, client_socket)
        except Exception as e:
            chat_interface.display_message(f"Error manejando cliente: {e}")
            clients.remove(client_socket)
            client_socket.close()
            break

def receive_file(client_socket, filename):
    with open(os.path.join('received_files', os.path.basename(filename)), 'wb') as f:
        while True:
            bytes_read = client_socket.recv(1024)
            if bytes_read.endswith(b'FILETRANSFERCOMPLETE'):
                f.write(bytes_read[:-20])  # remove FILETRANSFERCOMPLETE
                break
            f.write(bytes_read)
    print(f"Archivo recibido: {filename}")

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

def send_file_callback(filename):
    for client in clients:
        client.sendall(f"FILE:{filename}".encode('utf-8'))

def main():
    root = tk.Tk()
    chat_interface = ChatInterface(root, lambda msg: broadcast(f"Servidor: {msg}"), send_file_callback)
    server_thread = threading.Thread(target=start_server, args=(chat_interface,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
