import streamlit as st

from utilities_pathway.fixed_params import page_setup
from utilities_pathway.inputs import write_text_from_file

page_setup()

write_text_from_file('pages/text_for_pages/6_Resources.txt',
                     head_lines_to_skip=2)
