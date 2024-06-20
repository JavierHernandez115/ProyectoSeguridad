import funciones
import os

mensajelargo='mensajelargo.txt'
clave_aes_path = 'clave_aes'
aes_flie='aes.bin'
def GenerarClaveAes():
    ClaveAes=funciones.generar_clave_aes()
    
    with open(clave_aes_path, 'wb') as key_file:
        key_file.write(ClaveAes)


def GenerarLlavesServidor():
    clavePrivada=funciones.generar_clave_privada_rsa("ClavePrivada_Serv", "123456")
    clavePrivada=funciones.generar_clave_publica_rsa("ClavePrivada_Serv", "ClavePublica_Serv","123456")
    
def GenerarLlavesCliente():
    clavePrivada=funciones.generar_clave_privada_rsa("ClavePrivada_Client", "123456")
    clavePrivada=funciones.generar_clave_publica_rsa("ClavePrivada_Client", "ClavePublica_Client","123456")

def Encriptar(cout, ClavePublica, Stego, is_file=False):
    mensaje=""
    if is_file:
        if  os.path.exists(cout):
            mensaje=cout
    else:
        mensaje="mensaje"
        with open(mensaje, 'w') as f:            
            f.write(cout)

    #Generando el hash_sha384
    hash_sha384=funciones.generar_hash_sha384(mensaje)

    funciones.encriptar_archivo_aes(mensaje,"mensaje.enc",clave_aes_path)

    funciones.encriptar_clave_rsa(clave_aes_path,ClavePublica,aes_flie)
    #Encriptando RSA_Invertido as m

    #Generar hash512
    funciones.generar_hash_sha512("mensaje.enc")

    #Esconder el mensaje
    funciones.esconder_mensaje(Stego,"mensaje.enc","Oculto.wav","15Agosto2003")

    #Generar HashBlake2:
    funciones.generar_hash_blake2("Oculto.wav")

def Desencriptar(ClavePrivada):
    if(funciones.validar_hash_blake2("Oculto.wav","hashb2")):
        #Coincide el hash b2
        print("El hash b2 coincide")

        if(funciones.extraer_archivo("Oculto.wav","15Agosto2003")):
            print("Se extrajo el estegobjeto")

            if(funciones.validar_hash_sha512("mensaje.enc","hash512")):
                print("Hash512 coincide")

                funciones.desencriptar_clave_rsa(aes_flie,ClavePrivada,clave_aes_path)

                funciones.desencriptar_archivo_aes("mensaje.enc","mensaje",clave_aes_path)
                if(funciones.validar_hash_sha384("mensaje","hash384")):
                    print("Los hashes384 Coinciden")
                else:
                    print("Los hashes384 no coinciden")

            else:
                print("hash512 no coincide")
        else:
            print("error al extraer el mensaje del stegobjeto")    
    else:
        #No Coincide el hash b2
        print("El hash b2 no coincide")

#GenerarClaveAes()
#GenerarLlavesServidor()
#Encriptar(mensajelargo,"ClavePublica_Serv","mp4.wav",True)
#Desencriptar("ClavePrivada_Serv")