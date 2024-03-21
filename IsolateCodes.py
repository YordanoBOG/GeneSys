import csv
import argparse

# ALL OF THIS SHOULD BE PRIVATE
# python IsolateCodes -csv ../datos/Hotel_Reservations.csv -col room_type_reserved
# python IsolateCodes -csv ../datos/BVBRC_sp_gene_reverse_transcriptase.csv -col BRC ID

##############################################################################
##############################################################################
##############################################################################
##############################################################################

def make_parser():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Argument parser for csv pathfile and column name which will be isolated')

    # Add arguments
    # ERROR: can't open file '/home/bruno/Documentos/UGR/IngInformatica/Grado/Curso4/TFG/trabajo/IsolateCodes': [Errno 2] No such file or directory
    parser.add_argument('script', help='First argument contains the name o this python script')
    parser.add_argument('path_to_csv', help='Input csv file path')
    parser.add_argument('id_column_name', help="Name of the column that contains string's ID")

    return parser

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# It asks the user to introduce the path to a csv file and the name of the column they want to
# isolate in a new csv, and calls the function that reads the given csv. NO ANYMORE

def get_data():
    args_parser = make_parser() # make parser
    args = args_parser.parse_args() # parse arguments
    return ( process_codes(args.path_to_csv, args.id_column_name) ) # access arguments

    #path_to_csv = input("Please, introduce csv's pathname: ") # ../datos/BVBRC_sp_gene_reverse_transcriptase.csv | ../datos/Hotel_Reservations.csv
    #id_column_name = input("Please, introduce the name of the column that contains string's ID: ") # BRC ID | room_type_reserved
    #return ( process_codes(path_to_csv, id_column_name) )

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# PRE: "header" must have the same number of columns as "data"
# It takes a header and some data to save in a given csv path

def save_csv_code_column(csv_name, header, data):
    return_status = 3
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
# It opens a certain path to a csv file, opens it and saves a new csv file that contains
# the given column name

def process_codes(csv_path, column_name):
    return_status = 3
    try:
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file) # Let's trait csv file as a list

            # Check if "code_column" exists
            if column_name not in csv_reader.fieldnames:
                print(f"Column '{column_name}' not found.")
                return_status = 1
            
            # Get column's values without column's name
            gotten_column = [row[column_name] for row in csv_reader]
            
            # Save column
            print(f"Column '{column_name}' found. Starting saving...")
            new_csv_path = csv_path[:-4] + "_new.csv" # Remove the last 4 characters of csv's path: ".csv" and add "_new.csv" instead
            data_header = [str(column_name)]
            return_status = ( save_csv_code_column(new_csv_path, data_header, gotten_column) ) # call to save column

            #for row in gotten_column:
                #print(row)

    except FileNotFoundError:
        print(f"Cannot find '{csv}' file.")
        return_status = 2
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

    return return_status

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# MAIN. It runs the program till there are no errors in the execution

return_status = get_data()

#while return_status != 0:
#    get_data()
print (return_status)
