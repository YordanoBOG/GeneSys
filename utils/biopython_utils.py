# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This script contains functions that will be employed by all modules that require any biopython common tool
"""

from Bio import Align


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# Returns E-value between two proteins given a default K and lambda parameters
def calculate_e_value(protein_one, protein_two, K=0.1, lambda_=0.267):
    aligner = Align.PairwiseAligner() # Create an aligner object
    aligner.mode = 'local'
    alignments = aligner.align(protein_one, protein_two) # Perform local alignment
    best_alignment = alignments[0] # Extract the best alignment
    score = best_alignment.score

    # For e-value calculation, we generally need to perform database search and use statistical models.
    # Here, we assume that we have a large enough database and statistical model parameters.
    # We apply a empirical method to estimate e-value based on score
    # These constants would normally be derived from the database and scoring system
    m = len(protein_one)
    n = len(protein_two)
    e_value = K * m * n * (2.718 ** (-lambda_ * score)) # Calculate e-value

    message = "Best Alignment Score: " + score + "\n" + "E-value: " + e_value + "\n" + "Alignment: " + best_alignment
    print(message)

    return e_value


###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Calculate the percentage of similarity between two protein sequences.

Args:
protein1 (str): First protein sequence.
protein2 (str): Second protein sequence.

Returns:
float: Percentage of similarity between the two protein sequences.
"""
def get_coincidence_percentage(protein_one, protein_two):
    aligner = Align.PairwiseAligner() # Create an aligner object
    aligner.mode = 'local'
    alignments = aligner.align(protein_one, protein_two) # Perform local alignment
    best_alignment = alignments[0] # Extract the best alignment
    
    # Calculate the number of matches
    aligned_seq1 = best_alignment.aligned[0]
    aligned_seq2 = best_alignment.aligned[1]
    
    matches = 0
    for (start1, end1), (start2, end2) in zip(aligned_seq1, aligned_seq2):
        matches += sum(1 for a, b in zip(protein_one[start1:end1], protein_two[start2:end2]) if a == b)
    
    # Calculate the similarity percentage
    total_length = min(len(protein_one), len(protein_two))
    similarity_percentage = (matches / total_length) * 100
    
    return similarity_percentage

