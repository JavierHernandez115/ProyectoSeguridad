import socket
import threading
import tkinter as tk
import logging
from chat_interfaz import ChatInterfaz  # Asegúrate de que el archivo chat_interfaz.py esté en el mismo directorio

logging.basicConfig(level=logging.DEBUG)

def obtener_ip_local():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception as e:
        logging.error(f"Error al obtener IP local: {e}")
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def manejar_cliente(cliente_socket, chat_interfaz):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if mensaje:
                logging.debug(f"Mensaje recibido del cliente: {mensaje}")
                chat_interfaz.mostrar_mensaje("Cliente", mensaje)
                with open('mensaje.txt', 'a') as archivo:
                    archivo.write(f"Cliente: {mensaje}\n")
                cliente_socket.send("Mensaje recibido".encode('utf-8'))
            else:
                break
        except Exception as e:
            logging.error(f"Error al manejar cliente: {e}")
            break

    cliente_socket.close()

def iniciar_servidor(chat_interfaz):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip_local = obtener_ip_local()
    try:
        servidor.bind((ip_local, 9999))
        servidor.listen(5)
        logging.info(f"Servidor escuchando en {ip_local}:9999")
    except Exception as e:
        logging.error(f"Error al iniciar el servidor: {e}")
        return

    while True:
        try:
            cliente_socket, direccion = servidor.accept()
            logging.info(f"Conexión aceptada de {direccion}")
            cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente_socket, chat_interfaz))
            cliente_thread.start()
        except Exception as e:
            logging.error(f"Error al aceptar conexión: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    chat_interfaz = ChatInterfaz(root)
    server_thread = threading.Thread(target=iniciar_servidor, args=(chat_interfaz,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()
