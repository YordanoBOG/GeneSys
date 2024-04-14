#!/bin/bash

# Obtiene un .fasta para la muestra con BRC ID fig|90371.5175.peg.1275 como prueba

code="90371.5175"
nombre="output.fasta"
#genomeID="fig| ( 90371.5175 ) ESTO ES LO QUE USAS CON "p3-genome-fasta <codigo>" para obtener el .fasta
#$d->set_raw($mode);
#my $triples = $d->fasta_of($genomeID);
echo `p3-genome-fasta --protein $code > $nombre`;