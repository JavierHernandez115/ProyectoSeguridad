import tkinter as tk
from tkinter import ttk, filedialog
import socket
import threading
import os
from chat_interface import ChatInterface
import funciones  # Asumiendo que este módulo contiene las funciones mencionadas
import main


main.GenerarLlavesCliente()

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

def connect_to_server(ip, chat_interface):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, 12345))
        chat_interface.display_message(f"Conectado al servidor en {ip}:12345")

        # Recibir el archivo de la clave pública del servidor
        file_request = client_socket.recv(8)
        if file_request == b'SENDFILE':
            filename = client_socket.recv(1024).decode('utf-8')
            receive_file(client_socket, filename)

        # Enviar el archivo de la clave pública del cliente
        client_socket.send(b'SENDFILE')
        client_socket.send(b'ClavePublica_Client')
        send_file(client_socket, 'ClavePublica_Client')

        def receive_messages():
            while True:
                try:
                    data_type = client_socket.recv(4)
                    if data_type == b'TEXT':
                        message = client_socket.recv(1024).decode('utf-8')
                        if message:
                            chat_interface.display_message(message)
                    elif data_type == b'FILE':
                        filename = client_socket.recv(1024).decode('utf-8')
                        file_data = client_socket.recv(1024*1024)
                        with open(f"received_{filename}", 'wb') as file:
                            file.write(file_data)
                        chat_interface.display_message(f"Archivo {filename} recibido")
                except Exception as e:
                    chat_interface.display_message(f"Error recibiendo mensaje: {e}")
                    break

        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        return client_socket
    except Exception as e:
        chat_interface.display_message(f"No se pudo conectar al servidor: {e}")
        return None

def start_chat_interface(ip):
    root = tk.Tk()
    chat_interface = ChatInterface(root, lambda msg: send_message(msg, client_socket), lambda file_path: send_file(file_path, client_socket))
    client_socket = connect_to_server(ip, chat_interface)
    root.mainloop()

def send_message(message, client_socket):
    if client_socket:
        try:
            client_socket.send(b'TEXT')
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

def send_file(file_path, client_socket):
    if client_socket:
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
                client_socket.send(b'FILE')
                client_socket.send(os.path.basename(file_path).encode('utf-8'))
                client_socket.send(data)
        except Exception as e:
            print(f"Error enviando archivo: {e}")

def main():
    root = tk.Tk()
    root.title("Conectar al servidor")
    root.geometry("300x150")

    frame = ttk.Frame(root, padding=20)
    frame.pack(expand=True)

    ip_label = ttk.Label(frame, text="Ingrese la IP del servidor:")
    ip_label.pack(pady=5)

    ip_entry = ttk.Entry(frame, width=30)
    ip_entry.pack(pady=5)

    def on_accept():
        ip = ip_entry.get()
        root.destroy()
        start_chat_interface(ip)

    accept_button = ttk.Button(frame, text="Aceptar", command=on_accept)
    accept_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()