# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file implements a GeneSys example task that allows the user to
read a csv file with one column that corresponds to BVRC codes,
obtain the appropiate gene sequences associated with each code and
store all of them in a .fasta file while filtering repeated sequences.
It is exclusively aimed to work with BVRC codes from
PATRIC databases, and it has not been tested in other contexts.
"""

import csv
import subprocess

from modules.baseobjects import Task
from modules.PATRIC_protein_processing.patric_protein_processing_utils import save_fasta_string

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class GenerateFasta(Task):

    __csv_codes_path = ""
    __fasta_pathname = "" # This is the pathname of the final .fasta file that would store all the proteins. It might be taken as a parameter by the next task of a patricproteinprocessing workflow

    ###### INIT ######

    def __init__(self, path_to_protein_codes_csv="./", fasta_folder_path="./proteins.fasta"):
        super().__init__()
        self.__csv_codes_path = path_to_protein_codes_csv
        self.__fasta_pathname = fasta_folder_path # This is the fasta file in which we will save protein strings

    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['csv_codes_path'] = self.__csv_codes_path
        parameters['fasta_pathname'] = self.__fasta_pathname
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__csv_codes_path = parameters['csv_codes_path']
        self.__fasta_pathname = parameters['fasta_pathname']
    
    # There is a value that we do not want to show when we get this task as a string
    def show_info(self):
        gen_fasta_dict = self.to_dict()
        gen_fasta_dict.pop('returned_info') # We remove returned info from __str__method as it is too long to be worth to be showed
        gen_fasta_dict.pop('returned_value')
        return str(gen_fasta_dict)
    
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self.__acces_codes()

    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commands in order to get the protein string and save it in as a new fasta file
    def __acces_codes(self):
        try:
            with open(self.__csv_codes_path, 'r') as csv_file: # Open csv codes path
                csv_reader = csv.DictReader(csv_file) # We trait the csv file as a list
                
                # If the csv file has more than a column, then it is not a proper csv file
                if len(csv_reader.fieldnames) != 1:
                    self._returned_info = "ERROR. CSV codes file must have only one column, corresponding to PATRIC protein codes\n"
                    self._returned_value = 1
                else:
                    try:
                        column_name = csv_reader.fieldnames[0] # We know that there is only one column so the first column is the column that we are looking for
                        codes_column = [row[column_name] for row in csv_reader] # Isolate the codes of the column in a list
                        self.__obtain_protein_strings(codes_column) # Method that creates a fasta file in the proper path

                    except Exception as e:
                        self._returned_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
                        self._returned_value = 2

        except FileNotFoundError:
            self._returned_info = f"Cannot find '{self.__csv_path}' file"
            self._returned_value = 3
        
        except Exception as e:
            self._returned_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
            self._returned_value = 2
    
    # This function calls BV-BRC commands and, for each protein code, gets its protein string
    # value, and for each protein, calls a function that saves it as a fasta file in the appropiate path
    def __obtain_protein_strings(self, codes):
        try:
            touch_result = subprocess.run(['touch', self.__fasta_pathname]) # Create the fasta file
            if touch_result.returncode == 0:
                fasta_file = open(self.__fasta_pathname, 'w') # Open .fasta file where we will save all the encountered unique proteins
                procesed_proteins = [] # List where we will locate all the protein strings that we have already saved as fasta files
                for protein_code in codes:
                    # We specify the path 'utils/getprotein.sh' because we assume that we are executing this script from genesys.py context
                    get_protein_bash_command_result = subprocess.run(['modules/PATRIC_protein_processing/getprotein.sh', protein_code], capture_output=True, text=True) # We execute a tiny bash script that executes the proper BV-BRC tool which gets a protein string from its code. The capture_output=True argument captures the output of the command, and text=True decodes the output as text
                    if get_protein_bash_command_result.returncode == 0:
                        protein_string = get_protein_bash_command_result.stdout.rsplit(' ', 1)[-1]  # rsplit() is used to split the command_result variable starting from the right side
                                                                                                    # (from the end) using blank spaces as delimiters. The [-1] index retrieves the last
                                                                                                    # part after splitting. It's important to note that the given structure of command_result is:
                                                                                                    # "id feature.aa_sequence <given_code> <returned_string>" as the employed BV-BRC "feature.aa_sequence" tool returns a 2x2 matrix
                        if protein_string!="feature.aa_sequence\n": # If we have isolated the string "feature.aa_sequence\n", it means that the BV-BRC command that we run in "getprotein.sh" has not found any asociated protein to the code
                            if self.__code_not_procesed(protein_string, procesed_proteins): # Before saving the protein, we check is it was already saved
                                self._returned_info += save_fasta_string(protein_string, protein_code, fasta_file) # Call the function that saves the .fasta file.
                                procesed_proteins.append(protein_string) # We add the protein into the procesed proteins list once it is saved
                            else:
                                self._returned_info += f"\nProtein with code <{protein_code}> and string <<<<< {protein_string} >>>>>\n turned out to reference an ALREADY SAVED protein sequence\n"
                                continue # Jump directly to the next step of the loop
                        else:
                            self._returned_info += f"\nCode <{protein_code}> did NOT return any asociated protein string\n"
                            continue # Jump directly to the next step of the loop
                    else:
                        # Error
                        self._returned_info += f"\nError while getting {protein_code} code: {get_protein_bash_command_result.stderr}"
                        self._returned_value = 4
                fasta_file.close()
            else:
                self._returned_info += f"\nUnexpected error occurred while creating the .fasta file: {touch_result.stderr}"
                self._returned_value = 5
        except Exception as e:
            self._returned_info += f"\nUnexpected error occurred while getting protein strings from protein codes: {e}"
            self._returned_value = 6

    # This function checks if a certain code is already in a list of previously procesed codes.
    # It is called in order to avoid saving two different .fasta files that contain the same protein
    def __code_not_procesed(self, protein, procesed_proteins):
        result = True
        for procesed_protein in procesed_proteins:
            if len(protein) == len(procesed_protein): # If the lenght between the protein strings is different, they are not the same one. This will be the majority of the cases
                if protein == procesed_protein:
                    result = False
                    break # Exit the loop
                else:
                    continue
            else:
                continue
        return result
    
