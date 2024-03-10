from Bio import Blast

# Blast.tool = 'biopython' # Already biopython by default
Blast.email = 'bruogal@gmail.com' # They will report you via this email in case there were any problems

fasta_sequence = open('blast_practice_data/new_species.fasta').read()
result_stream = Blast.qblast("blastn", "nt", fasta_sequence) # Using Blastn to compare a nucleotide sequence against the official nucleotide (nt) database

# DON'T execute. The resulting stream still requires management.