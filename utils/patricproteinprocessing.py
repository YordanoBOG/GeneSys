# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

"""

import subprocess
#from genericpath import exists # Aún debes ver si puedes aplicarlo, sirve para verificar si existe el archivo especificado en una ruta dada
import csv
from utils.baseobjects import Task
from importlib import import_module

##############################################################################
##############################################################################
##############################################################################
##############################################################################


class IsolateColumn(Task):
    """
    This class receives a given csv path with raw data downloaded from
    PATRIC databases and isolates a given column from that path
    """
    __returned_value = -1
    __returned_info = ""
    __csv_path = ""
    __column_name = ""

    ###### INIT ######

    def __init__(self, csv_path="", col_name=""):
        super().__init__()
        self.__csv_path = csv_path
        self.__column_name = col_name

    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['returned_value'] = self.__returned_value
        parameters['returned_info'] = self.__returned_info
        parameters['csv_path'] = self.__csv_path
        parameters['column_name'] = self.__column_name
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__returned_value = parameters['returned_value']
        self.__returned_info = parameters['returned_info']
        self.__csv_path = parameters['csv_path']
        self.__column_name = parameters['column_name']
    
    '''
    # This method allows the user to know if the execution was succesful
    def get_returned_value(self):
        return self.__returned_value
    
    # This method allows the user to get the stored info about the execution
    def get_returned_info(self):
        return self.__returned_info
    '''
    
    ###### TASK EXECUTION METHODS ######
    
    # This is the method which will be called by the user to create a new csv with the isolated column
    def run(self):
        self.__process_codes()
    
    # This method isolates the requested column form the specified csv path and calls
    # to "save_csv_code_column" to save the column in a new csv
    def __process_codes(self):
        try:
            with open(self.__csv_path, 'r') as csv_file: # Open csv path
                csv_reader = csv.DictReader(csv_file) # We trait the csv file as a list
                
                # Isolate column's values
                try:
                    gotten_column = [row[self.__column_name] for row in csv_reader]
                
                    # Save column
                    self.__returned_info = f"Column '{self.__column_name}' found. Starting saving..."
                    new_csv_path = self.__csv_path[:-4] + "_new.csv" # Remove the last 4 characters of csv's path: ".csv" and add "_new.csv" instead
                    self.__save_csv_code_column(new_csv_path, gotten_column) # call that will save the column in a new csv

                except Exception as e:
                    self.__returned_info = f"Unexpected error occurred while trying to access the column: {e}\nPlease, verify that the specified column exists"
                    self.__returned_value = 1

        except FileNotFoundError:
            self.__returned_info = f"Cannot find '{self.__csv_path}' file"
            self.__returned_value = 2
        
        except Exception as e:
            self.__returned_info = f"Unexpected error occurred: {e}"
            self.__returned_value = 3
    
    # It saves a given column of data in the specified csv path
    def __save_csv_code_column(self, csv_name, data):
        try:
            with open(csv_name, 'w', newline='') as csv_file:
                csv_file.write(str(self.__column_name)+'\n') # write column's name
                for row in data:
                    csv_file.write(str(row)+'\n')   # write each row
            self.__returned_info += "\nnew CSV file was saved succesfully"
            self.__returned_value = 0

        except Exception as e:
            self.__returned_info += f"\nUnexpected error occurred: {e}"
            self.__returned_value = 3

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class GenerateFasta(Task):

    __returned_value = -1
    __returned_info = ""
    __csv_codes_path = ""
    __fasta_folder_path = ""

    ###### INIT ######

    def __init__(self, path_to_protein_codes_csv="", fasta_folder_path=""):
        self.__csv_codes_path = path_to_protein_codes_csv
        self.__fasta_folder_path = fasta_folder_path

    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['returned_value'] = self.__returned_value
        parameters['returned_info'] = self.__returned_info
        parameters['csv_codes_path'] = self.__csv_codes_path
        parameters['fasta_folder_path'] = self.__fasta_folder_path
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__returned_value = parameters['returned_value']
        self.__returned_info = parameters['returned_info']
        self.__csv_codes_path = parameters['csv_codes_path']
        self.__fasta_folder_path = parameters['fasta_folder_path']
    
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self.__acces_codes()

        # We save the execution results in a text file
        results_file_name = self.__fasta_folder_path+"/results.txt"
        touch_result = subprocess.run(['touch', results_file_name]) # Create the results info file
        if touch_result.returncode == 0:
            # Write class' metadata into the results file
            info = self.__returned_info + "\n" + str(self.__returned_value)
            results_file = open(results_file_name, 'w')
            results_file.write(info)

    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commands in order to get the protein string and save it in as a new fasta file
    def __acces_codes(self):
        try:
            with open(self.__csv_codes_path, 'r') as csv_file: # Open csv codes path
                csv_reader = csv.DictReader(csv_file) # We trait the csv file as a list
                
                # If the csv file has more than a column, then it is not a proper csv file
                if len(csv_reader.fieldnames) != 1:
                    self.__returned_info = "ERROR. CSV codes file must have only one column, corresponding to PATRIC protein codes\n"
                    self.__returned_value = 1
                else:
                    try:
                        column_name = csv_reader.fieldnames[0] # We know that there is only one column so the first column is the column that we are looking for
                        codes_column = [row[column_name] for row in csv_reader] # Isolate the codes of the column in a list
                        self.__obtain_protein_strings(codes_column) # Method that creates a fasta file in the proper path

                    except Exception as e:
                        self.__returned_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
                        self.__returned_value = 2

        except FileNotFoundError:
            self.__returned_info = f"Cannot find '{self.__csv_path}' file"
            self.__returned_value = 3
        
        except Exception as e:
            self.__returned_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
            self.__returned_value = 2
    
    # This function calls BV-BRC commands and, for each protein code, gets its protein string
    # value, and for each protein, calls a function that saves it as a fasta file in the appropiate path
    def __obtain_protein_strings(self, codes):
        try:
            fasta_file_name = str(self.__fasta_folder_path) + "/proteins.fasta" # This is the fasta file in which we will save the given protein string
            touch_result = subprocess.run(['touch', fasta_file_name]) # Create the fasta file
            if touch_result.returncode == 0:
                fasta_file = open(fasta_file_name, 'w') # Open .fasta file where we will save all the encountered unique proteins
                procesed_proteins = [] # List where we will locate all the protein strings that we have already saved as fasta files
                for protein_code in codes:
                    # We specify the path 'utils/getprotein.sh' because we assume that we are executing this script from genesys.py context
                    get_protein_bash_command_result = subprocess.run(['utils/getprotein.sh', protein_code], capture_output=True, text=True) # We execute a tiny bash script that executes the proper BV-BRC tool which gets a protein string from its code. The capture_output=True argument captures the output of the command, and text=True decodes the output as text
                    if get_protein_bash_command_result.returncode == 0:
                        protein_string = get_protein_bash_command_result.stdout.rsplit(' ', 1)[-1]  # rsplit() is used to split the command_result variable starting from the right side
                                                                                                    # (from the end) using blank spaces as delimiters. The [-1] index retrieves the last
                                                                                                    # part after splitting. It's important to note that the given structure of command_result is:
                                                                                                    # "id feature.aa_sequence <given_code> <returned_string>" as the employed BV-BRC "feature.aa_sequence" tool returns a 2x2 matrix
                        if protein_string!="feature.aa_sequence\n": # If we have isolated the string "feature.aa_sequence\n", it means that the BV-BRC command that we run in "getprotein.sh" has not found any asociated protein to the code
                            if self.__code_not_procesed(protein_string, procesed_proteins): # Before saving the protein, we check is it was already saved
                                self.__save_protein(protein_string, protein_code, fasta_file) # Call the function that saves the .fasta file. It receives the code and the result of the script itself
                                procesed_proteins.append(protein_string) # We add the protein into the procesed proteins list once it is saved
                            else:
                                self.__returned_info += f"\nProtein with code <{protein_code}> and string <<<<< {protein_string} >>>>>\n turned out to reference an ALREADY SAVED protein sequence\n"
                                continue # Jump directly to the next step of the loop
                        else:
                            self.__returned_info += f"\nCode <{protein_code}> did NOT return any asociated protein string\n"
                            continue # Jump directly to the next step of the loop
                    else:
                        # Error
                        self.__returned_info += f"\nError while getting {protein_code} code: {get_protein_bash_command_result.stderr}"
                        self.__returned_value = 4
                fasta_file.close()
            else:
                self.__returned_info += f"\nUnexpected error occurred while creating the .fasta file: {touch_result.stderr}"
                self.__returned_value = 5
        except Exception as e:
            self.__returned_info += f"\nUnexpected error occurred while getting protein strings from protein codes: {e}"
            self.__returned_value = 6

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

    # This function receives the result given by BRC-ID API and stores its protein string in a .fasta file
    # in the path specified by the arguments
    def __save_protein(self, protein_string, code, fasta_file):
        # Write the identifier line
        identifier_line = ">" + code + "\n"
        fasta_file.write(identifier_line)

        # Write the aminoacid sequence. We write the sequence in lines of a maximum of 80 characters so we follow the .fasta structure standard
        protein_lines = self.__split_fasta_sequence(protein_string)
        for line in protein_lines:
            line += "\n"
            fasta_file.write(line) # According to .fasta structure, each line of a fasta file always should have 80 characters or less 
        fasta_file.write("\n")
        
        self.__returned_info += f"\nProtein <<<<< {protein_string} >>>>> with code <{code}> WAS SAVED succesfully\n"
        self.__returned_value = 0

    # Returns a vector that contains an aminoacid sequence splitted in lines of 80 characters or less
    def __split_fasta_sequence(self, sequence): # If we write de sequence in the fasta file without calling this function, it will lasta a few seconds less
        result_sequences = [] # We declare a void vector
        for i in range(0, len(sequence), 80): # Iterate over the sequence splitting it in strings of a maximum of 80 characters
            result_sequences.append(sequence[i:i+80])
        return result_sequences
    
