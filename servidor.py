import socket
import threading
import netifaces

# Función para manejar la conexión con el cliente
def handle_client(client_socket, addr):
    print(f"[+] Conexión aceptada de {addr}")
    while True:
        try:
            # Recibe el archivo del cliente
            file_data = client_socket.recv(1024)
            if not file_data:
                break

            # Guarda el archivo recibido
            with open(f"mensaje_recibido_{addr[1]}.txt", 'wb') as file:
                file.write(file_data)
            
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
                while True:
                    part = file.read(1024)
                    if not part:
                        break
                    client_socket.sendall(part)
        except Exception as e:
            print(f"Error al manejar el cliente {addr}: {e}")
            break
        
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

while True:
    client_socket, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()
