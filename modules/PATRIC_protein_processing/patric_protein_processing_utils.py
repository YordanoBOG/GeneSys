# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file contains some functions that are employed by
more than one Task from the Patric Protein Processing
GeneSys module

WHAT if you move this functions to a class that inherits from Task
and make all the PATRIC processing classes as an inheritance from that
first class?
"""


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This function receives a protein string, its correspond BVRC ID code and
# an openned file in which that protein would be stored in fasta format.
# It returns an explanation message
def save_fasta_string(string, identifier, fasta_file):
    result = f"\nProtein still not processed\n"
    try: 
        # Write the identifier line
        identifier_line = ">" + identifier + "\n"
        fasta_file.write(identifier_line)

        # Write the aminoacid sequence. We write the sequence in lines of a maximum of 80 characters in order to follow the .fasta structure standard
        protein_lines = split_fasta_sequence(string)
        for line in protein_lines:
            line += "\n"
            fasta_file.write(line) # According to .fasta structure, each line of a fasta file always should have 80 characters or less 
        fasta_file.write("\n") # Write the last line jump
        result = f"\nProtein <{string}> with code <{identifier}> WAS SAVED succesfully\n"
    except Exception as e:
        result = f"\nError while writing the protein in a .fasta file: {e}\n"
    return result


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# Returns a vector that contains a sequence splitted in lines of 80 characters or less
def split_fasta_sequence(sequence) -> list:
    result_sequences = [] # We declare a void vector
    for i in range(0, len(sequence), 80): # Iterate over the sequence splitting it in strings of a maximum of 80 characters
        result_sequences.append(sequence[i:i+80])
    return result_sequences


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# Reads a .fasta file and returns its corresponding contained strings in a dictionary
def get_fasta_content(fasta_path):
    try:
        proteins = {}
        fasta_file = open(fasta_path, 'r') # Open input file for reading
        current_sequence_id = None # Here we will store the identifier line of a protein
        current_sequence = [] # Here we will store all the aminoacid lines corresponding to a same protein

        for line in fasta_file:
            line = line.strip() # strip removes the final newline character of the line, it is equivalent to line.replace('\n','')
            if line.startswith(">"): # If the first character of the line is ">", then we are in a identifier line
                if current_sequence_id is not None: # If this is true, it will mean that we have an already saved identifier
                                                    # from a previous readed protein, so we save that protein in the proteins
                                                    # dictionary before reading a new one
                    proteins[current_sequence_id] = ''.join(current_sequence) # Join the sequence by '', which is the character that we have put at the end of each line instead of '\n' by calling to strip() function
                current_sequence_id = line[1:] # The dictionary key for the new sequence will be the identifier line without the first character ">", correponding to the BVRC PATRIC code of the protein
                current_sequence = [] # clean the sequence that we are currently reading
            else: # We are not in an identifier line
                current_sequence.append(line)
        
        proteins[current_sequence_id] = ''.join(current_sequence) # process the final readen entry
        return True, proteins
    except Exception as e:
        return False, e



'''
###############################################################################
###############################################################################
###############################################################################
###############################################################################
# Reads a given path to a Newick file that contains BRC identifiers and returns a list of the proteins contained
# in the file while maintaining the order from the Newick file, or False
def get_newick_codes(newick_pathname):
    result = False
    with open(newick_pathname, 'r') as file:
        newick_content = file.read()

    if newick_content:
        # Extract protein codes using a simple parser
        # The parser will consider anything that matches the 'fig|2480626.3.peg.3140' pattern as a protein code
        protein_codes = []
        current_code = []
        recording = False # True if we are currently reading a protein code
        
        for char in newick_content:
            if recording: 
                if char.isalnum() or char in ".|":
                    current_code.append(char)
                else:
                    protein_codes.append(''.join(current_code)) # We just finished reading a protein, so we join it and add it to the proteins list
                    current_code = []
                    recording = False
            
            if char == '|':
                if len(current_code) > 0 and current_code[-1] == 'g':
                    recording = True
                current_code.append(char)
        
        # Ensure the last protein code is added
        if recording:
            protein_codes.append(''.join(current_code))
        
        result = protein_codes
    return result'''

    
