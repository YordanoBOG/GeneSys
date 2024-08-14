# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This script contains functions that will be employed by all modules that require any biopython common tool
"""

from Bio import Align
from Bio.Seq import Seq

'''
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
'''

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

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Receives a sequence of DNA bases and checks if they a have a stop codon at the end

Args:
bases (str): sequence of DNA bases.

Returns:
list of three items:
    boolean: True if there is a stop codon at the end of the sequence or the reversed sequence
while there is no other stop codon in the middle of it. False in other case.
    str: the sequence that has been received or the reversed one in case the codon was found in it
    str: information about the execution
"""
def has_valid_stop_codon(bases:str) -> list:
    result = [] # Here we will append a boolean, the sequence of bases and some context of the execution of the function
    result_bool = True
    result_context = f"\n\n----------------------\nChecking for stop codons in the sequence whose last 100 bases are:\n{bases[-100:]}\n" # We show just the last 100 bases of the string to make it more readable
    bases = bases.upper() # We will manipulate the bases in uppercase
    dna_seq = Seq(bases) # Create a Seq object
    
    if len(dna_seq) < 3: # Check if the sequence is at least 3 bases long
        result_bool = False
        result_context += "\nThe sequence is less than 3 characters long. It has no valid codons.\n"

    if result_bool:
        last_codon = str(dna_seq[-3:]) # Check if the last codon is a stop codon
        result_context += f"Sequence's last codon: {last_codon}"
        if not is_stop_codon_dna(last_codon): # If not, reverse the sequence and check the first codon
            result_context += f" -> Not valid stop codon. The string is going to be reversed."
            dna_seq = Seq.reverse_complement(dna_seq) # Reverse the string
            result_context += f"\nReversed sequence's last 100 bases:\n{str(dna_seq)[-100:]}\n"
            if dna_seq: # dna_seq will be False if the sequence is invalid
                last_codon_reversed = str(dna_seq[-3:])
                result_context += f"Reversed sequence's last codon: {last_codon_reversed}"
                if not is_stop_codon_dna(last_codon_reversed): # If still there is no valid stop codon, the string is not a valid one
                    result_context += f" -> Not valid stop codon. The sequence has no valid stop codons.\n"
                    result_bool = False
                else: # The reversed sequence has a valid stop codon
                    result_context += f" -> Valid stop codon.\n"
            else:
                result_context += "\nOh, no. The sequence turned out to not have valid bases.\n"
                result_bool = False
        else:
            result_context += f" -> Valid stop codon.\n"
        
        if result_bool: # If the string is still valid, we check also for stop codons in the middle of the string
            result_context += "\nChecking for stop codons in the middle of the sequence...\n"
            remainder = len(dna_seq)%3
            if remainder != 0: # Trim the sequence by removing its first characters in case it is not a multiple of three
                dna_seq = dna_seq[remainder:]
            for i in range(len(dna_seq)-4, -1, -3): # We skip the last 3 bases which correspond to the stop codon we have already found
                posible_codon = dna_seq[i-2:i+1]
                #print(posible_codon)
                if is_stop_codon_dna(posible_codon):
                    result_context += f"\nThe trio of bases {str(posible_codon)} turned out to be a stop codon. The sequence is not valid\n"
                    result_bool = False
                    break
            if result_bool:
                result_context += "\nThere are no stop codons in the middle of the sequence. The sequence is valid and has a stop codon.\n"

    result.append(result_bool)
    result.append(str(dna_seq)) # It may turn into some cast problems
    result.append(result_context)
    return result

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Checks if a given string of DNA bases is a valid stop codon

Args:
bases (str): sequence of DNA bases.

Returns:
boolean: True if the bases are a stop codon. False in other case
"""
def is_stop_codon_dna(bases) -> bool:
    return ( bases.__eq__("TAA") or
             bases.__eq__("TAG") or
             bases.__eq__("TGA")
           )

'''
###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Checks if a given string of RNA bases is a valid stop codon

Args:
bases (str): sequence of RNA bases.

Returns:
boolean: True if the bases are a stop codon. False in other case
"""
def is_stop_codon_rna(bases) -> bool:
    return ( bases.__eq__("UAG") or
             bases.__eq__("UAA") or
             bases.__eq__("UGA")
           )

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
returns the reverse of a given DNA or RNA string

Args:
sequence: sequence of DNA or RNA bases.

Returns:
string: the reverse string of the given one
"""
def reverse_sequence(sequence):
    comp = [] # List where to save the complementary sequence
    type_of_sequence = verify_type_of_sequence(sequence=sequence)
    if type_of_sequence == "DNA":
        for base in sequence:
            if base == "A":
                comp.append("T")
            elif base == "G":
                comp.append("C")
            elif base == "T":
                comp.append("A")
            elif base == "C":
                comp.append("G")
    elif type_of_sequence == "RNA":
        for base in sequence:
            if base == "U":
                comp.append("A")
            elif base == "G":
                comp.append("C")
            elif base == "A":
                comp.append("U")
            elif base == "C":
                comp.append("G")
    else:
        return False # return False if the string is invalid
       
    #comp_rev = comp[::-1] # reverse the order of the elements of the sequence
    #comp_rev = "".join(comp_rev)  # convert list to string
    #return comp_rev

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Specifies if a string of bases is DNA RNA or invalid

Args:
sequence: sequence of DNA or RNA bases.

Returns:
string: idicating if it is a DNA sequence, RNA sequence or invalid
"""
def verify_type_of_sequence(sequence):
    result = ""
    sequence = sequence.upper()
    seq = set(sequence)    # set the input sequence
     
    # confirm if its elements is equal to 
    # the set of valid DNA bases
    # Use a union method to ensure the
    # sequence is verified if does not
    # contain all the bases
    if seq == {"A", "T", "C", "G"}.union(seq):
        result = "DNA"
    elif seq == {"A", "U", "C", "G"}.union(seq):
        result = "RNA"
    else:
        result = "Invalid sequence"

    return result
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
"""
Receives a sequence of DNA bases and tranforms it into its corresponding amino acid sequence

Args:
sequence (str): sequence of DNA bases.

Returns:
list: a list of all the proteins found in the bases sequence, corresponding each to a protein that have
a stop codon right at the end of it.
"""
def from_bases_to_aminoacid(sequence:str):
    sequence = sequence.upper()
    dna_seq = Seq(sequence)
    protein_seq = dna_seq.translate() # .translate() turns the string of bases into an aminoacid sequence
    unfiltered_protein_list = str(protein_seq).split('*') # The obtained protein sequence has an asterisk * into any position that corresponds to a stop codon
    final_proteins_list = [protein for protein in unfiltered_protein_list if protein] # This line ensures that no empty strings are returned in the output list
    return final_proteins_list


