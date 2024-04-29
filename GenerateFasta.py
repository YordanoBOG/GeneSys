import csv
import argparse
import subprocess

# Execution through command line:
# python GenerateFasta.py ../datos/BVBRC_sp_gene_reverse_transcriptase_new.csv ../datos/fasta
# python GenerateFasta.py ../datos/BVBRC_sp_gene_RNA_directed_RNA_Polymerase_new.csv ../datos/fasta

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# For security reasons, we are going to work through private methods of a class

class GenerateFasta:

    __returned_value = -1
    __return_info = "Oh, no. Something went wrong"
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
        # POR AQUÍ NOS HEMOS QUEDADO
        try:
            protein_code = codes[0]
            get_protein_bash_command_result = subprocess.run(['./getprotein.sh', protein_code], capture_output=True, text=True) # We execute a tiny bash script that executes the proper BV-BRC tool which gets a protein string from its code. The capture_output=True argument captures the output of the command, and text=True decodes the output as text
            if get_protein_bash_command_result.returncode == 0:
                # Call the function that saves the .fasta file
                self.__save_fasta(get_protein_bash_command_result.stdout)
            else:
                # Error
                self.__return_info += f"\nError: {get_protein_bash_command_result.stderr}"
                self.__returned_value = 4

        except Exception as e:
            self.__return_info += f"\nUnexpected error occurred while getting protein strings from protein codes: {e}"
            self.__returned_value = 5

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This function receives the result given by BRC-ID API and stores its protein string in a .fasta file
    # in the path specified by the arguments
    def __save_fasta(self, command_result):
        # rsplit() is used to split the command_result variable starting from the right side
        # (from the end) using blank spaces as delimiters. The [-1] index retrieves the last
        # part after splitting. It's important to note that the given structure of command_result is:
        # "id feature.aa_sequence <given_code> <returned_string>" as the employed BV-BRC "feature.aa_sequence" tool returns a 2x2 matrix
        protein_string = command_result.rsplit(' ', 1)[-1]
        print(protein_string)

##############################################################################
##############################################################################
##############################################################################
##############################################################################

# MAIN section
getfastaobject = GenerateFasta() # Create an object to isolate the given column name in the given csv path
getfastaobject.run()
return_status = getfastaobject.get_returned_value()
return_info = getfastaobject.get_returned_info()

print (return_info)
print()
print (return_status)
print ("LLAMADA CON ÉXITO")