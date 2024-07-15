#!/bin/bash

# Gets the exit of the necessary BV-BRC CLI tools commands in order to get 30Kbases posi
# Exec example: $./get_30kilobases_up_and_down.sh "fig|90371.5175.peg.1255"
# Exec example: $./get_30kilobases_up_and_down.sh "MNRQPLPIIWQRIIFDPLSYIHPQRLQIAPEMIVRPAARAAANELILAAWRLKNGEKECIQNSLTQLWLRQWRRLPQVAYLLGCHKLRADLARQGALLGLPDWAQAFLAMHQGTSLSVCNKAPNHRFLLSVGYAQLNALNEFLPESLAQRFPLLFPPFIEEALKQDAVEMSILLLALQYAQKYPNTVPAFAC"

code="$1" # The first argument must be the protein's code

p3-get-feature-data --attr aa_sequence --type CDS > cds_sequence.fasta # La clave está en el CDS
#get-feature-dna-sequence --id BRC_ID --type CDS > cds_sequence.fasta
#protein_sequence=`p3-echo -t genome_id $code | p3-get-genome-features --eq feature_type,CDS # | p3-get-feature-data --attr aa_sequence`
#p3-get-feature-regions "$code" > "protein.fasta"
#protein_sequence=`p3-all-genomes --eq "Chromobacterium vaccinii strain CR5, SLATT domain-containing protein"`
#echo $protein_sequence

#p3-get-sequence --type protein --id $code --fasta > protein_sequence.fasta
#echo `p3-get-sequence --type protein --id $code --fasta`

#`p3-echo $code | p3-get-feature-data --attr aa_sequence`;
