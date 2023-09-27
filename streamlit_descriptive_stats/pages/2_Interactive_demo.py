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

    stroke_team_list = pd.read_csv(
        dir + './data_descriptive/stroke_teams.csv',
        index_col=False).sort_values('stroke_team')
    # List of stroke teams
    stroke_team_list = list(stroke_team_list.squeeze().values)

    # Add filter by region:
    # ----------------------------------------------------------------------------------------------- To do 

    # Add in all the year options:
    year_options = ['2016 to 2021', '2016', '2017',
                    '2018', '2019', '2020', '2021']
    stroke_team_list_years = [
        f'{s} ({y})'
        for s in ['all E+W'] + stroke_team_list
        for y in year_options
    ]
    # Builds a list containing:
    # Team 1 (2016 to 2021)
    # Team 1 (2016)
    # Team 1 (2017)
    # ...
    # Team 1 (2021)
    # Team 2 (2016 to 2021)
    # Team 2 (2016)
    # Team 2 (2017)
    # ...
    # Team 2 (2021)

    # Start with black circle for "all teams" group:
    emoji_teams_vals = ['⚫'] * len(year_options)
    # Cycle through these emoji for the other stroke teams:
    emoji_teams = ['🔴', '🟠', '🟡', '🟢', '🔵', '🟣'] # '🟤' '⚪' '⚫' ⏺
    for i in range(len(stroke_team_list)):
        emoji_teams_vals += [emoji_teams[i % len(emoji_teams)]] * len(year_options)
    # st.write(text_colours_vals)
    emoji_teams_dict = dict(zip(stroke_team_list_years, emoji_teams_vals))

    text_colours = ['blue', 'green', 'orange', 'red', 'violet', 'grey', 'rainbow']
    text_colours_vals = []
    for i in range(len(stroke_team_list) + 1):
        text_colours_vals += [text_colours[i % len(text_colours)]] * len(year_options)
    # st.write(text_colours_vals)
    text_colours_dict = dict(zip(stroke_team_list_years, text_colours_vals))
    # st.write(text_colours_dict)


    # Use the format function in the multiselect to highlight the
    # options that use all years of the data.
    # Because the current ordering of the list is by team and then
    # by year, this also visually breaks up the list into groups of
    # each team.
    stroke_teams_selected = st.multiselect(
        'Stroke team',
        options=stroke_team_list_years,
        # default='⏺ all E+W (2016 to 2021)'
        default='all E+W (2016 to 2021)',
        # format_func=(lambda x: f'⏺ {x}'
        #              if year_options[0] in x else f'{x}')
        # format_func=(lambda x: f':{text_colours_dict[x]}[⏺ {x}]')
        # format_func=(lambda x: f''':{text_colours_dict[x]}[⏺] {x}''')
        format_func=(lambda x: f'{emoji_teams_dict[x]} {x}')
        )

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
        set(stroke_team_list_years) -
        set(summary_stats_df.columns)
    )

    teams_to_show = stroke_teams_selected

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

    row_order = [
        'count',
        'age',
        'male',
        'infarction',
        'stroke severity',
        'onset-to-arrival time',
        'onset known',
        'arrive in 4  hours',
        'precise onset known',
        'onset during sleep',
        'use of AF anticoagulants',
        'prior disability',
        'prestroke mrs 0-2',
        'arrival-to-scan time',
        'thrombolysis',
        'scan-to-thrombolysis time',
        'death',
        'discharge disability',
        'increased disability due to stroke',
        'mrs 5-6',
        'mrs 0-2'
    ]
    df_to_show = df_to_show.loc[row_order]
    st.table(df_to_show)

    # ----- The end! -----


if __name__ == '__main__':
    main()
