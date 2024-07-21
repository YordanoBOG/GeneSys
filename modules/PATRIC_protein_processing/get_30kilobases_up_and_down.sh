#!/bin/bash

# Gets 30k bases up and down from a given BV-BRC ID using BV-BRC command line tool.
# It returns a DNA sequence, not an aminoacid sequence, and accepts all the codes
# from which get the parameters' bases given to the script. Stores the result
# in a fasta file because the output of the BV-BRC
# applied command returns the sequence using such format.

# Exec example: $./get_30kilobases_up_and_down.sh "fig|1108595.43.peg.4364" "fig|110937.20.peg.4387" "fig|1124743.5.peg.1997" "fig|1134687.838.peg.7253" "fig|1144547.3.peg.5220"

echo > ./feature_regions.fasta; # Clean fasta results file's content
for code in "$@"
do
    echo
    echo `p3-echo $code | p3-get-feature-regions --distance 30000 >> ./feature_regions.fasta`
    echo >> ./feature_regions.fasta; # Add one blank space between entries
done

