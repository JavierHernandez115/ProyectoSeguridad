import socket
import funciones_principales
import os

# Configuración del cliente
server_ip = input("Ingresa la dirección IP del servidor: ")
server_port = 8888  # Cambiar el puerto aquí si es necesario

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect((server_ip, server_port))
    print("Conexión exitosa con el servidor")
except socket.error as e:
    print(f"Error al conectar con el servidor: {e}")
    exit()

# Generar llaves del cliente
funciones_principales.GenerarLlavesCliente()

# Enviar archivo ClavePublica_Client al servidor
with open("ClavePublica_Client", 'rb') as file:
    data = file.read()
    client.sendall(data)
    client.sendall(b'<<END>>')  # Enviar marcador de finalización

# Recibir el archivo ClavePublica_Serv del servidor
with open("ClavePublica_Serv", 'wb') as file:
    while True:
        file_data = client.recv(1024)
        if b'<<END>>' in file_data:
            file.write(file_data.replace(b'<<END>>', b''))
            break
        file.write(file_data)

print("Archivo ClavePublica_Serv recibido y guardado.")

while True:
    # Pedir mensaje al usuario
    msg = input("Escribe un mensaje: ")

    # Guardar mensaje en un archivo
    with open("mensaje_cliente.txt", 'w') as file:
        file.write(msg)
    
    # Encriptar mensaje
    funciones_principales.Encriptar('mensaje_cliente.txt', 'ClavePublica_Serv', 'Oculto.wav', is_file=True)

    # Enviar archivos encriptados al servidor
    for filename in ['Oculto.jpeg', 'hash384', 'hash512', 'hashb2']:
        with open(filename, 'rb') as file:
            data = file.read()
            client.sendall(data)
            client.sendall(b'<<END>>')  # Enviar marcador de finalización
        os.remove(filename)  # Eliminar archivo después de enviarlo

    # Recibir los archivos del servidor
    for filename in ['Oculto_respuesta.jpeg', 'hash384_respuesta', 'hash512_respuesta', 'hashb2_respuesta']:
        with open(filename, 'wb') as file:
            while True:
                file_data = client.recv(1024)
                if b'<<END>>' in file_data:
                    file.write(file_data.replace(b'<<END>>', b''))
                    break
                file.write(file_data)

    # Aquí puedes agregar código para desencriptar Oculto_respuesta.jpeg si es necesario
    print("Archivos de respuesta recibidos y guardados.")
