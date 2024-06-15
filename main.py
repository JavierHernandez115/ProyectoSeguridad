import funciones
#Generacion de claves
clavePrivada=funciones.generar_clave_privada_rsa("ClavePrivada_Con", "15Agosto2003")
clavePrivada=funciones.generar_clave_publica_rsa("ClavePrivada_Con", "ClavePublica_Con","15Agosto2003")

#Hash_sha384 del mensaje o archivo
mensaje="este es un mensaje de prueba"
ArchivoPrueba="mprdeprueba.mp3"
hash_sha384 = funciones.generar_hash_sha384(ArchivoPrueba)
print(f"SHA-384: {hash_sha384}")

#Encriptacion RSA_Invertido
funciones.encriptar_rsa_invertido(ArchivoPrueba,"ClavePublica_Con")


#Desencriptar rsa_invertido
funciones.desencriptar_rsa_invertido("mensaje_encriptado.bin","ClavePrivada_Con")