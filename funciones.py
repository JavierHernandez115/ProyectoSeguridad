import subprocess
import os
#Generar el HASH en SHA-384 del mensaje
def generar_hash_sha384(input_data):
    if os.path.isfile(input_data):
        file_path = input_data
        with open(file_path, 'rb') as f:
            mensaje = f.read()
    else:
        # Si es un texto, lo escribe a un archivo permanente
        file_path = 'mensaje.txt'
        with open(file_path, 'wb') as f:
            f.write(input_data.encode() if isinstance(input_data, str) else input_data)
        with open(file_path, 'rb') as f:
            mensaje = f.read()
    sha384_path = "hash384.txt"

    # Genera el hash usando sha384sum
    proceso = subprocess.Popen(['sha384sum'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    hash_output, _ = proceso.communicate(input=mensaje)

    with open(sha384_path, 'wb') as f:  
        f.write(hash_output.split()[0]) 
    return hash_output.split()[0].decode(), file_path
# Ejemplo de uso
#hash_sha384 = generar_hash_sha384(mensaje)
#print(f"SHA-384: {hash_sha384}")

#Encriptar el mensaje con RSA invertido

def encriptar_rsa_invertido(archivo_mensaje, clave_publica_path, archivo_salida):
    comando = f"openssl pkeyutl  -encrypt -inkey {clave_publica_path} -pubin -in {archivo_mensaje} -out {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)


# Ejemplo de uso
#clave_publica_path = 'ruta/a/clave_publica.pem'
#encriptar_rsa_invertido(mensaje, clave_publica_path)

#Generar el HASH sha512
def generar_hash_sha512(file_path):
    comando = ['sha512sum', file_path]
    hash_output = subprocess.check_output(comando).split()[0].decode()
    return hash_output
# Ejemplo de uso
#hash_sha512 = generar_hash_sha512('mensaje_encriptado.bin')
#print(f"SHA-512: {hash_sha512}")

#Esteganografia
def esconder_mensaje(archivo_cover, archivo_mensaje, archivo_salida, password):
    comando = f"steghide embed -cf {archivo_cover} -ef {archivo_mensaje} -sf {archivo_salida} -p {password}"
    subprocess.run(comando, shell=True)

    # Ejemplo de uso
#archivo_cover = 'ruta/a/archivo_cover.png'
#archivo_mensaje = 'mensaje_encriptado.bin'
#archivo_salida = 'ruta/a/archivo_salida.png'
#password = 'contraseña_secreta'
#esconder_mensaje(archivo_cover, archivo_mensaje, archivo_salida, password)

#Generar el HASH Blake2
def generar_hash_blake2(file_path):
    comando = ['b2sum', file_path]
    hash_output = subprocess.check_output(comando).split()[0].decode()
    return hash_output
# Ejemplo de uso
#hash_blake2 = generar_hash_blake2('mensaje_encriptado.bin')
#print(f"Blake2: {hash_blake2}")

#Validar el hash BLake 2 
def validar_hash_blake2(archivo_extraido, hash_blake2_original):
    hash_blake2_calculado = generar_hash_blake2(archivo_extraido)
    return hash_blake2_calculado == hash_blake2_original

# Ejemplo de uso
#archivo_stego = 'ruta/remota/a/archivo_salida.png'
#archivo_extraido = 'mensaje_encriptado_extraido.bin'
#password = 'contraseña_secreta'
#hash_blake2_original = 'hash_blake2_original'

#Validar HAsh SHA-512
def validar_hash_sha512(file_path, hash_original):
    hash_calculado = generar_hash_sha512(file_path)
    return hash_calculado == hash_original

# Ejemplo de uso
#if validar_hash_sha512('mensaje_encriptado_extraido.bin', hash_sha512):
    #print("Hash SHA-512 válido.")
#else:
    #print("Error: Hash SHA-512 no válido.")

#Desencriptar el mensaje usando la clave privada
def desencriptar_rsa(archivo_mensaje_encriptado, clave_privada_path, archivo_salida):
    comando = f"openssl rsautl -decrypt -inkey {clave_privada_path} -in {archivo_mensaje_encriptado} -out {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)

# Ejemplo de uso
#clave_privada_path = 'ruta/a/clave_privada.pem'
#mensaje_desencriptado = desencriptar_rsa_invertido('mensaje_encriptado_extraido.bin', clave_privada_path)

#Validar el hash sha-384
def validar_hash_sha384(mensaje, hash_original):
    return generar_hash_sha384(mensaje) == hash_original

# Ejemplo de uso
#if validar_hash_sha384(mensaje_desencriptado, hash_sha384):
    #print("El mensaje no ha sido alterado. Está listo.")
#else:
    #print("Error: El mensaje ha sido alterado.")


#Generar Llaves
def generar_clave_privada_rsa(nombre_archivo, password):
    comando_privada = f"openssl genpkey -algorithm RSA -out {nombre_archivo} -aes256 -pass pass:{password}"
    subprocess.run(comando_privada, shell=True)
    print(f"Clave privada generada y guardada en '{nombre_archivo}'.")

# Generar clave pública RSA
def generar_clave_publica_rsa(nombre_archivo_privada, nombre_archivo_publica, password):
    comando_publica = f"openssl rsa -pubout -in {nombre_archivo_privada} -out {nombre_archivo_publica} -passin pass:{password}"
    subprocess.run(comando_publica, shell=True)
    print(f"Clave pública generada y guardada en '{nombre_archivo_publica}'.")

