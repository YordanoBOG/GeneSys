import csv
import argparse
import subprocess

# Execution through command line:
# python GenerateFasta.py ../datos/muestra_reducida.csv ../datos/fasta_pruebas
# python GenerateFasta.py ../datos/BVBRC_slatt_domain-containing_protein_new.csv ../datos/fasta

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# For security reasons, we are going to work through private methods of a class

class GenerateFasta:

    __returned_value = -1
    __return_info = ""
    __csv_codes_path = ""
    __fasta_folder_path = ""
    __parser = None # parser that allows us to manipulate the arguments within each class object

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################

    def __init__(self):
        # Create object's parser in order to manipulate arguments
        self.__parser = argparse.ArgumentParser(description='Argument parser for protein codes csv pathfile and folder pathfile where to save .fasta files')
        self.__parser.add_argument('path_to_protein_codes_csv', help='Input protein codes csv file path')
        self.__parser.add_argument('path_to_fasta_folder', help="Input folder where .fasta files will be saved")
        args = self.__parser.parse_args() # parse parser arguments

        self.__csv_codes_path = args.path_to_protein_codes_csv
        self.__fasta_folder_path = args.path_to_fasta_folder

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This method allows the user to know if the execution was succesful
    def get_returned_value(self):
        return self.__returned_value
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This method allows the user to get the stored info about the execution
    def get_returned_info(self):
        return self.__return_info
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This is the method which will be called by the user in order to store de .fasta files
    def run(self):
        self.__acces_codes()

        # We save the execution results in a text file
        results_file_name = self.__fasta_folder_path+"/generate_fasta_results.txt"
        touch_result = subprocess.run(['touch', results_file_name]) # Create the results info file
        if touch_result.returncode == 0:
            # Write class' metadata into the results file
            info = self.__return_info + "\n" + str(self.__returned_value)
            results_file = open(results_file_name, 'w')
            results_file.write(info)

    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This method isolates the ID's column from the specified csv path and calls
    # to BV-BRC CLI commandas in order to get the protein string and save it in as a new fasta file
    def __acces_codes(self):
        try:
            with open(self.__csv_codes_path, 'r') as csv_file: # Open csv codes path
                csv_reader = csv.DictReader(csv_file) # We trait the csv file as a list
                
                # If the csv file has more than a column, then it is not a proper csv file
                if len(csv_reader.fieldnames) != 1:
                    self.__return_info = "ERROR. CSV codes file must have only one column, corresponding to PATRIC protein codes\n"
                    self.__returned_value = 1
                else:
                    try:
                        column_name = csv_reader.fieldnames[0] # We know that there is only one column so the first column is the column that we are looking for
                        codes_column = [row[column_name] for row in csv_reader] # Isolate the codes of the column in a list
                        self.__obtain_protein_strings(codes_column) # Method that creates fasta files in the proper path

                    except Exception as e:
                        self.__return_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
                        self.__returned_value = 2

        except FileNotFoundError:
            self.__return_info = f"Cannot find '{self.__csv_path}' file"
            self.__returned_value = 3
        
        except Exception as e:
            self.__return_info = f"Unexpected error occurred while trying to access the CSV codes file: {e}\n"
            self.__returned_value = 2
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This function calls BV-BRC commands and, for each protein code, gets its protein string
    # value, and for each protein, calls a function that saves it as a fasta file in the appropiate path
    def __obtain_protein_strings(self, codes):
        try:
            procesed_proteins = [] # List where we will locate all the protein strings that we have already saved as fasta files
            for protein_code in codes:
                get_protein_bash_command_result = subprocess.run(['./getprotein.sh', protein_code], capture_output=True, text=True) # We execute a tiny bash script that executes the proper BV-BRC tool which gets a protein string from its code. The capture_output=True argument captures the output of the command, and text=True decodes the output as text
                if get_protein_bash_command_result.returncode == 0:
                    protein_string = get_protein_bash_command_result.stdout.rsplit(' ', 1)[-1]  # rsplit() is used to split the command_result variable starting from the right side
                                                                                                # (from the end) using blank spaces as delimiters. The [-1] index retrieves the last
                                                                                                # part after splitting. It's important to note that the given structure of command_result is:
                                                                                                # "id feature.aa_sequence <given_code> <returned_string>" as the employed BV-BRC "feature.aa_sequence" tool returns a 2x2 matrix
                    if protein_string!="feature.aa_sequence\n": # If we have isolated the string "feature.aa_sequence\n", it means that the BV-BRC command that we run in "getprotein.sh" has not found any asociated protein to the code
                        if self.__code_not_procesed(protein_string, procesed_proteins): # Before saving the protein, we check is it was already saved
                            self.__save_fasta(protein_string, protein_code) # Call the function that saves the .fasta file. It receives the code and the result of the script itself
                            procesed_proteins.append(protein_string) # We add the protein into the procesed proteins list once it is saved
                        else:
                            self.__return_info += f"\nProtein with code <{protein_code}> and string <<<<< {protein_string} >>>>>\n turned out to reference an ALREADY SAVED protein sequence\n"
                            continue # Jump directly to the next step of the loop
                    else:
                        self.__return_info += f"\nCode <{protein_code}> did NOT return any asociated protein string\n"
                        continue # Jump directly to the next step of the loop
                else:
                    # Error
                    self.__return_info += f"\nError while getting {protein_code} code: {get_protein_bash_command_result.stderr}"
                    self.__returned_value = 4

        except Exception as e:
            self.__return_info += f"\nUnexpected error occurred while getting protein strings from protein codes: {e}"
            self.__returned_value = 5

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
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

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This function receives the result given by BRC-ID API and stores its protein string in a .fasta file
    # in the path specified by the arguments
    def __save_fasta(self, protein_string, code):
        fasta_file_name = str(self.__fasta_folder_path) + "/code_" + str(code) + ".fasta" # This is the fasta file in which we will save the given protein string
        touch_result = subprocess.run(['touch', fasta_file_name]) # Create the fasta file
        
        if touch_result.returncode == 0:
            # Write the identifier line
            fasta_file = open(fasta_file_name, 'w')
            identifier_line = ">" + code + "\n"
            fasta_file.write(identifier_line)

            # Write the aminoacid sequence. We write the sequence in lines of a maximum of 80 characters so we follow the .fasta structure standard
            protein_lines = self.__split_fasta_sequence(protein_string)
            for line in protein_lines:
                line += "\n"
                fasta_file.write(line) # According to .fasta structure, each line of a fasta file always should have 80 characters or less 
            
            self.__return_info += f"\nProtein with code <{code}> WAS SAVED succesfully into {fasta_file_name} with string <<<<< {protein_string} >>>>>\n"
            self.__returned_value = 0
        else:
            # Error
            self.__return_info += f"\nError: {touch_result.stderr}"
            self.__returned_value = 4

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # Returns a vector that contains an aminoacid sequence splitted in lines of 80 characters or less
    def __split_fasta_sequence(self, sequence): # If we write de sequence in the fasta file without calling this function, it will lasta a few seconds less
        result_sequences = [] # We declare a void vector
        for i in range(0, len(sequence), 80): # Iterate over the sequence splitting it in strings of a maximum of 80 characters
            result_sequences.append(sequence[i:i+80])
        return result_sequences

##############################################################################
##############################################################################
##############################################################################
##############################################################################

# MAIN section
getfastaobject = GenerateFasta() # Create an object to isolate the given column name in the given csv path
getfastaobject.run()
#return_status = getfastaobject.get_returned_value()
#return_info = getfastaobject.get_returned_info()

#print (return_info)
#print (return_status)
print ("LLAMADA CON ÉXITO")