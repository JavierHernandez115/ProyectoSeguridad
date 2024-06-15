import subprocess

def check_command(command):
    try:
        # Ejecuta el comando `which` para verificar si el comando está disponible
        result = subprocess.run(['which', command], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            print(f"El comando '{command}' está instalado en: {result.stdout.decode().strip()}")
        else:
            print(f"El comando '{command}' no está instalado.")
    except Exception as e:
        print(f"Ha ocurrido un error al verificar el comando '{command}': {e}")

# Lista de comandos a verificar
comandos = ['python3', 'git', 'curl', 'docker','steghide','b2sum']

for comando in comandos:
    check_command(comando)
