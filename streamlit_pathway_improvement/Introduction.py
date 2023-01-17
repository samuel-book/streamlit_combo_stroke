"""
Streamlit app for the stroke outcome model.
"""
import streamlit as st

from utilities_pathway.fixed_params import page_setup
from utilities_pathway.inputs import write_text_from_file

page_setup()

write_text_from_file('pages/text_for_pages/1_Intro.txt',
                     head_lines_to_skip=3)
