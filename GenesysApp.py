# This provides a Kivy GUI for GeneSYS app
import kivy
kivy.require('2.3.0') # replace with your current kivy version!

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# from kivy.uix.widget import Widget
import subprocess


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# We want to add a certain quantity of buttons (more than 2) to the menu that executes the program that isolates the codes
'''
class AddIsolateCodesButtons(GridLayout):
    def __init__(self, **kwargs):
        super(AddIsolateCodesButtons, self).__init__(**kwargs)
        self.rows = 1
        self.cols = 3
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class generates a fasta file per each protein string code given in a csv file,
# and stores them in a folder which must be specified, too
#'''
class FastaGenerationScreen(GridLayout):
    def __init__(self, **kwargs):
        super(FastaGenerationScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        self.rows = 3 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2
        
        # Add text boxes
        #'''
        self.add_widget(Label(text="Please, introduce protein codes csv's pathname: "))
        self.csv_codes_path = TextInput(multiline=False)
        self.add_widget(self.csv_codes_path)
        self.add_widget(Label(text="Please, introduce folder's pathname where to save new fasta files : "))
        self.folder_pathname = TextInput(multiline=False)
        self.add_widget(self.folder_pathname)
        #'''

        # Create a button with margins
        exec_generate_fasta_button = Button(text='Generate fasta files', size_hint=(None, None), size=(150, 50), on_press=self.execute_get_fasta)
        #exec_generate_fasta_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        #exec_generate_fasta_button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        self.add_widget(exec_generate_fasta_button)

        # Create a button which allows to return to the main menu
        main_menu_button = Button(text='Return to main menu', size_hint=(None, None), size=(150, 50), on_press=self.return_to_main_menu)
        #main_menu_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        #main_menu_button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        self.add_widget(main_menu_button)

        # ¿QUÉ TAL UNA CASILLA QUE EN CASO DE ESTAR MARCADA ESPECIFIQUE QUE LOS .FASTA SE SUBAN A LA NUBE, A GOOGLE DRIVE POR EJEMPLO?

    # Call the script that isolates gene codes with the given arguments
    def execute_get_fasta(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        csv_codes_path = self.csv_codes_path.text
        saving_pathname = self.folder_pathname.text
        subprocess.run(["python", "GenerateFasta.py", csv_codes_path, saving_pathname]) # csv_path and column_name are arguments

    def return_to_main_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        # Open the main menu
        menu_screen = MenuScreen()
        self.parent.add_widget(menu_screen)
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class implements the menu that allows to generate a csv file with the isolated
# protein codes given a certain csv path and a column name
#'''
class IsolateCodesScreen(GridLayout):
    def __init__(self, **kwargs):
        super(IsolateCodesScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        self.rows = 3 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2
        
        # Add text boxes
        self.add_widget(Label(text="Please, introduce csv's pathname: "))
        self.csvpath = TextInput(multiline=False)
        self.add_widget(self.csvpath)
        self.add_widget(Label(text="Please, introduce the name of the column that contains protein string's ID: "))
        self.columnname = TextInput(multiline=False)
        self.add_widget(self.columnname)

        # Create a button with margins
        exec_isolate_codes_button = Button(text='Isolate codes', size_hint=(None, None), size=(150, 50), on_press=self.execute_get_codes)
        #exec_isolate_codes_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        #exec_isolate_codes_button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        self.add_widget(exec_isolate_codes_button)

        # Create a button which allows to return to the main menu
        main_menu_button = Button(text='Return to main menu', size_hint=(None, None), size=(150, 50), on_press=self.return_to_main_menu)
        #main_menu_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        #main_menu_button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        self.add_widget(main_menu_button)

    # Call the script that isolates gene codes with the given arguments
    def execute_get_codes(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        csv_path = self.csvpath.text
        column_name = self.columnname.text
        subprocess.run(["python", "IsolateCodes.py", csv_path, column_name]) # csv_path and column_name are arguments

    def return_to_main_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        # Open the main menu
        menu_screen = MenuScreen()
        self.parent.add_widget(menu_screen)
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class MenuScreen(GridLayout): # This screen will show via buttons all the available functionality of the app
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.rows = 3 # We ask the GridLayout to manage its children in 1 column and 3 rows.
        self.cols = 1

        # Button that opens the menu that isolates PATRIC codes given a csv path and a column name (in the future it may will only receive a CSV path, assuming the column we are searching for is 'BRC ID')
        isolate_codes_button = Button(text='Isolate PATRIC Codes', size_hint=(None, None), size=(150, 50), on_press=self.open_isolate_codes_menu)
        self.add_widget(isolate_codes_button)

        # Button that opens the menu that generates fasta files with protein strings, given a csv path where those proteins' codes are stored in an unique column and a new path where those protein codes will be stored
        generate_fasta_button = Button(text='Generate ".fasta" files', size_hint=(None, None), size=(150, 50), on_press=self.open_fasta_files_menu)
        self.add_widget(generate_fasta_button)

    def open_isolate_codes_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        # Open the isolate codes menu
        isolate_codes_screen = IsolateCodesScreen()
        self.parent.add_widget(isolate_codes_screen)

    def open_fasta_files_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        # Open the fasta files generation menu
        fasta_generation_screen = FastaGenerationScreen()
        self.parent.add_widget(fasta_generation_screen)
        
    '''
    # Main menu dropdown
    self.main_menu = DropDown()
    
    # Submenu buttons
    for i in range(2):
        submenu_button = Button(text=f'Submenu {i + 1}')
        submenu_button.bind(on_release=self.open_submenu)
        self.main_menu.add_widget(submenu_button)

    def open_submenu(self, instance):
        # Close the main menu dropdown
        self.main_menu.dismiss()

        # Create a new dropdown for the submenu
        submenu = DropDown()

        # Add items to the submenu
        for i in range(3):
            submenu_button = Button(text=f'Submenu Item {i + 1}')
            submenu.add_widget(submenu_button)

        # Open the submenu dropdown
        submenu.open(instance)
    #'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class GenesysApp(App):
    def build(self):
        menu = MenuScreen()
        return menu

###############################################################################
###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    GenesysApp().run()
    