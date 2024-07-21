#import re
import subprocess

from modules.baseobjects import Task
from modules.PATRIC_protein_processing.patric_protein_processing_utils import save_fasta_string, get_fasta_content

class FromOrderedNewickToFasta(Task): # to EXCEL
    __pathname_to_reduced_proteins = ""
    __protein_codes = []
    __pathname_to_reduced_ordered_proteins = ""
    #__reduced_ordered_proteins = {}

    ###### INIT ######

    def __init__(self, newick_pathname="./proteins.newick", 
                 pathname_to_reduced_proteins="./reduced_proteins.fasta"):
        # When we load this class from a json file, it gives the following error:
        # Unexpected error occurred: [Errno 2] No existe el archivo o el directorio: './proteins.fasta'
        # Which is because we are instantiating an object of this class when we load the
        # json file, but it is not dangerous as we are filling the object's attributes with
        # the information contained in the json file right after its instantiation
        super().__init__()
        self.__get_proteins_from_newick(newick_pathname) # Fill self.__protein_codes
        self.__pathname_to_reduced_proteins = pathname_to_reduced_proteins
        self.__pathname_to_reduced_ordered_proteins = self.__pathname_to_reduced_proteins[:-6] + "_reordered.fasta"

    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['pathname_to_reduced_proteins'] = self.__pathname_to_reduced_proteins
        parameters['protein_codes'] = self.__protein_codes
        parameters['pathname_to_reduced_ordered_proteins'] = self.__pathname_to_reduced_ordered_proteins
        #parameters['reduced_ordered_proteins'] = self.__reduced_ordered_proteins
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__pathname_to_reduced_ordered_proteins = parameters['pathname_to_reduced_ordered_proteins']
        self.__protein_codes = parameters['protein_codes']
        self.__pathname_to_reduced_proteins = parameters['pathname_to_reduced_proteins']
        #self.__reduced_ordered_proteins = parameters['reduced_ordered_proteins']

    # Return information that might be useful for the user
    def show_info(self):
        reduce_sample_dict = self.to_dict()
        reduce_sample_dict.pop('returned_info') # We remove returned info as it is too long to be worth to be showed
        reduce_sample_dict.pop('protein_codes')
        #reduce_sample_dict.pop('reduced_ordered_proteins')
        return str(reduce_sample_dict)
    
    ###### FILL CLASS VALUES METHODS #####

    def __get_proteins_from_newick(self, newick_pathname):
        try:
            newick_file = open(newick_pathname, 'r') # Open input file for reading
            newick_content = newick_file.read()
            
            protein_codes = []
            current_code = [] # Here we will store all the aminoacid lines corresponding to a same protein
            recording = False # True if we are currently reading a protein code
            for char in newick_content:
                if char.__eq__("'"): # "'"" always marks the start or the finish of a protein
                    if not recording: # If we are not recording, then we have found a new protein
                        recording = True
                    else: # If we are recording, then we have finished reading a protein
                        protein_codes.append(''.join(current_code)) # so we join it and add it to the proteins list
                        current_code = []
                        recording = False
                # elif recording and (char.isalnum() or char in ".|figpeg"): # more specific
                elif recording: # If there is no "'" but we are reading a protein, we add the current cahr to the current protein code
                        current_code.append(char)
            # Ensure the last protein code is added
            if recording:
                protein_codes.append(''.join(current_code))
            
            self.__protein_codes = protein_codes

        except Exception as e:
            print(f"\n\nUnexpected error occurred while oppening the newick file: {e}")
            self._returned_info = f"Unexpected error occurred while oppening the newick file:\n{e}\n\n"


    #'''
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self._returned_info = ""
        self._returned_value = 0
        self.__reorganize_proteins()

    
    def __reorganize_proteins(self):
        success, result = get_fasta_content(self.__pathname_to_reduced_proteins)
        if success:
            self._returned_info += "Fasta file with reduced proteins was readen succesfully\n\n"
            reordered_protein_codes = [] # Empty list that will store the reorganized protein codes
            reordered_protein_strings = [] # The same for the protein strings. The same position in both lists will refer to a same protein
            for protein_code in self.__protein_codes:
                try:
                    protein_string = result[protein_code]
                    reordered_protein_codes.append(protein_code)
                    reordered_protein_strings.append(protein_string)
                    self._returned_info += f"\n\n\nProtein <{protein_code}> was found in the fasta file: {e}\n\n"
                except Exception as e:
                    self._returned_info += f"\n\n\nERROR while searching for protein <{protein_code}> in the fasta file: {e}\n\n"
            
            # Save the results
            try:
                touch_fasta = subprocess.run(['touch', self.__pathname_to_reduced_ordered_proteins]) # Create the fasta file
                if touch_fasta.returncode == 0:
                    fasta_file = open(self.__pathname_to_reduced_ordered_proteins, 'w')
                    for index in range(0, len(reordered_protein_codes)):
                        self._returned_info += save_fasta_string(reordered_protein_strings[index], reordered_protein_codes[index], fasta_file) # Call the function that saves the .fasta file
                    fasta_file.close()
                    self._returned_info += f"\n\n.fasta file {self.__pathname_to_reduced_ordered_proteins} was writen succesfully"
                    self._returned_value = 0
                else:
                    self._returned_info += f"\n\nUnexpected error occurred while creating the reduced proteins .fasta file: {touch_fasta.stderr}"
            except Exception as e:
                self._returned_info += f"\n\nUnexpected error occurred while getting protein strings from protein codes: {e}"
        else:
            self._returned_info += f"ERROR while reading proteins from fasta file: {result}\n\n"
        
        
        
