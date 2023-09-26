"""
Streamlit app template.

Because a long app quickly gets out of hand,
try to keep this document to mostly direct calls to streamlit to write
or display stuff. Use functions in other files to create and
organise the stuff to be shown. In this example, most of the work is
done in functions stored in files named container_(something).py
"""
# ----- Imports -----
import streamlit as st
import pandas as pd
# import numpy as np

# Custom functions:
from utilities_descriptive.fixed_params import page_setup
# from utilities.inputs import \
#     write_text_from_file
# Containers:
# import utilities.container_inputs
# import utilities.container_results
# import utilities.container_details


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# Descriptive statistics')

    # ###########################
    # ########## SETUP ##########
    # ###########################
    st.header('Setup')
    st.subheader('Inputs')

    stroke_team_list = pd.read_csv(
        './data/stroke_teams.csv', index_col=False).sort_values('stroke_team')

    stroke_teams_selected = st.multiselect(
        'Stroke team', options=stroke_team_list)

    limit_to_4hr = st.toggle('Limit to arrival within 4hr')

    if limit_to_4hr:
        summary_stats_file = 'summary_stats_4hr.csv'
    else:
        summary_stats_file = 'summary_stats.csv'

    summary_stats_df = pd.read_csv(
        './data/' + summary_stats_file, index_col=0
    )

    teams_to_show = ['all E+W'] + stroke_teams_selected

    # ###########################
    # ######### RESULTS #########
    # ###########################
    st.header('Results')

    st.write(summary_stats_df[teams_to_show])

    # ----- The end! -----


if __name__ == '__main__':
    main()
