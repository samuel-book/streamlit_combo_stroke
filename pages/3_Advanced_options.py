import streamlit as st

# from utilities.fixed_params import page_setup
# from utilities.inputs import write_text_from_file

# page_setup()

# write_text_from_file('pages/text_for_pages/3_Advanced.txt',
#                      head_lines_to_skip=2)

# import streamlit_lifetime_stroke.pages.2_Interactive_demo
import sys
# st.write(sys.path)

sys.path.append('./streamlit_lifetime_stroke/')
sys.path.append('./streamlit_lifetime_stroke/pages/')
sys.path.append('./streamlit_lifetime_stroke/utilities/')
# st.write(sys.path)

# Change current working directory 
# import os
# os.chdir('./streamlit_lifetime_stroke/')

# import streamlit_lifetime_stroke.pages.2_Interactive_demo
import importlib
foo = importlib.import_module('./pages/2_Interactive_demo.py', package='2_Interactive_demo.py')