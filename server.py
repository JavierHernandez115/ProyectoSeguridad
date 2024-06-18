import socket
import threading
import tkinter as tk
import os
from chat_interface import ChatInterface
import funciones  # Asumiendo que este módulo contiene las funciones mencionadas
import main 
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



main.GenerarLlavesServidor()

def send_file(client_socket, file_path):
    with open(file_path, 'rb') as file:
        while (chunk := file.read(1024)):
            client_socket.send(chunk)
    client_socket.send(b'<EOF>')  # Indicar el final del archivo

def receive_file(client_socket, file_path):
    with open(file_path, 'wb') as file:
        while True:
            chunk = client_socket.recv(1024)
            if chunk.endswith(b'<EOF>'):
                file.write(chunk[:-5])  # Remove the <EOF> marker
                break
            file.write(chunk)

def broadcast(message, current_client=None):
    for client in clients:
        if client['socket'] != current_client:
            try:
                client['socket'].send(message.encode('utf-8'))
            except:
                client['socket'].close()
                clients.remove(client)

def handle_client(client_socket, chat_interface):
    try:
        # Enviar el archivo de la clave pública del servidor
        client_socket.send(b'SENDFILE')
        client_socket.send(b'ClavePublica_Serv')
        send_file(client_socket, 'ClavePublica_Serv')

        # Recibir el archivo de la clave pública del cliente
        file_request = client_socket.recv(8)
        if file_request == b'SENDFILE':
            filename = client_socket.recv(1024).decode('utf-8')
            receive_file(client_socket, filename)

        clients.append({'socket': client_socket, 'public_key_file': filename})

        while True:
            data_type = client_socket.recv(4)
            if data_type == b'TEXT':
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                chat_interface.display_message(f"Cliente: {message}")
                broadcast(message, client_socket)
            elif data_type == b'FILE':
                filename = client_socket.recv(1024).decode('utf-8')
                file_data = client_socket.recv(1024*1024)
                with open(f"received_{filename}", 'wb') as file:
                    file.write(file_data)
                chat_interface.display_message(f"Archivo {filename} recibido")
                broadcast(f"Archivo {filename} recibido", client_socket)
    except:
        client_socket.close()
        clients.remove(client_socket)

def start_server(chat_interface):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    chat_interface.display_message(f"Servidor escuchando en {HOST}:{PORT}")

    while True:
        client_socket, client_address = server.accept()
        chat_interface.display_message(f"Conexión aceptada de {client_address}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket, chat_interface))
        client_thread.start()

def main():
    root = tk.Tk()
    chat_interface = ChatInterface(root, lambda msg: broadcast(f"Servidor: {msg}"), broadcast)
    server_thread = threading.Thread(target=start_server, args=(chat_interface,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()

if __name__ == "__main__":
    main()
