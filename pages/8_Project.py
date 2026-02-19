import streamlit as st

from utilities_top.fixed_params import page_setup
from utilities_top.inputs import write_text_from_file

page_setup()

st.markdown('''# Our projects

The demo pages on this app show the results of various projects, including:
''')

cols_projects = st.columns(2)
with cols_projects[0]:
    st.info('''
    __SAMueL-2 & SAMueL-3__  
    (Stroke Audit and Machine Learning)

    Using clinical pathway simulation to model the potential benefit of improving the emergency stroke pathway, and using machine learning to compare clinical decision-making around thrombolysis between hospitals.
    ''')

with cols_projects[1]:
    st.error('''
    __OPTIMIST__  
    (OPTimising IMplementation of Ischaemic Stroke Thrombectomy)

    Optimising the pre-hospital stroke way to maximise the benefit of thrombolysis and thrombectomy.
    ''')

st.markdown('''
Some of the models presented here, for example the stroke outcome and lifetime mortality models, will continue to be used in future projects.
''')

write_text_from_file('pages/text_for_pages/4_Project.txt',
                    head_lines_to_skip=2)

st.image('pages/text_for_pages/NIHR_screenshot.png')
