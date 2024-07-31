# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This file starts the Genesys app UI
"""

from screens.genesys import MenuScreen

from kivy.app import App
from kivy.lang import Builder # This is necesary when we have the .kv files in a diferent folder than our main application

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