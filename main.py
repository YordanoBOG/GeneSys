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