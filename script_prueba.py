import subprocess

comando = "ls -l"

resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#'''
# Muestra la salida del comando
print("Salida del comando:")
print(resultado.stdout)

# Muestra los errores, si los hay
print("Errores (si los hay):")
print(resultado.stderr)
#'''