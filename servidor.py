import socket
import threading
import tkinter as tk
from chat_interfaz import ChatInterfaz  # Asegúrate de que el archivo chat_interfaz.py esté en el mismo directorio

def manejar_cliente(cliente_socket, chat_interfaz):
    while True:
        try:
            mensaje = cliente_socket.recv(1024).decode('utf-8')
            if mensaje:
                chat_interfaz.mostrar_mensaje("Cliente", mensaje)
                with open('mensaje.txt', 'a') as archivo:
                    archivo.write(f"Cliente: {mensaje}\n")
                cliente_socket.send("Mensaje recibido".encode('utf-8'))
            else:
                break
        except:
            break

    cliente_socket.close()

def iniciar_servidor(chat_interfaz):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((socket.gethostbyname(socket.gethostname()), 9999))
    servidor.listen(5)
    print(f"Servidor escuchando en {socket.gethostbyname(socket.gethostname())}:9999")

    while True:
        cliente_socket, direccion = servidor.accept()
        cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente_socket, chat_interfaz))
        cliente_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    chat_interfaz = ChatInterfaz(root)
    server_thread = threading.Thread(target=iniciar_servidor, args=(chat_interfaz,))
    server_thread.daemon = True
    server_thread.start()
    root.mainloop()
