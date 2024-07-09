# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file provides a full Kivy GUI for GeneSys app
"""

from modules.PATRIC_protein_processing.isolate_column import IsolateColumn
from modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from modules.baseobjects import Workflow
from utils.kivy_utils import update_label_text_size, check_fasta_format, check_json_format, check_txt_format, check_csv_format

import threading # We will use multithreading to execute long tasks while allowing the user to keep using GeneSys' UI
import ctypes

#import smtplib
#from email.message import EmailMessage

import kivy
kivy.require('2.3.0') # replace with your current kivy version!
from kivy.app import App
from kivy.lang import Builder # This is necesary when we have the .kv files in a diferent folder than our main application
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
#from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.core.window import Window
#from kivy.clock import Clock
# from kivy.uix.widget import Widget


###############################################################################
###############################################################################
###############################################################################
###############################################################################
# In the ReduceSampleScreen, check if scientific notation is given properly as an argument
# The file structure has been changed. Reorganize all the imports and re-execute a workflow to make sure it still works
# This class creates a Task that reduces the sample from a given .fasta file,
# given a certain e-value which marks the maximum similarity that will
# determine wether two sequences from that .fasta are similar enough to be
# considered equal
class ReduceSampleScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(ReduceSampleScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4 # Determine how many rows and columns will the GridLayout have
        self.cols = 2

        # Welcome message

        # Add text boxes
        #'''
        fasta_pathname_text_label = Label(text="Please, introduce the pathname to the .fasta file that contains the proteins to reduce (if a previous GenerateFasta task is defined for this workflow, its parameter <__fasta_pathname> value will be taken as this parameter instead of the one given in this text box. If no one is given, <./proteins.fasta> by default): ")
        #update_label_text_size(fasta_pathname_text_label)
        self.add_widget(fasta_pathname_text_label)
        self.fasta_pathname_text_input = TextInput(multiline=False)
        self.add_widget(self.fasta_pathname_text_input)
        
        reduced_sample_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file where to save the reduced sample (<./reduced_proteins.fasta> by default): ")
        #update_label_text_size(reduced_sample_fasta_text_label)
        self.add_widget(reduced_sample_fasta_text_label)
        self.reduced_sample_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.reduced_sample_fasta_text_input)

        '''limit_e_value_text_label = Label(text="Please, introduce the e-value which will be used as the minimum required in order to consider that two proteins are different (notation: 1e<your_value>)(1e-20 by default): ")
        update_label_text_size(limit_e_value_text_label)
        self.add_widget(limit_e_value_text_label)
        self.limit_e_value_text_input = TextInput(multiline=False)
        self.add_widget(self.limit_e_value_text_input)
        #'''

        limit_percentage_text_label = Label(text="Please, introduce the similarity percentage (just the number) which will be used as the minimum required in order to consider that two proteins are different (85 by default): ")
        update_label_text_size(limit_percentage_text_label)
        self.add_widget(limit_percentage_text_label)
        self.limit_percentage_text_input = TextInput(multiline=False)
        self.add_widget(self.limit_percentage_text_input)
        #'''

        # Create a button with margins
        exec_reduce_sample_button = Button(text='Generate task', size_hint=(None, None), size=(150, 50), on_press=self.generate_task)
        exec_reduce_sample_button.bind(texture_size=exec_reduce_sample_button.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_reduce_sample_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # First, we set the pathname to the fasta file with the proteins to reduce given by the user
        fasta_pathname = self.fasta_pathname_text_input.text
        if fasta_pathname.__eq__(""):
            fasta_pathname = "./proteins.fasta"
        # We chekc if the previous task of the workflow stores a specific fasta_pathname.
        # In that case, it will be taken as the fasta_pathname of the new task
        # instead of the one previously set by the user
        workflow_tasks = self.__workflow.get_tasks()
        if len(workflow_tasks) is not 0: # If there are previous tasks in the workflow
            last_task = workflow_tasks[-1] # Get the last task that was added to the workflow
            last_task_dict = last_task.to_dict()
            if last_task_dict['type'] == 'modules.PATRIC_protein_processing.generate_fasta.GenerateFasta': # If the last task of the workflow correspondos to a GenerateFasta object
                print("\n\nTHE LAST TASK OF THE WORKFLOW IS AN GENERATEFASTA OBJECT. FASTA_PATHNAME WILL BE TAKEN FROM ITS PARAMETERS\n\n")
                fasta_pathname = last_task_dict['fasta_pathname']
        
        reduced_sample_pathname = self.reduced_sample_fasta_text_input.text
        if reduced_sample_pathname.__eq__(""): # In case the user did not specify any pathname
            reduced_sample_pathname = "./reduced_proteins.fasta"

        limit_percentage_text = self.limit_percentage_text_input.text
        if limit_percentage_text.__eq__(""):
            limit_percentage_text = "85"
        #limit_e_value = convert_to_scientific_notation(limit_percentage_text)
        try:
            limit_percentage = float(limit_percentage_text)
            if limit_percentage not in range(0,100):
                limit_percentage = False
        except:
            limit_percentage = False

        if not limit_percentage: # Validate if e-value format is correct
            self.limit_percentage_text_input.text = "INCORRECT FORMAT"
        if not check_fasta_format(fasta_pathname): # Validate fasta_pathname as a fasta file
            self.fasta_pathname_text_input.text = "NOT A FASTA FORMAT"
        if not check_fasta_format(reduced_sample_pathname): # Validate reduced_sample_pathname as a fasta file
            self.reduced_sample_fasta_text_input.text = "NOT A FASTA FORMAT"
        if limit_percentage and check_fasta_format(fasta_pathname) and check_fasta_format(reduced_sample_pathname):
            # Create a new task only if the format of the given arguments is correct
            reduce_sample = ReduceSample(fasta_pathname=fasta_pathname,
                                         pathname_to_reduced_proteins=reduced_sample_pathname,
                                         percentage=limit_percentage)
            self.__workflow.add_task(reduce_sample)

            # Return to the workflow screen passing the updated workflow
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = TaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)


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
        protein_codes_text_label = Label(text="Please, introduce protein codes csv's pathname (if a previous IsolateColumn task is defined for this workflow, its returned <csv_codes_path> value will be taken as this parameter instead of the one given in this text box): ")
        update_label_text_size(protein_codes_text_label)
        self.add_widget(protein_codes_text_label)
        self.csv_codes_path = TextInput(multiline=False)
        self.add_widget(self.csv_codes_path)
        
        self.add_widget(Label(text="Please, introduce folder's pathname where to save new fasta files (current folder by default): "))
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
        csv_codes_pathname = self.csv_codes_path.text

        # We chekc if the previous task of the workflow stores a specific csv_codes_path.
        # In that case, that csv_codes_path will be taken as the csv_codes_path of the new task
        # instead of the one previously set by the user
        workflow_tasks = self.__workflow.get_tasks()
        if len(workflow_tasks) is not 0: # If there are previous tasks in the workflow
            last_task = workflow_tasks[-1] # Get the last task that was added to the workflow
            last_task_dict = last_task.to_dict()
            if last_task_dict['type'] == 'modules.PATRIC_protein_processing.isolate_column.IsolateColumn': # If the last task of the workflow correspondos to an IsolateColumn object
                print("\n\nTHE LAST TASK OF THE WORKFLOW IS AN ISOLATECOLUMN OBJECT. CSV_CODES_PATH WILL BE TAKEN FROM ITS PARAMETERS\n\n")
                csv_codes_pathname = last_task_dict['csv_codes_path']
        
        saving_pathname = self.folder_pathname.text
        if saving_pathname.__eq__(""): # In case the user did not specifed any path
            saving_pathname = "./proteins.fasta"

        if not check_fasta_format(saving_pathname):
            self.folder_pathname.text = "NOT A FASTA FORMAT"

        if not check_csv_format(csv_codes_pathname):
            self.csv_codes_path.text = "NOT A CSV FORMAT"
        
        if check_fasta_format(saving_pathname) and check_csv_format(csv_codes_pathname):
            gen_fasta = GenerateFasta(csv_codes_pathname, saving_pathname) # data/muestra_reducida.csv data/fasta_pruebas
            self.__workflow.add_task(gen_fasta)

            # Return to the workflow screen passing the updated workflow
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = TaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
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
        self.add_widget(Label(text="Please, introduce the name of the column that contains protein string's ID (BRC ID by default): "))
        self.columnname = TextInput(multiline=False)
        self.add_widget(self.columnname)

        # Create a button with margins
        exec_isolate_codes_button = Button(text='Generate Task', size_hint=(None, None), size=(150, 50), on_press=self.generate_task)
        exec_isolate_codes_button.bind(texture_size=exec_isolate_codes_button.setter('size'))
        self.add_widget(exec_isolate_codes_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Create a new task and insert it in the workflow
        csv_pathname = self.csvpath.text
        column_name = self.columnname.text
        if column_name.__eq__(""): # In case the user did not specifed any column
            column_name = "BRC ID"

        if check_csv_format(csv_pathname):
            isolate_column = IsolateColumn(csv_pathname, column_name) # data/BVBRC_slatt_domain-containing_protein.csv BRC ID
            self.__workflow.add_task(isolate_column)
            
            # Return to the task selection screen passing the updated workflow
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = TaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
        else:
            self.csvpath.text = "NOT A CSV FORMAT"
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
        self.rows = 6
        self.cols = 1

        # Insertar mensaje de bienvenida

        isolate_codes_button = Button(text='Isolate PATRIC codes', size_hint=(None, None), size=(150, 50), on_press=self.open_isolate_codes_menu)
        isolate_codes_button.bind(texture_size=isolate_codes_button.setter('size'))
        self.add_widget(isolate_codes_button)

        gen_fasta_button = Button(text='Generate ".fasta" files', size_hint=(None, None), size=(150, 50), on_press=self.open_fasta_files_menu)
        gen_fasta_button.bind(texture_size=gen_fasta_button.setter('size'))
        self.add_widget(gen_fasta_button)

        reduce_sample_button = Button(text='Reduce sample', size_hint=(None, None), size=(150, 50), on_press=self.open_reduce_sample_menu)
        reduce_sample_button.bind(texture_size=reduce_sample_button.setter('size'))
        self.add_widget(reduce_sample_button)

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

    def open_reduce_sample_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        reduce_sample_screen = ReduceSampleScreen(self.__workflow) # Open the fasta files generation menu
        self.parent.add_widget(reduce_sample_screen)

    def open_workflow_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = WorkflowScreen(self.__workflow) # Open the isolate codes menu
        self.parent.add_widget(workflow_screen)

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(1, None), size=(200, 200))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.show_info(),
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
        self.add_widget(Label(text="Introduce the pathname where to save .json workflow (./workflow.json by default): "))
        self.jsonpathname = TextInput(multiline=False)
        self.add_widget(self.jsonpathname)
        #self.add_widget(Label(text="Introduce the name of the json file (including <.json> ending)(<workflow.json> by default): "))
        #self.jsonname = TextInput(multiline=False)
        #self.add_widget(self.jsonname)

        # Create a button with margins
        exec_generate_json_button = Button(text='Generate .json file', size_hint=(None, None), size=(150, 50), on_press=self.generate_json)
        exec_generate_json_button.bind(texture_size=exec_generate_json_button.setter('size'))
        self.add_widget(exec_generate_json_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_json(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        if self.jsonpathname.text.__eq__(""):
            self.jsonpathname.text = "./workflow.json"
        json_pathname = self.jsonpathname.text
        if check_json_format(json_pathname):
            self.__workflow.generate_json(path=json_pathname) # Call to generate_json Workflow class method
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            workflow_screen = WorkflowScreen(self.__workflow)
            self.parent.add_widget(workflow_screen)
        else:
            self.jsonpathname.text = "NOT A JSON FORMAT"

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
        json_pathname = self.jsonpathname.text
        if json_pathname == "":
            json_pathname = "./workflow.json"
        if check_json_format(json_pathname):
            self.__workflow.get_from_json(json_path=json_pathname)            
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            workflow_screen = WorkflowScreen(self.__workflow)
            self.parent.add_widget(workflow_screen)
        else:
            self.jsonpathname.text = "NOT A JSON FORMAT"

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class WorkflowScreen(GridLayout):
    # Botón que permita cancelar el workflow actualmente en ejecución. ¿Cómo hago que funcione el workflow si cambio de pantalla? Si vuelves al menú principal, haz que se cancele automáticamente. Nuevo campo booleano en Workflow que indique si se está ejecutando o no, y lo usas para determinar si hay que cancelarlo o no
    # Label que te diga si actualmente hay alguna tarea ejecutándose o no. Requerirá un booleano en la clase Workflow que especifique si se está ejecutando el objeto workflow o no.
    # Clustering y módulos de ciencia de datos
    __workflow = None # This class stores a GeneSys workflow and implements ways to manipulate it
    
    def __init__(self, workflow=Workflow(), **kwargs): # It receives a workflow set as a new, empty workflow by default
        super(WorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.

        self.workflow_thread = None # This is the reference to the thread that will run the workflow
        self.__workflow = workflow
        self.rows = 9 # We ask the GridLayout to manage its children in 1 column and 6 rows.
        self.cols = 1

        # Insert welcome message

        self.add_tasks_button = Button(text='Add tasks to the workflow', size_hint=(None, None), size=(150, 50), on_press=self.open_add_tasks)
        self.add_tasks_button.bind(texture_size=self.add_tasks_button.setter('size'))
        self.add_widget(self.add_tasks_button)

        rm_last_task_button = Button(text='Remove last task from the workflow', size_hint=(None, None), size=(150, 50), on_press=self.rm_last_task)
        rm_last_task_button.bind(texture_size=rm_last_task_button.setter('size'))
        self.add_widget(rm_last_task_button)

        clean_workflow_button = Button(text='Clean workflow', size_hint=(None, None), size=(150, 50), on_press=self.clean_workflow)
        clean_workflow_button.bind(texture_size=clean_workflow_button.setter('size'))
        self.add_widget(clean_workflow_button)

        # Save workflow button that generates a json with the current workflow parameters and objects
        self.save_workflow_button = Button(text='Save workflow in .json format', size_hint=(None, None), size=(150, 50), on_press=self.save_workflow)
        self.save_workflow_button.bind(texture_size=self.save_workflow_button.setter('size'))
        self.add_widget(self.save_workflow_button)

        # Load workflow button that fills the workflow with the data stored in a json file
        self.load_workflow_button = Button(text='Load workflow from a .json file', size_hint=(None, None), size=(150, 50), on_press=self.load_workflow)
        self.load_workflow_button.bind(texture_size=self.load_workflow_button.setter('size'))
        self.add_widget(self.load_workflow_button)

        self.run_workflow_button = Button(text='Run workflow', size_hint=(None, None), size=(150, 50), on_press=self.run_workflow)
        self.run_workflow_button.bind(texture_size=self.run_workflow_button.setter('size'))
        self.add_widget(self.run_workflow_button)

        self.cancel_workflow_button = Button(text='Cancel workflow', size_hint=(None, None), size=(150, 50), on_press=self.cancel_workflow)
        self.cancel_workflow_button.bind(texture_size=self.cancel_workflow_button.setter('size'))
        self.add_widget(self.cancel_workflow_button)
        self.cancel_workflow_button.disabled = True

        # Create a button which allows you to return to the main menu
        self.main_menu_button = Button(text='Return to main menu (the current workflow will be deleted. It is recommended to save it first)', size_hint=(None, None), size=(150, 50), on_press=self.return_to_main_menu)
        self.main_menu_button.bind(texture_size=self.main_menu_button.setter('size'))
        self.add_widget(self.main_menu_button)

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

    def load_workflow(self, instance): # We want to choose where to save JSON file and which name should be goven to it, so we define a specific screen for it
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        load_workflow_screen = GenerateWorkflowFromJsonScreen(self.__workflow) # Open the menu that asks the user where to save current workflow
        self.parent.add_widget(load_workflow_screen)

    def run_workflow(self, instance):
        # Execute the workflow in a separated thread
        self.workflow_thread = threading.Thread(target=self.execute_workflow) # We must specifically define a funciton that runs the workflow, otherwise the workflow will be executed before calling to task_thread.start()
        self.run_workflow_button.disabled = True # Disable buttons
        self.add_tasks_button.disabled = True
        self.save_workflow_button.disabled = True
        self.load_workflow_button.disabled = True
        self.main_menu_button.disabled = True
        self.cancel_workflow_button.disabled = False # Able cancel button
        self.workflow_thread.start()

    def execute_workflow(self):
        self.__workflow.run()
        from kivy.clock import Clock # Update the UI from the main thread using Clock
        Clock.schedule_once(lambda dt: self.on_task_complete(self.__workflow.show_info())) # creates an anonymous function that takes the dt parameter and calls self.on_task_complete and allows to pass workflow_info as a parameter, otherwise, it would be imposible to pass dt and workflow_info at the same time

    def on_task_complete(self, workflow_data=""):
        # Create the popup content
        message_text = "Your Genesys workflow is completed:\n\n" + workflow_data
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        message = Label(text=message_text)
        close_button = Button(text="Close", size_hint=(None, None), size=(100, 50))
        box.add_widget(message) # Add the message and the close button to the layout
        box.add_widget(close_button)
        popup = Popup(title='Workflow completed!', content=box, size_hint=(None, None), size=(300, 200)) # Create pop up
        close_button.bind(on_press=popup.dismiss) # Bind the close button to close the popup
        popup.open() # Open the popup

        self.run_workflow_button.disabled = False # Recover the button functionality (in case we changed of screen, this line will not have any effect)
        self.add_tasks_button.disabled = False
        self.save_workflow_button.disabled = False
        self.load_workflow_button.disabled = False
        self.main_menu_button.disabled = False
        self.cancel_workflow_button.disabled = True

    def cancel_workflow(self, instance):
        if self.workflow_thread is not None: # Kill workflow's execution
            self._kill_thread(self.workflow_thread)
            self.workflow_thread = None
    
    def _kill_thread(self, thread):
        if not thread.is_alive():
            return
        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("Nonexistent thread id")
        elif res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")
    
    def return_to_main_menu(self, instance):
        self.__workflow.clean()
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        menu_screen = MenuScreen() # Open the main menu
        self.parent.add_widget(menu_screen)

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(1, None), size=(200, 200))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.show_info(),
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
# This screen preceeds the creation of a workflow and asks the user to give
# a .txt pathname where to save the results given by workflow's tasks

# SIGUE ABAJO
class SelectResultsPathnameWorkflowScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(SelectResultsPathnameWorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 3
        self.cols = 2

        # Welcome message
        
        # Add text boxes
        self.add_widget(Label(text="Introduce the pathname of the .txt results file of the workflow (<./workflow_results.txt> by default): "))
        self.txtpathname = TextInput(multiline=False)
        self.add_widget(self.txtpathname)

        # Create a button with margins
        exec_create_workflow_button = Button(text='Create workflow', size_hint=(None, None), size=(150, 50), on_press=self.create_workflow)
        exec_create_workflow_button.bind(texture_size=exec_create_workflow_button.setter('size'))
        self.add_widget(exec_create_workflow_button)

    def create_workflow(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Load workflow from json file
        txt_pathname = self.txtpathname.text
        if txt_pathname.__eq__(""):
            txt_pathname = "./workflow_results.txt"
        if check_txt_format(txt_pathname):
            tasks_empty_list = []
            workflow_parameters = {
                'returned_info': '',
                'returned_value': -1,
                'tasks': tasks_empty_list,
                'results_file': txt_pathname
            }
            self.__workflow.set_parameters(workflow_parameters)            
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            workflow_screen = WorkflowScreen(self.__workflow)
            self.parent.add_widget(workflow_screen)
        else:
            self.txtpathname.text = "NOT A TXT FORMAT"

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
        select_results_screen = SelectResultsPathnameWorkflowScreen() # Open the isolate codes menu
        self.parent.add_widget(select_results_screen)

    def open_documentation(self, instance):
        pass # Open PDF with the documentation
        '''
        ##############################################
        ##############################################
        ##############################################
        NOT DONE
        ##############################################
        ##############################################
        ##############################################
        '''

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