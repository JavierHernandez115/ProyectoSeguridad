import tkinter as tk
from tkinter import ttk
import socket
import threading
from chat_interface import ChatInterface

def connect_to_server(ip, chat_interface):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, 12345))
        chat_interface.display_message(f"Conectado al servidor en {ip}:12345")

        def receive_messages():
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message:
                        chat_interface.display_message(message)
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
    chat_interface = ChatInterface(root, lambda msg: send_message(msg, client_socket))
    client_socket = connect_to_server(ip, chat_interface)
    root.mainloop()

def send_message(message, client_socket):
    if client_socket:
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Error enviando mensaje: {e}")

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
