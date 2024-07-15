#!/bin/bash

# Gets the exit of «p3-echo $codigo | p3-get-feature-data --attr aa_sequence» BV-BRC CLI tools command
# Exec example: $./getprotein.sh "fig|90371.5175.peg.1255"

code="$1" # The first argument must be the protein's code

echo `p3-echo $code | p3-get-feature-data --attr aa_sequence`;
