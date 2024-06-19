import socket

# Configuración del cliente
server_ip = input("Ingresa la dirección IP del servidor: ")
server_port = 9999

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((server_ip, server_port))

while True:
    # Pedir mensaje al usuario
    msg = input("Escribe un mensaje: ")

    # Guardar mensaje en un archivo
    with open("mensaje_cliente.txt", 'w') as file:
        file.write(msg)
    
    # Enviar archivo al servidor
    with open("mensaje_cliente.txt", 'rb') as file:
        client.sendall(file.read())

    # Recibir el archivo del servidor
    file_data = client.recv(1024)
    with open("respuesta_servidor.txt", 'wb') as file:
        file.write(file_data)
    
    print("[*] Archivo recibido del servidor y guardado como 'respuesta_servidor.txt'")
