import csv
import argparse

# Execution through command line:
# python IsolateCodes.py ../datos/Hotel_Reservations.csv room_type_reserved
# python IsolateCodes.py ../datos/BVBRC_slatt_domain-containing_protein.csv BRC ID

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# For security reasons, we are going to create the new csv file with the isolated column using private methods of a class

class IsolateColumn:

    __returned_value = -1
    __return_info = "Oh, no. Something went wrong"
    __csv_path = ""
    __column_name = ""
    __parser = None # parser that allows us to manipulate the arguments within each class object

    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################

    def __init__(self):
        # Create object's parser in order to manipulate arguments
        self.__parser = argparse.ArgumentParser(description='Argument parser for csv pathfile and column name which will be isolated')
        self.__parser.add_argument('path_to_csv', help='Input csv file path')
        self.__parser.add_argument('id_column_name', help="Name of the column that contains string's ID")
        args = self.__parser.parse_args() # parse parser arguments

        self.__csv_path = args.path_to_csv
        self.__column_name = args.id_column_name

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
    # This is the method which will be called by the user to create a new csv with the isolated column
    def run(self):
        self.__process_codes()
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
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
                    self.__return_info = f"Column '{self.__column_name}' found. Starting saving..."
                    new_csv_path = self.__csv_path[:-4] + "_new.csv" # Remove the last 4 characters of csv's path: ".csv" and add "_new.csv" instead
                    self.__save_csv_code_column(new_csv_path, gotten_column) # call that will save the column in a new csv

                except Exception as e:
                    self.__return_info = f"Unexpected error occurred while trying to access the column: {e}\nPlease, verify that the specified column exists"
                    self.__returned_value = 1

        except FileNotFoundError:
            self.__return_info = f"Cannot find '{self.__csv_path}' file"
            self.__returned_value = 2
        
        except Exception as e:
            self.__return_info = f"Unexpected error occurred: {e}"
            self.__returned_value = 3
    
    ##############################################################################
    ##############################################################################
    ##############################################################################
    ##############################################################################
    
    def __save_csv_code_column(self, csv_name, data):
        try:
            with open(csv_name, 'w', newline='') as csv_file:
                csv_file.write(str(self.__column_name)+'\n') # write column's name
                for row in data:
                    csv_file.write(str(row)+'\n')   # write each row
            self.__return_info += "\nnew CSV file was saved succesfully"
            self.__returned_value = 0

        except Exception as e:
            self.__return_info += f"\nUnexpected error occurred: {e}"
            self.__returned_value = 3

##############################################################################
##############################################################################
##############################################################################
##############################################################################

# MAIN section. It runs the program

isolatecolumnobject = IsolateColumn() # Create an object to isolate the given column name in the given csv path
isolatecolumnobject.run()
return_status = isolatecolumnobject.get_returned_value()
return_info = isolatecolumnobject.get_returned_info()

print (return_info)
print (return_status)