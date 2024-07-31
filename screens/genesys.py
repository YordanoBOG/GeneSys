# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file provides a full Kivy GUI for GeneSys app generic workflow manipulation
"""

from . import patric_protein_processing

from modules.baseobjects import Workflow
from utils.kivy_utils import check_json_format, check_txt_format#, update_label_text_size, check_fasta_format, check_csv_format, check_newick_format

import threading # We will use multithreading to execute long tasks while allowing the user to keep using GeneSys' UI
import ctypes

import kivy
kivy.require('2.3.0') # replace with your current kivy version!
#from kivy.lang import Builder # This is necesary when we have the .kv files in a diferent folder than our main application
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
    __workflow_type = ""

    def __init__(self, type:str, workflow=Workflow(), **kwargs): # It receives a workflow set as a new, empty workflow by default
        super(WorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.

        self.workflow_thread = None # This is the reference to the thread that will run the workflow
        self.__workflow = workflow
        self.__workflow_type = type
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
        if self.__workflow_type.__eq__("PATRIC"):
            task_screen = patric_protein_processing.PatricTaskScreen(workflow=self.__workflow)
            self.parent.add_widget(task_screen)
        # elif sentences if there are more developed screens for a workflow
        else:
            self.return_to_main_menu()

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
    __workflow_type = ""

    def __init__(self, type:str, workflow=Workflow(), **kwargs):
        super(SelectResultsPathnameWorkflowScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.__workflow_type = type # If it is "PATRIC", the menu that contains tasks for manipulating PATRIC databases will be opened
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
            workflow_screen = WorkflowScreen(type=self.__workflow_type, workflow=self.__workflow)
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
        workflow_menu_button = Button(text='Create new PATRIC protein manipulation GeneSys workflow', size_hint=(None, None), size=(150, 50), on_press=self.open_workflow_menu)
        workflow_menu_button.bind(texture_size=workflow_menu_button.setter('size'))
        self.add_widget(workflow_menu_button)

    def open_workflow_menu(self, instance): # menu_key specifies which set of task can be added to the workflow, and it will determine which workflow manipulation screen must be open
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        select_results_screen = SelectResultsPathnameWorkflowScreen(type="PATRIC") # Open the isolate codes menu
        self.parent.add_widget(select_results_screen)

