"""
Descriptive statistics demo.

This app reads in a dataframe containing descriptive statistics
and displays selected parts of it nicely. The stats exist for
acute stroke teams in the SSNAP data.

The dataframe is created in a notebook that is also included in
the app's repository. The data that goes into it is secret.
"""
# ----- Imports -----
import streamlit as st
import pandas as pd


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
from utilities_descriptive.fixed_params import all_teams_str, all_years_str
import utilities_descriptive.container_inputs
import utilities_descriptive.container_results
import utilities_descriptive.container_plots


def main():
    # ###########################
    # ##### START OF SCRIPT #####
    # ###########################
    page_setup()

    # Title:
    st.markdown('# 📊 Descriptive statistics')

    # Build up the page layout:
    _ = """
    +-----------------------------------------------------------------+
    | 📊 Descriptive statistics                                       |
    |                                                                 |
    +----------cols_inputs_map[0]----------+---cols_inputs_map[1]-----+
    |                                      |                          |
    |       container_input_regions        |                          |
    |                                      |      container_map       |
    |        container_input_teams         |                          |
    +--------------------------------------+--------------------------+
    |                       container_warnings                        |
    |                                                                 |
    |                   container_input_4hr_toggle                    |
    |                                                                 |
    |                        container_results                        |
    |                                                                 |
    |                        container_violins                        |
    +-----------------------------------------------------------------+
    """

    cols_inputs_map = st.columns([0.6, 0.4])
    with cols_inputs_map[0]:
        container_input_regions = st.container()
    with cols_inputs_map[0]:
        container_input_teams = st.container()
    with cols_inputs_map[1]:
        container_map = st.container()

    container_warnings = st.container()
    container_input_4hr_toggle = st.container()
    container_results_table = st.container()
    container_violins = st.container()

    # Each team input box:
    with container_input_teams:
        st.markdown('### Select stroke teams')
        cols_t = st.columns(3)
        with cols_t[0]:
            st.markdown('All years:')
        with cols_t[1]:
            st.markdown('Separate years:')
        for col in cols_t[2:]:
            with col:
                # Unicode looks-like-a-space character
                # for vertical alignment with the other columns
                # that have text in.
                st.markdown('\U0000200B')
        containers_list_team_inputs = [
            cols_t[0],             # All years
            cols_t[1], cols_t[2],  # 2016, 2017
            cols_t[1], cols_t[2],  # 2018, 2019
            cols_t[1], cols_t[2]   # 2020, 2021
        ]

    with container_input_regions:
        st.markdown('### Filter by region')
        containers_list_region_inputs = st.columns(3)

    # ###########################
    # ########## SETUP ##########
    # ###########################

    # Decide which descriptive stats file to use:
    with container_input_4hr_toggle:
        limit_to_4hr = st.toggle('Limit to arrival within 4hr')
    if limit_to_4hr:
        summary_stats_file = 'summary_stats_4hr.csv'
    else:
        summary_stats_file = 'summary_stats.csv'
    # Read in the data:
    summary_stats_df = pd.read_csv(
        f'{dir}/data_descriptive/{summary_stats_file}',
        index_col=0
        )

    # Import list of all stroke teams:
    df_stroke_team = pd.read_csv(
        f'{dir}/data_descriptive/hospitals_and_lsoas_descriptive_stats.csv',
        index_col=False
        ).sort_values('Stroke Team')

    with container_map:
        # Plot the team locations
        utilities_descriptive.container_plots.\
            plot_geography_pins(df_stroke_team)

    # List of years in the data:
    year_options = sorted(set(summary_stats_df.loc['year']))
    # Move the "all years" option to the front of the list:
    year_options.remove(all_years_str)
    year_options = [all_years_str] + year_options

    with container_input_regions:
        # Select regions:
        regions_selected = utilities_descriptive.container_inputs.\
            inputs_region_choice(
                df_stroke_team,
                containers_list_region_inputs
                )

    with container_input_teams:
        # Select stroke teams:
        stroke_teams_selected = utilities_descriptive.container_inputs.\
            input_stroke_teams_to_highlight(
                df_stroke_team,
                regions_selected,
                all_teams_str,
                year_options,
                all_years_str=all_years_str,
                containers=containers_list_team_inputs
                )

    # ###########################
    # ######### RESULTS #########
    # ###########################

    # Check that all of the requested data exists.
    # Remove any teams that don't exist and print a warning message.
    df_to_show = utilities_descriptive.container_results.\
        check_teams_in_stats_df(
            summary_stats_df,
            stroke_teams_selected,
            container_warnings
        )

    # Update the order of the rows to this:
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

    with container_results_table:
        st.header('Results')
        st.table(df_to_show)

    # #########################
    # ######### PLOTS #########
    # #########################

    with container_violins:
        st.header('Feature breakdown')

        # User inputs for which feature to plot:
        feature = st.selectbox(
            'Pick a feature to plot',
            options=row_order,
            # default='count'
        )

        # Remove the (year) string from the selected teams:
        stroke_teams_selected_without_year = [
            team.split(' (')[0] for team in stroke_teams_selected]

        utilities_descriptive.container_plots.plot_violins(
            summary_stats_df,
            feature,
            year_options,
            stroke_teams_selected_without_year,
            all_years_str,
            all_teams_str
            )

    # ----- The end! -----


if __name__ == '__main__':
    main()
