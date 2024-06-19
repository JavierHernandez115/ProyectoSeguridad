import socket

# Configuración del cliente
server_ip = input("Ingresa la dirección IP del servidor: ")
server_port = 8888  # Cambiar el puerto aquí si es necesario

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server_ip, server_port))
except socket.error as e:
    print(f"Error al conectar con el servidor: {e}")
    exit()

while True:
    # Pedir mensaje al usuario
    msg = input("Escribe un mensaje: ")

    # Guardar mensaje en un archivo
    with open("mensaje_cliente.txt", 'w') as file:
        file.write(msg)
    
    # Enviar archivo al servidor
    with open("mensaje_cliente.txt", 'rb') as file:
        while True:
            part = file.read(1024)
            if not part:
                break
            client.sendall(part)

    # Recibir el archivo del servidor
    file_data = b''
    while True:
        part = client.recv(1024)
        if not part:
            break
        file_data += part
    
    with open("respuesta_servidor.txt", 'wb') as file:
        file.write(file_data)
    
    # Leer y mostrar el mensaje de respuesta del servidor
    with open("respuesta_servidor.txt", 'r') as file:
        response_msg = file.read()
        print(f"Respuesta del servidor: {response_msg}")
