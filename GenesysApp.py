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
        self.add_widget(Label(text="Please, introduce the name of the column that contains string's ID: "))
        self.columnname = TextInput(multiline=False)
        self.add_widget(self.columnname)

        # Create a button with margins
        button = Button(text='Execute', size_hint=(None, None), size=(150, 50), on_press=self.execute_get_codes)
        button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        self.add_widget(button)

    # Call the script that isolates gene codes with the given arguments
    def execute_get_codes(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        csv_path = self.csvpath.text
        column_name = self.columnname.text
        subprocess.run(["python", "IsolateCodes.py", csv_path, column_name]) # csv_path and column_name are arguments
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

        # Button that opens the menu who isolates PATRIC codes given a csv path and a column name (in the future it will only receive a CSV path, assuming the column we are searching for is 'BRC ID')
        main_menu_button = Button(text='Isolate PATRIC Codes', size_hint=(None, None), size=(150, 50), on_press=self.open_isolate_codes_menu)
        self.add_widget(main_menu_button)

    def open_isolate_codes_menu(self, instance):
        # Open the isolate codes menu
        isolate_codes_screen = IsolateCodesScreen()
        self.parent.add_widget(isolate_codes_screen)
        
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
    