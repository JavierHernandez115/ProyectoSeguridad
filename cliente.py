import socket
import threading
import tkinter as tk
from tkinter import messagebox
import logging
from chat_interfaz import ChatInterfaz  # Asegúrate de que el archivo chat_interfaz.py esté en el mismo directorio
from cliente_interfaz import ClienteInterfaz  # Asegúrate de que el archivo cliente_interfaz.py esté en el mismo directorio

logging.basicConfig(level=logging.DEBUG)

def iniciar_chat(cliente_socket):
    root = tk.Tk()
    chat_interfaz = ChatInterfaz(root)
    chat_interfaz.cliente_socket = cliente_socket  # Añadimos el socket al chat
    recibir_thread = threading.Thread(target=recibir_mensajes, args=(cliente_socket, chat_interfaz))
    recibir_thread.daemon = True
    recibir_thread.start()
    root.mainloop()

def recibir_mensajes(cliente_socket, chat_interfaz):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if mensaje:
                logging.debug(f"Mensaje recibido del servidor: {mensaje}")
                chat_interfaz.mostrar_mensaje("Servidor", mensaje)
                with open('mensaje.txt', 'a') as archivo:
                    archivo.write(f"Servidor: {mensaje}\n")
        except Exception as e:
            logging.error(f"Error al recibir mensajes: {e}")
            break

def conectar_y_mostrar_chat(ip):
    try:
        cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.info(f"Intentando conectar a {ip}:9999")
        cliente_socket.connect((ip, 9999))
        iniciar_chat(cliente_socket)
    except Exception as e:
        logging.error(f"No se pudo conectar al servidor: {e}")
        messagebox.showerror("Error", f"No se pudo conectar al servidor: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    cliente_interfaz = ClienteInterfaz(root)
    cliente_interfaz.conectar = lambda: conectar_y_mostrar_chat(cliente_interfaz.ip_entry.get())
    root.mainloop()
