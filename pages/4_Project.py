import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file

page_setup()

if __name__ == '__main__':

    write_text_from_file('pages/text_for_pages/4_Project.txt',
                     head_lines_to_skip=2)
    st.write('oi oi')
