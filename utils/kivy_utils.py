# -*- coding: utf-8 -*-

"""
@author: Bruno Otero Galadí (bruogal@gmail.com)

This script contains functions that will be employed at the Kivy GUI
"""

import re

from kivy.uix.label import Label

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# This method updates the size of a given label so that the text that the label stores
# is entirely shown
def update_label_text_size(label:Label):
    # Update the text size to match the label's width
    label.text_size = (label.width, None)
    
    # Optional: Adjust the label's height to fit the text
    label.texture_update()
    label.height = label.texture_size[1]

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# This function checks if a given string matches the notation of
# numbers in scientific notation and returns the given string as
# a float in case it matches properly
def convert_to_scientific_notation(string_param):
    result = False
    pattern = r'^-?\d+(\.\d+)?([eE][-+]?\d+)?$' # Regular expression for validating scientific notation
    if re.match(pattern, string_param):
        result = float(string_param)
    return result

##############################################################################
##############################################################################
##############################################################################
##############################################################################
# Checks if a given pathname ends with ".fasta" string
def check_fasta_format(pathname):
    result = False
    if pathname[-6:].__eq__(".fasta"):
        result = True
    return result
