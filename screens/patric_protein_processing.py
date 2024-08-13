# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file provides a full Kivy GUI for GeneSys app
"""

from . import genesys

from modules.PATRIC_protein_processing.isolate_column import IsolateColumn
from modules.PATRIC_protein_processing.generate_fasta import GenerateFasta
from modules.PATRIC_protein_processing.reduce_sample import ReduceSample
from modules.PATRIC_protein_processing.get_30kb_upanddown import Get30KbProteins
from modules.PATRIC_protein_processing.get_codons_from_features import GetCodonsFromFeatures
#from modules.PATRIC_protein_processing.from_ordered_newick_to_fasta import FromOrderedNewickToFasta
from modules.baseobjects import Workflow
#from utils.kivy_utils import update_label_text_size #, convert_to_scientific_notation
from utils.check_format_utils import check_fasta_format, check_csv_format, check_json_format #, check_newick_format

#import threading # We will use multithreading to execute long tasks while allowing the user to keep using GeneSys' UI
#import ctypes

#import smtplib
#from email.message import EmailMessage

import kivy
kivy.require('2.3.0') # replace with your current kivy version!
from kivy.uix.gridlayout import GridLayout
#from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
#from kivy.uix.dropdown import DropDown
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
#from kivy.uix.popup import Popup
from kivy.core.window import Window
#from kivy.clock import Clock
# from kivy.uix.widget import Widget


'''
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
class FromOrderedNewickToFastaScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(FromOrderedNewickToFastaScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4 # Determine how many rows and columns will the GridLayout have
        self.cols = 2

        # Welcome message

        # Add text boxes
        newick_pathname_text_label = Label(text="Please, introduce the pathname to the .newick file that contains the ordered protein codes (<./proteins.newick> by default): ")
        self.add_widget(newick_pathname_text_label)
        self.newick_pathname_text_input = TextInput(multiline=False)
        self.add_widget(self.newick_pathname_text_input)
        
        reduced_sample_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file that sotres the reduced proteins sample (<./reduced_proteins.fasta> by default): ")
        self.add_widget(reduced_sample_fasta_text_label)
        self.reduced_sample_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.reduced_sample_fasta_text_input)

        # Create a button with margins
        exec_reorder_proteins_sample_button = Button(text='Generate task', size_hint=(None, None), size=(150, 50), on_press=self.generate_task)
        exec_reorder_proteins_sample_button.bind(texture_size=exec_reorder_proteins_sample_button.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_reorder_proteins_sample_button)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # First, we set the pathname to the fasta file with the proteins to reduce given by the user
        newick_pathname = self.newick_pathname_text_input.text
        if newick_pathname.__eq__(""):
            newick_pathname = "./proteins.newick"

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

        if not check_newick_format(newick_pathname): # Validate fasta_pathname as a fasta file
            self.newick_pathname_text_input.text = "NOT A NEWICK FORMAT"
        if not check_fasta_format(reduced_sample_pathname): # Validate reduced_sample_pathname as a fasta file
            self.reduced_sample_fasta_text_input.text = "NOT A FASTA FORMAT"
        if check_newick_format(newick_pathname) and check_fasta_format(reduced_sample_pathname):
            # Create a new task only if the format of the given arguments is correct
            reduce_sample = FromOrderedNewickToFasta(newick_pathname=newick_pathname,
                                         pathname_to_reduced_proteins=reduced_sample_pathname)
            self.__workflow.add_task(reduce_sample)

            # Return to the workflow screen passing the updated workflow
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class creates a Task that recognizes the stop codons contained in a fasta file
# that stores some aminoacid sequences corresponding each to all the proteins that surround
# a given SLAT domain containing protein bait. It creates a dicitonary where each key is a bait
# and its corresponding value is a list of all the proteins that surround the bait.
# It returns a json file with the dictionary.
class RecognizeCodonsScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(RecognizeCodonsScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 3
        self.cols = 2

        # Add text boxes
        #'''        
        feature_regions_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file where the features are stored (<./feature_regions.fasta> by default)(If a previous Get30KBScreen task is defined for this workflow, its parameter <__pathname_to_feature_proteins> value will be taken as this parameter instead of the one given in this text box): ")
        self.add_widget(feature_regions_fasta_text_label)
        self.feature_regions_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.feature_regions_fasta_text_input)

        json_results_label = Label(text="Please, introduce the pathname of the .json file where to save the recognized codons (<./codons.json> by default): ")
        self.add_widget(json_results_label)
        self.json_results_text_input = TextInput(multiline=False)
        self.add_widget(self.json_results_text_input)
        #'''

        # Button to create de task
        exec_recognize_codons = Button(text='Generate task',
                                        size_hint=(None, None),
                                        size=(300, 100),
                                        halign='center',
                                        on_press=self.generate_task)
        exec_recognize_codons.bind(texture_size=exec_recognize_codons.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_recognize_codons)

        # Button to return to task selection screen
        exec_return_to_task_screen = Button(text='Return to task selection menu',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.return_to_task_screen)
        exec_return_to_task_screen.bind(texture_size=exec_return_to_task_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_task_screen)

    # Call the script that recognizes the codons
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        feature_regions_fasta_pathname = self.feature_regions_fasta_text_input.text
        if feature_regions_fasta_pathname.__eq__(""):
            feature_regions_fasta_pathname = "./feature_regions.fasta"

        json_results_pathname = self.json_results_text_input.text
        if json_results_pathname.__eq__(""):
            json_results_pathname = "./codons.json"

        # We chekc if the previous task of the workflow stores a specific __pathname_to_feature_proteins.
        # In that case, it will be taken as the __pathname_to_feature_proteins parameter of the new task
        # instead of the one set by the user
        workflow_tasks = self.__workflow.get_tasks()
        if len(workflow_tasks) is not 0: # If there are previous tasks in the workflow
            last_task = workflow_tasks[-1] # Get the last task that was added to the workflow
            last_task_dict = last_task.to_dict()
            if last_task_dict['type'] == 'modules.PATRIC_protein_processing.get_30kb_upanddown.Get30KbProteins': # If the last task of the workflow correspondos to a Get30KbProteins object
                print("\n\nTHE LAST TASK OF THE WORKFLOW IS A Get30KbProteins OBJECT. __pathname_to_feature_proteins WILL BE TAKEN FROM ITS PARAMETERS\n\n")
                feature_regions_fasta_pathname = last_task_dict['pathname_to_feature_proteins']

        # Check formats
        if not check_json_format(json_results_pathname):
            self.json_results_text_input.text = "NOT A JSON FORMAT"
        if not check_fasta_format(feature_regions_fasta_pathname):
            self.feature_regions_fasta_text_input.text = "NOT A FASTA FORMAT"
        
        if check_json_format(json_results_pathname) and check_fasta_format(feature_regions_fasta_pathname):
            # Create a new task only if the format of the given arguments is correct
            get_codons = GetCodonsFromFeatures(pathname_to_feature_proteins=feature_regions_fasta_pathname,
                                               pathname_to_json_results=json_results_pathname,
                                              )
            self.__workflow.add_task(get_codons)
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
            
    def return_to_task_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = PatricTaskScreen(workflow=self.__workflow)
        self.parent.add_widget(task_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class creates a Task that gets a maximum 30,000 kilobases up and down from each protein
# contained in a fasta file, corresponding to proteins that surround the ones
# stored in the fasta, which work as baits for their respective surrounding proteins.
class Get30KBScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(Get30KBScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 3
        self.cols = 2

        # Add text boxes
        #'''        
        reduced_sample_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file where the reduced sample is saved (<./reduced_proteins.fasta> by default)(If a previous ReduceSample task is defined for this workflow, its parameter <__pathname_to_reduced_proteins> value will be taken as this parameter instead of the one given in this text box): ")
        self.add_widget(reduced_sample_fasta_text_label)
        self.reduced_sample_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.reduced_sample_fasta_text_input)

        feature_regions_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file where to save the features regions of the proteins (<./feature_regions.fasta> by default): ")
        self.add_widget(feature_regions_fasta_text_label)
        self.feature_regions_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.feature_regions_fasta_text_input)
        #'''

        # Create a button with margins
        exec_get_features = Button(text='Generate task',
                                    size_hint=(None, None),
                                    size=(300, 100),
                                    halign='center',
                                    on_press=self.generate_task)
        exec_get_features.bind(texture_size=exec_get_features.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_get_features)

        # Button to return to task selection screen
        exec_return_to_task_screen = Button(text='Return to task selection menu',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.return_to_task_screen)
        exec_return_to_task_screen.bind(texture_size=exec_return_to_task_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_task_screen)

    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        reduced_sample_fasta_pathname = self.reduced_sample_fasta_text_input.text
        if reduced_sample_fasta_pathname.__eq__(""):
            reduced_sample_fasta_pathname = "./reduced_proteins.fasta"

        feature_regions_fasta_pathname = self.feature_regions_fasta_text_input.text
        if feature_regions_fasta_pathname.__eq__(""):
            feature_regions_fasta_pathname = "./feature_regions.fasta"

        # We chekc if the previous task of the workflow stores a specific __pathname_to_reduced_proteins.
        # In that case, it will be taken as the __pathname_to_reduced_proteins parameter of the new task
        # instead of the one set by the user
        workflow_tasks = self.__workflow.get_tasks()
        if len(workflow_tasks) is not 0: # If there are previous tasks in the workflow
            last_task = workflow_tasks[-1] # Get the last task that was added to the workflow
            last_task_dict = last_task.to_dict()
            if last_task_dict['type'] == 'modules.PATRIC_protein_processing.reduce_sample.ReduceSample': # If the last task of the workflow correspondos to a ReduceSample object
                print("\n\nTHE LAST TASK OF THE WORKFLOW IS AN REDUCESAMPLE OBJECT. __pathname_to_reduced_proteins WILL BE TAKEN FROM ITS PARAMETERS\n\n")
                reduced_sample_fasta_pathname = last_task_dict['pathname_to_reduced_proteins']

        # Check fasta format
        if not check_fasta_format(reduced_sample_fasta_pathname): # Validate fasta_pathname as a fasta file
            self.reduced_sample_fasta_text_input.text = "NOT A FASTA FORMAT"
        if not check_fasta_format(feature_regions_fasta_pathname):
            self.feature_regions_fasta_text_input.text = "NOT A FASTA FORMAT"
        
        if check_fasta_format(reduced_sample_fasta_pathname) and check_fasta_format(feature_regions_fasta_pathname):
            # Create a new task only if the format of the given arguments is correct
            get_30kb = Get30KbProteins(pathname_to_reduced_proteins=reduced_sample_fasta_pathname,
                                       pathname_to_feature_proteins=feature_regions_fasta_pathname)
            self.__workflow.add_task(get_30kb)
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
            
    def return_to_task_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = PatricTaskScreen(workflow=self.__workflow)
        self.parent.add_widget(task_screen)

###############################################################################
###############################################################################
###############################################################################
###############################################################################
# This class creates a Task that reduces the sample from a given .fasta file,
# given a certain percentage which marks the maximum similarity that will
# determine wether two sequences from the .fasta are similar enough to be
# considered from the same family
class ReduceSampleScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow=Workflow(), **kwargs):
        super(ReduceSampleScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 4 # Determine how many rows and columns will the GridLayout have
        self.cols = 2

        # Add text boxes
        #'''
        fasta_pathname_text_label = Label(text="Please, introduce the pathname to the .fasta file that contains the proteins to reduce (if a previous GenerateFasta task is defined for this workflow, its parameter <__fasta_pathname> value will be taken as this parameter instead of the one given in this text box. If no one is given, <./proteins.fasta> by default): ")
        self.add_widget(fasta_pathname_text_label)
        self.fasta_pathname_text_input = TextInput(multiline=False)
        self.add_widget(self.fasta_pathname_text_input)
        
        reduced_sample_fasta_text_label = Label(text="Please, introduce the pathname of the .fasta file where to save the reduced sample (<./reduced_proteins.fasta> by default): ")
        self.add_widget(reduced_sample_fasta_text_label)
        self.reduced_sample_fasta_text_input = TextInput(multiline=False)
        self.add_widget(self.reduced_sample_fasta_text_input)

        limit_percentage_text_label = Label(text="Please, introduce the similarity percentage (just the number) which will be used as the minimum required in order to consider that two proteins are different (85 by default): ")
        self.add_widget(limit_percentage_text_label)
        self.limit_percentage_text_input = TextInput(multiline=False)
        self.add_widget(self.limit_percentage_text_input)
        #'''

        # Create a button with margins
        exec_reduce_sample_button = Button(text='Generate task',
                                           size_hint=(None, None),
                                           size=(300, 100),
                                           halign='center',
                                           on_press=self.generate_task)
        exec_reduce_sample_button.bind(texture_size=exec_reduce_sample_button.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_reduce_sample_button)

        # Button to return to task selection screen
        exec_return_to_task_screen = Button(text='Return to task selection menu',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.return_to_task_screen)
        exec_return_to_task_screen.bind(texture_size=exec_return_to_task_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_task_screen)

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
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)

    def return_to_task_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = PatricTaskScreen(workflow=self.__workflow)
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
        self.rows = 3 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2

        # Welcome message

        # Add text boxes
        #'''
        protein_codes_text_label = Label(text="Please, introduce protein codes csv's pathname (if a previous IsolateColumn task is defined for this workflow, its returned <csv_codes_path> value will be taken as this parameter instead of the one given in this text box): ")
        self.add_widget(protein_codes_text_label)
        self.csv_codes_path = TextInput(multiline=False)
        self.add_widget(self.csv_codes_path)
        
        self.add_widget(Label(text="Please, introduce folder's pathname where to save new fasta files (current folder by default): "))
        self.folder_pathname = TextInput(multiline=False)
        self.add_widget(self.folder_pathname)
        #'''

        # Create a button with margins
        exec_generate_fasta_button = Button(text='Generate task',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.generate_task)
        exec_generate_fasta_button.bind(texture_size=exec_generate_fasta_button.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_generate_fasta_button)

        # Button to return to task selection screen
        exec_return_to_task_screen = Button(text='Return to task selection menu',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.return_to_task_screen)
        exec_return_to_task_screen.bind(texture_size=exec_return_to_task_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_task_screen)

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
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)

    def return_to_task_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = PatricTaskScreen(workflow=self.__workflow)
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
        self.rows = 3 # We ask the GridLayout to manage its children in two columns and 3 rows.
        self.cols = 2
        
        # Add text boxes
        self.add_widget(Label(text="Please, introduce csv's pathname: "))
        self.csvpath = TextInput(multiline=False)
        self.add_widget(self.csvpath)
        self.add_widget(Label(text="Please, introduce the name of the column that contains protein string's ID (BRC ID by default): "))
        self.columnname = TextInput(multiline=False)
        self.add_widget(self.columnname)

        # Create a button with margins
        exec_isolate_codes_button = Button(text='Generate Task',
                                           size_hint=(None, None),
                                           size=(300, 100),
                                           halign='center',
                                           on_press=self.generate_task)
        exec_isolate_codes_button.bind(texture_size=exec_isolate_codes_button.setter('size'))
        self.add_widget(exec_isolate_codes_button)

        # Button to return to task selection screen
        exec_return_to_task_screen = Button(text='Return to task selection menu',
                                            size_hint=(None, None),
                                            size=(300, 100),
                                            halign='center',
                                            on_press=self.return_to_task_screen)
        exec_return_to_task_screen.bind(texture_size=exec_return_to_task_screen.setter('size')) # The size of the button adapts automatically depending on the length of the text that it contains
        self.add_widget(exec_return_to_task_screen)
    
    # Call the script that isolates gene codes with the given arguments
    def generate_task(self, instance): # 'instance' is the name and reference to the object instance of the Class CustomBnt. You use it to gather information about the pressed Button. instance.text would be the text on the Button
        # Create a new task and insert it in the workflow
        csv_pathname = self.csvpath.text
        column_name = self.columnname.text
        if column_name.__eq__(""): # In case the user did not specifed any column
            column_name = "BRC ID"

        if check_csv_format(csv_pathname):
            isolate_column = IsolateColumn(csv_pathname, column_name)
            self.__workflow.add_task(isolate_column)
            
            # Return to the task selection screen passing the updated workflow
            self.clear_widgets() # Clean the objects in the screen before adding the new ones
            task_screen = PatricTaskScreen(self.__workflow)
            self.parent.add_widget(task_screen)
        else:
            self.csvpath.text = "NOT A CSV FORMAT"

    def return_to_task_screen(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        task_screen = PatricTaskScreen(workflow=self.__workflow)
        self.parent.add_widget(task_screen)
#'''

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class PatricTaskScreen(GridLayout):

    __workflow = None

    def __init__(self, workflow: Workflow, **kwargs):
        super(PatricTaskScreen, self).__init__(**kwargs) # One should not forget to call super in order to implement the functionality of the original class being overloaded. Also note that it is good practice not to omit the **kwargs while calling super, as they are sometimes used internally.
        
        self.__workflow = workflow
        self.rows = 7
        self.cols = 1

        isolate_codes_button = Button(text='Isolate PATRIC codes',
                                      halign='center',
                                      on_press=self.open_isolate_codes_menu)
        self.add_widget(isolate_codes_button)

        gen_fasta_button = Button(text='Generate ".fasta" files',
                                  halign='center',
                                  on_press=self.open_fasta_files_menu)
        self.add_widget(gen_fasta_button)

        reduce_sample_button = Button(text='Reduce sample',    
                                      halign='center',
                                      on_press=self.open_reduce_sample_menu)
        self.add_widget(reduce_sample_button)

        get_30kb_from_proteins_sample_button = Button(text='Get 30 kilobases up and down from given proteins',
                                                      halign='center',
                                                      on_press=self.open_get30KBupanddown_menu)
        self.add_widget(get_30kb_from_proteins_sample_button)

        get_codons_from_bases_button = Button(text='Find protein codons from a set of genome bases',
                                              halign='center',
                                              on_press=self.open_get_codons_menu)
        self.add_widget(get_codons_from_bases_button)

        '''reorder_proteins_sample_button = Button(text='Reorder sample from a .newick file', size_hint=(None, None), size=(150, 50), on_press=self.reorder_proteins_menu)
        reorder_proteins_sample_button.bind(texture_size=reorder_proteins_sample_button.setter('size'))
        self.add_widget(reorder_proteins_sample_button)'''

        # Button that opens the menu that allows manipulating all options concerning a workflow
        workflow_menu_button = Button(text='Return to workflow menu',
                                      halign='center',
                                      on_press=self.open_workflow_menu)
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

    def open_get30KBupanddown_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        get30kb_screen = Get30KBScreen(self.__workflow)
        self.parent.add_widget(get30kb_screen)

    def open_get_codons_menu(self, instance):
        self.clear_widgets()
        get_codons_screen = RecognizeCodonsScreen(self.__workflow)
        self.parent.add_widget(get_codons_screen)

    '''def open_reorder_proteins_sample_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        reorder_sample_screen = FromOrderedNewickToFastaScreen(self.__workflow)
        self.parent.add_widget(reorder_sample_screen)'''

    def open_workflow_menu(self, instance):
        self.clear_widgets() # Clean the objects in the screen before adding the new ones
        workflow_screen = genesys.WorkflowScreen(type='PATRIC', workflow=self.__workflow) # Open the isolate codes menu
        self.parent.add_widget(workflow_screen)

    def show_workflow_info(self): # Workflow info is shown through a function because it might be called from other methods that modify the workflow
        scroll_view = ScrollView(size_hint=(None, None), size=(Window.width, 250))
        scroll_view.bar_width = 10  # Adjust the scrollbar width here
        workflow_info_label = Label(text='Current Workflow:\n'+self.__workflow.show_info(),
                                    size_hint=(None, None),
                                    size=(Window.width, 250), # Width = Window width / number of columns defined in the view
                                    halign='center',
                                    valign='middle',
                                )
        workflow_info_label.bind(texture_size=workflow_info_label.setter('size'))
        scroll_view.add_widget(workflow_info_label)
        self.add_widget(scroll_view)

