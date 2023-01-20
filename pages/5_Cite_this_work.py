import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file

page_setup()

st.warning(''.join([
    ':warning: __To do:__ ',
    'The text on this page needs updating for the final app.'
]))

write_text_from_file('pages/text_for_pages/5_Citation.txt',
                     head_lines_to_skip=2)
