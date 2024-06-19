import socket
import threading
import netifaces
import funciones_principales

# Función para manejar la conexión con el cliente
def handle_client(client_socket, addr):
    print(f"[+] Conexión aceptada de {addr}")
    try:
        # Enviar archivo ClavePublica_Serv al cliente
        with open("ClavePublica_Serv", 'rb') as file:
            client_socket.sendall(file.read())

        print("Archivo ClavePublica_Serv enviado al cliente.")

        # Recibir archivo ClavePublica_Client del cliente
        with open("ClavePublica_Client", 'wb') as file:
            file_data = client_socket.recv(1024)
            while file_data:
                file.write(file_data)
                file_data = client_socket.recv(1024)

        print("Archivo ClavePublica_Client recibido y guardado.")

        while True:
            # Recibe el archivo del cliente
            with open(f"mensaje_recibido_{addr[1]}.txt", 'wb') as file:
                file_data = client_socket.recv(1024)
                while file_data:
                    file.write(file_data)
                    file_data = client_socket.recv(1024)

            # Leer el archivo recibido
            with open(f"mensaje_recibido_{addr[1]}.txt", 'r') as file:
                received_msg = file.read()
                print(f"[{addr}] {received_msg}")

            # Pedir mensaje al usuario del servidor
            response_msg = input("Escribe un mensaje para el cliente: ")

            # Guardar el mensaje de respuesta en un archivo
            with open(f"mensaje_respuesta_{addr[1]}.txt", 'w') as file:
                file.write(response_msg)

            # Enviar el archivo de respuesta al cliente
            with open(f"mensaje_respuesta_{addr[1]}.txt", 'rb') as file:
                client_socket.sendall(file.read())
    except Exception as e:
        print(f"Error al manejar el cliente {addr}: {e}")
    finally:
        client_socket.close()

# Obtiene la IP de la interfaz de red
def get_local_ip():
    interfaces = netifaces.interfaces()
    for iface in interfaces:
        addrs = netifaces.ifaddresses(iface)
        if netifaces.AF_INET in addrs:
            ip_info = addrs[netifaces.AF_INET][0]
            if ip_info['addr'] != '127.0.0.1':
                return ip_info['addr']
    return '127.0.0.1'

server_ip = get_local_ip()  # Obtiene la IP local correcta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, 8888))  # Cambiar el puerto aquí si es necesario
server.listen(5)
print(f"[*] Servidor escuchando en {server_ip}:8888")
funciones_principales.GenerarLlavesServidor()

while True:
    client_socket, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()
