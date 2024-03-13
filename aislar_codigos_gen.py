import csv

def get_data():
    path_to_csv = input("Please, introduce csv's pathname: ") # /home/bruno/Documentos/UGR/IngInformatica/Grado/Curso4/TFG/datos/.csv
    id_column_name = input("Please, introduce the name of the column that contains string's ID: ")
    return ( get_codes(path_to_csv, id_column_name) )

##############################################################################
##############################################################################
##############################################################################
##############################################################################

#def save_column(csv_name, data)

##############################################################################
##############################################################################
##############################################################################
##############################################################################

def get_codes(csv_path, column_name):
    try:
        with open(csv_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file) # Let's trait csv file as a list

            # Check if "code_column" exists
            if column_name not in csv_reader.fieldnames:
                print(f"Column '{column_name}' not found.")
                return 1
            
            # Get column's values without column's name
            gotten_column = [row[column_name] for row in csv_reader]
            
            # Save column
            print(f"Column '{column_name}' found. Starting saving...")
            # get csv's new name
            # call to save_column
            for valor in gotten_column:
                print(valor)
            return 0

    except FileNotFoundError:
        print(f"Cannot find '{csv}' file.")
        return 2
    
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return 3

##############################################################################
##############################################################################
##############################################################################
##############################################################################

return_status = get_data()

while return_status != 0:
    get_data()