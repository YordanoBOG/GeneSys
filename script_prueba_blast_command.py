import subprocess

base_datos = input("Introduce BLAST database path: ") # ../db/new_species
cadena_a_comparar = input("Introduce BLAST string path with which compare previous input: ") # blast_practice_data/queries/mismatch.fasta
doc_resultado = input("Introduce result document path (result.txt by default): ") or 'result.txt'
comando = "blastn -db " + base_datos + " -query " + cadena_a_comparar + " > " + doc_resultado

resultado = subprocess.run(comando, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

#'''
# Muestra la salida del comando
print("Salida del comando:")
print(resultado.stdout)

# Muestra los errores, si los hay
print("Errores (si los hay):")
print(resultado.stderr)
#'''