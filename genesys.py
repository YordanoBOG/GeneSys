# This provides a Kivy GUI for GeneSYS app
import kivy
kivy.require('2.3.0') # replace with your current kivy version!

from utils.patricproteinprocessing import IsolateColumn, GenerateFasta
from utils.baseobjects import Workflow

from kivy.app import App
from kivy.lang import Builder # This is necesary when we have the .kv files in a diferent folder than our main application
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
#from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
# from kivy.uix.widget import Widget

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# dic parameter is not necesary. By default, this function will receive a workflow and
# return it as a dictionary
'''
def workflow_to_dict(workflow: Workflow, dic = {}):
    dic['workflow'] = workflow
    return dic
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class generates a fasta file per each protein string code given in a csv file,
# and stores them in a folder which must be specified, too
#'''
class FastaGenerationScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(FastaGenerationScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2

        # Welcome message

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
        exec_generate_fasta_button = Button(text='Generate task', size_hint=(None, None), size=(150, 50), on_press=self.generate_task)
        #exec_generate_fasta_button.pos_hint = {'center_x': 0.5, 'center_y': 0.5}  # Position the button at the center of the layout
        #exec_generate_fasta_button.padding = [20, 20]  # Set padding/margins (left and right: 20 pixels, top and bottom: 20 pixels)
        exec_generate_fasta_button.bind(texture_size=exec_generate_fasta_button.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_generate_fasta_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Create a new task and update the workflow
        csv_codes_path = self.csv_codes_path.text
        saving_pathname = self.folder_pathname.text
        gen_fasta = GenerateFasta(csv_codes_path, saving_pathname) # ../data/muestra_reducida.csv ../data/fasta_pruebas
        self.__workflow.add_task(gen_fasta)

        # Return to the workflow screen passing the updated workflow
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = TaskScreen(self.__workflow)
        self.parent.add_widget(task_screen)
        '''
        csv_codes_path = self.csv_codes_path.text
        saving_pathname = self.folder_pathname.text
        gen_fasta = task.GenerateFasta(csv_codes_path, saving_pathname) # ../data/muestra_reducida.csv ../data/fasta_pruebas
                                                                         # ../data/BVBRC_slatt_domain-containing_protein_new.csv ../data/fasta
        gen_fasta.run()
        #subprocess.run(["python", "utils/GenerateFasta.py", csv_codes_path, saving_pathname]) # csv_path and column_name are arguments
        '''
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class implements the menu that allows to generate a csv file with the isolated
# protein codes given a certain csv path and a column name
#'''
class IsolateCodesScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(IsolateCodesScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2

        # Welcome message
        
        # Add text boxes
        self.add_widget(Label(text="Please, introduce csv's pathname: "))
        self.csvpath = TextInput(multiline=False)
        self.add_widget(self.csvpath)
        self.add_widget(Label(text="Please, introduce the name of the column that contains protein string's ID: "))
        self.columnname = TextInput(multiline=False)
        self.add_widget(self.columnname)

        # Create a button with margins
        exec_isolate_codes_button = Button(text='Generate Task', size_hint=(None, None), size=(150, 50), on_press=self.generate_task)
        exec_isolate_codes_button.bind(texture_size=exec_isolate_codes_button.setter('size'))
        self.add_widget(exec_isolate_codes_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Create a new task and insert it in the workflow
        csv_path = self.csvpath.text
        column_name = self.columnname.text
        isolate_column = IsolateColumn(csv_path, column_name) # ../data/BVBRC_slatt_domain-containing_protein.csv BRC ID
        self.__workflow.add_task(isolate_column)
        
        # Return to the task selection screen passing the updated workflow
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = TaskScreen(self.__workflow)
        self.parent.add_widget(task_screen)
        '''
        isolate_column.run()
        print(isolate_column.get_parameters()['returned_info'])
        #subprocess.run(["python", "utils/IsolateCodes.py", csv_path, column_name]) # csv_path and column_name are arguments
        '''
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class TaskScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow: Workflow, **kwargs):
        super(TaskScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 5 # We ask the GridLayout to manage its children in 1 column and 3 rows.
        self.cols = 1 # Igualno renta predefinir estas cosas

        # Insertar mensaje de bienvenida

        isolate_codes_button = Button(text='Isolate PATRIC codes', size_hint=(None, None), size=(150, 50), on_press=self.open_isolate_codes_menu)
        isolate_codes_button.bind(texture_size=isolate_codes_button.setter('size'))
        self.add_widget(isolate_codes_button)

        gen_fasta_button = Button(text='Generate ".fasta" files', size_hint=(None, None), size=(150, 50), on_press=self.open_fasta_files_menu)
        gen_fasta_button.bind(texture_size=gen_fasta_button.setter('size'))
        self.add_widget(gen_fasta_button)

        # Button that opens the menu that allows manipulating all options concerning a workflow
        workflow_menu_button = Button(text='Return to workflow menu', size_hint=(None, None), size=(150, 50), on_press=self.open_workflow_menu)
        workflow_menu_button.bind(texture_size=workflow_menu_button.setter('size'))
        self.add_widget(workflow_menu_button)

        self.show_workflow_info()

    def open_isolate_codes_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        isolate_codes_screen = IsolateCodesScreen(self.__workflow) # Open the isolate codes menu
        self.parent.add_widget(isolate_codes_screen)

    def open_fasta_files_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        fasta_generation_screen = FastaGenerationScreen(self.__workflow) # Open the fasta files generation menu
        self.parent.add_widget(fasta_generation_screen)

    def open_workflow_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(self.__workflow) # Open the isolate codes menu
        self.parent.add_widget(workflow_screen)

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(1, None), size=(200, 200))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.__str__(),
                                    size_hint=(None, None),
                                    size=(200, 200),
                                    halign='center',
                                    valign='middle',
                                    text_size=(Window.width, None)
                                )
        workflow_info_label.bind(texture_size=workflow_info_label.setter('size'))
        scroll_view.add_widget(workflow_info_label)
        self.add_widget(scroll_view)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This screen allows the user to choose where to save the workflow in json format
# and the name of the .json file
class GenerateJsonScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(GenerateJsonScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4
        self.cols = 2

        # Welcome message
        
        # Add text boxes
        self.add_widget(Label(text="Introduce the path where to save .json workflow (current path by default): "))
        self.jsonpath = TextInput(multiline=False)
        self.add_widget(self.jsonpath)
        self.add_widget(Label(text="Introduce the name of the json file (including <.json> ending)(<workflow.json> by default): "))
        self.jsonname = TextInput(multiline=False)
        self.add_widget(self.jsonname)

        # Create a button with margins
        exec_generate_json_button = Button(text='Generate .json file', size_hint=(None, None), size=(150, 50), on_press=self.generate_json)
        exec_generate_json_button.bind(texture_size=exec_generate_json_button.setter('size'))
        self.add_widget(exec_generate_json_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_json(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Call to generate_json Workflow class method
        if self.jsonpath.text == "":
            self.jsonpath.text = "."
        if self.jsonname.text == "":
            self.jsonname.text = "workflow.json"
        json_pathname = self.jsonpath.text + "/" + self.jsonname.text
        self.__workflow.generate_json(path=json_pathname)
        
        # Return to the Workflow screen
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(self.__workflow)
        self.parent.add_widget(workflow_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This screen allows the user to give a .json path which will load a workflow
# previously saved in that path
class GenerateWorkflowFromJsonScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(GenerateWorkflowFromJsonScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 3
        self.cols = 2

        # Welcome message
        
        # Add text boxes
        self.add_widget(Label(text="Introduce the pathname of the .json workflow (<./workflow.json> by default): "))
        self.jsonpathname = TextInput(multiline=False)
        self.add_widget(self.jsonpathname)

        # Create a button with margins
        exec_generate_workflow_button = Button(text='Load workflow from json', size_hint=(None, None), size=(150, 50), on_press=self.generate_workflow)
        exec_generate_workflow_button.bind(texture_size=exec_generate_workflow_button.setter('size'))
        self.add_widget(exec_generate_workflow_button)

    def generate_workflow(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Load workflow from json file
        if self.jsonpathname.text == "":
            self.jsonpathname.text = "./workflow.json"
        self.__workflow.get_from_json(json_path=self.jsonpathname.text)
        
        # Return to the Workflow screen passing the updated workflow
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(self.__workflow)
        self.parent.add_widget(workflow_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class WorkflowScreen(GridLayout):

    __workflow = None # This class stores a GeneSys workflow and implements ways to manipulate it

    def __init__(self, workflow=Workflow(), **kwargs): # It receives a workflow set as a new, empty workflow by default
        super(WorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.

        self.__workflow = workflow
        self.rows = 8 # We ask the GridLayout to manage its children in 1 column and 6 rows.
        self.cols = 1

        # Insertar mensaje de bienvenida (ocupa una fila)

        add_tasks_button = Button(text='Add tasks to the workflow', size_hint=(None, None), size=(150, 50), on_press=self.open_add_tasks)
        add_tasks_button.bind(texture_size=add_tasks_button.setter('size'))
        self.add_widget(add_tasks_button)

        rm_last_task_button = Button(text='Remove last task from the workflow', size_hint=(None, None), size=(150, 50), on_press=self.rm_last_task)
        rm_last_task_button.bind(texture_size=rm_last_task_button.setter('size'))
        self.add_widget(rm_last_task_button)

        clean_workflow_button = Button(text='Clean workflow', size_hint=(None, None), size=(150, 50), on_press=self.clean_workflow)
        clean_workflow_button.bind(texture_size=clean_workflow_button.setter('size'))
        self.add_widget(clean_workflow_button)

        # Save workflow button that generates a json with the current workflow parameters and objects
        save_workflow_button = Button(text='Save workflow in .json format', size_hint=(None, None), size=(150, 50), on_press=self.save_workflow)
        save_workflow_button.bind(texture_size=save_workflow_button.setter('size'))
        self.add_widget(save_workflow_button)

        # Load workflow button that fills the workflow with the data stored in a json file
        load_workflow_button = Button(text='Load workflow from a .json file', size_hint=(None, None), size=(150, 50), on_press=self.load_workflow)
        load_workflow_button.bind(texture_size=load_workflow_button.setter('size'))
        self.add_widget(load_workflow_button)

        # Create a button which allows you to return to the main menu
        main_menu_button = Button(text='Return to main menu (the current workflow will be deleted. It is recommended to save it first)', size_hint=(None, None), size=(150, 50), on_press=self.return_to_main_menu)
        main_menu_button.bind(texture_size=main_menu_button.setter('size'))
        self.add_widget(main_menu_button)

        # Show current workflow in a non-editable text window
        self.show_workflow_info()
    
    def open_add_tasks(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = TaskScreen(self.__workflow)
        self.parent.add_widget(task_screen)

    def rm_last_task(self, instance):
        self.__workflow.remove_last_task()
        for widget in self.children: # Remove the current widget that we are using for the workflow
            if hasattr(widget, 'id') and widget.id == 'WorkflowScrollView': # Remove the widget if it has the ID attribute set and it is our workflow's scrollbar
                self.remove_widget(widget)
                break
        self.show_workflow_info()

    def clean_workflow(self, instance):
        self.__workflow.clean()
        for widget in self.children: # Remove the current widget that we are using for the workflow
            if hasattr(widget, 'id') and widget.id == 'WorkflowScrollView': # Remove the widget if it has the ID attribute set and it is our workflow's scrollbar
                self.remove_widget(widget)
                break
        self.show_workflow_info() # Show the current workflow in a new widget

    def save_workflow(self, instance): # Poder elegir dónde lo guardamos y cómo llamar al fichero .json, lo que requiere una nueva ventana
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        save_workflow_screen = GenerateJsonScreen(self.__workflow) # Open the menu that asks the user where to save current workflow
        self.parent.add_widget(save_workflow_screen)

    def load_workflow(self, instance): # Poder elegir dónde lo guardamos y cómo llamar al fichero .json, lo que requiere una nueva ventana
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        load_workflow_screen = GenerateWorkflowFromJsonScreen(self.__workflow) # Open the menu that asks the user where to save current workflow
        self.parent.add_widget(load_workflow_screen)
    
    def return_to_main_menu(self, instance):
        self.__workflow.clean()
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        menu_screen = MenuScreen() # Open the main menu
        self.parent.add_widget(menu_screen)

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(1, None), size=(200, 200))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.__str__(),
                                    size_hint=(None, None),
                                    size=(200, 200),
                                    halign='center',
                                    valign='middle',
                                    text_size=(Window.width, None)
                                )
        workflow_info_label.bind(texture_size=workflow_info_label.setter('size'))
        scroll_view.add_widget(workflow_info_label)
        scroll_view.id = 'WorkflowScrollView' # It is crucial to asign an ID to this widget as we may need to remove it specifically at some point
        self.add_widget(scroll_view)

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class MenuScreen(GridLayout): # This screen will show via buttons all the available functionality of the app
    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.rows = 3 # We ask the GridLayout to manage its children in 1 column and 3 rows.
        self.cols = 1

        # Insertar mensaje de bienvenida

        # Button that opens the menu that allows manipulating all options concerning a workflow
        workflow_menu_button = Button(text='Create new GeneSys workflow', size_hint=(None, None), size=(150, 50), on_press=self.open_workflow_menu)
        workflow_menu_button.bind(texture_size=workflow_menu_button.setter('size'))
        self.add_widget(workflow_menu_button)

        # Button that opens documentation of GeneSys project
        view_documentation_button = Button(text='View documentation', size_hint=(None, None), size=(150, 50), on_press=self.open_documentation)
        view_documentation_button.bind(texture_size=view_documentation_button.setter('size'))
        self.add_widget(view_documentation_button)

    def open_workflow_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen() # Open the isolate codes menu
        self.parent.add_widget(workflow_screen)

    def open_documentation(self, instance):
        pass # Open PDF with the documentation
        
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
        Builder.load_file('kv_files/genesys.kv') # We use the Builder class to explicitly load the .kv file
        menu = MenuScreen()
        return menu

###############################################################################
###############################################################################
###############################################################################
###############################################################################

if __name__ == '__main__':
    GenesysApp().run()