"""
Data sources info page.
"""
import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file


page_setup()

# st.markdown('# :hospital: Stroke Predictions')
st.warning('This page is work in progress.', icon='⚠️')
write_text_from_file('info/data_sources_cheatsheet.md',
                     head_lines_to_skip=0)
