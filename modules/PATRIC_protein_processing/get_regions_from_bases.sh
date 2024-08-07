#!/bin/bash

# Gets all the regions contained in a genome given all its bases

# Exec example: $./get_regions_from_bases.sh

#echo > ./proteins_from_regions.fasta; # Clean fasta results file's content
#bases="$1"; # $1
#echo `p3-echo $1 | p3-get-features-by-sequence > ./proteins_from_regions.txt`;
#p3-get-features-by-sequence --nohead --dna --input ./feature_regions.fasta > ./proteins_from_regions.txt;

#echo `p3-echo "d41d8cd98f00b204e9800998ecf8427e" | p3-find-features --attr patric_id --debug --eq aa_sequence_md5 > ./my_features.txt`;

#echo `p3-echo $1 | p3-get-genome-features --attr patric_id > ./my_features.txt`;
#echo `p3-echo $1 | p3-genome-md5 > ./my_features.txt`;
#echo `p3-echo d41d8cd98f00b204e9800998ecf8427e | p3-get-genome-features --attr patric_id --attr aa_sequence > ./my_features.txt`;
echo `p3-all-genomes --eq genome_id,1108595.43 | p3-get-genome-features --attr patric_id --attr aa_sequence > ./my_features.txt`;
#proteina="MSENKYTPPQTPEELVLTWIKRVRESQFSHHHCVEFYKVVHFAIGVPATILTAIVGTSIFKVATSSPNSSPSYLIISLSILAAILSGLQTFLNVQAKINAHKIAADKFSEIRRDLEEAYATSQINATLISAAKTKYNNATQNAPDVSSSVFSKITTILYKSPQ";
#echo `p3-echo 1108595.43 | p3-get-genome-features --attr patric_id --attr aa_sequence --le aa_sequence,$proteina > ./my_features.txt`;
# echo `p3-echo <genome_id> | p3-get-genome-features --attr patric_id --attr aa_sequence --le aa_sequence,<proteina_actual_que_intentamos_verificar_si_es_una_region_valida_o_no> > ./my_features.txt`;
# Se pueden obtener las features de un determinado fig|[1108595.43 -> esta parte].peg.4364 correspondiente al genome_id sobre el que se puede ejecutar
# p3-get-genome-features que devuelve estos campos:
aa_length
aa_sequence (related)
aa_sequence_md5
accession
alt_locus_tag
annotation
brc_id
classifier_round
classifier_score
codon_start
date_inserted
date_modified
ec (derived) (multi)
end
feature_id
feature_type
figfam_id
function (derived)
gene
gene_id
genome_id
genome_name
go (multi)
location
na_length
na_sequence (related)
na_sequence_md5
notes (multi)
og_id
owner
p2_feature_id
pathway (related) (multi)
patric_id
pdb_accession (multi)
pgfam_id
plfam_id
product
property (multi)
protein_id
public
refseq_locus_tag
segments (multi)
sequence_id
sog_id
start
strand
subsystem (related) (multi)
taxon_id
text (multi)
uniprotkb_accession
user_read (multi)
user_write (multi)
# aa_sequence es una cadena de aminoácidos que puede buscarse dentro de las 60k
# bases aisladas y, en caso de que se encuentre dentro, tomar esa proteína y su código
# como una región del genoma que estamos analizando.
# Esto significa que vas a tener que pasar los 60k genes a proteína para poder hacer la comparación.

# Y puestos a pasar los genes a proteínas, puedes mejor
# aprovechar las opciones del comando <p3-get-genome-features>:
--attr STR... (or -a)      field(s) to return
--count (or -K)            if specified, a count of records returned
                            will be displayed instead of the records
                            themselves
--equal STR... (or -e)     search constraint(s) in the form
                            field_name,value
                            aka --eq
--lt STR...                less-than search constraint(s) in the form
                            field_name,value
--le STR...                less-or-equal search constraint(s) in the
                            form field_name,value
--gt STR...                greater-than search constraint(s) in the
                            form field_name,value
--ge STR...                greater-or-equal search constraint(s) in
                            the form field_name,value
--ne STR...                not-equal search constraint(s) in the form
                            field_name,value
--in STR...                any-value search constraint(s) in the form
                            field_name,value1,value2,...,valueN
--keyword STR              if specified, a keyword or phrase that
                            shoould be in at least one field of every
                            record
--required STR... (or -r)  field(s) required to have values
--debug                    display debugging on STDERR
--delim STR                delimiter to place between object names
--col STR (or -c)          column number (1-based) or name
--batchSize INT (or -b)    input batch size
--nohead                   file has no headers
--input STR (or -i)        name of the input file (if not the
                            standard input)
--fields (or -f)           Show available fields
--selective                Use batch query (only for small number of
                            features per genome)
--help (or -h)             display usage information
# que, entre otras cosas, te permite buscar regiones usando limitaciones (constraints)
# sobre el campo aa_sequence, de manera que busques regiones solo en las proteínas que le pases
# en especificando --le (buscar regiones menores o iguales a <campo>,<valor_campo>, en este caso
# aa_sequence,<gen original pasado a proteínas>)

# No sé si funcionaría, pero en cualquier caso, creo que no te hará falta usar p3-all-genomes
#para disponer del código sobre el que buscar las regiones
