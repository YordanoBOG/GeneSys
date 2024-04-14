#!/bin/bash

# Obtiene un archivo con la salida de la orden «p3-echo $codigo | p3-get-feature-data --attr aa_sequence > $file» de BV-BRC CLI
# Exec example: $./getprotein.sh fig|90371.5175.peg.1275 output_protein_90371.5175.txt

echo $1;

code=$1 # The first argument must be protein's code
file=$2 # Second argument must be file's name

echo `p3-echo $code | p3-get-feature-data --attr aa_sequence > $file`;
