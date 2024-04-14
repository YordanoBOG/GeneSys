import csv
import argparse

# Execution through command line:
# python IsolateCodes.py ../datos/Hotel_Reservations.csv room_type_reserved
# python IsolateCodes.py ../datos/BVBRC_sp_gene_reverse_transcriptase.csv BRC ID

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# Creates a parser that allows us to manipulate the arguments
def make_parser():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Argument parser for csv pathfile and column name which will be isolated')

    # Add arguments to the parser
    parser.add_argument('path_to_csv', help='Input csv file path')
    parser.add_argument('id_column_name', help="Name of the column that contains string's ID")

    return parser

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# For security reasons, we are going to create the new csv file with the isolated column using private methods of a class

class IsolateColumn:

    __returned_value = -1
    __csv_path = ""
    __column_name = ""

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################

    def __init__(self, csv_path, column_name):
        self.__csv_path = csv_path
        self.__column_name = column_name

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
    # This is the method which will be called by the user to create a new csv with the isolated column
    def run(self):
        self.__returned_value = self.__process_codes()
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    # This method isolates the requested column form the specified csv path and calls
    # to "save_csv_code_column" to save the column in a new csv
    def __process_codes(self):
        return_status = 3
        try:
            with open(self.__csv_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file) # We trait the csv file as a list
                
                # Isolate column's values
                try:
                    gotten_column = [row[self.__column_name] for row in csv_reader]
                
                # Save column
                    print(f"Column '{self.__column_name}' found. Starting saving...")
                    new_csv_path = self.__csv_path[:-4] + "_new.csv" # Remove the last 4 characters of csv's path: ".csv" and add "_new.csv" instead
                    data_header = [str(self.__column_name)]
                    return_status = ( self.__save_csv_code_column(new_csv_path, data_header, gotten_column) ) # call that will save the column in a new csv

                except Exception as e:
                    print(f"Unexpected error occurred while trying to access the column: {e}")
                    return_status = 1

        except FileNotFoundError:
            print(f"Cannot find '{self.__csv_path}'")
            return_status = 2
        
        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        return return_status
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    
    def __save_csv_code_column(self, csv_name, header, data):
        return_status = 3 # This value will change to 0 if the method executes succesfully
        try:
            with open(csv_name, 'w', newline='') as csv_file:
                for column in header:
                    csv_file.write(str(column)+'\n') # write column's name
                for row in data:
                    csv_file.write(str(row)+'\n')   # write each row

            print("CSV file saved successfully")
            return_status = 0

        except Exception as e:
            print(f"Unexpected error occurred: {e}")

        return return_status

##############################################################################
##############################################################################
##############################################################################
##############################################################################

# MAIN section. It runs the program

args_parser = make_parser() # make parser
args = args_parser.parse_args() # parse parser arguments

isolatecolumnobject = IsolateColumn(args.path_to_csv, args.id_column_name) # Create an object to isolate the given column name in the given csv path
isolatecolumnobject.run()
return_status = isolatecolumnobject.get_returned_value()

#while return_status != 0:
#    get_data()
print (return_status)
