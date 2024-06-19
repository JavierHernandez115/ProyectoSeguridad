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
        client.sendall(file.read())

    # Recibir el archivo del servidor
    file_data = client.recv(1024)
    with open("respuesta_servidor.txt", 'wb') as file:
        file.write(file_data)
    
    # Leer y mostrar el mensaje de respuesta del servidor
    with open("respuesta_servidor.txt", 'r') as file:
        response_msg = file.read()
        print(f"Respuesta del servidor: {response_msg}")
