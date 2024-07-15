#import re
import subprocess

from modules.baseobjects import Task
#from modules.PATRIC_protein_processing.patric_protein_processing_utils import save_fasta_string, get_fasta_content, get_newick_codes

class FromOrederdNewickToFasta(Task):
    __pathname_to_reduced_proteins = ""
    __protein_codes = []
    __pathname_to_reduced_ordered_proteins = ""
    #__reduced_ordered_proteins = {}

    ###### INIT ######

    def __init__(self, newick_pathname="../../data/3-reduced_proteins alignment FastTree Tree.newick", 
                 pathname_to_reduced_proteins="./reduced_proteins.fasta"):
        # When we load this class from a json file, it gives the following error:
        # Unexpected error occurred: [Errno 2] No existe el archivo o el directorio: './proteins.fasta'
        # Which is because we are instantiating an object of this class when we load the
        # json file, but it is not dangerous as we are filling the object's attributes with
        # the information contained in the json file right after its instantiation
        super().__init__()
        self.__get_proteins_from_newick(newick_pathname) # Fill self.__protein_codes
        self.__pathname_to_reduced_proteins = pathname_to_reduced_proteins
    
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
            
            self.__protein_codes = protein_codes
            print(str(self.__protein_codes)) # Llámalo desde la interfaz
        
        else:
            print(f"\n\nUnexpected error occurred while oppening the newick file.")
            self._returned_info = f"Unexpected error occurred while oppening the newick file."


    '''
    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self._returned_info = ""
        self.__reduce_proteins()

        
    def __reduce_proteins(self):
        temp_proteins = list(self.__proteins.values()) # Copy the values (not the keys) of the initial set of proteins in a temporary list. BEWARE, it may be a superfitial copy
        temp_proteins_index = 0 # We will use an index to access the list, as we will process the proteins
                                # by operating from the current position
                                # whose protein we are analyzing
        while temp_proteins_index < len(temp_proteins):
            prot = temp_proteins[temp_proteins_index]
            if prot not in self.__reduced_proteins.values(): # If the current protein that it is being processed has not been added to the final reduced proteins dictionary yet
                self._returned_info += "\n-----------------------\nComparing protein\n<" + str(prot) + ">\n"
                compare_proteins_index = temp_proteins_index+1 # We will start comparing the current protein with those that are right after the next position of the list
                while compare_proteins_index < len(temp_proteins): # This loop will not be executed for the last protein of the list
                    compared_prot = temp_proteins[compare_proteins_index]
                    self._returned_info += "...with protein:\n<" + str(compared_prot) + ">\n\n"
                    if self.__biopython_compare(prot, compared_prot): # Check if the e_value between two proteins is smaller than the limit e_value of the class (using Biopython tools)
                        # Remove current compared_prot from the temporary list, since it is a protein too similar to "prot"
                        # We do not update "compare_proteins_index" since the current position now stores a new protein to compare
                        self._returned_info += " which did not return a smaller percentage. It is deleted from the protein list.\n\n\n"
                        temp_proteins.pop(compare_proteins_index)
                    else:
                        self._returned_info += " which returned a smaller percentage. It is NOT deleted from the protein list.\n\n\n"
                        compare_proteins_index += 1 # The current compared protein has not been deleted, so we compare the next protein
                
                # Include the current protein in the final proteins dictionary
                dict_protein_element = self.__find_first_matching_item(prot) # Search for the current protein in the proteins class dictionary
                                                                             # It should match only one element as we should have removed
                                                                             # repeated proteins from the .fasta file in a previous task
                if dict_protein_element[0]:
                    # We should enter here always
                    self.__reduced_proteins[dict_protein_element[0]] = dict_protein_element[1] # Asign the key and item values to the returned tuple from __find_first_matching_item
                    self._returned_info += "\nProtein <" + str(prot) + "> with code <" + str(dict_protein_element[0]) + "> has been saved to the reduced proteins dictionary\n"
                else:
                    self._returned_info += "\nThere was no match for protein <" + str(prot) + "> in the protein dictionary\n"
            else:
                # This should never be executed as we are assuming that there are no repeated proteins in the list
                self._returned_info += "\nProtein <" + str(prot) + "> was already in the reduced proteins list\n"
            temp_proteins_index += 1

        self.__generate_reduced_fasta() # Save the reduced proteins sample in a new fasta file

    
    # This function uses the utils.biopython_utils library to catch the similarity percentage from a comparisson between two proteins
    # Returns True if the stored percentage of the class is smaller than the given percentage of the comparisson
    # Note: the bigger the percentage is, the similar the proteins are
    def __biopython_compare(self, prot_one, prot_two):
        result = False
        try:
            percentage = get_coincidence_percentage(prot_one, prot_two)
            self._returned_info += "Similarity percentage " + str(percentage)
            #res_eval[0] # The first returned value is the E-value
            if percentage > self.__limit_percentage:
                result = True
                self._returned_info += " HIGHER THAN limit " + str(self.__limit_percentage)
            else:
                pass
                self._returned_info += " SMALLER THAN limit " + str(self.__limit_percentage)
        except Exception as e:
            self._returned_info += f"Error: {e}"
        return result


    # Returns the first element from self.__proteins that matches a specific item value, correspondign to a certain protein string
    def __find_first_matching_item(self, value):
        for key, val in self.__proteins.items():
            if val == value:
                return key, val
        return False, False # Returns False if no match is found
    

    # Create a .fasta file with the reduced protein sample in the pathname specified in class' parameters
    def __generate_reduced_fasta(self):
        try:
            touch_fasta = subprocess.run(['touch', self.__pathname_to_reduced_proteins]) # Create the fasta file
            if touch_fasta.returncode == 0:
                fasta_file = open(self.__pathname_to_reduced_proteins, 'w')
                for protein_key, protein_string in self.__reduced_proteins.items():
                    self._returned_info += save_fasta_string(protein_string, protein_key, fasta_file) # Call the function that saves the .fasta file. It receives the code and the result of the script itself
                fasta_file.close()
                self._returned_info += f"\n\n.fasta file {self.__pathname_to_reduced_proteins} was writen succesfully"
                self._returned_value = 0
            else:
                self._returned_info += f"\n\nUnexpected error occurred while creating the reduced proteins .fasta file: {touch_fasta.stderr}"
        except Exception as e:
            self._returned_info += f"\n\nUnexpected error occurred while getting protein strings from protein codes: {e}"
    '''

# MAIN
'''ordered_newick_to_fasta = FromOrederdNewickToFasta("../../data/3-reduced_proteins alignment FastTree Tree.newick",
                                                   "../../data/fasta/reduced_proteins.fasta")
print(str(ordered_newick_to_fasta.get_parameters["protein_codes"]))'''

