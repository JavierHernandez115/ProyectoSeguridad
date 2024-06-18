import funciones
import os


#Generacion de claves
#clavePrivada=funciones.generar_clave_privada_rsa("ClavePrivada_Con", "15Agosto2003")
#clavePrivada=funciones.generar_clave_publica_rsa("ClavePrivada_Con", "ClavePublica_Con","15Agosto2003")


mensaje="este es un mensaje de prueba"
archivo="imagen.jpeg"



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

    #Encriptando RSA_Invertido
    funciones.encriptar_rsa_invertido(mensaje,ClavePublica,"mensaje.enc")

    #Generar hash512
    funciones.generar_hash_sha512("mensaje.enc")

    #Esconder el mensaje
    funciones.esconder_mensaje(Stego,"mensaje.enc","Oculto.jpeg","15Agosto2003")

    #Generar HashBlake2:
    funciones.generar_hash_blake2("Oculto.jpeg")

def Desencriptar():
    if(funciones.validar_hash_blake2("Oculto.jpeg","hashb2")):
        #Coincide el hash b2
        print("El hash b2 coincide")

        if(funciones.extraer_archivo("Oculto.jpeg","15Agosto2003")):
            print("Se extrajo el estegobjeto")

            if(funciones.validar_hash_sha512("mensaje.enc","hash512")):
                print("Hash512 coincide")

                funciones.desencriptar_rsa("mensaje.enc","ClavePrivada_Con","mensaje.mp3")
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


#Encriptar("prueba.mp3","ClavePublica_Con","imagen.jpeg",True)
Desencriptar()


