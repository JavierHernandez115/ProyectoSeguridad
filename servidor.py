import socket
import threading

# Función para manejar la conexión con el cliente
def handle_client(client_socket, addr):
    print(f"[+] Conexión aceptada de {addr}")
    while True:
        # Recibe el archivo del cliente
        file_data = client_socket.recv(1024)
        if not file_data:
            break

        # Guarda el archivo recibido
        with open(f"mensaje_recibido_{addr[1]}.txt", 'wb') as file:
            file.write(file_data)
        
        # Enviar respuesta al cliente
        response_msg = "Mensaje recibido correctamente"
        with open(f"mensaje_respuesta_{addr[1]}.txt", 'w') as file:
            file.write(response_msg)

        with open(f"mensaje_respuesta_{addr[1]}.txt", 'rb') as file:
            client_socket.sendall(file.read())
        
    client_socket.close()

# Configuración del servidor
server_ip = socket.gethostbyname(socket.gethostname())  # Obtiene la IP de la máquina donde se ejecuta
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((server_ip, 9999))
server.listen(5)
print(f"[*] Servidor escuchando en {server_ip}:9999")

while True:
    client_socket, addr = server.accept()
    client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
    client_handler.start()
