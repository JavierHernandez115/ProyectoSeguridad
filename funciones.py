import subprocess
import secrets
import os
import subprocess
import tempfile

def generar_hash_sha384(input_data):

    comando = f"openssl dgst -sha384 {input_data}"
    print(comando)
    result = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)

    # El resultado de openssl incluye una línea con el hash, como "SHA384(stdin)= <hash>"
    # o "SHA384(<filename>)= <hash>", por lo que tomamos solo la última parte.
    hash_value = result.stdout.split("= ")[1].strip()
    archivo_hash=f"hash384"
    with open(archivo_hash , 'w') as f:
            f.write(hash_value)
    return hash_value


#Encriptar el mensaje con RSA invertido

def encriptar_rsa_invertido(archivo_mensaje, clave_publica_path, archivo_salida):
    comando = f"openssl pkeyutl -encrypt -inkey {clave_publica_path} -pubin -in {archivo_mensaje} -out {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)

# Ejemplo de uso:
# encriptar_rsa_invertido("imagen.jpg", "ClavePublica_Con.pem")

# Ejemplo de uso
#clave_publica_path = 'ruta/a/clave_publica.pem'
#encriptar_rsa_invertido(mensaje, clave_publica_path)

#Generar el HASH sha512
def generar_hash_sha512(file_path):
    print(file_path)
    comando = ['sha512sum', file_path]
    hash_output = subprocess.check_output(comando).split()[0].decode()
    
    archivo_hash="hash512"
    with open(archivo_hash, 'w') as f:
        f.write(hash_output)
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
    archivo_hash="hashb2"
    with open(archivo_hash, 'w') as f:
        f.write(hash_output)
    return hash_output
# Ejemplo de uso
#hash_blake2 = generar_hash_blake2('mensaje_encriptado.bin')
#print(f"Blake2: {hash_blake2}")

#Validar el hash BLake 2 
def validar_hash_blake2(archivo_extraido, hash_blake2_original):
    with open(hash_blake2_original, 'r') as f:
        hash_blake2_original = f.read().strip()
    
    # Calcular el hash BLAKE2 del archivo extraído
    hash_blake2_calculado = generar_hash_blake2(archivo_extraido)
    
    # Comparar ambos hashes
    return hash_blake2_calculado == hash_blake2_original

# Ejemplo de uso
#archivo_stego = 'ruta/remota/a/archivo_salida.png'
#archivo_extraido = 'mensaje_encriptado_extraido.bin'
#password = 'contraseña_secreta'
#hash_blake2_original = 'hash_blake2_original'

#Validar HAsh SHA-512
def validar_hash_sha512(file_path, hash_original):
    with open(hash_original, 'r')as f:
        hash_original=f.read().strip()

    hash_calculado = generar_hash_sha512(file_path)
    return hash_calculado == hash_original

# Ejemplo de uso
#if validar_hash_sha512('mensaje_encriptado_extraido.bin', hash_sha512):
    #print("Hash SHA-512 válido.")
#else:
    #print("Error: Hash SHA-512 no válido.")

#Desencriptar el mensaje usando la clave privada
def desencriptar_rsa(archivo_mensaje_encriptado, clave_privada_path, archivo_salida):
    comando = f"openssl pkeyutl -decrypt -inkey {clave_privada_path} -in {archivo_mensaje_encriptado} -out {archivo_salida}"
    subprocess.run(comando, shell=True, check=True)


# Ejemplo de uso
#clave_privada_path = 'ruta/a/clave_privada.pem'
#mensaje_desencriptado = desencriptar_rsa_invertido('mensaje_encriptado_extraido.bin', clave_privada_path)

#Validar el hash sha-384
def validar_hash_sha384(mensaje, hash_original):
    with open(hash_original, 'r')as f:
        hash_original=f.read().strip()

    return generar_hash_sha384(mensaje) == hash_original

#Extraer StegoObjeto

def extraer_archivo(archivo_stego, password):
    # Crear el comando steghide para extraer el archivo oculto
    comando = f"steghide extract -sf {archivo_stego} -p {password}"
    
    # Ejecutar el comando usando subprocess
    resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if resultado.returncode == 0:
        # Eliminar el archivo esteganográfico
        #os.remove(archivo_stego)
        return True
    else:
        print(f"Error al extraer el archivo oculto: {resultado.stderr.decode()}")
        return False

# Ejemplo de uso
#if validar_hash_sha384(mensaje_desencriptado, hash_sha384):
    #print("El mensaje no ha sido alterado. Está listo.")
#else:
    #print("Error: El mensaje ha sido alterado.")Desencriptar rsa_invertido
#funciones.desencriptar_rsa("mensaje.enc","ClavePrivada_Con","mensaje.


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

def generar_clave_aes(longitud=32):
    return secrets.token_bytes(longitud)

def encriptar_archivo_aes(archivo_entrada, archivo_salida, clave_aes_path):
    comando = f"openssl enc -aes-256-cbc -salt -in {archivo_entrada} -out {archivo_salida} -pass file:{clave_aes_path}"
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"Archivo '{archivo_entrada}' encriptado exitosamente como '{archivo_salida}'")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la encriptación: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")
    clave_aes_path = 'clave_aes.bin'

def encriptar_clave_rsa(clave_aes_path, clave_publica_path, archivo_salida):
    comando = f"openssl pkeyutl -encrypt -inkey {clave_publica_path} -pubin -in {clave_aes_path} -out {archivo_salida}"
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"Clave AES encriptada exitosamente como '{archivo_salida}'")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la encriptación: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def desencriptar_clave_rsa(archivo_clave_encriptada, clave_privada_path, archivo_clave_aes):
    comando = f"openssl pkeyutl -decrypt -inkey {clave_privada_path} -in {archivo_clave_encriptada} -out {archivo_clave_aes}"
    try:
        subprocess.run(comando, shell=True, check=True)
        with open(archivo_clave_aes, 'rb') as key_file:
            clave_aes = key_file.read()
        print("Clave AES desencriptada exitosamente")
        return clave_aes
    except subprocess.CalledProcessError as e:
        print(f"Error durante la desencriptación: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

def desencriptar_archivo_aes(archivo_encriptado, archivo_salida, clave_aes_path):
    comando = f"openssl enc -d -aes-256-cbc -in {archivo_encriptado} -out {archivo_salida} -pass file:{clave_aes_path}"
    try:
        subprocess.run(comando, shell=True, check=True)
        print(f"Archivo '{archivo_encriptado}' desencriptado exitosamente como '{archivo_salida}'")
    except subprocess.CalledProcessError as e:
        print(f"Error durante la desencriptación: {e}")
    except Exception as e:
        print(f"Ocurrió un error: {e}")

