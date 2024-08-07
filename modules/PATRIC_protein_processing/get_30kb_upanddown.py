# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file implements a GeneSys task that reads a fasta file with
BV-BRC proteins and generates up to 30kb that refer to more proteins
that surround each protein given by the fasta file, which work as bait
"""

import subprocess

from modules.baseobjects import Task
from utils.fasta_processing_utils import get_fasta_content

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class Get30KbProteins(Task):

    __pathname_to_reduced_proteins = ""
    __pathname_to_feature_proteins = ""
    __bait_proteins = {}

    ###### INIT ######

    def __init__(self, pathname_to_reduced_proteins="./reduced_proteins.fasta",
                 pathname_to_feature_proteins = "./feature_regions.fasta"):
        # When we load this class from a json file, it gives the following error:
        # Unexpected error occurred: [Errno 2] No existe el archivo o el directorio: './proteins.fasta'
        # Which is because we are instantiating an object of this class when we load the
        # json file, but it is not dangerous as we are filling the object's attributes with
        # the information contained in the json file right after its instantiation
        super().__init__()
        self.__get_proteins_from_fasta(pathname_to_reduced_proteins) # Fill self.__bait_proteins
        self.__pathname_to_reduced_proteins = pathname_to_reduced_proteins
        self.__pathname_to_feature_proteins = pathname_to_feature_proteins

    
    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['pathname_to_reduced_proteins'] = self.__pathname_to_reduced_proteins
        parameters['pathname_to_feature_proteins'] = self.__pathname_to_feature_proteins
        parameters['bait_proteins'] = self.__bait_proteins
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__pathname_to_reduced_proteins = parameters['pathname_to_reduced_proteins']
        self.__pathname_to_feature_proteins = parameters['pathname_to_feature_proteins']
        self.__bait_proteins = parameters['bait_proteins']
    
    # There is a value that we do not want to show when we get this task as a string
    def show_info(self):
        gen_fasta_dict = self.to_dict()
        gen_fasta_dict.pop('returned_info') # We remove returned info from __str__method as it is too long to be worth to be showed
        gen_fasta_dict.pop('returned_value')
        gen_fasta_dict.pop('bait_proteins')
        return str(gen_fasta_dict)
    
    
    ###### FILL CLASS VALUES METHODS #####

    def __get_proteins_from_fasta(self, fasta_pathname):
        get_prot_res = get_fasta_content(fasta_path=fasta_pathname) # Returns a tuple where the first element is a boolean of the result
        if get_prot_res[0]:
            self.__bait_proteins = get_prot_res[1]
        else:
            print(f"\n\nUnexpected error occurred while getting the proteins from the fasta file: {get_prot_res[1]}")
            self._returned_info = f"Unexpected error occurred while getting the proteins from the fasta file: {get_prot_res[1]}"
            self._returned_value = 3

    
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self.__get_30kb()


    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commands in order to get the protein string and save it in as a new fasta file
    def __get_30kb(self):
        try:
            # We execute a bash script that executes the proper BV-BRC tool which gets up 30kb correpsonding to regions surrounding a protein.
            # It receives all the BV-BRC IDs from which get the proteins and stores them in a temporal
            # fasta file in "./feature_regions.fasta" output
            args_list = [self.__pathname_to_feature_proteins] # The arguments will be the BV_BRC proteins' IDs stored as list preceeded by the pathname where to save the features
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
            self._returned_value = 2

    
