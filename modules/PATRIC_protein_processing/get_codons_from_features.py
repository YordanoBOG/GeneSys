# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file implements a GeneSys task that reads a fasta file
that refer to proteins that surround baits and recognizes all the proteins
asociated to each bait. It generates an EXCEL file with the baits and its
corresponding proteins
"""

#import json
import pandas as pd

from modules.baseobjects import Task
from utils.fasta_processing_utils import get_fasta_content
from utils.biopython_utils import has_valid_stop_codon, from_bases_to_aminoacid

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class GetCodonsFromFeatures(Task):

    __pathname_to_feature_proteins = ""
    __pathname_to_excel_results = ""

    ###### INIT ######

    def __init__(self, pathname_to_feature_proteins = "./feature_regions.fasta",
                 pathname_to_excel_results = "./check_stop_codons.xlsx"):
        super().__init__()
        self.__pathname_to_feature_proteins = pathname_to_feature_proteins
        self.__pathname_to_excel_results = pathname_to_excel_results
    
    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['pathname_to_feature_proteins'] = self.__pathname_to_feature_proteins
        parameters['pathname_to_excel_results'] = self.__pathname_to_excel_results
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__pathname_to_feature_proteins = parameters['pathname_to_feature_proteins']
        self.__pathname_to_excel_results = parameters['pathname_to_excel_results']
    
    # There is a value that we do not want to show when we get this task as a string
    def show_info(self):
        gen_fasta_dict = self.to_dict()
        gen_fasta_dict.pop('returned_info') # We remove returned info from __str__method as it is too long to be worth to be showed
        gen_fasta_dict.pop('returned_value')
        return str(gen_fasta_dict)
    
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self._returned_value = -1
        self._returned_info = ""
        self.__get_codons()

    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commands in order to get the protein string and save it in as a new fasta file
    def __get_codons(self):
        read_features_result = get_fasta_content(self.__pathname_to_feature_proteins) # Returns a tuple
        if read_features_result[0]: # If the first value of the tuple is True, it means the funtion "get_fasta_content" was succesful
            codons_dict = self.__recognize_stop_codons(read_features_result[1]) # Isolate codons of each bait
            self.__save_results(codons_dict) # Save found codons
            self._returned_info += "\n\nTask done\n\n"
            self._returned_value = 0
        else:
            self._returned_info += "Error while trying to read the features: " + str(read_features_result[1])
            self._returned_value = 1

    # Takes the readen dictionary of baits with all the bases that surround each and transforms the bases
    # of a given bait into a list of valid codons, and returns the modified dictionary
    def __recognize_stop_codons(self, baits_and_bases:dict):
        baits_and_codons = {} # We will return this dictionary
        for bait_id, bases in baits_and_bases.items(): # "bait_id" are keys and "bases" are the corresponding values of the dictionary
            self._returned_info += f"\n\n################\n################\n################\nAnalyzing set of nucleotides whose bait protein is {bait_id}...\n"
            codons_list = self.__divide_by_stop_codons(bases)
            if codons_list: # If the list of features separated by stop codons is not empty
                baits_and_codons[bait_id] = codons_list # Add the features separated by codons and the bait to the new dictionary
            else:
                self._returned_info += "There were no valid proteins related to the bait.\n"
        return baits_and_codons
    
    # Takes a string of bases and transforms each found codon into a protein, and returns all the proteins as a list
    def __divide_by_stop_codons(self, bases:str):
        # Recognize all the uppercase sequences in the string of bases (because they may correspond to final valid codons)
        stop_codon_sequences = []
        current_sequence = ""

        for char in bases:
            if char.isupper(): # Add the current character if it is uppercase
                current_sequence += char
            else:
                if current_sequence: # If it is an empty sequence, it will mean we have readen a lowercase letter before, which means we wouldn't have any new uppercase string to process
                    is_stop_codon_result = has_valid_stop_codon(current_sequence) # Returns a trio of values
                    self._returned_info += is_stop_codon_result[2] # The third returned value is information about the execution
                    if is_stop_codon_result[0]:
                        current_sequence_protein = "".join( from_bases_to_aminoacid(is_stop_codon_result[1]) ) # We will store the aminoacid string instead of the nucleotyde one
                                                                                                               # from_bases_to_aminoacid returns a list of proteins (check out utils.biopython_utils.from_bases_to_aminoacid) so we join it before appending it to the list
                        stop_codon_sequences.append(current_sequence_protein) # The second returned value is the string that has been processed, which may have been returned reversed
                        self._returned_info += f"\nThe nucleotide string has been saved as its equivalent amino acid string: {current_sequence_protein}"
                    
                    current_sequence = "" # Reinitialize current sequences' value because we have readen a lowercase character just after an uppercase one

        # Append the last sequence if there is one and corresponds to a codon
        if current_sequence:
            is_stop_codon_result = has_valid_stop_codon(current_sequence)
            self._returned_info += is_stop_codon_result[2]
            if is_stop_codon_result[0]:
                current_sequence_protein = "".join( from_bases_to_aminoacid(is_stop_codon_result[1]) ) # We will store the aminoacid string instead of the nucleotyde one
                stop_codon_sequences.append(current_sequence_protein)
                self._returned_info += f"\nThe nucleotide string has been saved as its equivalent amino acid string: {current_sequence_protein}"

        return stop_codon_sequences

    # This creates the EXCEL file that contaisn the dictionary of codons
    def __save_results(self, dict_of_baits_and_codons:dict):
        try:
            # Prepare data for Excel
            data = []
            for key, sequences in dict_of_baits_and_codons.items():
                for sequence in sequences:
                    data.append([key, sequence])
            df = pd.DataFrame(data, columns=['Key', 'Sequence']) # Convert to DataFrame
            df.to_excel(self.__pathname_to_excel_results, index=False) # Write DataFrame to Excel file
            self._returned_info += f"\nResults were saved to {str(self.__pathname_to_excel_results)} excel results file.\n"
            self._returned_value = 0
        except Exception as e:
            self._returned_info = f"Error. Unable to write on file {self.__pathname_to_excel_results}: {e}"
            self._returned_value = 2

    
