import tkinter as tk
from tkinter import ttk, filedialog
import socket
import threading
import os

class ChatInterface:
    def __init__(self, master, send_callback, send_file_callback):
        self.master = master
        self.send_callback = send_callback
        self.send_file_callback = send_file_callback

        self.master.title("Chat")
        self.master.geometry("400x500")

        self.frame = ttk.Frame(self.master, padding=20)
        self.frame.pack(expand=True, fill=tk.BOTH)

        self.text_area = tk.Text(self.frame, state='disabled', wrap='word')
        self.text_area.pack(pady=10, padx=10, expand=True, fill=tk.BOTH)

        self.message_entry = ttk.Entry(self.frame, width=50)
        self.message_entry.pack(pady=5, padx=10, side=tk.LEFT, expand=True, fill=tk.X)
        self.message_entry.bind('<Return>', lambda event: self.send_message())

        self.send_button = ttk.Button(self.frame, text="Enviar", command=self.send_message)
        self.send_button.pack(pady=5, padx=10, side=tk.RIGHT)

        self.send_file_button = ttk.Button(self.frame, text="Enviar archivo", command=self.send_file)
        self.send_file_button.pack(pady=5, padx=10, side=tk.RIGHT)

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.send_callback(message)
            self.message_entry.delete(0, tk.END)

    def send_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.send_file_callback(file_path)

    def display_message(self, message):
        self.text_area.config(state='normal')
        self.text_area.insert(tk.END, f"{message}\n")
        self.text_area.config(state='disabled')
        self.text_area.yview(tk.END)

def connect_to_server(ip, chat_interface):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((ip, 12345))
        chat_interface.display_message(f"Conectado al servidor en {ip}:12345")

        def receive_messages():
            while True:
                try:
                    message = client_socket.recv(1024).decode('utf-8')
                    if message.startswith('FILE:'):
                        filename = message.split(':', 1)[1]
                        chat_interface.display_message(f"Recibiendo archivo: {filename}")
                        receive_file(client_socket, filename)
                    elif message:
                        chat_interface.display_message(message)
                except Exception as e:
                    chat_interface.display_message(f"Error recibiendo mensaje: {e}")
                    break

        def receive_file(client_socket, filename):
            with open(os.path.join('received_files', os.path.basename(filename)), 'wb') as f:
                while True:
                    bytes_read = client_socket.recv(1024)
                    if bytes_read.endswith(b'FILETRANSFERCOMPLETE'):
                        f.write(bytes_read[:-20])  # remove FILETRANSFERCOMPLETE
                        break
                    f.write(bytes_read)
            chat_interface.display_message(f"Archivo recibido: {filename}")

        receive_thread = threading.Thread(target=receive_messages)
        receive_thread.daemon = True
        receive_thread.start()

        return client_socket
    except Exception as e:
        chat_interface.display_message(f"No se pudo conectar al servidor: {e}")
        return None

def send_file(client_socket, chat_interface, file_path):
    if file_path:
        chat_interface.display_message(f"Enviando archivo: {file_path}")
        client_socket.sendall(f"FILE:{file_path}".encode('utf-8'))
        with open(file_path, 'rb') as f:
            while True:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                client_socket.sendall(bytes_read)
        client_socket.sendall(b'FILETRANSFERCOMPLETE')

def start_chat_interface(ip):
    root = tk.Tk()
    chat_interface = ChatInterface(
        root, 
        lambda msg: send_message(msg, client_socket), 
        lambda file_path: send_file(client_socket, chat_interface, file_path)
    )
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
