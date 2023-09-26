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


# Add an extra bit to the path if we need to.
# Try importing something as though we're running this from the same
# directory as the landing page.
try:
    from utilities_descriptive.fixed_params import page_setup
except ModuleNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # streamlit_lifetime_stroke.
    import sys
    sys.path.append('./streamlit_descriptive_stats/')
    # The following should work now:
    from utilities_descriptive.fixed_params import page_setup
try:
    test_file = pd.read_csv(
        './data_descriptive/stroke_teams.csv',
        index_col='stroke_team'
        )
    dir = './'
except FileNotFoundError:
    # If the import fails, add the landing page directory to path.
    # Assume that the script is being run from the directory above
    # the landing page directory, which is called
    # stroke_outcome_app.
    dir = 'streamlit_descriptive_stats/'

# Custom functions:
# from utilities_descriptive.fixed_params import page_setup
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
        dir + './data_descriptive/stroke_teams.csv',
        index_col=False).sort_values('stroke_team')
    # List of stroke teams
    stroke_team_list = list(stroke_team_list.squeeze().values)

    stroke_teams_selected = st.multiselect(
        'Stroke team', options=stroke_team_list)

    limit_to_4hr = st.toggle('Limit to arrival within 4hr')

    if limit_to_4hr:
        summary_stats_file = 'summary_stats_4hr.csv'
    else:
        summary_stats_file = 'summary_stats.csv'

    summary_stats_df = pd.read_csv(
        dir + './data_descriptive/' + summary_stats_file, index_col=0
    )

    # Find which teams are in the stroke teams options but
    # are not in the stats dataframe:
    missing_teams_list = (
        set(stroke_team_list) -
        set(summary_stats_df.columns)
    )

    teams_to_show = ['all E+W'] + stroke_teams_selected

    # ###########################
    # ######### RESULTS #########
    # ###########################
    st.header('Results')

    try:
        df_to_show = summary_stats_df[teams_to_show]
    except KeyError:
        # Remove teams that aren't in the dataframe:
        reduced_teams_to_show = []
        for team in teams_to_show:
            if team in missing_teams_list:
                st.markdown(f':warning: There is no data for {team}.')
            else:
                reduced_teams_to_show.append(team)
        df_to_show = summary_stats_df[reduced_teams_to_show]

    st.write(df_to_show)

    # ----- The end! -----


if __name__ == '__main__':
    main()
