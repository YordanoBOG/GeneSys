# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file implements a GeneSys task that reads a fasta file
that refer to proteins that surround baits and recognizes all the proteins
asociated to each bait. It generates a JSON file with the baits and its
corresponding proteins
"""

import subprocess
import json

from modules.baseobjects import Task
from utils.fasta_processing_utils import get_fasta_content

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class GetCodonsFromFeatures(Task):

    __pathname_to_feature_proteins = ""
    __pathname_to_json_codons = ""
    __protein_codons = {} # Dictionary where each key is a protein BRC ID and its value is a list of protein codons

    ###### INIT ######

    def __init__(self, pathname_to_feature_proteins = "./feature_regions.fasta",
                 pathname_to_json_results = "./codons.json"):
        super().__init__()
        self.__pathname_to_feature_proteins = pathname_to_feature_proteins
        self.__pathname_to_json_codons = pathname_to_json_results
    
    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['pathname_to_feature_proteins'] = self.__pathname_to_feature_proteins
        parameters['pathname_to_json_codons'] = self.__pathname_to_json_codons
        parameters['protein_codons'] = self.__protein_codons
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__pathname_to_feature_proteins = parameters['pathname_to_feature_proteins']
        self.__pathname_to_json_codons = parameters['pathname_to_json_codons']
        self.__protein_codons = parameters['protein_codons']
    
    # There is a value that we do not want to show when we get this task as a string
    def show_info(self):
        gen_fasta_dict = self.to_dict()
        gen_fasta_dict.pop('returned_info') # We remove returned info from __str__method as it is too long to be worth to be showed
        gen_fasta_dict.pop('returned_value')
        gen_fasta_dict.pop('protein_codons')
        return str(gen_fasta_dict)
    
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self._returned_info = ""
        self.__get_codons()

    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commands in order to get the protein string and save it in as a new fasta file
    def __get_codons(self):
        read_features_result = get_fasta_content(self.__pathname_to_feature_proteins) # Returns a tuple
        if read_features_result[0]: # If the first value of the tuple is True, it means the funtion "get_fasta_content" was succesful
            codons_dict = read_features_result[1]
            # Do what it needs to be done in order to recognize the given codons
            self.__save_results(codons_dict)
            self._returned_info += "Done"
            self._returned_value = 0
        else:
            self._returned_info += "Error while trying to read the features: " + str(read_features_result[1])
            self._returned_value = 1

    # This creates the JSON file that contaisn the dictionary of codons
    def __save_results(self, dict_of_baits_and_codons:dict):
        try:
            with open(self.__pathname_to_json_codons, "w+") as json_file:
                json.dump(dict_of_baits_and_codons, json_file)
        except:
            self._returned_info = "Error. Unable to write on file {}".format(self.__pathname_to_json_codons)
            self._returned_value = 2
        
        
        '''try:
            # We execute a bash script that executes the proper BV-BRC tool which gets up 30kb correpsonding to regions surrounding a protein.
            # It receives all the BV-BRC IDs from which get the proteins and stores them in a temporal
            # fasta file in "./feature_regions.fasta" output
            args_list = [self.__pathname_to_feature_proteins] # The arguments will be the BV_BRC proteins' IDs stored as a list preceeded by the pathname where to save the features
            for code in self.__bait_proteins.keys():
                args_list.append(code)
            sh_command = ["modules/PATRIC_protein_processing/get_30kilobases_up_and_down.sh"] + args_list
            get_30kb_fasta_result = subprocess.run(sh_command, capture_output=True, text=True)
            if get_30kb_fasta_result.returncode == 0:
                self._returned_info += f"\n\nThe file with the bases corresponding to up to 30kb of the regions surrounding the given proteins was written succesfully\n"
                self._returned_value = 0 # Jump directly to the next step of the loop
                # En el archivo aparece un espacio en blanco al final de cada identificador (pero no de las cadenas) que debe eliminarse al leerse de nuevo
            else:
                # Error
                self._returned_info += f"\n\nERROR while getting the file with the bases corresponding to up to 30kb of the regions surrounding the given proteins\n"
                self._returned_value = 1
        except Exception as e:
            self._returned_info += f"\nUnexpected error occurred while executing the bash script that gets 30kb up and down from the given proteins: {e}"
            self._returned_value = 2'''

    
