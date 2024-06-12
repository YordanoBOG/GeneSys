#import re
import subprocess

from modules.baseobjects import Task
from modules.PATRIC_protein_processing.patric_protein_processing_utils import save_fasta_string

class ReduceSample(Task):
    __limit_e_value = 0
    __returned_info = ""
    #__path_to_blast_db = "" # Not asigned
    __pathname_to_reduced_proteins = ""
    __proteins_pathname = ""
    __results_file_pathname = ""
    __proteins = {}
    __reduced_proteins = {}

    ###### INIT ######

    def __init__(self, fasta_pathname="./proteins.fasta", 
                 pathname_to_reduced_proteins="./reduced_proteins.fasta",
                 e_value=1e-20):
        super().__init__()
        self.__proteins_pathname = fasta_pathname
        self.__get_proteins_from_fasta(fasta_pathname) # Fill self.__proteins
        self.__pathname_to_reduced_proteins = pathname_to_reduced_proteins
        self.__results_file_pathname = str(pathname_to_reduced_proteins.rsplit('/')[:-1][0]) + "/reduced_sample_results.txt" # Get all the path to the reduced sample file and set it as the path for the results file
        self.__limit_e_value = e_value # e_value syntax is properly checked at the Kivy UI
    
    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        #parameters['path_to_blast_db'] = self.__path_to_blast_db
        parameters['pathname_to_reduced_proteins'] = self.__pathname_to_reduced_proteins
        parameters['proteins_pathname'] = self.__proteins_pathname
        parameters['results_file_pathname'] = self.__results_file_pathname
        parameters['proteins'] = self.__proteins # It is not useful to show the initial sample, only the reduced one
        parameters['returned_info'] = self.__returned_info # Same occurs for returned info
        parameters['reduced_proteins'] = self.__reduced_proteins
        parameters['limit_e_value'] = self.__limit_e_value
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        #self.__path_to_blast_db = parameters['path_to_blast_db']
        self.__pathname_to_reduced_proteins = parameters['pathname_to_reduced_proteins']
        self.__proteins_pathname = parameters['proteins_pathname']
        self.__results_file_pathname = parameters['results_file_pathname']
        self.__proteins = parameters['proteins']
        self.__returned_info = parameters['returned_info'] # Same occurs for returned info
        self.__reduced_proteins = parameters['reduced_proteins']
        self.__limit_e_value = parameters['limit_e_value']

    # Return information that might be useful for the user
    def show_info(self):
        reduce_sample_dict = self.to_dict()
        reduce_sample_dict.pop('returned_info') # We remove returned info as it is too long to be worth to be showed
        reduce_sample_dict.pop('proteins')
        reduce_sample_dict.pop('reduced_proteins')
        return str(reduce_sample_dict)
    
    ###### FILL CLASS VALUES METHODS #####

    def __get_proteins_from_fasta(self, fasta_pathname):
        try:
            self.__proteins = {}
            fasta_file = open(fasta_pathname, 'r') # Open input file for reading
            current_sequence_id = None # Here we will store the identifier line of a protein
            current_sequence = [] # Here we will store all the aminoacid lines corresponding to a same protein

            for line in fasta_file:
                line = line.strip() # strip removes the final newline character of the line, it is equivalent to line.replace('\n','')
                if line.startswith(">"): # If the first character of the line is ">", then we are in a identifier line
                    if current_sequence_id is not None: # If this is true, it will mean that we have an already saved identifier
                                                        # from a previous readed protein, so we save that protein in the proteins
                                                        # dictionary before reading a new one
                        self.__proteins[current_sequence_id] = ''.join(current_sequence) # Join the sequence by '', which is the character that we have put at the end of each line instead of '\n' by calling to strip() function
                    current_sequence_id = line[1:] # The dictionary key for the new sequence will be the identifier line without the first character ">", correponding to the BVRC PATRIC code of the protein
                    current_sequence = [] # clean the sequence that we are currently reading
                else: # We are not in an identifier line
                    current_sequence.append(line)
            
            self.__proteins[current_sequence_id] = ''.join(current_sequence) # process the final readen entry
        except Exception as e:
            print(f"\n\nUnexpected error occurred: {e}")
            self.__returned_info += f"Unexpected error occurred: {e}"

    ###### TASK EXECUTION METHODS ######

    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self.__reduce_proteins()

        # We save the execution results in a text file
        touch_result = subprocess.run(['touch', self.__results_file_pathname]) # Create the results info file
        if touch_result.returncode == 0:
            # Write class' metadata into the results file
            info = self.__returned_info + "\n" + str(self.__returned_value)
            results_file = open(self.__results_file_pathname, 'w')
            results_file.write(info)

        
    def __reduce_proteins(self):
        """
        Clase que lea un fasta y reduzca la muestra de proteínas de ese .fasta al 85% de
        coincidencia o más, y las guarde en un nuevo .fasta; la comparación de cadenas se
        hace con BLAST (aunque puedes mirar si existe un equivalente en BVRC). Al comparar
        dos cadenas de aminoácidos en BLAST (que pueden no tener la misma longitud), se
        devuelven varias medidas, entre ellas:
        -> Porcentaje de similaridad: que el usuario fije un porcentaje (85 por defecto), y
        se emplee ese valor para decidir si conservas o no una proteína.
        -> e-value: expresa la probabilidad de obtener la similitud existente entre
        dos cadenas de aminoácidos dadas si ambas fueran generadas aleatoriamente. Cuanto
        más bajo, más similares son entre sí. Que el usuario elija el e-value umbral, por
        defecto, 10e-30
        Un posible algoritmo es:
            -> Copias la lista de proteínas original al completo en una lista temporal.
                La lista final inicialmente está vacía.
            -> Mientras no se llegue al final de la lista temporal:
                -> Tomas la primera proteína de la lista temporal que no se encuentre
                    en la lista final.
                -> La comparas una a una con el resto de proteínas de la lista temporal,
                    y eliminas de la lista temporal aquellas que sean iguales según el
                    umbral dado. Añades la proteína que has comparado a la lista final.
                -> Repetir hasta que no se puedan extraer más proteínas de la lista
                    temporal que cumplan las condiciones para ser procesadas
            -> Generas un nuevo fasta con las proteínas de la lista final.
            """
        temp_proteins = list(self.__proteins.values()) # Copy the values (not the keys) of the initial set of proteins in a temporary list
        temp_proteins_index = 0 # We will use an index to access the list, as we will process the proteins
                                # by operating from the current position
                                # whose protein we are analyzing
        while temp_proteins_index < len(temp_proteins):
            prot = temp_proteins[temp_proteins_index]
            self.__returned_info += f"\n-----------------------\nWe are comparing protein <{prot}>\n"
            if prot not in self.__reduced_proteins.values(): # If the current protein that it is being processed has not been added to the final reduced proteins dictionary yet
                compare_proteins_index = temp_proteins_index+1 # We will start comparing the current protein with those that are right after the next position of the list
                while compare_proteins_index < len(temp_proteins): # This loop will not be executed for the last protein of the list
                    compared_prot = temp_proteins[compare_proteins_index]
                    if self.__blast_compare(prot, compared_prot): # Check if the e_value between two proteins is smaller than the limit e_value of the class (using Blast)
                        # Remove current compared_prot from the temporary list, since it is a protein too similar to "prot"
                        # We do not update "compare_proteins_index" since the current position now stores a new protein to compare
                        self.__returned_info += f"Protein <{compared_prot}> returned a smaller e-value than {str(self.__limit_e_value)}. The protein is removed from the set\n"
                        temp_proteins.pop(compare_proteins_index)
                    else:
                        self.__returned_info += f"Protein <{compared_prot}> did not return a smaller e-value than {str(self.__limit_e_value)}. The protein is NOT removed from the set\n"
                        compare_proteins_index += 1 # The current compared protein has not been deleted, so we compare the next protein
                
                # Include the current protein in the final proteins dictionary
                dict_protein_element = self.__find_first_matching_item(prot) # Search for the current protein in the proteins class dictionary
                                                                             # It should match only one element as we should have removed
                                                                             # repeated proteins from the .fasta file we have readed in a previous task
                if dict_protein_element:
                    # We should enter here always
                    self.__reduced_proteins[dict_protein_element[0]] = dict_protein_element[1] # Asign the key and item values to the returned tuple from __find_first_matching_item
                    self.__returned_info += f"\nProtein <{prot}> with code <{str(dict_protein_element[0])}> has been saved to the reduced proteins dictionary\n"
                else:
                    self.__returned_info += f"\nThere was no match for protein <{prot}> in the protein dictionary\n"
                
        self.__generate_reduced_fasta() # Save the reduced proteins sample in a new fasta file

    
    # This function uses BLAST Python tool to catch the e_value from a comparisson between two proteins
    # Returns True if the stored e_value of the class is bigger than the given e_value of the comparisson
    def __blast_compare(self, prot_one, prot_two):
        pass # You still have to do this


    # Returns the first element from self.__proteins that matches a specific item value, correspondign to a certain amynoacid string
    def __find_first_matching_item(self, value):
        result = False # Return False if no match is found
        for key, val in self.__proteins.items():
            if val == value:
                result = tuple(key, val)
        return result
    
    # Create a .fasta file with the reduced protein sample in the pathname specified in class' parameters
    def __generate_reduced_fasta(self):
        try:
            touch_fasta = subprocess.run(['touch', self.__pathname_to_reduced_proteins]) # Create the fasta file
            if touch_fasta.returncode == 0:
                fasta_file = open(self.__pathname_to_reduced_proteins, 'w')
                for protein_key, protein_string in self.__reduced_proteins.items():
                    self.__returned_info += save_fasta_string(protein_string, protein_key, fasta_file) # Call the function that saves the .fasta file. It receives the code and the result of the script itself
                fasta_file.close()
                self.__returned_info += f"\n\n.fasta file {self.__pathname_to_reduced_proteins} was writen succesfully"
            else:
                self.__returned_info += f"\n\nUnexpected error occurred while creating the reduced proteins .fasta file: {touch_fasta.stderr}"
        except Exception as e:
            self.__returned_info += f"\n\nUnexpected error occurred while getting protein strings from protein codes: {e}"


# MAIN
'''
reduce_sample = ReduceSample(
    "/home/bruno/Documentos/UGR/IngInformatica/Grado/Curso4/TFG/GeneSys/data/fasta/proteins.fasta",
    "/home/bruno/Documentos/UGR/IngInformatica/Grado/Curso4/TFG/GeneSys/data/fasta/reduced_proteins.fasta",
    "1e-20") # "../data/fasta/proteins.fasta"
message = "\n\n\n" + reduce_sample.__str__() + "\n\n"
print(message)
'''

