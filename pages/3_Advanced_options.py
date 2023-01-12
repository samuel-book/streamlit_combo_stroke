import streamlit as st

# from utilities.fixed_params import page_setup
# from utilities.inputs import write_text_from_file

# page_setup()

# write_text_from_file('pages/text_for_pages/3_Advanced.txt',
#                      head_lines_to_skip=2)

# import streamlit_lifetime_stroke.pages.2_Interactive_demo
import sys
# st.write(sys.path)


from pathlib import Path


# app1 = Path('./streamlit_lifetime_stroke/')
# app1_pages = Path.joinpath(app1, 'pages')
# app1_utils = Path.joinpath(app1, 'utilities_lifetime')
# app1_demo = Path.joinpath(app1_pages, '2_Interactive_demo.py')

# # sys.path.append(str(app1))
# # sys.path.append(str(app1_pages))
# # sys.path.append(str(app1_utils))
# # # sys.path.append(app1_demo)
# # sys.path.append('./streamlit_lifetime_stroke/')
# # sys.path.append('./streamlit_lifetime_stroke/pages/')
# # sys.path.append('./streamlit_lifetime_stroke/utilities/')
# st.write(sys.path)

# Change current working directory
# import os
# os.chdir('./streamlit_lifetime_stroke/')

# import streamlit_lifetime_stroke.pages.2_Interactive_demo

import importlib
# lifetime_module = importlib.import_module(
    # # str(app1_demo),
    # '/pages/2_Interactive_demo.py', #2_Interactive_demo',
    # # '.streamlit_lifetime_stroke.pages.2_Interactive_demo',
    # package='2_Interactive_demo'
    # # package='lifetime_module'
    # )
# lifetime_module = importlib.import_module(
#     # str(app1_demo),
#     './streamlit_lifetime_stroke/pages/', #2_Interactive_demo',
#     # '.streamlit_lifetime_stroke.pages.2_Interactive_demo',
#     package='2_Interactive_demo.py'
#     # package='lifetime_module'
#     )
utilities_lifetime = importlib.import_module('streamlit_lifetime_stroke.utilities_lifetime')
# utilities_lifetime.fixed_params = importlib.import_module('streamlit_lifetime_stroke.utilities_lifetime.fixed_params')
# st.write(utilities_lifetime.fixed_params.colours_excel)
# from utilities_lifetime.fixed_params import colours_excel
# st.write(colours_excel)

lifetime_module = importlib.import_module('streamlit_lifetime_stroke.pages.2_Interactive_demo', package='2_Interactive_demo.py')

lifetime_module.main()
