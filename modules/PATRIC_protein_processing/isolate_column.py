# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file implements a GeneSys example task that allows the user to
isolate a given column of a .csv into a new .csv. It is
exclusively aimed to work with .csv files downloaded from
PATRIC db, and it has not been tested in other contexts.
"""

import csv

from modules.baseobjects import Task

##############################################################################
##############################################################################
##############################################################################
##############################################################################

class IsolateColumn(Task):
    """
    This class receives a given csv path with raw data downloaded from
    PATRIC databases and isolates a given column from that path
    """
    __csv_path = ""
    __column_name = ""
    __csv_codes_path = "" # This is the parameter that the next step of a patricproteinprocessing workflow, GenerateFasta, might take as an argument. It is creeated right in the previous step of the workflow

    ###### INIT ######

    def __init__(self, csv_path="./", col_name="BRC ID"):
        super().__init__()
        self.__csv_path = csv_path
        self.__column_name = col_name
        self.__csv_codes_path = self.__csv_path[:-4] + "_new.csv"

    ###### GET/SET METHODS ######

    # We include all the parameters that this class has into a dictionary, and we return that dictionary
    def get_parameters(self) -> dict:
        parameters = super().get_parameters()
        parameters['csv_path'] = self.__csv_path
        parameters['column_name'] = self.__column_name
        parameters['csv_codes_path'] = self.__csv_codes_path
        return parameters
    
    # We set the parameters of the class from a dictionary received as an argument, both the superclass parameters and the current class ones
    def set_parameters(self, parameters):
        super().set_parameters(parameters)
        self.__csv_path = parameters['csv_path']
        self.__column_name = parameters['column_name']
        self.__csv_codes_path = parameters['csv_codes_path']

    # Return information that might be useful for the user
    def show_info(self):
        isolate_col_dict = self.to_dict()
        isolate_col_dict.pop('returned_info') # We remove returned info as it is too long to be worth to be showed
        isolate_col_dict.pop('returned_value')
        return str(isolate_col_dict)
    
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
                    self._returned_info = f"Column '{self.__column_name}' found. Starting saving..."
                    self.__save_csv_code_column(gotten_column) # call that will save the column in a new csv

                except Exception as e:
                    self._returned_info = f"Unexpected error occurred while trying to access the column: {e}\nPlease, verify that the specified column exists"
                    self._returned_value = 1

        except FileNotFoundError:
            self._returned_info = f"Cannot find '{self.__csv_path}' file"
            self._returned_value = 2
        
        except Exception as e:
            self._returned_info = f"Unexpected error occurred: {e}"
            self._returned_value = 3
    
    # It saves a given column of data in the specified csv path
    def __save_csv_code_column(self, data):
        try:
            with open(self.__csv_codes_path, 'w', newline='') as csv_file:
                csv_file.write(str(self.__column_name)+'\n') # write column's name
                for row in data:
                    csv_file.write(str(row)+'\n')   # write each row
            self._returned_info += "\nnew CSV file was saved succesfully"
            self._returned_value = 0

        except Exception as e:
            self._returned_info += f"\nUnexpected error occurred: {e}"
            self._returned_value = 3