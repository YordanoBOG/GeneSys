# This provides a Kivy GUI for GeneSYS app
import kivy
kivy.require('2.3.0') # replace with your current kivy version!

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
# from kivy.uix.widget import Widget
import subprocess

###############################################################################
###############################################################################
###############################################################################
###############################################################################

# class TextBox

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class MenuScreen(GridLayout):
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        self.rows = 3 # We ask the GridLayout to manage its children in two columns and add a Label and a TextInput for the username and password.
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